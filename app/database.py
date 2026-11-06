import os
from types import SimpleNamespace

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fittrack.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# JWT configuration
settings = SimpleNamespace(
    SECRET_KEY=os.getenv("SECRET_KEY", "change-this-secret-key"),
    ALGORITHM="HS256",
    ACCESS_TOKEN_EXPIRE_MINUTES=30
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


