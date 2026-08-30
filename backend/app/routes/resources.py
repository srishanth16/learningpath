from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.models import Resource

router = APIRouter(prefix="/api", tags=["Resources"])


@router.get("/resources")
def list_resources(
    domain: str = Query(None),
    skill: str = Query(None),
    difficulty: str = Query(None),
    type: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Resource)

    if domain:
        query = query.filter(Resource.domain == domain)
    if skill:
        query = query.filter(Resource.skill == skill)
    if difficulty:
        query = query.filter(Resource.difficulty == difficulty)
    if type:
        query = query.filter(Resource.type == type)
    if search:
        query = query.filter(Resource.title.ilike(f"%{search}%"))

    resources = query.all()
    return [_format_resource(r) for r in resources]


@router.get("/resources/{resource_id}")
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Resource not found")
    return _format_resource(resource)


def _format_resource(r: Resource) -> dict:
    return {
        "id": r.id,
        "title": r.title,
        "description": r.description,
        "domain": r.domain,
        "skill": r.skill,
        "difficulty": r.difficulty,
        "estimated_hours": r.estimated_hours,
        "type": r.type,
        "prerequisites": r.prerequisites or [],
        "url": r.url or "",
        "rating": r.rating,
        "tags": r.tags or [],
    }
