<<<<<<< HEAD
# Claude Code Instructions - Phase II Full-Stack Application

## Project Context
You are building **Phase II** of Evolution-Todo: a full-stack web application with Next.js frontend and FastAPI backend.

## Your Role
Generate production-ready code based on specifications. Follow the structure and conventions defined in the constitution and specs.

## Project Structure
```
phase-2-web/
├── frontend/           # Next.js 16 App Router
│   ├── src/app/        # Pages
│   ├── src/components/ # React components
│   └── src/lib/        # Utils, API client
└── backend/            # FastAPI
    ├── src/
    │   ├── models/     # SQLModel models
    │   ├── schemas/    # Pydantic schemas
    │   ├── routers/    # API routes
    │   └── main.py     # FastAPI app
    └── tests/
```

## Workflow
1. Read specifications from `@../specs/`
2. Read constitution principles from `@../constitution.md`
3. Generate code following best practices
4. Use type hints (Python) and TypeScript (optional for speed)
5. Implement proper error handling

## Backend Guidelines (FastAPI)
- Use SQLModel for database models
- Use Pydantic schemas for request/response
- JWT authentication with `python-jose`
- Password hashing with `passlib[bcrypt]`
- CORS enabled for frontend communication
- All routes under `/api/` prefix

## Frontend Guidelines (Next.js)
- Use App Router (not Pages Router)
- Server components by default
- Client components only when needed
- Tailwind CSS for styling
- API calls via fetch in `src/lib/api.ts`
- Better Auth for authentication (if time permits)

## Database
- Use SQLModel models
- Auto-generate tables on startup
- SQLite for development (fast setup)
- PostgreSQL for production (if deployed)

## Authentication Flow
1. User registers: POST /api/auth/register
2. User logs in: POST /api/auth/login → receives JWT token
3. Frontend stores token in localStorage
4. All API requests include: `Authorization: Bearer <token>`
5. Backend validates token on protected routes

## API Conventions
- RESTful design
- JSON responses
- HTTP status codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found)
- Error format: `{"detail": "Error message"}`

## Constraints
- No manual coding - generate from specs
- Keep it simple for time constraint
- Focus on functionality over polish
- Prioritize MUST HAVE features

## Testing Strategy
- Manual testing via browser
- Test user registration/login
- Test task CRUD operations
- Verify multi-user isolation

Ready to implement! Use: "Implement [feature-name]" to start.
=======
# Claude Code Instructions - Phase I Console Todo App

## Project Context

You are helping build **Phase I** of a hackathon project: an **in-memory Python console Todo application**.

This project follows **Spec-Driven Development** - all specifications are written BEFORE code generation.

## Your Role

You are **Claude Code** - an AI coding assistant that generates code based on specifications.

**Critical Rule**: You must ONLY generate code that is explicitly defined in the specifications. Do NOT add features, modify architecture, or make assumptions beyond what is specified.

## Project Structure
```
phase1-console/
├── CONSTITUTION.md          # Project principles and constraints
├── CLAUDE.md               # This file - your instructions
├── specs/                  # All specifications (READ THESE FIRST)
│   ├── overview.md         # Project overview
│   ├── features/
│   │   └── task-crud.md    # Feature requirements (WHAT to build)
│   ├── plan.md             # Architecture plan (HOW to build)
│   └── tasks.md            # Task breakdown (step-by-step)
└── src/                    # Source code (YOU GENERATE THIS)
    ├── models.py
    ├── storage.py
    ├── todo_manager.py
    ├── ui.py
    └── main.py
```

## Workflow: How to Work with Me

### Step 1: Read Specifications FIRST
Before generating ANY code, you MUST read these files in order:

1. `@CONSTITUTION.md` - Understand project principles
2. `@specs/overview.md` - Understand project scope
3. `@specs/features/task-crud.md` - Understand WHAT to build
4. `@specs/plan.md` - Understand HOW to build
5. `@specs/tasks.md` - Understand detailed breakdown

### Step 2: Implement Tasks in Order
Tasks MUST be implemented in this exact order (defined in `specs/tasks.md`):

1. **T-001**: Create Task Model (`src/models.py`)
2. **T-002**: Implement Storage (`src/storage.py`)
3. **T-003**: Implement TodoManager (`src/todo_manager.py`)
4. **T-004**: Implement Console UI (`src/ui.py`)
5. **T-005**: Create Main Entry Point (`src/main.py`)

### Step 3: Implementation Rules

