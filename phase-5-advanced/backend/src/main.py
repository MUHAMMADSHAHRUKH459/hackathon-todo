# src/main.py
import os

# Manually set only database variables
os.environ['DATABASE_URL'] = "postgresql://neondb_owner:npg_OnC1e4KspNdk@ep-purple-hat-ahw4nk3o-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
os.environ['SECRET_KEY'] = "hackathon-production-secret-key-phase2-2026"
os.environ['ALGORITHM'] = "HS256"
os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] = "1440"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models.database import init_db
from src.routers import auth_routes, task_routes, chat_routes, tag_routes

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="Full-Stack Todo Application API with AI Chatbot - Phase V Advanced",
    version="5.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(task_routes.router)
app.include_router(chat_routes.router)
app.include_router(tag_routes.router)  # NEW - Phase 5

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized!")
    print("🤖 AI Chatbot enabled!")
    print("✨ Phase V Advanced Features enabled!")

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Todo API - Phase V (Advanced Cloud Deployment)",
        "status": "running",
        "version": "5.0",
        "features": ["AI Chatbot", "Priorities", "Tags", "Due Dates"]
    }