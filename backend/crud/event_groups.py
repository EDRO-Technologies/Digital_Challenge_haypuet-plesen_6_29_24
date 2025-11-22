from sqlmodel import Session, select
from fastapi import HTTPException
from ..entity import EventGroup, User, Group
from ..schemas import EventGroupCreate, EventGroupUpdate

def create_event_group(session: Session, data: EventGroupCreate) -> EventGroup:
    if session.get(User, data.event_id) is None:
        raise HTTPException(404, "Event not found")
    if session.get(Group, data.group_id) is None:
        raise HTTPException(404, "Group not found")
    obj = EventGroup(**data.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def get_event_group(session: Session, obj_id: int) -> EventGroup | None:
    return session.get(EventGroup, obj_id)

def list_event_groups(session: Session, event_id=None, group_id=None, limit=50, offset=0):
    stmt = select(EventGroup)
    if event_id is not None:
        stmt = stmt.where(EventGroup.user_id == event_id)
    if group_id is not None:
        stmt = stmt.where(EventGroup.group_id == group_id)
    stmt = stmt.limit(limit).offset(offset)
    return session.exec(stmt).all()

def update_event_group(session: Session, obj: EventGroup, data: EventGroupUpdate) -> EventGroup:
    payload = data.model_dump(exclude_unset=True)
    if "event_id" in payload and session.get(User, payload["event_id"]) is None:
        raise HTTPException(404, "Event not found")
    if "group_id" in payload and session.get(Group, payload["group_id"]) is None:
        raise HTTPException(404, "Group not found")
    for k, v in payload.items():
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def delete_event_group(session: Session, obj: EventGroup):
    session.delete(obj)
    session.commit()