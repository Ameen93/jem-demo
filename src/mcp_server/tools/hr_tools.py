"""HR MCP tools for employee data retrieval."""

import logging
import uuid
from datetime import date, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from src.db.connection import get_session
from src.db.models import Employee, LeaveBalance

logger = logging.getLogger(__name__)


def get_employee(employee_id: str, session: Optional[Session] = None) -> dict:
    """Retrieve employee profile by ID.

    Args:
        employee_id: Employee ID (e.g. "EMP001").
        session: Optional SQLAlchemy session. If not provided, creates one
                 via get_session(). Pass explicitly for testing.

    Returns:
        MCP response dict with success/data or success/error/code.
    """
    if session is not None:
        return _get_employee_impl(employee_id, session)

    try:
        with get_session() as s:
            return _get_employee_impl(employee_id, s)
    except Exception:
        logger.exception("Unexpected error in get_employee")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}


def _get_employee_impl(employee_id: str, session: Session) -> dict:
    """Internal implementation for get_employee."""
    try:
        employee = session.get(Employee, employee_id)
        if employee is None:
            return {
                "success": False,
                "error": "Employee not found",
                "code": "NOT_FOUND",
            }
        return {"success": True, "data": employee.to_dict()}
    except Exception:
        logger.exception("Unexpected error in get_employee")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}


def get_leave_balance(employee_id: str, session: Optional[Session] = None) -> dict:
    """Retrieve leave balances for an employee.

    Args:
        employee_id: Employee ID (e.g. "EMP005").
        session: Optional SQLAlchemy session for testing.

    Returns:
        MCP response dict with leave balances keyed by type.
    """
    if session is not None:
        return _get_leave_balance_impl(employee_id, session)

    try:
        with get_session() as s:
            return _get_leave_balance_impl(employee_id, s)
    except Exception:
        logger.exception("Unexpected error in get_leave_balance")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}


def _get_leave_balance_impl(employee_id: str, session: Session) -> dict:
    """Internal implementation for get_leave_balance."""
    try:
        employee = session.get(Employee, employee_id)
        if employee is None:
            return {
                "success": False,
                "error": "Employee not found",
                "code": "NOT_FOUND",
            }
        balances = (
            session.query(LeaveBalance)
            .filter_by(employee_id=employee_id)
            .all()
        )
        data = {b.leave_type: b.balance_days for b in balances}
        return {"success": True, "data": data}
    except Exception:
        logger.exception("Unexpected error in get_leave_balance")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}


def _count_business_days(start: date, end: date) -> int:
    """Count business days between start and end (inclusive)."""
    days = 0
    current = start
    while current <= end:
        if current.weekday() < 5:  # Mon-Fri
            days += 1
        current += timedelta(days=1)
    return days


def submit_leave_request(
    employee_id: str,
    start_date: str,
    end_date: str,
    leave_type: str,
    session: Optional[Session] = None,
) -> dict:
    """Submit a leave request for an employee.

    Args:
        employee_id: Employee ID.
        start_date: Start date in ISO format (YYYY-MM-DD).
        end_date: End date in ISO format (YYYY-MM-DD).
        leave_type: Type of leave (annual, sick, family).
        session: Optional SQLAlchemy session for testing.

    Returns:
        MCP response dict with request confirmation or error.
    """
    if session is not None:
        return _submit_leave_request_impl(
            employee_id, start_date, end_date, leave_type, session
        )

    try:
        with get_session() as s:
            return _submit_leave_request_impl(
                employee_id, start_date, end_date, leave_type, s
            )
    except Exception:
        logger.exception("Unexpected error in submit_leave_request")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}


def _submit_leave_request_impl(
    employee_id: str,
    start_date: str,
    end_date: str,
    leave_type: str,
    session: Session,
) -> dict:
    """Internal implementation for submit_leave_request."""
    try:
        employee = session.get(Employee, employee_id)
        if employee is None:
            return {
                "success": False,
                "error": "Employee not found",
                "code": "NOT_FOUND",
            }

        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)

        if end < start:
            return {
                "success": False,
                "error": "End date must be on or after start date",
                "code": "INVALID_DATES",
            }

        days = _count_business_days(start, end)
        if days <= 0:
            return {
                "success": False,
                "error": "Date range contains no business days",
                "code": "INVALID_DATES",
            }

        balance = (
            session.query(LeaveBalance)
            .filter_by(employee_id=employee_id, leave_type=leave_type)
            .first()
        )

        if balance is None or balance.balance_days < days:
            return {
                "success": False,
                "error": "Insufficient leave balance",
                "code": "INSUFFICIENT_BALANCE",
            }

        balance.balance_days -= days
        balance.used_ytd += days
        session.flush()

        request_id = f"LR-{uuid.uuid4().hex[:8].upper()}"
        return {
            "success": True,
            "data": {
                "request_id": request_id,
                "status": "approved",
                "days": days,
            },
        }
    except Exception:
        logger.exception("Unexpected error in submit_leave_request")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}
