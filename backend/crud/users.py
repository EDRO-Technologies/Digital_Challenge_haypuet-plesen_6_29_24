from sqlmodel import Session, select
from ..entity import User
from ..schemas import UserCreate, UserUpdate

def create_user(session: Session, data: UserCreate) -> User:
    obj = User(**data.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def get_user_by_tg_id(session: Session, telegram_id: int) -> User | None:
    with session:
        statement = select(User).where(User.telegram_id == telegram_id)
        user = session.scalar(statement)
    return user

def list_users(session: Session, role=None, need_notification=None, q=None, limit=50, offset=0):
    stmt = select(User)
    if role is not None:
        stmt = stmt.where(User.role == role)
    if need_notification is not None:
        stmt = stmt.where(User.need_notification == need_notification)
    if q:
        stmt = stmt.where(User.name.ilike(f"%{q}%"))
    stmt = stmt.limit(limit).offset(offset)
    return session.exec(stmt).all()

def update_user(session: Session, obj: User, data: UserUpdate) -> User:
    payload = data.model_dump(exclude_unset=True)
    for k, v in payload.items():
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def delete_user(session: Session, obj: User):
    session.delete(obj)
    session.commit()