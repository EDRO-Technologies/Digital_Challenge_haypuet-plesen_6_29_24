from typing import List
from fastapi import APIRouter, Query
from ..deps import SessionDep
from ..schemas import LocationCreate, LocationRead, LocationUpdate
from ..entity import Location
from ..crud.base import get_object_or_404
from ..crud import locations as crud

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("", response_model=LocationRead, status_code=201)
def create_location(data: LocationCreate, session: SessionDep):
    return crud.create_location(session, data)

@router.get("/{location_id}", response_model=LocationRead)
def get_location(location_id: int, session: SessionDep):
    return get_object_or_404(session, Location, location_id)

@router.get("", response_model=List[LocationRead])
def list_locations(
    session: SessionDep,
    address_q: str | None = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return crud.list_locations(session, address_q, limit, offset)

@router.patch("/{location_id}", response_model=LocationRead)
def update_location(location_id: int, data: LocationUpdate, session: SessionDep):
    obj = get_object_or_404(session, Location, location_id)
    return crud.update_location(session, obj, data)

@router.delete("/{location_id}", status_code=204)
def delete_location(location_id: int, session: SessionDep):
    obj = get_object_or_404(session, Location, location_id)
    crud.delete_location(session, obj)
    return None