import time
import datetime

from sqlmodel import Field, SQLModel, create_engine, Relationship
from enum import IntEnum
from .config import Config

class UserRole(IntEnum):
    admin = 1
    teacher = 2
    student = 3

class EventsPeriodicity(IntEnum):
    once = 0
    all_weeks = 1
    even = 2
    odd = 3

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    telegram_id: int | None = Field(nullable=True, default=None)
    role: UserRole = Field(nullable=False, default=UserRole.student)
    need_notification: bool = Field(nullable=False, default=False)

class Group(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)

class UserGroup(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(nullable=False, default=None, foreign_key="user.id")
    group_id: int = Field(nullable=False, default=None, foreign_key="group.id")

class Location(SQLModel, table=True):
    id: int = Field(primary_key=True)
    address: str = Field(nullable=False)
    room: str | None = Field(nullable=True, default=None)

class Event(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    week_day: int = Field(nullable=False, default=1)
    num: int = Field(nullable=False, default=0)
    time: int = Field(nullable=False, default=int(time.time()))
    date: datetime.datetime | None = Field(nullable=True, default=None)
    duration: int = Field(nullable=False, default=80)
    periodicity: EventsPeriodicity = Field(nullable=False, default=EventsPeriodicity.once)
    location: int = Field(nullable=True, foreign_key="location.id")
    created_by: int = Field(nullable=False, foreign_key="user.id")
    teacher: int = Field(nullable=True, foreign_key="user.id")
    created_by_user: User = Relationship(sa_relationship_kwargs={"foreign_keys": "Event.created_by"})
    teacher_user: User = Relationship(sa_relationship_kwargs={"foreign_keys": "Event.teacher"})
    location_instance: Location = Relationship(sa_relationship_kwargs={"foreign_keys": "Event.location"})

class EventGroup(SQLModel, table=True):
    id: int = Field(primary_key=True)
    event_id: int = Field(nullable=False, foreign_key="event.id")
    group_id: int = Field(nullable=False, foreign_key="group.id")

class EventLog(SQLModel, table=True):
    id: int = Field(primary_key=True)
    old_event: int = Field(nullable=False, foreign_key="event.id")
    new_event: int = Field(nullable=False, foreign_key="event.id")

def drop_db_and_tables(eng):
    SQLModel.metadata.drop_all(eng)

def create_db_and_tables(eng):
    SQLModel.metadata.create_all(eng)

if __name__ == "__main__":
    config = Config()
    postgre_url = f"postgresql://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}"
    engine = create_engine(postgre_url)
    # drop_db_and_tables(engine)
    create_db_and_tables(engine)
