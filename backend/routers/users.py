from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from ..deps import SessionDep
from ..schemas import UserCreate, UserRead, UserUpdate
from ..entity import UserRole, User
from ..crud.base import get_object_or_404
from ..crud import users as crud

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserRead, status_code=201)
def create_user(data: UserCreate, session: SessionDep):
    return crud.create_user(session, data)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: SessionDep):
    obj = crud.get_user(session, user_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return obj

@router.get("/telegram_id/{telegram_id}", response_model=UserRead)
def get_user(telegram_id: int, session: SessionDep):
    obj = crud.get_user_by_tg_id(session, telegram_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return obj

@router.get("", response_model=List[UserRead])
def list_users(
    session: SessionDep,
    role: UserRole | None = None,
    need_notification: bool | None = None,
    q: str | None = Query(None, description="Поиск по имени"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return crud.list_users(session, role, need_notification, q, limit, offset)

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, session: SessionDep):
    obj = get_object_or_404(session, User, user_id)  # avoid circular
    return crud.update_user(session, obj, data)

@router.patch("/telegram_id/{telegram_id}", response_model=UserRead)
def update_user(telegram_id: int, data: UserUpdate, session: SessionDep):
    obj = crud.get_user_by_tg_id(session, telegram_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.update_user(session, obj, data)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, session: SessionDep):
    obj = get_object_or_404(session, User, user_id)
    crud.delete_user(session, obj)
    return None