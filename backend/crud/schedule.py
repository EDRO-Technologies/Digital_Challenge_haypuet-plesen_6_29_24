import datetime
from sqlmodel import Session, select
from fastapi import HTTPException
from ..entity import Event, Location, EventsPeriodicity
from ..schemas import EventCreate, EventUpdate

def create_schedule_from_excel_json(session: Session, events: EventCreate):
    ...