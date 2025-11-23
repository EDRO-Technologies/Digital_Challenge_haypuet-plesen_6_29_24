from sqlmodel import SQLModel, create_engine
from .config import Config

config = Config()
POSTGRE_URL = (
    f"postgresql://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}"
    f"@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}"
)

engine = create_engine(POSTGRE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)