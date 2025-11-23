import datetime
import time
from typing import BinaryIO

from sqlmodel import Session, select

from ..parser import ScheduleParser
from fastapi import HTTPException
from ..entity import Event, Location, EventsPeriodicity, UserRole
from ..schemas import EventCreate, EventUpdate, UserCreate, GroupCreate, LocationCreate, EventGroupCreate
from ..crud import users, events, groups, locations, event_groups

from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo

def create_schedule_from_excel_file(session: Session, file: BinaryIO) -> list[Event | None]:
    parser = ScheduleParser(file=file)
    parser.parse_file()
    schedule = parser.to_flat_json()
    if not schedule:
        return []

    events_list = []

    for event in schedule:
        teacher_name = event.get("teacher_name")
        if teacher_name is not None and teacher_name != "" and "." in teacher_name:
            teacher = users.list_users(q=teacher_name[:teacher_name.index(".")], session=session)
            if len(teacher) == 0:
                teacher = users.create_user(session=session, data=UserCreate.model_validate({
                    "name": teacher_name,
                    "telegram_id": None,
                    "role": UserRole.teacher,
                    "need_notification": False
                }))
            else:
                teacher = teacher[0]
        else:
            teacher = None

        group_name = event.get("group_name")
        if group_name is not None and group_name != "":
            group = groups.list_groups(session=session, q=group_name)
            if len(group) == 0:
                group = groups.create_group(session=session, data=GroupCreate.model_validate({
                    "name": group_name,
                }))
            else:
                group = group[0]
        else:
            group = None

        room_name = event.get("room")
        if room_name is not None and room_name != "":
            location = locations.list_locations(session=session, room_q=room_name)
            if len(location) == 0:
                location = locations.create_location(session=session, data=LocationCreate.model_validate({
                    "address": f"Корпус {room_name[0]}",
                    "room": room_name,
                }))
            else:
                location = location[0]
        else:
            location = None

        # events_from_db = events.list_events(session=session, week_day=event.get("week_day"), )

        tz = ZoneInfo("Asia/Yekaterinburg")
        base = datetime.combine(date.today(), time(8, 30), tzinfo=tz)

        num = event.get("num")
        if num is not None:
            for t in range(int(event.get("num"))-1):
                base = base + timedelta(hours=1, minutes=20)

            ts_base = int(base.timestamp())
        else:
            ts_base = int(datetime.now().timestamp())

        event = events.create_event(session=session, data=EventCreate.model_validate({
            "name": event.get("event_name"),
            "week_day": event.get("week_day"),
            "num": event.get("num"),
            "periodicity": event.get("periodicity"),
            "time": ts_base,
            "duration": 80,
            "created_by": teacher.id if teacher else None,
            "location": location.id if location else None,
            "teacher": teacher.id if teacher else None,
        }))

        event_groups.create_event_group(session=session, data=EventGroupCreate.model_validate({
            "event_id": event.id,
            "group_id": group.id
        }))

        events_list.append(event)

    return events_list