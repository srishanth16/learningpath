from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.models import ChatMessage, User
from ..schemas.schemas import ChatRequest
from ..ai.ai_service import chat_with_ai

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat")
async def chat(data: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not data.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Save user message
    user_msg = ChatMessage(
        user_id=data.user_id,
        role="user",
        content=data.message,
    )
    db.add(user_msg)
    db.commit()

    # Get AI response
    result = await chat_with_ai(db, data.user_id, data.message)

    # Save assistant message
    assistant_msg = ChatMessage(
        user_id=data.user_id,
        role="assistant",
        content=result["response"],
    )
    db.add(assistant_msg)
    db.commit()

    return result


@router.get("/chat/{user_id}")
def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id
    ).order_by(ChatMessage.created_at.asc()).all()

    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in messages
    ]
