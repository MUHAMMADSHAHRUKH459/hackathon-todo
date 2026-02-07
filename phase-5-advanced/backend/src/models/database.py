# src/models/database.py
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# SQLAlchemy setup
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    print("📁 Using SQLite database")
else:
    # PostgreSQL/Neon connection
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    print("🐘 Using PostgreSQL (Neon) database")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Priority Enum (Phase 5)
class PriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

# Task Model (Updated - Phase 5)
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, index=True)
    priority = Column(String(10), default="medium", index=True)  # NEW - Phase 5
    due_date = Column(DateTime, nullable=True)  # NEW - Phase 5
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="tasks")
    tags = relationship("TaskTag", back_populates="task", cascade="all, delete-orphan")  # NEW

# Tag Model (NEW - Phase 5)
class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    color = Column(String(7), default="#3B82F6")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User")
    tasks = relationship("TaskTag", back_populates="tag", cascade="all, delete-orphan")

# Task-Tag Association (NEW - Phase 5)
class TaskTag(Base):
    __tablename__ = "task_tags"
    
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
    
    # Relationships
    task = relationship("Task", back_populates="tags")
    tag = relationship("Tag", back_populates="tasks")

# Conversation Model (Phase 3)
class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    owner = relationship("User")

# Message Model (Phase 3)
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    owner = relationship("User")

# Create tables
def init_db():
    print(f"🔗 Connecting to database...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified!")
        print("✨ Phase 5 tables added: Tags, TaskTags, Priority, DueDate")
    except Exception as e:
        print(f"❌ Database error: {e}")
        raise