from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.models import (
    User, LearningPath, LearningPathItem, Resource, Progress, LearningGoal
)
from ..schemas.schemas import GeneratePathRequest, PathItemUpdate
from ..recommender.engine import generate_learning_path

router = APIRouter(prefix="/api", tags=["Learning Path"])


@router.post("/learning-path/generate")
def generate_path(data: GeneratePathRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    goal = db.query(LearningGoal).filter(
        LearningGoal.user_id == data.user_id,
        LearningGoal.is_active == True
    ).first()
    if not goal:
        raise HTTPException(status_code=400, detail="No active goal found. Please set a goal first.")

    # Delete existing path for this user
    existing = db.query(LearningPath).filter(LearningPath.user_id == data.user_id).all()
    for ep in existing:
        db.query(LearningPathItem).filter(LearningPathItem.path_id == ep.id).delete()
        db.delete(ep)

    # Generate new path
    path_data = generate_learning_path(db, data.user_id)
    if not path_data or not path_data.get("items"):
        raise HTTPException(status_code=400, detail="Could not generate learning path. Check your goal and skills.")

    path = LearningPath(
        user_id=data.user_id,
        title=path_data["title"],
        description=path_data["description"],
        phases=[{k: v for k, v in p.items()} for p in path_data["phases"]],
        milestones=path_data["milestones"],
    )
    db.add(path)
    db.flush()

    # Create items
    for item_data in path_data["items"]:
        item = LearningPathItem(
            path_id=path.id,
            resource_id=item_data["resource"].id,
            phase=item_data["phase"],
            order=item_data["order"],
            status=item_data["status"],
            reason=item_data["reason"],
        )
        db.add(item)

    db.commit()
    db.refresh(path)
    return _format_path(db, path)


@router.get("/learning-path/{user_id}")
def get_learning_path(user_id: int, db: Session = Depends(get_db)):
    path = db.query(LearningPath).filter(
        LearningPath.user_id == user_id
    ).order_by(LearningPath.created_at.desc()).first()

    if not path:
        return None

    return _format_path(db, path)


@router.put("/learning-path/items/{item_id}")
def update_path_item(item_id: int, data: PathItemUpdate, db: Session = Depends(get_db)):
    item = db.query(LearningPathItem).filter(LearningPathItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.status = data.status
    resource = db.query(Resource).filter(Resource.id == item.resource_id).first()

    # Update progress tracking
    path = db.query(LearningPath).filter(LearningPath.id == item.path_id).first()
    if path and resource:
        if data.status == "completed":
            # Update or create progress
            progress = db.query(Progress).filter(
                Progress.user_id == path.user_id,
                Progress.resource_id == item.resource_id
            ).first()
            if progress:
                progress.completed = True
                progress.progress_pct = 100
                from datetime import datetime
                progress.completed_at = datetime.utcnow()
            else:
                from datetime import datetime
                db.add(Progress(
                    user_id=path.user_id,
                    resource_id=item.resource_id,
                    progress_pct=100,
                    completed=True,
                    completed_at=datetime.utcnow()
                ))

            # Unlock next items in same phase or next phase
            _unlock_next_items(db, path, item)

        elif data.status == "in_progress":
            progress = db.query(Progress).filter(
                Progress.user_id == path.user_id,
                Progress.resource_id == item.resource_id
            ).first()
            if not progress:
                db.add(Progress(
                    user_id=path.user_id,
                    resource_id=item.resource_id,
                    progress_pct=50,
                    completed=False,
                ))

    db.commit()
    return {"message": "Item updated", "status": data.status}


def _unlock_next_items(db: Session, path: LearningPath, completed_item: LearningPathItem):
    """Unlock subsequent items after completion."""
    # Get all completed titles for prerequisite checking
    completed_progress = db.query(Progress).filter(
        Progress.user_id == path.user_id,
        Progress.completed == True
    ).all()
    completed_resource_ids = {p.resource_id for p in completed_progress}
    completed_resources = [db.query(Resource).get(rid) for rid in completed_resource_ids]
    completed_titles = {r.title for r in completed_resources if r}

    # Also add the just-completed item
    just_completed = db.query(Resource).get(completed_item.resource_id)
    if just_completed:
        completed_titles.add(just_completed.title)

    # Get all locked items
    locked_items = db.query(LearningPathItem).filter(
        LearningPathItem.path_id == path.id,
        LearningPathItem.status == "locked"
    ).order_by(LearningPathItem.phase, LearningPathItem.order).all()

    for locked_item in locked_items:
        resource = db.query(Resource).get(locked_item.resource_id)
        if resource:
            prereqs = resource.prerequisites or []
            if all(p in completed_titles for p in prereqs):
                locked_item.status = "available"


def _format_path(db: Session, path: LearningPath) -> dict:
    items = db.query(LearningPathItem).filter(
        LearningPathItem.path_id == path.id
    ).order_by(LearningPathItem.phase, LearningPathItem.order).all()

    formatted_items = []
    for item in items:
        resource = db.query(Resource).filter(Resource.id == item.resource_id).first()
        formatted_items.append({
            "id": item.id,
            "resource_id": item.resource_id,
            "resource": {
                "id": resource.id,
                "title": resource.title,
                "description": resource.description,
                "domain": resource.domain,
                "skill": resource.skill,
                "difficulty": resource.difficulty,
                "estimated_hours": resource.estimated_hours,
                "type": resource.type,
                "prerequisites": resource.prerequisites or [],
                "url": resource.url or "",
                "rating": resource.rating,
                "tags": resource.tags or [],
            } if resource else None,
            "phase": item.phase,
            "order": item.order,
            "status": item.status,
            "reason": item.reason,
        })

    return {
        "id": path.id,
        "user_id": path.user_id,
        "title": path.title,
        "description": path.description,
        "phases": path.phases or [],
        "milestones": path.milestones or [],
        "items": formatted_items,
        "created_at": path.created_at.isoformat() if path.created_at else None,
    }
