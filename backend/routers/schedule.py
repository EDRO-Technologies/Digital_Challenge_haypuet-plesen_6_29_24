from typing import List
from fastapi import APIRouter, HTTPException, Query, status, UploadFile
from ..deps import SessionDep
from ..schemas import UserCreate, UserRead, UserUpdate, EventRead
from ..entity import UserRole, User, Event
from ..crud import schedule as crud

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.post("/upload", response_model=list[EventRead], status_code=201)
def upload_file(file: UploadFile, session: SessionDep):
    return crud.create_schedule_from_excel_file(session, file.file)
