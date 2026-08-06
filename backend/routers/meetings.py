from __future__ import annotations
import datetime as dt
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.db_models import get_session, Meeting, ActionItem, Employee
from backend.core_ext.sentiment_analyzer import analyze_sentiment
from backend.core_ext.deadline_predictor import predict_deadline
from backend.core_ext.task_assigner import auto_assign_all

router = APIRouter()


class ProcessMeetingRequest(BaseModel):
    source: str  # YouTube URL, meeting recording URL, or local file path
    language: str = "english"


def _run_real_pipeline(source: str, language: str) -> dict:
    """Uses YOUR existing, working pipeline from main.py."""
    from main import run_pipeline
    return run_pipeline(source, language)


def _process_and_store(source: str, language: str, db: Session):
    result = _run_real_pipeline(source, language)

    sentiment = analyze_sentiment(result["transcript"])

    roster = [e.name for e in db.query(Employee).all()]
    action_items = auto_assign_all(result.get("action_items") or [], result["transcript"], roster)
    action_items = [predict_deadline(t) for t in action_items]

    meeting = Meeting(
        external_ref=source,
        title=result.get("title"),
        date=dt.datetime.utcnow(),
        language=language,
        transcript=result.get("transcript"),
        summary=result.get("summary"),
        key_decisions=str(result.get("key_decisions")),
        open_questions=str(result.get("open_questions")),
        sentiment=sentiment["sentiment"],
        sentiment_confidence=sentiment["confidence"],
    )
    db.add(meeting)
    db.flush()  # get meeting.id

    for t in action_items:
        db.add(ActionItem(
            meeting_id=meeting.id,
            task=t.get("task", ""),
            owner=t.get("owner"),
            owner_is_predicted=t.get("owner_is_predicted", False),
            deadline=str(t.get("deadline")),
            deadline_is_predicted=t.get("deadline_is_predicted", False),
            priority=t.get("priority", "medium"),
            status=t.get("status", "Pending"),
        ))
    db.commit()
    return meeting.id


@router.post("/process")
def process_meeting(req: ProcessMeetingRequest, background_tasks: BackgroundTasks,
                     db: Session = Depends(get_session)):
    """Kicks off the full pipeline (transcription -> summary -> tasks -> sentiment
    -> auto-assignment -> deadline prediction) and stores the result. Runs in the
    background since transcription can take a while; poll GET /api/meetings to see it land."""
    try:
        background_tasks.add_task(_process_and_store, req.source, req.language, db)
        return {"status": "processing", "message": "Meeting is being processed. It will appear in the meetings list shortly."}
    except Exception as e:
        raise HTTPException(500, f"Failed to start processing: {e}")


@router.get("")
def list_meetings(db: Session = Depends(get_session)):
    meetings = db.query(Meeting).order_by(Meeting.date.desc()).all()
    return [{
        "id": m.id, "title": m.title, "date": m.date.isoformat() if m.date else None,
        "language": m.language, "sentiment": m.sentiment,
        "sentiment_confidence": m.sentiment_confidence,
        "summary": (m.summary or "")[:220],
        "task_count": len(m.tasks),
    } for m in meetings]


@router.get("/{meeting_id}")
def get_meeting(meeting_id: int, db: Session = Depends(get_session)):
    m = db.query(Meeting).get(meeting_id)
    if not m:
        raise HTTPException(404, "Meeting not found")
    return {
        "id": m.id, "title": m.title, "date": m.date.isoformat() if m.date else None,
        "language": m.language, "transcript": m.transcript, "summary": m.summary,
        "key_decisions": m.key_decisions, "open_questions": m.open_questions,
        "sentiment": m.sentiment, "sentiment_confidence": m.sentiment_confidence,
        "tasks": [{
            "id": t.id, "task": t.task, "owner": t.owner,
            "owner_is_predicted": t.owner_is_predicted, "deadline": t.deadline,
            "deadline_is_predicted": t.deadline_is_predicted, "priority": t.priority,
            "status": t.status,
        } for t in m.tasks],
    }
