"""Tests for MCP tools - get_employee, get_leave_balance."""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

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


class TestGetEmployee:
    """Tests for get_employee MCP tool."""

    def test_returns_success_for_valid_employee(self):
        """AC #1: get_employee(employee_id="EMP001") returns success with data."""
        from src.mcp_server.tools.hr_tools import get_employee

        with seeded_session() as session:
            result = get_employee("EMP001", session)
            assert result["success"] is True
            assert "data" in result

    def test_returns_correct_employee_fields(self):
        """AC #1: Response data includes name, department, role, hire_date, preferred_language, employment_status."""
        from src.mcp_server.tools.hr_tools import get_employee

        with seeded_session() as session:
            result = get_employee("EMP001", session)
            data = result["data"]
            assert data["name"] == "Sipho Dlamini"
            assert data["department"] == "Retail - Checkers Sandton"
            assert data["role"] == "Sales Assistant"
            assert data["hire_date"] == "2024-03-15"
            assert data["preferred_language"] == "zu"
            assert data["employment_status"] == "active"

    def test_returns_error_for_invalid_employee(self):
        """AC #2: get_employee(employee_id="INVALID") returns error response."""
        from src.mcp_server.tools.hr_tools import get_employee

        with seeded_session() as session:
            result = get_employee("INVALID", session)
            assert result["success"] is False
            assert result["error"] == "Employee not found"
            assert result["code"] == "NOT_FOUND"

    def test_response_format_success(self):
        """Response format matches {"success": True, "data": {...}}."""
        from src.mcp_server.tools.hr_tools import get_employee

        with seeded_session() as session:
            result = get_employee("EMP001", session)
            assert set(result.keys()) == {"success", "data"}
            assert isinstance(result["data"], dict)

    def test_response_format_error(self):
        """Response format matches {"success": False, "error": "...", "code": "..."}."""
        from src.mcp_server.tools.hr_tools import get_employee

        with seeded_session() as session:
            result = get_employee("INVALID", session)
            assert set(result.keys()) == {"success", "error", "code"}

    def test_all_employees_retrievable(self):
        """All 12 employees can be retrieved."""
        from src.mcp_server.tools.hr_tools import get_employee

        with seeded_session() as session:
            for i in range(1, 13):
                emp_id = f"EMP{str(i).zfill(3)}"
                result = get_employee(emp_id, session)
                assert result["success"] is True, f"Failed for {emp_id}"


class TestGetLeaveBalance:
    """Tests for get_leave_balance MCP tool."""

    def test_returns_correct_balances(self):
        """AC #1: Nomvula (EMP005) has annual=9, sick=7, family=2."""
        from src.mcp_server.tools.hr_tools import get_leave_balance

        with seeded_session() as session:
            result = get_leave_balance("EMP005", session)
            assert result["success"] is True
            data = result["data"]
            assert data["annual"] == 9
            assert data["sick"] == 7
            assert data["family"] == 2

    def test_returns_error_for_invalid_employee(self):
        """AC #2: Invalid employee returns error."""
        from src.mcp_server.tools.hr_tools import get_leave_balance

        with seeded_session() as session:
            result = get_leave_balance("INVALID", session)
            assert result["success"] is False
            assert result["code"] == "NOT_FOUND"

    def test_response_format(self):
        """Response format matches MCP standard."""
        from src.mcp_server.tools.hr_tools import get_leave_balance

        with seeded_session() as session:
            result = get_leave_balance("EMP001", session)
            assert set(result.keys()) == {"success", "data"}
            assert isinstance(result["data"], dict)

    def test_all_employees_have_balances(self):
        """All 12 employees have leave balances."""
        from src.mcp_server.tools.hr_tools import get_leave_balance

        with seeded_session() as session:
            for i in range(1, 13):
                emp_id = f"EMP{str(i).zfill(3)}"
                result = get_leave_balance(emp_id, session)
                assert result["success"] is True, f"Failed for {emp_id}"
                data = result["data"]
                assert "annual" in data, f"{emp_id} missing annual"
                assert "sick" in data, f"{emp_id} missing sick"
                assert "family" in data, f"{emp_id} missing family"
