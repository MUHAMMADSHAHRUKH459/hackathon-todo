# Phase V API Documentation

## Base URL
```
Development: http://127.0.0.1:8000
Production: https://api.yourdomain.com
```

## Authentication
All endpoints require Bearer token except auth endpoints.
```http
Authorization: Bearer <token>
```

---

## Tags Endpoints

### Create Tag
```http
POST /api/tags
```

**Request:**
```json
{
  "name": "Work",
  "color": "#3B82F6"
}
```

**Query Parameters:**
- `user_id` (required): User ID

**Response:**
```json
{
  "id": 1,
  "name": "Work",
  "color": "#3B82F6",
  "user_id": 1
}
```

---

### List Tags
```http
GET /api/tags?user_id=1
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Work",
    "color": "#3B82F6",
    "user_id": 1
  },
  {
    "id": 2,
    "name": "Personal",
    "color": "#10B981",
    "user_id": 1
  }
]
```

---

### Delete Tag
```http
DELETE /api/tags/1?user_id=1
```

**Response:**
```json
{
  "message": "Tag deleted"
}
```

---

## Tasks Endpoints (Updated)

### Create Task
```http
POST /api/tasks
```

**Request:**
```json
{
  "title": "Complete Phase V",
  "description": "Deploy to cloud",
  "priority": "high",
  "due_date": "2026-01-30T10:00:00Z"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete Phase V",
  "description": "Deploy to cloud",
  "priority": "high",
  "due_date": "2026-01-30T10:00:00",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-29T12:00:00",
  "updated_at": "2026-01-29T12:00:00"
}
```

---

### Update Task
```http
PUT /api/tasks/1
```

**Request:**
```json
{
  "title": "Updated title",
  "priority": "medium",
  "completed": true
}
```

---

## Priority Values
- `low` - 🟢 Low priority
- `medium` - 🟡 Medium priority (default)
- `high` - 🔴 High priority

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "detail": "Task not found"
}
```

### 500 Server Error
```json
{
  "detail": "Internal server error"
}
```