**For EACH task you implement:**
- Reference the task ID in code comments
- Follow the acceptance criteria exactly
- Use the code examples provided as templates
- Add type hints to all functions
- Handle all edge cases mentioned in specs

**Example Comment Format**:
```python
# Task T-001: Create Task Model
# Spec: specs/features/task-crud.md § Data Model
# Plan: specs/plan.md § models.py
```

## Code Generation Guidelines

### Style Requirements (from CONSTITUTION.md)
- Follow PEP 8 Python style guidelines
- Use type hints for all functions and class attributes
- Use descriptive variable names
- Keep functions focused and small (max 20 lines)
- Add docstrings to classes and public methods

### Validation Requirements
- Validate title: 1-200 characters, not empty
- Validate description: max 1000 characters
- Return `None` or `False` for not-found scenarios (don't raise exceptions in storage layer)
- Raise `ValueError` with clear messages for validation errors in manager layer

### Error Handling Strategy
- **Storage Layer**: Return None/False for not-found, never raise
- **Manager Layer**: Validate inputs, raise ValueError for invalid data
- **UI Layer**: Catch all exceptions, show friendly messages

## Example: How to Implement T-001

**User request**: "Implement Task T-001"

**Your process**:
1. Read `@specs/tasks.md` - find Task T-001 section
2. Read acceptance criteria
3. Read code example provided
4. Generate `src/models.py` following the template
5. Add proper comments referencing task and specs
6. Confirm implementation matches all acceptance criteria

**Your output**:
```python
# Task T-001: Create Task Model
# Spec: specs/features/task-crud.md § Data Model
# Plan: specs/plan.md § models.py

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    """
    Represents a todo task.
    
    Attributes:
        id: Unique task identifier
        title: Task title (1-200 chars)
        description: Optional task description (max 1000 chars)
        completed: Completion status
        created_at: Timestamp of creation
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        status = "✓" if self.completed else " "
        return f"[{self.id}] [{status}] {self.title}"
```

## Common Commands You'll Receive

### "Read the specs"
→ Read all files in `@specs/` folder to understand requirements

### "Implement Task T-XXX"
→ Read `@specs/tasks.md`, find task T-XXX, implement according to acceptance criteria

### "Implement all tasks"
→ Implement T-001 through T-005 in order

### "Review the code against specs"
→ Check if generated code matches all acceptance criteria in specs

### "Fix validation in TodoManager"
→ Read `@specs/features/task-crud.md` § Business Rules and update validation logic

## What You Should NOT Do

❌ **Don't** add features not in specifications  
❌ **Don't** change the architecture from plan.md  
❌ **Don't** skip validation requirements  
❌ **Don't** use external libraries (pure Python only)  
❌ **Don't** modify the data model structure  
❌ **Don't** implement database or file storage  

## What You SHOULD Do

✅ **Do** read specifications before coding  
✅ **Do** follow the architecture in plan.md exactly  
✅ **Do** implement all acceptance criteria  
✅ **Do** add proper error handling  
✅ **Do** use type hints everywhere  
✅ **Do** reference task IDs in comments  

## Testing Guidance

After implementation, the human will test manually. Your code should handle:

**Happy Paths**:
- Adding tasks with valid inputs
- Viewing tasks
- Updating tasks
- Deleting tasks
- Toggling completion

**Edge Cases**:
- Empty task list
- Invalid task IDs
- Empty/too-long titles
- Boundary values (200 chars, 1000 chars)

**Error Cases**:
- Invalid menu choices
- Non-numeric inputs

## Final Checklist

Before saying "implementation complete", verify:

- [ ] All 5 tasks (T-001 to T-005) implemented
- [ ] All acceptance criteria met
- [ ] All validation rules implemented
- [ ] All error messages match specs
- [ ] Type hints on all functions
- [ ] Comments reference task IDs
- [ ] No external dependencies added
- [ ] Code follows PEP 8 style

## Questions Protocol

If specifications are unclear or contradictory:
1. State what is unclear
2. Reference specific spec sections
3. Propose clarification questions
4. Wait for human to update specs
5. Do NOT make assumptions and proceed

## Summary

**Your mission**: Generate clean, well-structured Python code that perfectly matches the specifications. Follow the Spec-Driven Development workflow strictly. Read specs first, implement tasks in order, and never deviate from documented requirements.

**Remember**: Specifications are the source of truth. Code is generated to match specs, not the other way around.

---

Ready to begin! Use: "Implement Task T-001" to start.
>>>>>>> b98a1c10b9e3940485ced97c52d2c5194d1260e2
