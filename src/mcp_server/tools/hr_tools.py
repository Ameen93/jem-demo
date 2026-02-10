"""HR MCP tools for employee data retrieval."""

import logging
from typing import Optional

from sqlalchemy.orm import Session

from src.db.connection import get_session
from src.db.models import Employee

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
