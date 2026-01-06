# Implementation Plan - Phase I Console Todo App

## Architecture Overview

This application follows a **3-layer architecture**:
```
┌─────────────────────────────────────┐
│      User Interface Layer           │
│  (ui.py - Console I/O)              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Business Logic Layer           │
│  (todo_manager.py - Operations)     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Data Layer                     │
│  (storage.py - In-memory storage)   │
│  (models.py - Task model)           │
└─────────────────────────────────────┘
```

## Component Breakdown

### 1. Data Layer

#### models.py
**Purpose**: Define the Task data structure

**Class: Task**
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
```

**Responsibilities:**
- Define Task structure with type hints
- Provide data validation in constructor
- Implement string representation for display

---

#### storage.py
**Purpose**: Manage in-memory task storage

**Class: TaskStorage**
```python
class TaskStorage:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
    
    Methods:
    - add(task: Task) -> int
    - get(task_id: int) -> Task | None
    - get_all() -> list[Task]
    - update(task_id: int, task: Task) -> bool
    - delete(task_id: int) -> bool
```

**Responsibilities:**
- Store tasks in dictionary (key: id, value: Task)
- Generate unique IDs
- Provide CRUD operations
- Return None/False for not-found scenarios

---

### 2. Business Logic Layer

#### todo_manager.py
**Purpose**: Implement business logic and orchestration

**Class: TodoManager**
```python
class TodoManager:
    def __init__(self, storage: TaskStorage):
        self.storage = storage
    
    Methods:
    - create_task(title: str, description: str) -> Task
    - list_tasks() -> list[Task]
    - get_task(task_id: int) -> Task | None
    - update_task(task_id: int, title: str, description: str) -> bool
    - delete_task(task_id: int) -> bool
    - toggle_complete(task_id: int) -> bool
```

**Responsibilities:**
- Validate inputs (title length, etc.)
- Create Task objects with timestamps
- Delegate storage operations
- Implement business rules

---

### 3. User Interface Layer

#### ui.py
**Purpose**: Handle console input/output

**Class: ConsoleUI**
```python
class ConsoleUI:
    def __init__(self, manager: TodoManager):
        self.manager = manager
    
    Methods:
    - show_menu() -> None
    - prompt_add_task() -> None
    - prompt_view_tasks() -> None
    - prompt_update_task() -> None
    - prompt_delete_task() -> None
    - prompt_toggle_complete() -> None
    - get_input(prompt: str) -> str
    - display_tasks(tasks: list[Task]) -> None
    - display_error(message: str) -> None
    - display_success(message: str) -> None
```

**Responsibilities:**
- Display menu options
- Get user input
- Show formatted task lists
- Display error/success messages
- Handle menu navigation loop

---

#### main.py
**Purpose**: Application entry point
```python
def main():
    # Initialize components
    storage = TaskStorage()
    manager = TodoManager(storage)
    ui = ConsoleUI(manager)
    
    # Start application
    ui.run()

if __name__ == "__main__":
    main()
```

**Responsibilities:**
- Wire up dependencies
- Start the application

## Data Flow Examples

### Example 1: Add Task
```
User Input → UI.prompt_add_task()
          → Manager.create_task(title, desc)
          → Validate inputs
          → Create Task object with ID and timestamp
          → Storage.add(task)
          → Return Task
          → UI displays success message
```

### Example 2: View Tasks
```
User Input → UI.prompt_view_tasks()
          → Manager.list_tasks()
          → Storage.get_all()
          → Return list[Task]
          → UI.display_tasks(tasks)
```

### Example 3: Toggle Complete
```
User Input → UI.prompt_toggle_complete()
          → Get task_id from user
          → Manager.toggle_complete(task_id)
          → Storage.get(task_id)
          → Flip task.completed
          → Storage.update(task_id, task)
          → UI displays new status
```

## Menu Structure
```
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit

Enter choice (1-6):
```

## Error Handling Strategy

| Layer | Responsibility |
|-------|----------------|
| UI Layer | Catch all exceptions, show friendly messages |
| Manager Layer | Validate inputs, raise ValueError for invalid data |
| Storage Layer | Return None/False for not-found, never raise |

## Validation Rules

### Title Validation
```python
def validate_title(title: str) -> None:
    if not title or title.strip() == "":
        raise ValueError("Title cannot be empty")
    if len(title) > 200:
        raise ValueError("Title must be 200 characters or less")
```

### Description Validation
```python
def validate_description(description: str) -> None:
    if len(description) > 1000:
        raise ValueError("Description must be 1000 characters or less")
```

## File Organization
```
src/
├── main.py              # Entry point (10-15 lines)
├── models.py            # Task model (20-30 lines)
├── storage.py           # In-memory storage (50-70 lines)
├── todo_manager.py      # Business logic (80-100 lines)
└── ui.py                # Console interface (150-200 lines)
```

## Dependencies

**Standard Library Only:**
- `dataclasses` - For Task model
- `datetime` - For timestamps
- `typing` - For type hints

**No external packages required.**

## Testing Strategy (Manual)

1. **Happy Path**: Test all features with valid inputs
2. **Edge Cases**: 
   - Empty task list
   - Invalid task IDs
   - Empty/too-long titles
   - Boundary values (200 chars, 1000 chars)
3. **Error Handling**:
   - Invalid menu choices
   - Non-numeric inputs
   - Edge case inputs

## Implementation Order

1. ✅ models.py - Define Task
2. ✅ storage.py - Implement storage
3. ✅ todo_manager.py - Business logic
4. ✅ ui.py - Console interface
5. ✅ main.py - Wire everything together
6. ✅ Manual testing