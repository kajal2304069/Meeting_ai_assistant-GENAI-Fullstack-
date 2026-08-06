from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db_models import get_session, Meeting
from backend.core_ext.search_engine import search as ai_search

router = APIRouter()


@router.get("")
def search_meetings(q: str, db: Session = Depends(get_session)):
    meetings = db.query(Meeting).all()
    payload = [{
        "id": m.id, "title": m.title,
        "date": m.date.isoformat() if m.date else None,
        "transcript": m.transcript or "", "summary": m.summary or "",
    } for m in meetings]
    return ai_search(q, payload)
