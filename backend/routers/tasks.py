from __future__ import annotations
import datetime as dt
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from backend.db_models import get_session, ActionItem, Meeting

router = APIRouter()


class StatusUpdate(BaseModel):
    status: str  # Pending | In Progress | Completed | Overdue


@router.get("")
def list_tasks(owner: Optional[str] = None, status: Optional[str] = None,
               db: Session = Depends(get_session)):
    q = db.query(ActionItem)
    if owner:
        q = q.filter(ActionItem.owner == owner)
    if status:
        q = q.filter(ActionItem.status == status)
    tasks = q.all()

    today = dt.date.today()
    out = []
    for t in tasks:
        status_val = t.status
        try:
            if status_val == "Pending" and t.deadline and dt.datetime.strptime(t.deadline, "%Y-%m-%d").date() < today:
                status_val = "Overdue"
        except Exception:
            pass
        out.append({
            "id": t.id, "meeting_id": t.meeting_id, "task": t.task, "owner": t.owner,
            "owner_is_predicted": t.owner_is_predicted, "deadline": t.deadline,
            "deadline_is_predicted": t.deadline_is_predicted, "priority": t.priority,
            "status": status_val,
        })
    return out


@router.patch("/{task_id}/status")
def update_status(task_id: int, body: StatusUpdate, db: Session = Depends(get_session)):
    t = db.query(ActionItem).get(task_id)
    if not t:
        raise HTTPException(404, "Task not found")
    t.status = body.status
    if body.status == "Completed":
        t.completed_at = dt.date.today().isoformat()
    db.commit()
    return {"id": t.id, "status": t.status}


@router.post("/{task_id}/remind")
def send_reminder(task_id: int, db: Session = Depends(get_session)):
    """Hook this up to your email service (utils/audio_processor.py's sibling,
    e.g. utils/email_service.py) to actually send mail. Marks reminder_sent for now."""
    t = db.query(ActionItem).get(task_id)
    if not t:
        raise HTTPException(404, "Task not found")
    t.reminder_sent = True
    db.commit()
    # TODO: plug in real email send, e.g.:
    # from utils.email_service import send_email
    # send_email(to=owner_email(t.owner), subject="Task reminder", body=f"Reminder: {t.task} due {t.deadline}")
    return {"id": t.id, "reminder_sent": True}
