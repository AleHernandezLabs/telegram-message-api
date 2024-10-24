from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from src.config import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create database engine using the correct attribute from settings
engine = create_engine(
    settings.database_url,  # Make sure the lowercase `database_url` is used
    pool_pre_ping=True,     # Enable connection health checks
    pool_size=5,            # Set connection pool size
    max_overflow=10         # Maximum number of connections that can be created beyond pool_size
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for SQLAlchemy models
Base = declarative_base()

def init_db() -> None:
    """Initialize database by creating all tables."""
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session.
    Ensures the session is properly closed after use.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def check_database_connection() -> bool:
    """
    Check if the database connection is healthy.

    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")  # Simple query to check the connection
        return True
    except Exception as e:
        # Log the error for debugging and tracking purposes
        logger.error(f"Database connection error: {e}")
        return False
    finally:
        db.close()
