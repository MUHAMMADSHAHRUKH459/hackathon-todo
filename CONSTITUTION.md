# Todo App Constitution - Phase I

## Project Principles

### 1. Code Quality
- Follow PEP 8 Python style guidelines
- Use type hints for all functions
- Write clear, descriptive variable names
- Keep functions small and focused (max 20 lines)

### 2. Architecture
- Separate concerns: data storage, business logic, user interface
- Use classes for data models (Task class)
- Store tasks in memory using Python dict

### 3. User Experience
- Clear, friendly console messages
- Handle invalid inputs gracefully
- Provide helpful error messages
- Confirm actions (e.g., "Task added successfully")

### 4. Data Model
```python
Task:
  - id: int (auto-generated)
  - title: str (required, max 200 chars)
  - description: str (optional, max 1000 chars)
  - completed: bool (default False)
  - created_at: datetime
```

### 5. Tech Stack Constraints
- Python 3.14
- No external libraries for Phase I (pure Python)
- In-memory storage only (no database)
- Console-based interface

### 6. Testing Approach
- Manual testing for Phase I
- Test all CRUD operations
- Test edge cases (empty lists, invalid IDs, etc.)

## Development Rules

1. **Spec-First**: Never write code without a specification
2. **Claude Code Only**: All code must be generated via Claude Code
3. **No Manual Coding**: Refine specs until Claude generates correct code
4. **Iterative**: Build feature by feature, test after each

## Success Criteria

- All 5 basic features working correctly
- Clean, readable code
- Proper error handling
- User-friendly console interface

## Error Handling Strategy

| Layer | Responsibility |
|-------|----------------|
| UI Layer | Catch all exceptions, show friendly messages |
| Manager Layer | Validate inputs, raise ValueError for invalid data |
| Storage Layer | Return None/False for not-found, never raise |

## Validation Rules

### Title Validation
- Cannot be empty
- Must be trimmed (no leading/trailing spaces)
- Maximum 200 characters
- Error message: "Title cannot be empty" or "Title must be 200 characters or less"

### Description Validation
- Optional field
- Maximum 1000 characters
- Error message: "Description must be 1000 characters or less"

### Task ID Validation
- Must exist in storage
- Error message: "Task #X not found"