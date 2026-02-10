"""Standalone database seeding script."""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db.connection import get_engine, get_session
from src.db.seed import seed_database

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main() -> None:
    """Initialize database and seed with demo data."""
    get_engine()
    gen = get_session()
    session = next(gen)
    try:
        seed_database(session)
        gen.close()
    except Exception:
        try:
            gen.throw(Exception)
        except StopIteration:
            pass
        raise


if __name__ == "__main__":
    main()
