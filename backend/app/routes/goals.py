from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.models import LearningGoal, User
from ..schemas.schemas import GoalCreate, GoalAnalysisRequest
from ..ai.ai_service import analyze_goal_with_ai
from ..recommender.engine import detect_target_role

router = APIRouter(prefix="/api", tags=["Goals"])


@router.post("/goals")
def create_goal(data: GoalCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Deactivate previous goals
    db.query(LearningGoal).filter(
        LearningGoal.user_id == data.user_id,
        LearningGoal.is_active == True
    ).update({"is_active": False})

    target_role = data.target_role or detect_target_role(data.goal_text).title()

    goal = LearningGoal(
        user_id=data.user_id,
        goal_text=data.goal_text,
        target_role=target_role,
        is_active=True,
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)

    return {
        "id": goal.id,
        "goal_text": goal.goal_text,
        "target_role": goal.target_role,
        "is_active": goal.is_active,
        "created_at": goal.created_at.isoformat() if goal.created_at else None,
    }


@router.get("/goals/{user_id}")
def get_goals(user_id: int, db: Session = Depends(get_db)):
    goals = db.query(LearningGoal).filter(LearningGoal.user_id == user_id).all()
    return [
        {
            "id": g.id,
            "goal_text": g.goal_text,
            "target_role": g.target_role,
            "is_active": g.is_active,
            "created_at": g.created_at.isoformat() if g.created_at else None,
        }
        for g in goals
    ]


@router.post("/analyze-goal")
async def analyze_goal(data: GoalAnalysisRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not data.goal_text.strip():
        raise HTTPException(status_code=400, detail="Goal text cannot be empty")

    result = await analyze_goal_with_ai(db, data.user_id, data.goal_text)
    return result
