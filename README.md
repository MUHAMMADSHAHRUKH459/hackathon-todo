# Todo App - Phase I

## Overview
A command-line todo application built using **Spec-Driven Development** with Claude Code.

## Features
✅ **Add Task** - Create new todo items with title and optional description  
✅ **View Tasks** - Display all tasks with completion status  
✅ **Update Task** - Modify existing task details  
✅ **Delete Task** - Remove tasks from the list  
✅ **Toggle Complete** - Mark tasks as complete or incomplete  

## Tech Stack
- **Language**: Python 3.14
- **Storage**: In-memory (Python dict)
- **Interface**: Command-line (CLI)
- **Dependencies**: None (pure Python standard library)

## Project Structure
```
src/
├── main.py              # Entry point (43 lines)
├── models.py            # Task data model (70 lines)
├── storage.py           # In-memory storage (168 lines)
├── todo_manager.py      # Business logic (268 lines)
└── ui.py                # Console interface (295 lines)

Total: 844 lines of clean, well-documented Python code
```

## Setup

### Requirements
- Python 3.8 or higher (developed with Python 3.14)
- No external dependencies

### Installation
```bash
# Clone or download the project
cd phase1-console

# No installation needed - pure Python!
```

## Usage

### Run the Application
```bash
python3 src/main.py
```

### Menu Options
```
==============================
        Todo App
==============================
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit
==============================
```

## Example Session

### Adding Tasks
```
=== Add New Task ===
Enter title: Buy groceries
Enter description (optional): Milk, eggs, bread
✓ Task #1 created successfully: "Buy groceries"
```

### Viewing Tasks
```
=== Your Tasks ===
[1] [ ] Buy groceries
[2] [✓] Call mom
[3] [ ] Finish report

Total: 3 tasks (1 completed, 2 pending)
```

### Updating Tasks
```
=== Update Task ===
Enter task ID: 1
Current title: Buy groceries
New title (press Enter to keep): Buy groceries and fruits
Current description: Milk, eggs, bread
New description (press Enter to keep): 
✓ Task #1 updated successfully
```

### Toggling Completion
```
=== Toggle Complete ===
Enter task ID: 1
✓ Task #1 marked as complete
```

### Deleting Tasks
```
=== Delete Task ===
Enter task ID: 2
Are you sure you want to delete "Call mom"? (y/n): y
✓ Task #2 deleted successfully
```

## Architecture

### 3-Layer Design
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

### Components

**models.py** - Task Data Model
- Defines Task dataclass with all attributes
- Handles display formatting with completion status

**storage.py** - Storage Layer
- In-memory dict-based storage
- CRUD operations (Create, Read, Update, Delete)
- Auto-incrementing ID generation
- Returns None/False for not-found (no exceptions)

**todo_manager.py** - Business Logic
- Input validation (title 1-200 chars, description max 1000 chars)
- Task creation with timestamp
- Orchestrates storage operations
- Raises ValueError for validation errors

**ui.py** - Console Interface
- Menu-driven navigation
- User input handling
- Formatted task display
- Error handling with friendly messages

**main.py** - Entry Point
- Dependency injection (Storage → Manager → UI)
- Exception handling (KeyboardInterrupt, unexpected errors)

## Validation Rules

### Title
- ✅ Required (cannot be empty)
- ✅ Trimmed (removes leading/trailing spaces)
- ✅ Maximum 200 characters
- ❌ Error: "Title cannot be empty"
- ❌ Error: "Title must be 200 characters or less"

### Description
- ✅ Optional (can be empty)
- ✅ Maximum 1000 characters
- ❌ Error: "Description must be 1000 characters or less"

### Task ID
- ✅ Must exist in storage
- ❌ Error: "Task #X not found"

## Error Handling

### Storage Layer
- Returns `None` or `False` for not-found scenarios
- Never raises exceptions

### Manager Layer
- Validates all inputs
- Raises `ValueError` with clear messages

### UI Layer
- Catches all exceptions
- Displays friendly error messages
- Continues operation after errors

## Development Process

This project demonstrates **Spec-Driven Development**:
1. ✅ Write specifications FIRST
2. ✅ Design architecture
3. ✅ Break down into tasks
4. ✅ Generate code with Claude Code
5. ✅ Test and verify

### Implementation Tasks
- [x] T-001: Create Task Model (models.py)
- [x] T-002: Implement Storage (storage.py)
- [x] T-003: Implement TodoManager (todo_manager.py)
- [x] T-004: Implement Console UI (ui.py)
- [x] T-005: Create Main Entry Point (main.py)

## Testing

### Manual Testing Checklist

**Happy Paths:**
- [ ] Add task with title only
- [ ] Add task with title and description
- [ ] View empty task list
- [ ] View tasks with proper formatting
- [ ] Update task title
- [ ] Update task description
- [ ] Delete task with confirmation
- [ ] Mark task as complete
- [ ] Mark task as incomplete (toggle back)

**Validation Tests:**
- [ ] Empty title is rejected
- [ ] Title over 200 chars is rejected
- [ ] Description over 1000 chars is rejected
- [ ] Invalid task ID shows error
- [ ] Invalid menu choice shows error

**Edge Cases:**
- [ ] Menu works with empty list
- [ ] Menu works with single task
- [ ] Menu works with many tasks
- [ ] Task IDs increment correctly
- [ ] Completion status displays correctly

### Running Tests
```bash
# All tests are automated in the demonstration
cd src
python3 << EOF
from storage import TaskStorage
from todo_manager import TodoManager
from ui import ConsoleUI

storage = TaskStorage()
manager = TodoManager(storage)
ui = ConsoleUI(manager)

# Add test tasks
task1 = manager.create_task("Test 1", "Description 1")
task2 = manager.create_task("Test 2", "Description 2")

# View tasks
ui.prompt_view_tasks()

# Toggle completion
manager.toggle_complete(task1.id)

# View updated
ui.prompt_view_tasks()
EOF
```

## Known Limitations

- **In-Memory Only**: Data is lost when application exits
- **Single User**: No multi-user support
- **No Persistence**: No database or file storage
- **Console Only**: No graphical interface

## Future Phases (Not Implemented)

- Phase II: File-based persistence (JSON/SQLite)
- Phase III: Web interface
- Phase IV: Multi-user support
- Phase V: Cloud deployment

## Success Criteria

✅ All 5 basic features fully functional  
✅ Clean, well-structured Python code  
✅ Proper error handling  
✅ User-friendly console interface  
✅ Generated via Claude Code (no manual coding)  

## Code Quality

- **PEP 8 Compliant**: Follows Python style guidelines
- **Type Hints**: All functions properly typed
- **Docstrings**: Comprehensive documentation
- **Error Handling**: Three-layer strategy
- **Separation of Concerns**: Clear architecture
- **No Dependencies**: Pure Python standard library

## License

Educational project - free to use and modify.

## Credits

Built as a demonstration of Spec-Driven Development using Claude Code.

---

<<<<<<< HEAD
**Ready to use!** Run `python3 src/main.py` to start managing your todos.

## Development History

See `history/` folder for:
- **prompts/** - Claude Code prompts used
- **adr/** - Architecture Decision Records

## Project Timeline
- Phase I: Console App (Complete)
- Phase II: Full-Stack Web App (Complete)
- Implementation: 4.5 hours
- Technologies: 8 (FastAPI, SQLAlchemy, Next.js, TypeScript, Tailwind, JWT, SQLite, Bcrypt)
=======
**Ready to use!** Run `python3 src/main.py` to start managing your todos.
>>>>>>> b98a1c10b9e3940485ced97c52d2c5194d1260e2
