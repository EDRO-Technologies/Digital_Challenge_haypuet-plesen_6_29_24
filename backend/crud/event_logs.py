from sqlmodel import Session, select
from fastapi import HTTPException
from ..models import EventLog, Event
from ..schemas import EventLogCreate, EventLogUpdate

def create_event_log(session: Session, data: EventLogCreate) -> EventLog:
    if session.get(Event, data.old_event) is None:
        raise HTTPException(404, "Old event not found")
    if session.get(Event, data.new_event) is None:
        raise HTTPException(404, "New event not found")
    obj = EventLog(**data.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def get_event_log(session: Session, obj_id: int) -> EventLog | None:
    return session.get(EventLog, obj_id)

def list_event_logs(session: Session, old_event=None, new_event=None, limit=50, offset=0):
    stmt = select(EventLog)
    if old_event is not None:
        stmt = stmt.where(EventLog.old_event == old_event)
    if new_event is not None:
        stmt = stmt.where(EventLog.new_event == new_event)
    stmt = stmt.limit(limit).offset(offset)
    return session.exec(stmt).all()

def delete_event_log(session: Session, obj: EventLog):
    session.delete(obj)
    session.commit()