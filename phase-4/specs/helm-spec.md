# Helm Chart Specification - Phase IV

## Objective
Package the Todo Chatbot application as a Helm chart for easy deployment and management.

## Helm Chart Structure
```
helm-charts/
└── todo-app/
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── frontend-deployment.yaml
    │   ├── frontend-service.yaml
    │   ├── backend-deployment.yaml
    │   ├── backend-service.yaml
    │   ├── secrets.yaml
    │   └── _helpers.tpl
    └── README.md
```

## Chart.yaml
```yaml
apiVersion: v2
name: todo-app
description: A Helm chart for Todo Chatbot Application
type: application
version: 1.0.0
appVersion: "1.0"
keywords:
  - todo
  - chatbot
  - ai
  - openai
maintainers:
  - name: Your Name
    email: your.email@example.com
```

## values.yaml
```yaml
# Frontend Configuration
frontend:
  replicaCount: 2
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: Never
  service:
    type: NodePort
    port: 3000
    nodePort: 30000
  env:
    apiUrl: "http://todo-backend:8000"

# Backend Configuration
backend:
  replicaCount: 2
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: Never
  service:
    type: ClusterIP
    port: 8000
  env:
    databaseUrl: ""  # Set via --set or secrets
    openaiApiKey: ""  # Set via --set or secrets

# Secrets (base64 encoded)
secrets:
  databaseUrl: ""
  openaiApiKey: ""

# Resource Limits
resources:
  frontend:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi
  backend:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi
```

## Template Files

### templates/frontend-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.fullname" . }}-frontend
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
    app.kubernetes.io/component: frontend
spec:
  replicas: {{ .Values.frontend.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-app.selectorLabels" . | nindent 6 }}
      app.kubernetes.io/component: frontend
  template:
    metadata:
      labels:
        {{- include "todo-app.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: frontend
    spec:
      containers:
      - name: frontend
        image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}"
        imagePullPolicy: {{ .Values.frontend.image.pullPolicy }}
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: {{ .Values.frontend.env.apiUrl }}
        resources:
          {{- toYaml .Values.resources.frontend | nindent 10 }}
```

### templates/backend-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.fullname" . }}-backend
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
    app.kubernetes.io/component: backend
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-app.selectorLabels" . | nindent 6 }}
      app.kubernetes.io/component: backend
  template:
    metadata:
      labels:
        {{- include "todo-app.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: backend
    spec:
      containers:
      - name: backend
        image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
        imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {{ include "todo-app.fullname" . }}-secrets
              key: database-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: {{ include "todo-app.fullname" . }}-secrets
              key: openai-api-key
        resources:
          {{- toYaml .Values.resources.backend | nindent 10 }}
```

### templates/_helpers.tpl
```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
{{ include "todo-app.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## Helm Commands

### Create Chart Structure (using kubectl-ai)
```bash
kubectl-ai "create helm chart for todo-app with frontend and backend"
```

### Install Chart
```bash
# Install with default values
helm install todo-release ./helm-charts/todo-app

# Install with custom values
helm install todo-release ./helm-charts/todo-app \
  --set backend.env.databaseUrl="postgresql://..." \
  --set backend.env.openaiApiKey="sk-..."

# Install with values file
helm install todo-release ./helm-charts/todo-app \
  -f custom-values.yaml
```

### Upgrade Chart
```bash
helm upgrade todo-release ./helm-charts/todo-app
```

### Check Status
```bash
helm status todo-release
helm list
```

### Uninstall
```bash
helm uninstall todo-release
```

### Validate Chart
```bash
helm lint ./helm-charts/todo-app
helm template ./helm-charts/todo-app
```

## kubectl-ai + Helm Integration
```bash
# Deploy using kubectl-ai
kubectl-ai "install todo app using helm chart with 3 frontend replicas"

# Check deployment
kubectl-ai "show me all resources created by helm release todo-release"

# Troubleshoot
kubectl-ai "why is my helm deployment failing?"
```

## Success Criteria
- [ ] Helm chart structure created
- [ ] Chart.yaml properly configured
- [ ] values.yaml with all configurable options
- [ ] All template files render correctly
- [ ] helm lint passes without errors
- [ ] helm install deploys successfully
- [ ] Application accessible via NodePort
- [ ] helm upgrade works without downtime
- [ ] helm uninstall removes all resources