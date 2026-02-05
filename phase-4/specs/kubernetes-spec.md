# Kubernetes Specification - Phase IV

## Objective
Deploy Todo Chatbot on local Minikube cluster with proper service discovery and resource management.

## Architecture
```
┌────────────────────────────────────────────────────────────┐
│                    MINIKUBE CLUSTER                        │
│                                                            │
│  ┌──────────────────┐         ┌──────────────────┐       │
│  │  Frontend Pod    │         │  Backend Pod     │       │
│  │  ┌────────────┐  │         │  ┌────────────┐  │       │
│  │  │ Next.js    │  │         │  │ FastAPI    │  │       │
│  │  │ Container  │  │         │  │ + MCP      │  │       │
│  │  └────────────┘  │         │  └────────────┘  │       │
│  └────────┬─────────┘         └────────┬─────────┘       │
│           │                            │                  │
│  ┌────────▼─────────┐         ┌────────▼─────────┐       │
│  │  Frontend        │         │  Backend         │       │
│  │  Service         │         │  Service         │       │
│  │  (NodePort)      │         │  (ClusterIP)     │       │
│  │  Port: 30000     │         │  Port: 8000      │       │
│  └──────────────────┘         └──────────────────┘       │
│           │                            │                  │
└───────────┼────────────────────────────┼──────────────────┘
            │                            │
            │                            ▼
            │                   ┌─────────────────┐
            │                   │  Neon DB        │
            └──────────────────▶│  (External)     │
                                └─────────────────┘
```

## Kubernetes Resources

### 1. Frontend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://todo-backend:8000"
```

### 2. Frontend Service (NodePort)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
spec:
  type: NodePort
  selector:
    app: todo-frontend
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30000
```

### 3. Backend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: database-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: openai-api-key
```

### 4. Backend Service (ClusterIP)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
spec:
  type: ClusterIP
  selector:
    app: todo-backend
  ports:
  - port: 8000
    targetPort: 8000
```

### 5. Secrets (ConfigMap for non-sensitive data)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
type: Opaque
data:
  database-url: <base64-encoded-neon-url>
  openai-api-key: <base64-encoded-api-key>
```

## kubectl-ai Commands

### Deploy Application
```bash
kubectl-ai "deploy todo frontend with 2 replicas using todo-frontend:latest image"
kubectl-ai "deploy todo backend with 2 replicas using todo-backend:latest image"
```

### Create Services
```bash
kubectl-ai "create NodePort service for frontend on port 3000"
kubectl-ai "create ClusterIP service for backend on port 8000"
```

### Check Status
```bash
kubectl-ai "check if all pods are running"
kubectl-ai "show me the frontend service URL"
```

### Troubleshooting
```bash
kubectl-ai "why is the backend pod failing?"
kubectl-ai "show logs of frontend pod"
kubectl-ai "restart all backend pods"
```

## Deployment Steps

### 1. Start Minikube
```bash
minikube start
minikube status
```

### 2. Load Docker Images into Minikube
```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 3. Create Secrets
```bash
# Encode secrets
echo -n "postgresql://user:pass@neon.tech/db" | base64
echo -n "sk-your-openai-key" | base64

# Create secret
kubectl create secret generic todo-secrets \
  --from-literal=database-url='postgresql://...' \
  --from-literal=openai-api-key='sk-...'
```

### 4. Apply Manifests
```bash
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml
```

### 5. Access Application
```bash
minikube service todo-frontend --url
# Opens: http://192.168.49.2:30000
```

## Success Criteria
- [ ] Minikube cluster running
- [ ] Frontend pods: 2/2 Ready
- [ ] Backend pods: 2/2 Ready
- [ ] Services created and accessible
- [ ] Frontend can access backend via service name
- [ ] Application works end-to-end
- [ ] kubectl-ai can query and manage resources