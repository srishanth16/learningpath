from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.models import Skill, UserSkill, LearningGoal, User
from ..recommender.engine import detect_target_role, get_required_skills, analyze_skill_gaps

router = APIRouter(prefix="/api", tags=["Skills"])


@router.get("/skills")
def list_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    return [
        {"id": s.id, "name": s.name, "domain": s.domain, "description": s.description}
        for s in skills
    ]


@router.get("/skills/user/{user_id}")
def get_user_skills(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get active goal to determine required skills
    goal = db.query(LearningGoal).filter(
        LearningGoal.user_id == user_id,
        LearningGoal.is_active == True
    ).first()

    if goal:
        target_role = goal.target_role or detect_target_role(goal.goal_text)
        required_skills = get_required_skills(target_role.lower())
    else:
        required_skills = []

    gaps = analyze_skill_gaps(db, user_id, required_skills) if required_skills else {
        "current_skills": [],
        "skill_gaps": [],
        "priority_skills": [],
        "strong": [],
        "intermediate": [],
        "needs_improvement": [],
        "missing": [],
    }

    # Also return all user skills (even those not required for goal)
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    all_skills = []
    for us in user_skills:
        sk = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if sk:
            all_skills.append({"name": sk.name, "proficiency": us.proficiency, "domain": sk.domain})

    return {
        **gaps,
        "all_user_skills": all_skills,
        "required_skills": required_skills,
    }


@router.put("/skills/user/{user_id}")
def update_user_skills(user_id: int, skills: list[dict], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(UserSkill).filter(UserSkill.user_id == user_id).delete()

    for skill_data in skills:
        skill = db.query(Skill).filter(Skill.name == skill_data["name"]).first()
        if skill:
            db.add(UserSkill(
                user_id=user_id,
                skill_id=skill.id,
                proficiency=skill_data.get("proficiency", 0)
            ))

    db.commit()
    return {"message": "Skills updated"}
