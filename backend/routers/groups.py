from typing import List
from fastapi import APIRouter, Query
from ..deps import SessionDep
from ..schemas import GroupCreate, GroupRead, GroupUpdate
from ..entity import Group
from ..crud.base import get_object_or_404
from ..crud import groups as crud

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("", response_model=GroupRead, status_code=201)
def create_group(data: GroupCreate, session: SessionDep):
    return crud.create_group(session, data)

@router.get("/{group_id}", response_model=GroupRead)
def get_group(group_id: int, session: SessionDep):
    return get_object_or_404(session, Group, group_id)

@router.get("", response_model=List[GroupRead])
def list_groups(
    session: SessionDep,
    q: str | None = Query(None, description="Поиск по названию"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return crud.list_groups(session, q, limit, offset)

@router.patch("/{group_id}", response_model=GroupRead)
def update_group(group_id: int, data: GroupUpdate, session: SessionDep):
    obj = get_object_or_404(session, Group, group_id)
    return crud.update_group(session, obj, data)

@router.delete("/{group_id}", status_code=204)
def delete_group(group_id: int, session: SessionDep):
    obj = get_object_or_404(session, Group, group_id)
    crud.delete_group(session, obj)
    return None