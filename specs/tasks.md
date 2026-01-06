# Task Breakdown - Phase I Console Todo App

## Task Organization

Tasks are organized by component and must be implemented in order due to dependencies.

---

## Component 1: Data Models

### Task T-001: Create Task Model
**Priority**: HIGH  
**Estimated Lines**: 20-30  
**Dependencies**: None

**Description**: Implement the Task data model using dataclass.

**Acceptance Criteria**:
- [ ] Task class defined with all required fields
- [ ] Uses @dataclass decorator
- [ ] All fields have proper type hints
- [ ] created_at defaults to current datetime
- [ ] completed defaults to False
- [ ] __str__ method for readable display

**Reference**: 
- Spec: `specs/features/task-crud.md` § Data Model
- Plan: `specs/plan.md` § models.py

**Code Location**: `src/models.py`

**Example**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
```

---

## Component 2: Data Storage

### Task T-002: Implement In-Memory Storage
**Priority**: HIGH  
**Estimated Lines**: 50-70  
**Dependencies**: T-001

**Description**: Create TaskStorage class for in-memory task management.

**Acceptance Criteria**:
- [ ] TaskStorage class with private _tasks dict
- [ ] _next_id counter for auto-incrementing IDs
- [ ] add() method returns new task ID
- [ ] get() returns Task or None
- [ ] get_all() returns list of all tasks sorted by ID
- [ ] update() returns True/False
- [ ] delete() returns True/False
- [ ] All methods handle edge cases

**Reference**: 
- Spec: `specs/features/task-crud.md` § All User Stories
- Plan: `specs/plan.md` § storage.py

**Code Location**: `src/storage.py`

**Methods to Implement**:
```python
class TaskStorage:
    def __init__(self)
    def add(self, task: Task) -> int
    def get(self, task_id: int) -> Task | None
    def get_all(self) -> list[Task]
    def update(self, task_id: int, task: Task) -> bool
    def delete(self, task_id: int) -> bool
```

---

## Component 3: Business Logic

### Task T-003: Implement TodoManager
**Priority**: HIGH  
**Estimated Lines**: 80-100  
**Dependencies**: T-001, T-002

**Description**: Create TodoManager class with business logic and validation.

**Acceptance Criteria**:
- [ ] TodoManager takes TaskStorage in constructor
- [ ] create_task() validates title (1-200 chars)
- [ ] create_task() validates description (max 1000 chars)
- [ ] create_task() creates Task with auto-ID and timestamp
- [ ] list_tasks() returns all tasks
- [ ] get_task() wraps storage.get()
- [ ] update_task() validates inputs before update
- [ ] delete_task() wraps storage.delete()
- [ ] toggle_complete() flips completion status
- [ ] All validation errors raise ValueError with clear messages

**Reference**: 
- Spec: `specs/features/task-crud.md` § All User Stories + Business Rules
- Plan: `specs/plan.md` § todo_manager.py

**Code Location**: `src/todo_manager.py`

**Methods to Implement**:
```python
class TodoManager:
    def __init__(self, storage: TaskStorage)
    def create_task(self, title: str, description: str = "") -> Task
    def list_tasks(self) -> list[Task]
    def get_task(self, task_id: int) -> Task | None
    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool
    def delete_task(self, task_id: int) -> bool
    def toggle_complete(self, task_id: int) -> bool
    def _validate_title(self, title: str) -> None  # private helper
    def _validate_description(self, description: str) -> None  # private helper
