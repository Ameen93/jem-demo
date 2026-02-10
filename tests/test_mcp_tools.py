"""Tests for MCP tools - get_employee, get_leave_balance, submit_leave_request."""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.db.models import Base, LeaveBalance, LeaveType
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


class TestSubmitLeaveRequest:
    """Tests for submit_leave_request MCP tool."""

    def test_successful_leave_submission(self):
        """AC #1: Sufficient balance results in approved request and reduced balance."""
        from src.mcp_server.tools.hr_tools import submit_leave_request

        with seeded_session() as session:
            # Sipho (EMP001) has 12 annual leave days
            result = submit_leave_request(
                "EMP001", "2026-03-02", "2026-03-04", "annual", session
            )
            assert result["success"] is True
            data = result["data"]
            assert data["status"] == "approved"
            assert data["days"] == 3
            assert "request_id" in data

    def test_balance_reduced_after_submission(self):
        """AC #1: Balance is actually reduced in the database."""
        from src.mcp_server.tools.hr_tools import submit_leave_request

        with seeded_session() as session:
            # Sipho has 12 annual days, request 3
            submit_leave_request(
                "EMP001", "2026-03-02", "2026-03-04", "annual", session
            )
            balance = (
                session.query(LeaveBalance)
                .filter_by(employee_id="EMP001", leave_type=LeaveType.ANNUAL.value)
                .first()
            )
            assert balance.balance_days == 9  # 12 - 3

    def test_insufficient_balance_returns_error(self):
        """AC #2: Insufficient balance returns error."""
        from src.mcp_server.tools.hr_tools import submit_leave_request

        with seeded_session() as session:
            # Johan (EMP003) has only 2 annual leave days
            result = submit_leave_request(
                "EMP003", "2026-03-02", "2026-03-06", "annual", session
            )
            assert result["success"] is False
            assert result["error"] == "Insufficient leave balance"
            assert result["code"] == "INSUFFICIENT_BALANCE"

    def test_invalid_employee_returns_error(self):
        """Invalid employee returns NOT_FOUND error."""
        from src.mcp_server.tools.hr_tools import submit_leave_request

        with seeded_session() as session:
            result = submit_leave_request(
                "INVALID", "2026-03-02", "2026-03-04", "annual", session
            )
            assert result["success"] is False
            assert result["code"] == "NOT_FOUND"


class TestGetPayslip:
    """Tests for get_payslip MCP tool."""

    def test_earnings_calculation(self):
        """AC #1: Sipho (EMP001) 88hrs x R48.50 = R4268.00 gross."""
        from src.mcp_server.tools.hr_tools import get_payslip

        with seeded_session() as session:
            result = get_payslip("EMP001", "2026-02", session)
            assert result["success"] is True
            data = result["data"]
            assert data["gross_earnings"] == 4268.0
            assert data["hours_worked"] == 88

    def test_ewa_deductions_included(self):
        """AC #2: Thandiwe (EMP002) has R800 EWA deduction."""
        from src.mcp_server.tools.hr_tools import get_payslip

        with seeded_session() as session:
            result = get_payslip("EMP002", "2026-02", session)
            data = result["data"]
            assert data["ewa_deductions"] == 800

    def test_net_pay_correct(self):
        """AC #3: Thandiwe net = 3360 - 800 = 2560."""
        from src.mcp_server.tools.hr_tools import get_payslip

        with seeded_session() as session:
            result = get_payslip("EMP002", "2026-02", session)
            data = result["data"]
            assert data["gross_earnings"] == 3360.0
            assert data["net_pay"] == 2560.0

    def test_no_ewa_deductions(self):
        """Employee with no EWA has 0 deductions."""
        from src.mcp_server.tools.hr_tools import get_payslip

        with seeded_session() as session:
            result = get_payslip("EMP001", "2026-02", session)
            data = result["data"]
            assert data["ewa_deductions"] == 0
            assert data["net_pay"] == data["gross_earnings"]

    def test_invalid_employee_returns_error(self):
        """Invalid employee returns NOT_FOUND."""
        from src.mcp_server.tools.hr_tools import get_payslip

        with seeded_session() as session:
            result = get_payslip("INVALID", "2026-02", session)
            assert result["success"] is False
            assert result["code"] == "NOT_FOUND"
