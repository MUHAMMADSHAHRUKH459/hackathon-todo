# Docker Specification - Phase IV

## Objective
Containerize the Todo Chatbot application (Phase III) for Kubernetes deployment.

## Architecture
```
┌─────────────────┐     ┌─────────────────┐
│  Frontend       │     │  Backend        │
│  Container      │────▶│  Container      │
│  (Next.js)      │     │  (FastAPI+MCP)  │
│  Port: 3000     │     │  Port: 8000     │
└─────────────────┘     └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
            ┌─────────────────┐
            │  Neon DB        │
            │  (External)     │
            └─────────────────┘
```

## Container Requirements

### Frontend Container
- **Base Image**: `node:20-alpine`
- **Working Directory**: `/app`
- **Build Steps**:
  1. Copy package.json and package-lock.json
  2. Run `npm install`
  3. Copy application code
  4. Run `npm run build`
  5. Expose port 3000
  6. Start command: `npm start`

### Backend Container
- **Base Image**: `python:3.13-slim`
- **Working Directory**: `/app`
- **Build Steps**:
  1. Copy requirements.txt
  2. Run `pip install -r requirements.txt`
  3. Copy application code
  4. Expose port 8000
  5. Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://backend:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@neon.tech/dbname
OPENAI_API_KEY=your-api-key
```

## Docker Commands (Using Gordon)

### Build Images
```bash
docker ai "build frontend image from phase-3/frontend with tag todo-frontend:latest"
docker ai "build backend image from phase-3/backend with tag todo-backend:latest"
```

### Run Containers Locally (Test)
```bash
docker ai "run frontend container on port 3000"
docker ai "run backend container on port 8000"
```

### Push to Registry (Optional for cloud)
```bash
docker tag todo-frontend:latest yourusername/todo-frontend:latest
docker tag todo-backend:latest yourusername/todo-backend:latest
docker push yourusername/todo-frontend:latest
docker push yourusername/todo-backend:latest
```

## Success Criteria
- [ ] Frontend Dockerfile builds successfully
- [ ] Backend Dockerfile builds successfully
- [ ] Containers run locally without errors
- [ ] Frontend can connect to backend
- [ ] Backend can connect to Neon DB
- [ ] Images are under 500MB each (optimized)