```

---

## Component 4: User Interface

### Task T-004: Implement Console Menu
**Priority**: HIGH  
**Estimated Lines**: 150-200  
**Dependencies**: T-003

**Description**: Create ConsoleUI class for user interaction.

**Acceptance Criteria**:
- [ ] ConsoleUI takes TodoManager in constructor
- [ ] run() method shows menu in a loop until exit
- [ ] Menu displays 6 options clearly
- [ ] Each menu option calls appropriate prompt method
- [ ] Invalid menu choices show error and re-prompt
- [ ] Clear screen between operations (optional)

**Reference**: 
- Spec: `specs/features/task-crud.md` § All User Stories
- Plan: `specs/plan.md` § ui.py, Menu Structure

**Code Location**: `src/ui.py`

**Sub-tasks**:

#### T-004a: Menu System
```python
def run(self) -> None
def show_menu(self) -> None
def get_menu_choice(self) -> str
```

#### T-004b: Add Task Interface
```python
def prompt_add_task(self) -> None
# Get title and description
# Call manager.create_task()
# Show success or error message
```

**Example Interaction**:
```
=== Add New Task ===
Enter title: Buy groceries
Enter description (optional): Milk, eggs, bread
✓ Task #1 created successfully: "Buy groceries"
```

#### T-004c: View Tasks Interface
```python
def prompt_view_tasks(self) -> None
def display_tasks(self, tasks: list[Task]) -> None
# Format and display all tasks
# Show completion status with symbols
# Show total count
```

**Example Output**:
```
=== Your Tasks ===
[1] [ ] Buy groceries
[2] [✓] Call mom

Total: 2 tasks (1 completed, 1 pending)
```

#### T-004d: Update Task Interface
```python
def prompt_update_task(self) -> None
# Get task ID
# Show current values
# Get new values (empty = keep current)
# Call manager.update_task()
```

#### T-004e: Delete Task Interface
```python
def prompt_delete_task(self) -> None
# Get task ID
# Show confirmation prompt
# Call manager.delete_task()
```

#### T-004f: Toggle Complete Interface
```python
def prompt_toggle_complete(self) -> None
# Get task ID
# Call manager.toggle_complete()
# Show new status
```

#### T-004g: Helper Methods
```python
def get_input(self, prompt: str) -> str
def display_success(self, message: str) -> None
def display_error(self, message: str) -> None
def display_info(self, message: str) -> None
```

---

## Component 5: Application Entry

### Task T-005: Create Main Entry Point
**Priority**: MEDIUM  
**Estimated Lines**: 10-15  
**Dependencies**: T-004

**Description**: Wire up all components and start the application.

**Acceptance Criteria**:
- [ ] main() function creates all components
- [ ] Proper dependency injection (storage → manager → ui)
- [ ] Exception handling for unexpected errors
- [ ] Clean exit message

**Reference**: 
- Plan: `specs/plan.md` § main.py

**Code Location**: `src/main.py`

**Implementation**:
```python
from storage import TaskStorage
from todo_manager import TodoManager
from ui import ConsoleUI

def main():
    try:
        # Initialize components
        storage = TaskStorage()
        manager = TodoManager(storage)
        ui = ConsoleUI(manager)
        
        # Start application
        print("=== Todo App - Phase I ===\n")
        ui.run()
        
        print("\nThank you for using Todo App!")
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
```

---

## Implementation Order Summary

| Order | Task ID | Component | Priority |
|-------|---------|-----------|----------|
| 1 | T-001 | Task Model | HIGH |
| 2 | T-002 | Storage | HIGH |
| 3 | T-003 | TodoManager | HIGH |
| 4 | T-004 | Console UI | HIGH |
| 5 | T-005 | Main Entry | MEDIUM |

## Testing Checklist (After Implementation)

### Feature Tests
- [ ] Can add task with title only
- [ ] Can add task with title and description
- [ ] Can view empty task list
- [ ] Can view tasks with correct status symbols
- [ ] Can update task title
- [ ] Can update task description
- [ ] Can delete task with confirmation
- [ ] Can mark task as complete
- [ ] Can mark task as incomplete (toggle back)

### Validation Tests
- [ ] Empty title is rejected
- [ ] Title over 200 chars is rejected
- [ ] Description over 1000 chars is rejected
- [ ] Invalid task ID shows error
- [ ] Invalid menu choice shows error

### Edge Cases
- [ ] Menu works with list empty
- [ ] Menu works with single task
- [ ] Menu works with many tasks
- [ ] Task IDs increment correctly
- [ ] Timestamps are set correctly

---

## Total Estimated Lines of Code: 310-415 lines

**Breakdown**:
- models.py: 20-30 lines
- storage.py: 50-70 lines
- todo_manager.py: 80-100 lines
- ui.py: 150-200 lines
- main.py: 10-15 lines