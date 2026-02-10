"""HR MCP tools for employee data retrieval."""

import logging

from sqlalchemy.orm import Session

from src.db.models import Employee

logger = logging.getLogger(__name__)


def get_employee(employee_id: str, session: Session) -> dict:
    """Retrieve employee profile by ID.

    Args:
        employee_id: Employee ID (e.g. "EMP001").
        session: SQLAlchemy session.

    Returns:
        MCP response dict with success/data or success/error/code.
    """
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
