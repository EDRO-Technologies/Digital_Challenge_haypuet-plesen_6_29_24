from sqlmodel import Session, select
from ..entity import Location
from ..schemas import LocationCreate, LocationUpdate

def create_location(session: Session, data: LocationCreate) -> Location:
    obj = Location(**data.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def get_location(session: Session, obj_id: int) -> Location | None:
    return session.get(Location, obj_id)

def list_locations(session: Session, address_q=None, limit=50, offset=0):
    stmt = select(Location)
    if address_q:
        stmt = stmt.where(Location.address.ilike(f"%{address_q}%"))
    stmt = stmt.limit(limit).offset(offset)
    return session.exec(stmt).all()

def update_location(session: Session, obj: Location, data: LocationUpdate) -> Location:
    payload = data.model_dump(exclude_unset=True)
    for k, v in payload.items():
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

def delete_location(session: Session, obj: Location):
    session.delete(obj)
    session.commit()