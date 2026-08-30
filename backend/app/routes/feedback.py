from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.models import Feedback, User, Resource
from ..schemas.schemas import FeedbackCreate

router = APIRouter(prefix="/api", tags=["Feedback"])


@router.post("/feedback")
def submit_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    resource = db.query(Resource).filter(Resource.id == data.resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Check if feedback already exists
    existing = db.query(Feedback).filter(
        Feedback.user_id == data.user_id,
        Feedback.resource_id == data.resource_id
    ).first()

    if existing:
        existing.rating = data.rating
        existing.difficulty_rating = data.difficulty_rating
        existing.helpful = data.helpful
        existing.comment = data.comment
    else:
        feedback = Feedback(
            user_id=data.user_id,
            resource_id=data.resource_id,
            rating=data.rating,
            difficulty_rating=data.difficulty_rating,
            helpful=data.helpful,
            comment=data.comment,
        )
        db.add(feedback)

    db.commit()
    return {"message": "Feedback submitted successfully"}


@router.get("/feedback/{user_id}")
def get_feedback(user_id: int, db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).filter(Feedback.user_id == user_id).all()
    return [
        {
            "id": f.id,
            "resource_id": f.resource_id,
            "resource_title": db.query(Resource).filter(Resource.id == f.resource_id).first().title if db.query(Resource).filter(Resource.id == f.resource_id).first() else "",
            "rating": f.rating,
            "difficulty_rating": f.difficulty_rating,
            "helpful": f.helpful,
            "comment": f.comment,
            "created_at": f.created_at.isoformat() if f.created_at else None,
        }
        for f in feedbacks
    ]
