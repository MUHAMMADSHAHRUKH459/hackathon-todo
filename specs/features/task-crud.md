# Feature Specification: Task CRUD Operations

## Feature ID
F-001: Basic Task Management

## Description
Users can manage their todo tasks through a console interface with full CRUD (Create, Read, Update, Delete) operations plus completion tracking.

## User Stories

### US-001: Add Task
**As a user**, I want to create new tasks so that I can track things I need to do.

**Acceptance Criteria:**
- Title is required (1-200 characters)
- Description is optional (max 1000 characters)
- Task gets unique auto-generated ID
- Task is marked as incomplete by default
- Creation timestamp is automatically recorded
- Success message is displayed after creation

**Example Interaction:**
```
> Add Task
Enter title: Buy groceries
Enter description (optional): Milk, eggs, bread
✓ Task #1 created successfully: "Buy groceries"
```

### US-002: View All Tasks
**As a user**, I want to see all my tasks so that I know what needs to be done.

**Acceptance Criteria:**
- Display all tasks in a clear list format
- Show task ID, title, and completion status
- Show "No tasks found" if list is empty
- Display tasks in order of creation (oldest first)
- Show total count of tasks

**Example Output:**
```
Your Tasks:
[1] [ ] Buy groceries
[2] [✓] Call mom
[3] [ ] Finish report

Total: 3 tasks (1 completed, 2 pending)
```

### US-003: Update Task
**As a user**, I want to modify task details so that I can correct or improve task information.

**Acceptance Criteria:**
- User can update title and/or description
- User selects task by ID
- Original values are shown before update
- Empty input keeps original value
- Success message confirms update
- Error if task ID doesn't exist

**Example Interaction:**
```
> Update Task
Enter task ID: 1
Current title: Buy groceries
New title (press Enter to keep): Buy groceries and fruits
Current description: Milk, eggs, bread
New description (press Enter to keep): 
✓ Task #1 updated successfully
```

### US-004: Delete Task
**As a user**, I want to remove tasks so that I can clean up my list.

**Acceptance Criteria:**
- User selects task by ID
- Confirmation prompt before deletion
- Task is permanently removed
- Success message after deletion
- Error if task ID doesn't exist

**Example Interaction:**
```
> Delete Task
Enter task ID: 1
Are you sure you want to delete "Buy groceries"? (y/n): y
✓ Task #1 deleted successfully
```

### US-005: Mark Task Complete/Incomplete
**As a user**, I want to toggle task completion status so that I can track my progress.

**Acceptance Criteria:**
- User selects task by ID
- Toggle between complete ↔ incomplete
- Visual indicator shows status (✓ for complete)
- Success message shows new status
- Error if task ID doesn't exist

**Example Interaction:**
```
> Toggle Complete
Enter task ID: 1
✓ Task #1 marked as complete
```

## Data Model

### Task
```python
class Task:
    id: int              # Auto-generated, unique
    title: str           # Required, 1-200 chars
    description: str     # Optional, max 1000 chars
    completed: bool      # Default: False
    created_at: datetime # Auto-generated
```

## Business Rules

1. **Task ID**: Must be unique and auto-incremented
2. **Title Validation**: Cannot be empty, max 200 characters
3. **Description**: Optional field, max 1000 characters
4. **Deletion**: Permanent, no recovery option
5. **Empty List**: Show friendly message, not error

## Error Handling

| Scenario | Error Message |
|----------|---------------|
| Empty title | "Title cannot be empty" |
| Title too long | "Title must be 200 characters or less" |
| Description too long | "Description must be 1000 characters or less" |
| Invalid task ID | "Task #X not found" |
| Invalid input | "Invalid input. Please try again." |

## Non-Functional Requirements

- **Performance**: All operations complete in < 100ms
- **Usability**: Clear prompts and feedback messages
- **Reliability**: Handle all invalid inputs gracefully
- **Maintainability**: Clean, well-documented code