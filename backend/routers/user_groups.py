from typing import List
from fastapi import APIRouter, Query
from ..deps import SessionDep
from ..schemas import UserGroupCreate, UserGroupRead, UserGroupUpdate
from ..entity import UserGroup
from ..crud.base import get_object_or_404
from ..crud import user_groups as crud

router = APIRouter(prefix="/user-groups", tags=["user-groups"])

@router.post("", response_model=UserGroupRead, status_code=201)
def create_user_group(data: UserGroupCreate, session: SessionDep):
    return crud.create_user_group(session, data)

@router.get("/{id}", response_model=UserGroupRead)
def get_user_group(id: int, session: SessionDep):
    return get_object_or_404(session, UserGroup, id)

@router.get("", response_model=List[UserGroupRead])
def list_user_groups(
    session: SessionDep,
    user_id: int | None = None,
    group_id: int | None = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return crud.list_user_groups(session, user_id, group_id, limit, offset)

@router.patch("/{id}", response_model=UserGroupRead)
def update_user_group(id: int, data: UserGroupUpdate, session: SessionDep):
    obj = get_object_or_404(session, UserGroup, id)
    return crud.update_user_group(session, obj, data)

@router.delete("/{id}", status_code=204)
def delete_user_group(id: int, session: SessionDep):
    obj = get_object_or_404(session, UserGroup, id)
    crud.delete_user_group(session, obj)
    return None