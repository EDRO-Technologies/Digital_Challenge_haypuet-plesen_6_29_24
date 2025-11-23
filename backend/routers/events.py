from typing import List
import datetime
from fastapi import APIRouter, Query
from ..deps import SessionDep
from ..schemas import EventCreate, EventRead, EventUpdate
from ..entity import Event, EventsPeriodicity
from ..crud.base import get_object_or_404
from ..crud import events as crud

router = APIRouter(prefix="/events", tags=["events"])

@router.post("", response_model=EventRead, status_code=201)
def create_event(data: EventCreate, session: SessionDep):
    return crud.create_event(session, data)

@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, session: SessionDep):
    return get_object_or_404(session, Event, event_id)

@router.get("", response_model=List[EventRead])
def list_events(
    session: SessionDep,
    week_day: int | None = Query(None, ge=1, le=7),
    periodicity: EventsPeriodicity | None = None,
    location: int | None = None,
    date_from: datetime.datetime | None = None,
    date_to: datetime.datetime | None = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return crud.list_events(session, week_day, periodicity, location, date_from, date_to, limit, offset)

@router.patch("/{event_id}", response_model=EventRead)
def update_event(event_id: int, data: EventUpdate, session: SessionDep):
    obj = get_object_or_404(session, Event, event_id)
    return crud.update_event(session, obj, data)

@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, session: SessionDep):
    obj = get_object_or_404(session, Event, event_id)
    crud.delete_event(session, obj)
    return None

@router.get("/by_group_id/{group_id}", response_model=list[EventRead])
def list_events_by_group_id(group_id: int, session: SessionDep):
    return crud.get_by_group_id(session, group_id)