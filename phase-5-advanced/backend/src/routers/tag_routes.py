# src/routers/tag_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.database import get_db, User, Tag
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/tags", tags=["tags"])

class TagCreate(BaseModel):
    name: str
    color: str = "#3B82F6"

class TagResponse(BaseModel):
    id: int
    name: str
    color: str
    user_id: int
    
    class Config:
        from_attributes = True

@router.post("/", response_model=TagResponse)
def create_tag(tag: TagCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new tag"""
    new_tag = Tag(
        user_id=user_id,
        name=tag.name,
        color=tag.color
    )
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

@router.get("/", response_model=List[TagResponse])
def get_tags(user_id: int, db: Session = Depends(get_db)):
    """Get all user tags"""
    tags = db.query(Tag).filter(Tag.user_id == user_id).all()
    return tags

@router.delete("/{tag_id}")
def delete_tag(tag_id: int, user_id: int, db: Session = Depends(get_db)):
    """Delete a tag"""
    tag = db.query(Tag).filter(Tag.id == tag_id, Tag.user_id == user_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted"}