"""
Additive DB layer for the dashboard/API features (search index, task
tracking status, sentiment, productivity scores, employees). These are NEW
tables that reference your existing meetings/tasks by id/title — they do
not modify or replace database/save_data.py, so your working pipeline save
path keeps working exactly as-is.

If your existing schema already has a `meetings` / `tasks` table with
different columns, either:
  (a) point DATABASE_URL at the same Postgres DB — these tables will sit
      alongside yours, or
  (b) adjust the ForeignKey targets below to match your real table/column
      names once you share them.
"""
from __future__ import annotations
import os
import datetime as dt
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Float, Boolean,
    DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/meeting_ai")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    email = Column(String(200))
    team = Column(String(120))
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class Meeting(Base):
    __tablename__ = "meetings_index"
    id = Column(Integer, primary_key=True)
    external_ref = Column(String(255))  # source URL / file path from main.py
    title = Column(String(500))
    date = Column(DateTime, default=dt.datetime.utcnow)
    language = Column(String(50), default="english")
    transcript = Column(Text)
    summary = Column(Text)
    key_decisions = Column(Text)
    open_questions = Column(Text)
    sentiment = Column(String(20))
    sentiment_confidence = Column(Float)
    duration_minutes = Column(Float, nullable=True)

    tasks = relationship("ActionItem", back_populates="meeting", cascade="all, delete-orphan")


class ActionItem(Base):
    __tablename__ = "action_items_index"
    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings_index.id"))
    task = Column(Text, nullable=False)
    owner = Column(String(200))
    owner_is_predicted = Column(Boolean, default=False)
    deadline = Column(String(20))
    deadline_is_predicted = Column(Boolean, default=False)
    priority = Column(String(20), default="medium")
    status = Column(String(20), default="Pending")  # Pending | In Progress | Completed | Overdue
    completed_at = Column(String(20), nullable=True)
    reminder_sent = Column(Boolean, default=False)

    meeting = relationship("Meeting", back_populates="tasks")


class ProductivitySnapshot(Base):
    __tablename__ = "productivity_snapshots"
    id = Column(Integer, primary_key=True)
    employee_name = Column(String(200))
    score = Column(Float)
    completed = Column(Integer)
    total = Column(Integer)
    on_time_rate = Column(Float)
    computed_at = Column(DateTime, default=dt.datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
