import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DEFAULT_DATABASE_URL = "sqlite:///./weather.db"
configured_database_url = os.getenv("DATABASE_URL")

if configured_database_url and configured_database_url.startswith(("postgresql://", "postgresql+psycopg2://", "postgres://")):
    try:
        import psycopg2  # noqa: F401
    except ModuleNotFoundError:
        configured_database_url = None

DATABASE_URL = configured_database_url or DEFAULT_DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
