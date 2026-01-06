# Task T-003: Implement TodoManager
# Spec: specs/features/task-crud.md § All User Stories + Business Rules
# Plan: specs/plan.md § todo_manager.py

"""
Business logic layer for the Todo application.

This module provides the TodoManager class which orchestrates task operations,
enforces business rules, and validates inputs before delegating to storage.
"""

from typing import Optional
from models import Task
from storage import TaskStorage


class TodoManager:
    """
    Manages todo task operations with validation and business logic.
    
    Acts as an intermediary between the UI and storage layers, ensuring
    all business rules are enforced and inputs are validated before
    performing operations.
    
    Attributes:
        storage: TaskStorage instance for data persistence
    
    Example:
        >>> storage = TaskStorage()
        >>> manager = TodoManager(storage)
        >>> task = manager.create_task("Buy groceries", "Milk, eggs")
        >>> print(task.title)
        Buy groceries
    """
    
    def __init__(self, storage: TaskStorage) -> None:
        """
        Initialize TodoManager with a storage backend.
        
        Args:
            storage: TaskStorage instance for persisting tasks
        """
        self.storage = storage
    
    def create_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task with validation.
        
        Validates title and description, creates a Task object with
        auto-generated ID and timestamp, and stores it.
        
        Args:
            title: Task title (required, 1-200 characters)
            description: Optional task description (max 1000 characters)
        
        Returns:
            Task: The newly created task with assigned ID
        
        Raises:
            ValueError: If title is empty, too long, or description is too long
        
        Example:
            >>> manager = TodoManager(TaskStorage())
            >>> task = manager.create_task("Buy groceries", "Milk, eggs")
            >>> print(task.id)
            1
        """
        # Validate inputs
        self._validate_title(title)
        self._validate_description(description)
        
        # Create task (ID will be assigned by storage)
        task = Task(
            id=0,  # Placeholder, will be overwritten by storage
            title=title.strip(),
            description=description,
            completed=False
        )
        
        # Store and return
        self.storage.add(task)
        return task
    
    def list_tasks(self) -> list[Task]:
        """
        Retrieve all tasks from storage.
        
        Returns:
            List of all tasks, sorted by ID (oldest first)
        
        Example:
            >>> manager = TodoManager(TaskStorage())
            >>> manager.create_task("Task 1")
            >>> manager.create_task("Task 2")
            >>> tasks = manager.list_tasks()
            >>> len(tasks)
            2
        """
        return self.storage.get_all()
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a specific task by ID.
        
        Args:
            task_id: The unique identifier of the task
        
        Returns:
            Task object if found, None if not found
        
        Example:
            >>> manager = TodoManager(TaskStorage())
            >>> task = manager.create_task("Test")
            >>> retrieved = manager.get_task(task.id)
            >>> print(retrieved.title)
            Test
        """
        return self.storage.get(task_id)
    
    def update_task(
        self, 
        task_id: int, 
        title: Optional[str] = None, 
        description: Optional[str] = None
    ) -> bool:
        """
        Update an existing task's title and/or description.
        
        Retrieves the task, validates new values if provided, updates
        the fields, and saves back to storage. None values keep original.
        
        Args:
            task_id: The ID of the task to update
            title: New title (None to keep current), 1-200 chars if provided
            description: New description (None to keep current), max 1000 chars
        
        Returns:
            True if task was updated, False if task not found
        
        Raises:
            ValueError: If title is empty, too long, or description is too long
        
        Example:
            >>> manager = TodoManager(TaskStorage())
            >>> task = manager.create_task("Original")
            >>> manager.update_task(task.id, title="Updated")
            True
            >>> manager.update_task(999)
            False
        """
        # Get existing task
        task = self.storage.get(task_id)
        if task is None:
            return False
        
        # Validate and update title if provided
        if title is not None:
            self._validate_title(title)
            task.title = title.strip()
        
        # Validate and update description if provided
        if description is not None:
            self._validate_description(description)
            task.description = description
        
        # Save updated task
        return self.storage.update(task_id, task)
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from storage.
        
        Args:
            task_id: The ID of the task to delete
        
        Returns:
            True if task was deleted, False if task not found
        
        Example:
            >>> manager = TodoManager(TaskStorage())
            >>> task = manager.create_task("To delete")
            >>> manager.delete_task(task.id)
            True
            >>> manager.get_task(task.id)
            None
        """
        return self.storage.delete(task_id)
    
    def toggle_complete(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.
        
        Flips the task's completed status between True and False.
        
        Args:
            task_id: The ID of the task to toggle
        
        Returns:
            True if task was toggled, False if task not found
        
        Example:
            >>> manager = TodoManager(TaskStorage())
            >>> task = manager.create_task("Test")
            >>> print(task.completed)
            False
            >>> manager.toggle_complete(task.id)
            True
            >>> updated = manager.get_task(task.id)
            >>> print(updated.completed)
            True
        """
        # Get existing task
        task = self.storage.get(task_id)
        if task is None:
            return False
        
        # Toggle completion status
        task.completed = not task.completed
        
        # Save updated task
        return self.storage.update(task_id, task)
    
    def _validate_title(self, title: str) -> None:
        """
        Validate task title according to business rules.
        
        Rules:
        - Cannot be empty or whitespace only
        - Maximum 200 characters
        
        Args:
            title: The title to validate
        
        Raises:
            ValueError: If title is empty or too long
        
        Example:
            >>> manager = TodoManager(TaskStorage())
            >>> manager._validate_title("Valid title")  # No error
            >>> manager._validate_title("")  # Raises ValueError
        """
        if not title or title.strip() == "":
            raise ValueError("Title cannot be empty")
        
        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less")
    
    def _validate_description(self, description: str) -> None:
        """
        Validate task description according to business rules.
        
        Rules:
        - Maximum 1000 characters
        - Empty description is allowed (optional field)
        
        Args:
            description: The description to validate
        
        Raises:
            ValueError: If description is too long
        
        Example:
            >>> manager = TodoManager(TaskStorage())
            >>> manager._validate_description("Valid description")  # No error
            >>> manager._validate_description("x" * 1001)  # Raises ValueError
        """
        if len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")