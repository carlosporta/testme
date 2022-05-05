from contextlib import contextmanager
from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SqlalchemySession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

from ..settings import settings


Base: DeclarativeMeta = declarative_base()
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, future=True)
Session = sessionmaker(bind=engine)


@contextmanager
def get_session() -> Iterator[SqlalchemySession]:
    with Session() as session:
        yield session


def create_db(drop_tables: bool = False) -> None:
    Base.metadata.create_all(engine)
    if drop_tables:
        Base.metadata.drop_all(engine)
