from os import getenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = getenv("SQLALCHEMY_DATABASE_URI") or 'sqlite:///database.db'


settings = Settings()
