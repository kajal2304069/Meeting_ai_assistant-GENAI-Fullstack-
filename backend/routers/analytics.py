from __future__ import annotations
import datetime as dt
from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db_models import get_session, Meeting, ActionItem, Employee
from backend.core_ext.productivity_scorer import score_employee, score_team

router = APIRouter()


@router.get("/overview")
def overview(db: Session = Depends(get_session)):
    meetings = db.query(Meeting).all()
    tasks = db.query(ActionItem).all()
    today = dt.date.today()

    missed = 0
    for t in tasks:
        if t.status != "Completed" and t.deadline:
            try:
                if dt.datetime.strptime(t.deadline, "%Y-%m-%d").date() < today:
                    missed += 1
            except Exception:
                pass

    sentiment_counts = defaultdict(int)
    for m in meetings:
        if m.sentiment:
            sentiment_counts[m.sentiment] += 1

    return {
        "total_meetings": len(meetings),
        "total_tasks": len(tasks),
        "completed_tasks": len([t for t in tasks if t.status == "Completed"]),
        "missed_deadlines": missed,
        "sentiment_breakdown": dict(sentiment_counts),
    }


@router.get("/productivity")
def productivity(db: Session = Depends(get_session)):
    tasks = db.query(ActionItem).all()
    by_owner = defaultdict(list)
    for t in tasks:
        owner = t.owner or "Unassigned"
        by_owner[owner].append({
            "status": t.status, "deadline": t.deadline,
            "completed_at": t.completed_at, "priority": t.priority,
        })
    return score_team(by_owner)


@router.get("/productivity/{employee_name}")
def productivity_for(employee_name: str, db: Session = Depends(get_session)):
    tasks = db.query(ActionItem).filter(ActionItem.owner == employee_name).all()
    payload = [{
        "status": t.status, "deadline": t.deadline,
        "completed_at": t.completed_at, "priority": t.priority,
    } for t in tasks]
    return score_employee(payload)


@router.get("/meeting-trends")
def meeting_trends(db: Session = Depends(get_session)):
    meetings = db.query(Meeting).all()
    by_week = defaultdict(int)
    for m in meetings:
        if m.date:
            week = m.date.strftime("%Y-W%W")
            by_week[week] += 1
    return [{"week": k, "count": v} for k, v in sorted(by_week.items())]
