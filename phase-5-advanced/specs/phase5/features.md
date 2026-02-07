# Phase V Features Specification

## Feature 1: Task Priorities

### Description
Users can assign priority levels to tasks (Low, Medium, High).

### Implementation
**Backend:**
- Added `priority` column to Task model (default: "medium")
- Updated TaskCreate schema with priority field
- API accepts priority in create/update endpoints

**Frontend:**
- Priority dropdown in Add Task modal
- Color-coded priority badges:
  - 🔴 High - Red
  - 🟡 Medium - Yellow
  - 🟢 Low - Green
- Task card border changes based on priority
- High Priority count in stats

### User Flow
1. Click "Add Task"
2. Select priority from dropdown
3. Submit task
4. See priority badge on task card
5. View high priority count in stats

---

## Feature 2: Tags System

### Description
Custom tags for categorizing tasks.

### Implementation
**Backend:**
- `tags` table with user_id, name, color
- `task_tags` junction table
- Tag CRUD endpoints

**Frontend:**
- Tag management interface
- Tag chips on tasks
- Tag-based filtering
- Color picker for tags

### User Flow
1. Create custom tags (Work, Personal, Urgent)
2. Assign tags to tasks
3. Filter tasks by tags
4. Edit/delete tags

---

## Feature 3: Due Dates

### Description
Set deadlines for tasks.

### Implementation
**Backend:**
- Added `due_date` column (DateTime, nullable)
- API accepts ISO datetime strings

**Frontend:**
- Date picker in Add Task modal
- Due date display on tasks
- Overdue highlighting
- Sort by due date

---

## Feature 4: Search & Filter

### Description
Search tasks by title/description, filter by priority/tags/status.

### Implementation
**Backend:**
- Search query parameter
- Filter by multiple criteria
- Sorting options

**Frontend:**
- Search bar in dashboard
- Filter dropdown (All, Pending, Completed, High Priority)
- Sort options (Date, Priority, Title)

---

## Feature 5: Cloud Deployment

### Platforms
- DigitalOcean Kubernetes (DOKS)
- AWS EKS
- Google Cloud GKE

### Components
- Load Balancer
- Auto-scaling
- Database (Managed PostgreSQL)
- Redis (Optional caching)
- CI/CD pipeline

### Monitoring
- Prometheus + Grafana
- Application logs
- Error tracking (Sentry)
- Uptime monitoring