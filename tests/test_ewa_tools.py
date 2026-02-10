"""Tests for EWA MCP tools."""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base
from src.db.seed import seed_database


@contextmanager
def seeded_session():
    """Create a temporary in-memory database session with seed data."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    session = factory()
    try:
        seed_database(session)
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()


class TestCheckEwaEligibility:
    """Tests for check_ewa_eligibility MCP tool."""

    def test_eligible_employee_sipho(self):
        """AC #1: Sipho is eligible with correct amounts."""
        from src.mcp_server.tools.ewa_tools import check_ewa_eligibility

        with seeded_session() as session:
            result = check_ewa_eligibility("EMP001", session)
            assert result["success"] is True
            data = result["data"]
            assert data["eligible"] is True
            assert data["earned"] == 4268.0  # 88 * 48.50
            assert data["available"] == 2134.0  # 50% of earned
            assert data["outstanding"] == 0

    def test_probation_rejection_lerato(self):
        """AC #2: Lerato in probation gets rejected."""
        from src.mcp_server.tools.ewa_tools import check_ewa_eligibility

        with seeded_session() as session:
            result = check_ewa_eligibility("EMP004", session)
            assert result["success"] is True
            data = result["data"]
            assert data["eligible"] is False
            assert "probation" in data["reason"].lower()

    def test_outstanding_reduces_available_thandiwe(self):
        """AC #3: Thandiwe's R800 outstanding reduces available amount."""
        from src.mcp_server.tools.ewa_tools import check_ewa_eligibility

        with seeded_session() as session:
            result = check_ewa_eligibility("EMP002", session)
            data = result["data"]
            assert data["eligible"] is True
            assert data["outstanding"] == 800
            # 80 * 42.00 = 3360, 50% = 1680, available = 1680 - 800 = 880
            assert data["available"] == 880.0

    def test_r5000_cap(self):
        """Available capped at R5,000 for high earners."""
        from src.mcp_server.tools.ewa_tools import check_ewa_eligibility

        with seeded_session() as session:
            # Thabo (EMP006): 96hrs x R85.00 = R8,160. 50% = R4,080.
            # Under R5,000 cap so available = R4,080
            result = check_ewa_eligibility("EMP006", session)
            data = result["data"]
            assert data["earned"] == 8160.0
            assert data["available"] <= 5000

    def test_invalid_employee(self):
        """Invalid employee returns NOT_FOUND."""
        from src.mcp_server.tools.ewa_tools import check_ewa_eligibility

        with seeded_session() as session:
            result = check_ewa_eligibility("INVALID", session)
            assert result["success"] is False
            assert result["code"] == "NOT_FOUND"
