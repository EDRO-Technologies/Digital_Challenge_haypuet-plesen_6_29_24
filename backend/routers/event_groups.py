from typing import List
from fastapi import APIRouter, Query
from ..deps import SessionDep
from ..schemas import EventGroupCreate, EventGroupRead, EventGroupUpdate
from ..entity import EventGroup
from ..crud.base import get_object_or_404
from ..crud import event_groups as crud

router = APIRouter(prefix="/event-groups", tags=["event-groups"])

@router.post("", response_model=EventGroupRead, status_code=201)
def create_event_group(data: EventGroupCreate, session: SessionDep):
    return crud.create_event_group(session, data)

@router.get("/{id}", response_model=EventGroupRead)
def get_event_group(id: int, session: SessionDep):
    return get_object_or_404(session, EventGroup, id)

@router.get("", response_model=List[EventGroupRead])
def list_event_groups(
    session: SessionDep,
    event_id: int | None = None,
    group_id: int | None = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return crud.list_event_groups(session, event_id, group_id, limit, offset)

@router.patch("/{id}", response_model=EventGroupRead)
def update_event_group(id: int, data: EventGroupUpdate, session: SessionDep):
    obj = get_object_or_404(session, EventGroup, id)
    return crud.update_event_group(session, obj, data)

@router.delete("/{id}", status_code=204)
def delete_event_group(id: int, session: SessionDep):
    obj = get_object_or_404(session, EventGroup, id)
    crud.delete_event_group(session, obj)
    return None