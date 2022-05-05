from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///database.db'


settings = Settings()
