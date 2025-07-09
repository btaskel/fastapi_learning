from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import SQLALCHEMY_DATABASE_URL

_engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

BaseModel = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()