from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
# from schemas.leader_id_schemas import Event
from .config import Config
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from .db import create_db_and_tables
from .routers import users, groups, user_groups, locations, events, event_groups, event_logs

# from apiclient import apiclient

config = Config()

app = FastAPI(title="Schedule API", version="1.0.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# leader_id_client = apiclient.ApiClient(address=config.LEADER_ID_API, client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(user_groups.router)
app.include_router(locations.router)
app.include_router(events.router)
app.include_router(event_groups.router)
app.include_router(event_logs.router)