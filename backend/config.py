import os
from dotenv import load_dotenv


class Config(object):
    def __init__(self):
        load_dotenv()
        self.DATABASE_PORT = os.getenv("DATABASE_PORT")
        self.DATABASE_NAME = os.getenv("DATABASE_NAME")
        self.DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
        self.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
        self.DATABASE_HOST = os.getenv("DATABASE_HOST")

        for var in vars(self):
            if self.__getattribute__(var) is None:
                raise ValueError(f"tg_bot: переменная '{var}' должна быть установлена в окружении")

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance