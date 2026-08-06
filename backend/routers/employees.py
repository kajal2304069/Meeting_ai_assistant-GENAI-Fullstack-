from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.db_models import get_session, Employee

router = APIRouter()


class EmployeeIn(BaseModel):
    name: str
    email: str | None = None
    team: str | None = None


@router.get("")
def list_employees(db: Session = Depends(get_session)):
    return [{"id": e.id, "name": e.name, "email": e.email, "team": e.team}
            for e in db.query(Employee).all()]


@router.post("")
def add_employee(body: EmployeeIn, db: Session = Depends(get_session)):
    existing = db.query(Employee).filter(Employee.name == body.name).first()
    if existing:
        raise HTTPException(400, "Employee already exists")
    e = Employee(name=body.name, email=body.email, team=body.team)
    db.add(e)
    db.commit()
    return {"id": e.id, "name": e.name}
