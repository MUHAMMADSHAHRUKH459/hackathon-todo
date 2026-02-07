# Phase V - Cloud Deployment Guide

## Deployment Options

### Option 1: DigitalOcean (Recommended)
**Why:** Easiest, affordable, good for hackathons

**Steps:**
1. Create DOKS cluster ($12/month)
2. Push Docker images to registry
3. Apply Kubernetes manifests
4. Configure domain & SSL
5. Setup monitoring

**Cost:** ~$15-20/month

---

### Option 2: AWS EKS
**Why:** Enterprise-grade, scalable

**Steps:**
1. Create EKS cluster
2. Setup ECR for images
3. Configure IAM roles
4. Deploy with kubectl
5. Setup ALB ingress

**Cost:** ~$75/month

---

### Option 3: Google Cloud GKE
**Why:** Free tier, good integration

**Steps:**
1. Enable GKE API
2. Create cluster (Autopilot)
3. Push to Artifact Registry
4. Deploy workloads
5. Configure Cloud Load Balancer

**Cost:** Free tier available

---

## Pre-Deployment Checklist

### Code
- [x] All features working locally
- [x] Tests passing
- [x] Environment variables configured
- [x] Error handling implemented

### Docker
- [ ] Dockerfiles optimized
- [ ] Multi-stage builds
- [ ] Images under 500MB
- [ ] Health checks added

### Kubernetes
- [ ] Manifests created
- [ ] Resource limits set
- [ ] Secrets configured
- [ ] Services exposed

### Database
- [ ] Migration strategy
- [ ] Backup plan
- [ ] Connection pooling
- [ ] SSL enabled

### Security
- [ ] HTTPS enabled
- [ ] CORS configured
- [ ] Rate limiting
- [ ] Auth tokens secured

---

## DigitalOcean Deployment (Detailed)

### Step 1: Create Account
```bash
# Sign up at digitalocean.com
# Add payment method
# Get $200 credit (student/new user)
```

### Step 2: Install doctl
```bash
# Download from digitalocean.com/docs/apis-clis/doctl
# Authenticate
doctl auth init
```

### Step 3: Create Kubernetes Cluster
```bash
# Via UI or CLI
doctl kubernetes cluster create todo-cluster \
  --region nyc1 \
  --version 1.28 \
  --node-pool "name=worker-pool;size=s-2vcpu-4gb;count=2"
```

### Step 4: Connect kubectl
```bash
doctl kubernetes cluster kubeconfig save todo-cluster
kubectl get nodes
```

### Step 5: Create Container Registry
```bash
doctl registry create todo-registry
doctl registry login
```

### Step 6: Build & Push Images
```bash
# Backend
cd backend
docker build -t registry.digitalocean.com/todo-registry/backend:v1 .
docker push registry.digitalocean.com/todo-registry/backend:v1

# Frontend
cd ../frontend
docker build -t registry.digitalocean.com/todo-registry/frontend:v1 .
docker push registry.digitalocean.com/todo-registry/frontend:v1
```

### Step 7: Update Kubernetes Manifests
```yaml
# Update image paths in deployment files
image: registry.digitalocean.com/todo-registry/backend:v1
```

### Step 8: Deploy
```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get services
```

### Step 9: Get Load Balancer IP
```bash
kubectl get svc frontend-service
# Note EXTERNAL-IP
```

### Step 10: Configure Domain (Optional)
```bash
# Point domain to Load Balancer IP
# Setup SSL with cert-manager
```

---

## Environment Variables (Production)
```yaml
# Backend
DATABASE_URL: postgresql://user:pass@host/db
SECRET_KEY: production-secret-key-256-bits
OPENAI_API_KEY: sk-or-v1-...
CORS_ORIGINS: https://yourdomain.com

# Frontend
NEXT_PUBLIC_API_URL: https://api.yourdomain.com
```

---

## Monitoring Setup

### Prometheus + Grafana
```bash
# Install with Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
```

### Access Grafana
```bash
kubectl port-forward svc/prometheus-grafana 3000:80
# Login: admin / prom-operator
```

---

## Scaling

### Horizontal Pod Autoscaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Cost Optimization

1. Use node pools efficiently
2. Right-size resources
3. Enable autoscaling
4. Use managed database
5. Optimize images
6. Cache static assets
7. Use CDN for frontend

**Estimated Monthly Cost:**
- DOKS Cluster: $12
- Load Balancer: $10
- Managed DB: $15
- **Total: ~$37/month**

---

## Rollback Strategy
```bash
# List deployments
kubectl rollout history deployment/todo-backend

# Rollback to previous version
kubectl rollout undo deployment/todo-backend

# Rollback to specific revision
kubectl rollout undo deployment/todo-backend --to-revision=2
```

---

## Backup & Recovery

### Database Backups
- Automated daily backups (managed DB)
- Point-in-time recovery
- Manual snapshots before deployments

### Application State
- Store configs in ConfigMaps/Secrets
- Version control all manifests
- Document deployment procedures