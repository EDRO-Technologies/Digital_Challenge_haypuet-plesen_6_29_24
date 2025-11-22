from sqlmodel import Session, select
from fastapi import HTTPException
from ..entity import UserGroup, User, Group
from ..schemas import UserGroupCreate, UserGroupUpdate

def create_user_group(session: Session, data: UserGroupCreate) -> UserGroup:
    if session.get(User, data.user_id) is None:
        raise HTTPException(404, "User not found")
    if session.get(Group, data.group_id) is None:
        raise HTTPException(404, "Group not found")
    obj = UserGroup(**data.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def get_user_group(session: Session, obj_id: int) -> UserGroup | None:
    return session.get(UserGroup, obj_id)

def list_user_groups(session: Session, user_id=None, group_id=None, limit=50, offset=0):
    stmt = select(UserGroup)
    if user_id is not None:
        stmt = stmt.where(UserGroup.user_id == user_id)
    if group_id is not None:
        stmt = stmt.where(UserGroup.group_id == group_id)
    stmt = stmt.limit(limit).offset(offset)
    return session.exec(stmt).all()

def update_user_group(session: Session, obj: UserGroup, data: UserGroupUpdate) -> UserGroup:
    payload = data.model_dump(exclude_unset=True)
    if "user_id" in payload and session.get(User, payload["user_id"]) is None:
        raise HTTPException(404, "User not found")
    if "group_id" in payload and session.get(Group, payload["group_id"]) is None:
        raise HTTPException(404, "Group not found")
    for k, v in payload.items():
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def delete_user_group(session: Session, obj: UserGroup):
    session.delete(obj)
    session.commit()