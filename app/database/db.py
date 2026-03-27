from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from typing import Generator
from app.config.app_config import getAppConfig

Base = declarative_base()

config = getAppConfig()
engine = create_engine(config.database_url)

SessionEnv = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionEnv()
    try:
        yield db
    finally:
        db.close()
