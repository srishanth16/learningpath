from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.models import User, UserInterest, UserSkill, Skill, LearningGoal
from ..schemas.schemas import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter(prefix="/api", tags=["Profile"])


@router.post("/profile")
def create_profile(data: ProfileCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        education=data.education,
        experience_level=data.experience_level,
        weekly_hours=data.weekly_hours,
        learning_preferences=data.learning_preferences,
        current_role=data.current_role,
    )
    db.add(user)
    db.flush()

    # Add interests
    for interest in data.interests:
        db.add(UserInterest(user_id=user.id, interest=interest))

    # Add skills
    for skill_input in data.skills:
        skill = db.query(Skill).filter(Skill.name == skill_input.name).first()
        if skill:
            db.add(UserSkill(user_id=user.id, skill_id=skill.id, proficiency=skill_input.proficiency))

    # Add goal if provided
    if data.goal:
        from ..recommender.engine import detect_target_role
        target_role = detect_target_role(data.goal)
        db.add(LearningGoal(
            user_id=user.id,
            goal_text=data.goal,
            target_role=target_role.title(),
            is_active=True,
        ))

    db.commit()
    db.refresh(user)
    return _format_user(db, user)


@router.get("/profile/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _format_user(db, user)


@router.get("/profile/demo/load")
def get_demo_profile(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == "alex@demo.com").first()
    if not user:
        raise HTTPException(status_code=404, detail="Demo user not found. Database may not be seeded.")
    return _format_user(db, user)


@router.put("/profile/{user_id}")
def update_profile(user_id: int, data: ProfileUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.name is not None:
        user.name = data.name
    if data.education is not None:
        user.education = data.education
    if data.experience_level is not None:
        user.experience_level = data.experience_level
    if data.weekly_hours is not None:
        user.weekly_hours = data.weekly_hours
    if data.learning_preferences is not None:
        user.learning_preferences = data.learning_preferences
    if data.current_role is not None:
        user.current_role = data.current_role

    if data.interests is not None:
        db.query(UserInterest).filter(UserInterest.user_id == user_id).delete()
        for interest in data.interests:
            db.add(UserInterest(user_id=user_id, interest=interest))

    if data.skills is not None:
        db.query(UserSkill).filter(UserSkill.user_id == user_id).delete()
        for skill_input in data.skills:
            skill = db.query(Skill).filter(Skill.name == skill_input.name).first()
            if skill:
                db.add(UserSkill(user_id=user_id, skill_id=skill.id, proficiency=skill_input.proficiency))

    db.commit()
    db.refresh(user)
    return _format_user(db, user)


def _format_user(db: Session, user: User) -> dict:
    interests = db.query(UserInterest).filter(UserInterest.user_id == user.id).all()
    skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
    goals = db.query(LearningGoal).filter(LearningGoal.user_id == user.id).all()

    skill_list = []
    for us in skills:
        sk = db.query(Skill).filter(Skill.id == us.skill_id).first()
        if sk:
            skill_list.append({"name": sk.name, "proficiency": us.proficiency, "domain": sk.domain})

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "education": user.education,
        "experience_level": user.experience_level,
        "weekly_hours": user.weekly_hours,
        "learning_preferences": user.learning_preferences or [],
        "current_role": user.current_role,
        "interests": [i.interest for i in interests],
        "skills": skill_list,
        "goals": [
            {
                "id": g.id,
                "goal_text": g.goal_text,
                "target_role": g.target_role,
                "is_active": g.is_active,
                "created_at": g.created_at.isoformat() if g.created_at else None,
            }
            for g in goals
        ],
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }
