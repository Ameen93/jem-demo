"""EWA (Earned Wage Access) MCP tools."""

import logging
from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.db.connection import get_session
from src.db.models import (
    Employee,
    EmploymentStatus,
    EWAStatus,
    EWATransaction,
    Timesheet,
    TimesheetStatus,
)

logger = logging.getLogger(__name__)

MAX_EWA_AMOUNT = 5000
EWA_PERCENTAGE = 0.50
EWA_FEE = 10.0
PROBATION_MONTHS = 3


def check_ewa_eligibility(
    employee_id: str, session: Optional[Session] = None
) -> dict:
    """Check if an employee is eligible for an EWA advance.

    Args:
        employee_id: Employee ID.
        session: Optional SQLAlchemy session for testing.

    Returns:
        MCP response dict with eligibility details.
    """
    if session is not None:
        return _check_ewa_eligibility_impl(employee_id, session)

    try:
        with get_session() as s:
            return _check_ewa_eligibility_impl(employee_id, s)
    except Exception:
        logger.exception("Unexpected error in check_ewa_eligibility")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}


def _check_ewa_eligibility_impl(employee_id: str, session: Session) -> dict:
    """Internal implementation for check_ewa_eligibility."""
    try:
        employee = session.get(Employee, employee_id)
        if employee is None:
            return {
                "success": False,
                "error": "Employee not found",
                "code": "NOT_FOUND",
            }

        today = date(2026, 2, 10)  # Demo fixed date

        # Check probation (3 months from hire)
        months_employed = (today.year - employee.hire_date.year) * 12 + (
            today.month - employee.hire_date.month
        )
        if (
            employee.employment_status == EmploymentStatus.PROBATION.value
            or months_employed < PROBATION_MONTHS
        ):
            weeks_remaining = max(0, (PROBATION_MONTHS * 4) - (months_employed * 4))
            return {
                "success": True,
                "data": {
                    "eligible": False,
                    "reason": "Probation not complete",
                    "weeks_remaining": weeks_remaining,
                },
            }

        # Calculate earned from approved timesheets in current period
        timesheets = (
            session.query(Timesheet)
            .filter(
                Timesheet.employee_id == employee_id,
                Timesheet.status == TimesheetStatus.APPROVED.value,
            )
            .all()
        )
        total_hours = sum(ts.hours_worked for ts in timesheets)
        earned = total_hours * employee.hourly_rate

        # Calculate outstanding EWA balance
        outstanding_txns = (
            session.query(EWATransaction)
            .filter(
                EWATransaction.employee_id == employee_id,
                EWATransaction.status == EWAStatus.DISBURSED.value,
            )
            .all()
        )
        outstanding = sum(t.amount for t in outstanding_txns)

        # Calculate available: 50% of earned, capped at R5,000, minus outstanding
        available = min(earned * EWA_PERCENTAGE, MAX_EWA_AMOUNT) - outstanding
        available = max(0, available)

        return {
            "success": True,
            "data": {
                "eligible": True,
                "earned": earned,
                "available": available,
                "outstanding": outstanding,
            },
        }
    except Exception:
        logger.exception("Unexpected error in check_ewa_eligibility")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}
