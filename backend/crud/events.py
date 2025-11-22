import datetime
from sqlmodel import Session, select
from fastapi import HTTPException
from ..entity import Event, Location, EventsPeriodicity
from ..schemas import EventCreate, EventUpdate, EventRead
# from users import User


def create_event(session: Session, data: EventCreate) -> Event:
    obj = Event(**data.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def get_event(session: Session, obj_id: int) -> Event | None:
    return session.get(Event, obj_id)

def list_events(
    session: Session,
    week_day: int | None = None,
    periodicity: EventsPeriodicity | None = None,
    location: int | None = None,
    date_from: datetime.datetime | None = None,
    date_to: datetime.datetime | None = None,
    limit: int = 50,
    offset: int = 0,
):
    stmt = select(Event)
    if week_day is not None:
        stmt = stmt.where(Event.week_day == week_day)
    if periodicity is not None:
        stmt = stmt.where(Event.periodicity == periodicity)
    if location is not None:
        stmt = stmt.where(Event.location == location)
    if date_from is not None:
        stmt = stmt.where((Event.date.is_not(None)) & (Event.date >= date_from))
    if date_to is not None:
        stmt = stmt.where((Event.date.is_not(None)) & (Event.date <= date_to))
    stmt = stmt.limit(limit).offset(offset)
    return session.exec(stmt).all()

def update_event(session: Session, obj: Event, data: EventUpdate) -> Event:
    payload = data.model_dump(exclude_unset=True)
    if "location" in payload and session.get(Location, payload["location"]) is None:
        raise HTTPException(404, "Location not found")
    for k, v in payload.items():
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def delete_event(session: Session, obj: Event):
    session.delete(obj)
    session.commit()