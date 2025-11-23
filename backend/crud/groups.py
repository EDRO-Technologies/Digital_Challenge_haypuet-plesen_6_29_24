from sqlmodel import Session, select
from ..entity import Group
from ..schemas import GroupCreate, GroupUpdate

def create_group(session: Session, data: GroupCreate) -> Group:
    obj = Group(**data.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def get_group(session: Session, group_id: int) -> Group | None:
    return session.get(Group, group_id)

def list_groups(session: Session, q=None, limit=50, offset=0):
    stmt = select(Group)
    if q:
        stmt = stmt.where(Group.name.ilike(f"%{q}%"))
    stmt = stmt.limit(limit).offset(offset)
    return session.exec(stmt).all()

def update_group(session: Session, obj: Group, data: GroupUpdate) -> Group:
    payload = data.model_dump(exclude_unset=True)
    for k, v in payload.items():
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def delete_group(session: Session, obj: Group):
    session.delete(obj)
    session.commit()