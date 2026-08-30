from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database.db import get_db
from ..models.models import (
    User, Progress, Resource, LearningPath, LearningPathItem,
    LearningGoal, UserSkill, Skill, AssessmentResult, Feedback
)
from ..schemas.schemas import ProgressUpdate
from ..recommender.engine import (
    detect_target_role, get_required_skills, analyze_skill_gaps,
    get_suggested_projects, generate_recommendations
)

router = APIRouter(prefix="/api", tags=["Progress"])


@router.post("/progress")
def update_progress(data: ProgressUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    resource = db.query(Resource).filter(Resource.id == data.resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    progress = db.query(Progress).filter(
        Progress.user_id == data.user_id,
        Progress.resource_id == data.resource_id
    ).first()

    if progress:
        progress.progress_pct = data.progress_pct
        progress.completed = data.completed
        if data.completed:
            progress.completed_at = datetime.utcnow()
    else:
        progress = Progress(
            user_id=data.user_id,
            resource_id=data.resource_id,
            progress_pct=data.progress_pct,
            completed=data.completed,
            completed_at=datetime.utcnow() if data.completed else None,
        )
        db.add(progress)

    # Update user skill proficiency when completing a resource
    if data.completed:
        _update_skill_proficiency(db, data.user_id, resource)

    db.commit()
    return {"message": "Progress updated"}


@router.get("/progress/{user_id}")
def get_progress(user_id: int, db: Session = Depends(get_db)):
    progress_list = db.query(Progress).filter(Progress.user_id == user_id).all()
    result = []
    for p in progress_list:
        resource = db.query(Resource).filter(Resource.id == p.resource_id).first()
        result.append({
            "id": p.id,
            "resource_id": p.resource_id,
            "resource_title": resource.title if resource else "Unknown",
            "resource_type": resource.type if resource else "",
            "progress_pct": p.progress_pct,
            "completed": p.completed,
            "completed_at": p.completed_at.isoformat() if p.completed_at else None,
        })
    return result


@router.get("/dashboard/{user_id}")
def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get active goal
    goal = db.query(LearningGoal).filter(
        LearningGoal.user_id == user_id,
        LearningGoal.is_active == True
    ).first()

    # Get learning path
    path = db.query(LearningPath).filter(
        LearningPath.user_id == user_id
    ).order_by(LearningPath.created_at.desc()).first()

    # Get progress
    all_progress = db.query(Progress).filter(Progress.user_id == user_id).all()
    completed_progress = [p for p in all_progress if p.completed]
    completed_ids = {p.resource_id for p in completed_progress}

    # Overall progress
    total_path_items = 0
    completed_path_items = 0
    if path:
        items = db.query(LearningPathItem).filter(LearningPathItem.path_id == path.id).all()
        total_path_items = len(items)
        completed_path_items = sum(1 for i in items if i.status == "completed")

    overall_progress = round((completed_path_items / total_path_items) * 100) if total_path_items > 0 else 0

    # Skills developed
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    skills_developed = []
    for us in user_skills:
        sk = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if sk:
            skills_developed.append({
                "name": sk.name,
                "proficiency": us.proficiency,
                "domain": sk.domain,
            })

    # Learning streak (simplified: count consecutive days with completions)
    streak = _calculate_streak(completed_progress)

    # Hours learned
    hours = sum(
        db.query(Resource).filter(Resource.id == p.resource_id).first().estimated_hours
        for p in completed_progress
        if db.query(Resource).filter(Resource.id == p.resource_id).first()
    )

    # Next action
    next_action = None
    if path:
        next_item = db.query(LearningPathItem).filter(
            LearningPathItem.path_id == path.id,
            LearningPathItem.status.in_(["available", "in_progress"])
        ).order_by(LearningPathItem.phase, LearningPathItem.order).first()

        if next_item:
            resource = db.query(Resource).filter(Resource.id == next_item.resource_id).first()
            if resource:
                next_action = {
                    "item_id": next_item.id,
                    "title": resource.title,
                    "type": resource.type,
                    "estimated_hours": resource.estimated_hours,
                    "skill": resource.skill,
                    "status": next_item.status,
                }

    # Current milestone
    current_milestone = None
    upcoming_milestone = None
    if path and path.milestones:
        milestones = path.milestones
        for ms in milestones:
            ms_phase = ms.get("phase", 0)
            phase_items = db.query(LearningPathItem).filter(
                LearningPathItem.path_id == path.id,
                LearningPathItem.phase == ms_phase
            ).all() if path else []
            all_done = all(i.status == "completed" for i in phase_items) if phase_items else False

            if not all_done:
                if current_milestone is None:
                    current_milestone = ms.get("title", "")
                elif upcoming_milestone is None:
                    upcoming_milestone = ms.get("title", "")
                    break

    # Recommended projects
    target_role = goal.target_role.lower() if goal and goal.target_role else "data scientist"
    project_names = get_suggested_projects(target_role)
    projects = db.query(Resource).filter(
        Resource.type == "project",
        Resource.title.in_(project_names)
    ).limit(3).all()
    recommended_projects = [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "difficulty": p.difficulty,
            "estimated_hours": p.estimated_hours,
            "skill": p.skill,
        }
        for p in projects
    ]

    # Get recommendations
    recommendations = generate_recommendations(db, user_id)
    top_recommendations = []
    for rec in recommendations[:5]:
        r = rec["resource"]
        top_recommendations.append({
            "id": r.id,
            "title": r.title,
            "type": r.type,
            "skill": r.skill,
            "difficulty": r.difficulty,
            "estimated_hours": r.estimated_hours,
            "score": rec["score"],
            "reason": rec["reason"],
            "prerequisites_met": rec["prerequisites_met"],
        })

    return {
        "user_name": user.name,
        "overall_progress": overall_progress,
        "current_goal": goal.goal_text if goal else None,
        "target_role": goal.target_role if goal else None,
        "current_milestone": current_milestone,
        "skills_developed": skills_developed,
        "learning_streak": streak,
        "hours_learned": round(hours, 1),
        "completed_resources": len(completed_ids),
        "total_resources": total_path_items,
        "next_action": next_action,
        "upcoming_milestone": upcoming_milestone,
        "recommended_projects": recommended_projects,
        "recommendations": top_recommendations,
    }


def _calculate_streak(completed_progress):
    """Calculate learning streak from completion dates."""
    if not completed_progress:
        return 0

    dates = sorted(
        set(
            p.completed_at.date() for p in completed_progress
            if p.completed_at
        ),
        reverse=True
    )

    if not dates:
        return 0

    streak = 1
    for i in range(len(dates) - 1):
        diff = (dates[i] - dates[i + 1]).days
        if diff == 1:
            streak += 1
        else:
            break

    return streak


def _update_skill_proficiency(db: Session, user_id: int, resource: Resource):
    """Increase user's skill proficiency when completing a resource."""
    skill = db.query(Skill).filter(Skill.name == resource.skill).first()
    if not skill:
        return

    user_skill = db.query(UserSkill).filter(
        UserSkill.user_id == user_id,
        UserSkill.skill_id == skill.id
    ).first()

    # Determine proficiency boost based on resource difficulty
    boost = {"beginner": 15, "intermediate": 10, "advanced": 8}
    increase = boost.get(resource.difficulty, 10)

    if user_skill:
        user_skill.proficiency = min(100, user_skill.proficiency + increase)
    else:
        db.add(UserSkill(
            user_id=user_id,
            skill_id=skill.id,
            proficiency=min(100, increase)
        ))
