from fastapi import HTTPException, status
from sqlmodel import Session

def get_object_or_404(session: Session, model, obj_id: int):
    obj = session.get(model, obj_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} {obj_id} not found",
        )
    return obj