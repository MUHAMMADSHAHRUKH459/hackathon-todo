# src/mcp_tools/task_tools.py
from sqlalchemy.orm import Session
from src.models.database import Task, get_db
import json

async def add_task(user_id: int, title: str, description: str = "") -> str:
    """Create a new task for the user"""
    db = next(get_db())
    try:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        return json.dumps({
            "status": "success",
            "task_id": task.id,
            "title": task.title,
            "message": f"Created task: {task.title}"
        })
    except Exception as e:
        db.rollback()
        return json.dumps({"status": "error", "message": str(e)})
    finally:
        db.close()

async def list_tasks(user_id: int, status: str = "all") -> str:
    """Get all tasks for a user"""
    db = next(get_db())
    try:
        query = db.query(Task).filter(Task.user_id == user_id)
        
        if status == "pending":
            query = query.filter(Task.completed == False)
        elif status == "completed":
            query = query.filter(Task.completed == True)
        
        tasks = query.order_by(Task.created_at.desc()).all()
        
        task_list = [{
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "completed": t.completed,
            "created_at": t.created_at.isoformat()
        } for t in tasks]
        
        return json.dumps({
            "status": "success",
            "count": len(task_list),
            "tasks": task_list
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
    finally:
        db.close()

async def complete_task(user_id: int, task_id: int) -> str:
    """Mark a task as complete"""
    db = next(get_db())
    try:
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()
        
        if not task:
            return json.dumps({"status": "error", "message": "Task not found"})
        
        task.completed = True
        db.commit()
        
        return json.dumps({
            "status": "success",
            "task_id": task.id,
            "title": task.title,
            "message": f"Completed task: {task.title}"
        })
    except Exception as e:
        db.rollback()
        return json.dumps({"status": "error", "message": str(e)})
    finally:
        db.close()

async def delete_task(user_id: int, task_id: int) -> str:
    """Delete a task"""
    db = next(get_db())
    try:
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()
        
        if not task:
            return json.dumps({"status": "error", "message": "Task not found"})
        
        title = task.title
        db.delete(task)
        db.commit()
        
        return json.dumps({
            "status": "success",
            "message": f"Deleted task: {title}"
        })
    except Exception as e:
        db.rollback()
        return json.dumps({"status": "error", "message": str(e)})
    finally:
        db.close()

async def update_task(user_id: int, task_id: int, title: str = None, description: str = None) -> str:
    """Update a task's title or description"""
    db = next(get_db())
    try:
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()
        
        if not task:
            return json.dumps({"status": "error", "message": "Task not found"})
        
        if title:
            task.title = title
        if description is not None:
            task.description = description
        
        db.commit()
        
        return json.dumps({
            "status": "success",
            "task_id": task.id,
            "title": task.title,
            "message": f"Updated task: {task.title}"
        })
    except Exception as e:
        db.rollback()
        return json.dumps({"status": "error", "message": str(e)})
    finally:
        db.close()