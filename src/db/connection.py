"""Database connection management for Jem HR Demo."""

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

logger = logging.getLogger(__name__)

# Default database path
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DEFAULT_DB_PATH = DATA_DIR / "jem_hr.db"

_engine: Engine | None = None
_session_factory: sessionmaker[Session] | None = None


def get_engine(db_path: Path | None = None) -> Engine:
    """Get or create the SQLAlchemy engine.

    Args:
        db_path: Optional path to database file. Defaults to data/jem_hr.db.

    Returns:
        SQLAlchemy Engine instance.
    """
    global _engine

    if _engine is not None:
        return _engine

    if db_path is None:
        db_path = DEFAULT_DB_PATH

    # Ensure data directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    db_url = f"sqlite:///{db_path}"
    logger.info("Connecting to database: %s", db_path)

    _engine = create_engine(db_url, echo=False)

    # Create all tables
    Base.metadata.create_all(_engine)
    logger.info("Database tables initialized")

    return _engine


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get a database session as a context manager.

    Yields:
        SQLAlchemy Session instance.

    Example:
        with get_session() as session:
            employee = session.get(Employee, "EMP001")
    """
    global _session_factory

    if _session_factory is None:
        engine = get_engine()
        _session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    session = _session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def reset_engine() -> None:
    """Reset the engine and session factory. Used for testing."""
    global _engine, _session_factory
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _session_factory = None
