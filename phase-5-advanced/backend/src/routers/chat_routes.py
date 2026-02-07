# src/routers/chat_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.database import get_db, User, Conversation, Message
from src.ai.agent import run_agent
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    user_id: int  # Add user_id directly

class ChatResponse(BaseModel):
    conversation_id: int
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Chat endpoint with AI agent"""
    
    # Get user
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get or create conversation
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == user.id
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user.id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    
    # Get conversation history
    messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()
    
    history = [{"role": msg.role, "content": msg.content} for msg in messages]
    
    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        user_id=user.id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    db.commit()
    
    # Run AI agent
    response = await run_agent(user.id, request.message, history)
    
    # Save assistant response
    assistant_message = Message(
        conversation_id=conversation.id,
        user_id=user.id,
        role="assistant",
        content=response
    )
    db.add(assistant_message)
    db.commit()
    
    return ChatResponse(
        conversation_id=conversation.id,
        response=response
    )