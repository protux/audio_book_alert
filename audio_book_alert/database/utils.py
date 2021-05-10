from sqlalchemy import create_engine

from audio_book_alert import config


def get_connection_string() -> str:
    return config.get_settings().database_url


def get_database_schema() -> str:
    return config.get_settings().database_schema


def get_db_engine():
    connection_string = get_connection_string()
    if connection_string.startswith("sqlite"):
        return create_engine(
            connection_string, connect_args={"check_same_thread": False}
        )
    else:
        return create_engine(connection_string)
