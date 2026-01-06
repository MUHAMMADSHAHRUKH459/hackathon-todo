# Task T-002: Implement In-Memory Storage
# Spec: specs/features/task-crud.md § All User Stories
# Plan: specs/plan.md § storage.py

"""
In-memory storage layer for the Todo application.

This module provides the TaskStorage class which manages task persistence
using an in-memory dictionary. Tasks are stored with their ID as the key.
"""

from typing import Optional
from models import Task


class TaskStorage:
    """
    In-memory storage for Task objects.
    
    Manages task persistence using a dictionary with task IDs as keys.
    Provides CRUD operations and automatic ID generation.
    
    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Counter for generating unique task IDs
    
    Example:
        >>> storage = TaskStorage()
        >>> task = Task(id=0, title="Buy groceries")
        >>> task_id = storage.add(task)
        >>> retrieved = storage.get(task_id)
        >>> print(retrieved.title)
        Buy groceries
    """
    
    def __init__(self) -> None:
        """
        Initialize empty storage with ID counter starting at 1.
        """
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
    
    def add(self, task: Task) -> int:
        """
        Add a new task to storage.
        
        Assigns a unique ID to the task and stores it in the dictionary.
        The task's ID field is updated with the generated ID.
        
        Args:
            task: Task object to add (ID will be auto-assigned)
        
        Returns:
            int: The unique ID assigned to the task
        
        Example:
            >>> storage = TaskStorage()
            >>> task = Task(id=0, title="Test")
            >>> task_id = storage.add(task)
            >>> print(task_id)
            1
        """
        task.id = self._next_id
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task.id
    
    def get(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: The unique identifier of the task
        
        Returns:
            Task object if found, None if not found
        
        Example:
            >>> storage = TaskStorage()
            >>> task = Task(id=0, title="Test")
            >>> task_id = storage.add(task)
            >>> retrieved = storage.get(task_id)
            >>> print(retrieved.title)
            Test
            >>> storage.get(999)
            None
        """
        return self._tasks.get(task_id)
    
    def get_all(self) -> list[Task]:
        """
        Retrieve all tasks from storage.
        
        Returns tasks sorted by ID in ascending order (oldest first).
        
        Returns:
            List of all Task objects, sorted by ID. Empty list if no tasks.
        
        Example:
            >>> storage = TaskStorage()
            >>> storage.add(Task(id=0, title="Task 1"))
            1
            >>> storage.add(Task(id=0, title="Task 2"))
            2
            >>> tasks = storage.get_all()
            >>> len(tasks)
            2
            >>> [t.id for t in tasks]
            [1, 2]
        """
        return sorted(self._tasks.values(), key=lambda task: task.id)
    
    def update(self, task_id: int, task: Task) -> bool:
        """
        Update an existing task in storage.
        
        Replaces the task at the given ID with the provided task object.
        The task object should have the same ID as task_id.
        
        Args:
            task_id: The ID of the task to update
            task: The updated Task object
        
        Returns:
            True if task was updated, False if task_id not found
        
        Example:
            >>> storage = TaskStorage()
            >>> task = Task(id=0, title="Original")
            >>> task_id = storage.add(task)
            >>> task.title = "Updated"
            >>> storage.update(task_id, task)
            True
            >>> storage.update(999, task)
            False
        """
        if task_id not in self._tasks:
            return False
        self._tasks[task_id] = task
        return True
    
    def delete(self, task_id: int) -> bool:
        """
        Delete a task from storage.
        
        Permanently removes the task with the given ID.
        
        Args:
            task_id: The ID of the task to delete
        
        Returns:
            True if task was deleted, False if task_id not found
        
        Example:
            >>> storage = TaskStorage()
            >>> task = Task(id=0, title="Test")
            >>> task_id = storage.add(task)
            >>> storage.delete(task_id)
            True
            >>> storage.get(task_id)
            None
            >>> storage.delete(999)
            False
        """
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True