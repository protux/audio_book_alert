import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SQLAlchemySession

from audio_book_alert.database import utils

logger = logging.getLogger(__name__)

engine = utils.get_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
schema = utils.get_database_schema()
if schema:
    Base.metadata.schema = schema


def create_session() -> SQLAlchemySession:
    return SessionLocal()


def get_db() -> SessionLocal:
    db = create_session()
    try:
        yield db
    finally:
        db.close()
