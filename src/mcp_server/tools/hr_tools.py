"""HR MCP tools for employee data retrieval."""

import logging
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
