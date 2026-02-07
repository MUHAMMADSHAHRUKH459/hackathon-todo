# src/routers/task_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.database import get_db, Task, User
from src.schemas.schemas import TaskCreate, TaskUpdate, TaskResponse
from jose import JWTError, jwt
from datetime import datetime

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

SECRET_KEY = "your-secret-key-change-in-production-12345"
ALGORITHM = "HS256"

def get_current_user_from_header(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    print(f"\n🔐 Task route - Auth header: {authorization[:50] if authorization else 'None'}...")
    
    if not authorization:
        print("❌ No Authorization header!")
        raise HTTPException(status_code=401, detail="No authorization header")
    
    if not authorization.startswith("Bearer "):
        print("❌ Invalid auth format!")
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.replace("Bearer ", "")
    print(f"🔑 Extracted token: {token[:30]}...")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Token decoded: {payload}")
        
        user_id = payload.get("sub")
        user_id = int(user_id)
        print(f"🆔 User ID: {user_id} (type: {type(user_id)})")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            print(f"❌ User not found: {user_id}")
            raise HTTPException(status_code=401, detail="User not found")
        
        print(f"✅ User authenticated: {user.username}\n")
        return user
        
    except JWTError as e:
        print(f"❌ JWT Error: {e}\n")
        raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError as e:
        print(f"❌ Value Error: {e}\n")
        raise HTTPException(status_code=401, detail="Invalid user ID in token")

@router.get("", response_model=List[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    print(f"📋 Getting tasks for user: {current_user.username}")
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    print(f"✅ Found {len(tasks)} tasks")
    return tasks

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    print(f"➕ Creating task for user: {current_user.username}")
    
    # Parse due_date if provided
    due_date_obj = None
    if hasattr(task_data, 'due_date') and task_data.due_date:
        try:
            due_date_obj = datetime.fromisoformat(task_data.due_date.replace('Z', '+00:00'))
        except:
            pass
    
    new_task = Task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        priority=getattr(task_data, 'priority', 'medium'),  # NEW - Phase 5
        due_date=due_date_obj,  # NEW - Phase 5
        completed=False
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    print(f"✅ Task created: {new_task.id}")
    return new_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
    if hasattr(task_data, 'priority') and task_data.priority is not None:
        task.priority = task_data.priority  # NEW - Phase 5
    if hasattr(task_data, 'due_date') and task_data.due_date is not None:
        try:
            task.due_date = datetime.fromisoformat(task_data.due_date.replace('Z', '+00:00'))  # NEW - Phase 5
        except:
            pass
    
    db.commit()
    db.refresh(task)
    
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    db.delete(task)
    db.commit()
    
    return {"message": "Task deleted successfully"}