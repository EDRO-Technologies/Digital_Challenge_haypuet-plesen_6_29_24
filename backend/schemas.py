import time
import datetime
from sqlmodel import SQLModel
from .entity import UserRole, EventsPeriodicity

# User
class UserBase(SQLModel):
    name: str
    telegram_id: int | None = None
    role: UserRole = UserRole.student
    need_notification: bool = False

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: str | None = None
    telegram_id: int | None = None
    role: UserRole | None = None
    need_notification: bool | None = None

# Group
class GroupBase(SQLModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupRead(GroupBase):
    id: int

class GroupUpdate(SQLModel):
    name: str | None = None

# UserGroup
class UserGroupBase(SQLModel):
    user_id: int
    group_id: int

class UserGroupCreate(UserGroupBase):
    pass

class UserGroupRead(UserGroupBase):
    id: int

class UserGroupUpdate(SQLModel):
    user_id: int | None = None
    group_id: int | None = None

# Location
class LocationBase(SQLModel):
    address: str
    room: str | None = None

class LocationCreate(LocationBase):
    pass

class LocationRead(LocationBase):
    id: int

class LocationUpdate(SQLModel):
    address: str | None = None
    room: str | None = None

# Event
class EventBase(SQLModel):
    name: str
    week_day: int = 1
    num: int | None = None
    time: int = int(time.time())
    date: datetime.datetime | None = None
    duration: int = 80
    periodicity: EventsPeriodicity = EventsPeriodicity.once

class EventCreate(EventBase):
    location: int | None = None
    created_by: int | None = None
    teacher: int | None = None

class EventRead(EventBase):
    id: int
    location_instance: LocationRead | None = None
    created_by_user: UserRead | None = None
    teacher_user: UserRead | None = None

class EventUpdate(SQLModel):
    name: str | None = None
    week_day: int | None = None
    num: int | None = None
    time: int | None = None
    date: datetime.datetime | None = None
    duration: int | None = None
    periodicity: EventsPeriodicity | None = None
    location: int | None = None
    created_by: int | None = None
    teacher: int | None = None


# EventGroup
class EventGroupBase(SQLModel):
    event_id: int
    group_id: int

class EventGroupCreate(EventGroupBase):
    pass

class EventGroupRead(EventGroupBase):
    id: int

class EventGroupUpdate(SQLModel):
    event_id: int | None = None
    group_id: int | None = None

# EventLog
class EventLogBase(SQLModel):
    old_event: int
    new_event: int

class EventLogCreate(EventLogBase):
    pass

class EventLogRead(EventLogBase):
    id: int

class EventLogUpdate(SQLModel):
    old_event: int | None = None
    new_event: int | None = None

class ScheduleFromExcel(SQLModel):
    ...