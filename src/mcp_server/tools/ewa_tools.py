"""EWA (Earned Wage Access) MCP tools."""

import logging
import uuid
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
                Timesheet.pay_period_start <= today,
                Timesheet.pay_period_end >= today,
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


def request_ewa_advance(
    employee_id: str, amount: float, session: Optional[Session] = None
) -> dict:
    """Request an EWA advance for an employee.

    Args:
        employee_id: Employee ID.
        amount: Amount to advance in Rands.
        session: Optional SQLAlchemy session for testing.

    Returns:
        MCP response dict with transaction details or error.
    """
    if session is not None:
        return _request_ewa_advance_impl(employee_id, amount, session)

    try:
        with get_session() as s:
            return _request_ewa_advance_impl(employee_id, amount, s)
    except Exception:
        logger.exception("Unexpected error in request_ewa_advance")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}


def _request_ewa_advance_impl(
    employee_id: str, amount: float, session: Session
) -> dict:
    """Internal implementation for request_ewa_advance."""
    try:
        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be positive",
                "code": "INVALID_AMOUNT",
            }

        # Check eligibility first
        eligibility = _check_ewa_eligibility_impl(employee_id, session)
        if not eligibility["success"]:
            return eligibility

        data = eligibility["data"]
        if not data["eligible"]:
            return {
                "success": False,
                "error": data.get("reason", "Not eligible for EWA"),
                "code": "NOT_ELIGIBLE",
            }

        if amount > data["available"]:
            return {
                "success": False,
                "error": "Amount exceeds available balance",
                "code": "EXCEEDS_AVAILABLE",
            }

        # Create transaction
        now = datetime.now()
        txn_id = f"EWA-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        txn = EWATransaction(
            id=txn_id,
            employee_id=employee_id,
            amount=amount,
            fee=EWA_FEE,
            status=EWAStatus.DISBURSED.value,
            requested_at=now,
            disbursed_at=now,
        )
        session.add(txn)
        session.flush()

        return {
            "success": True,
            "data": {
                "transaction_id": txn_id,
                "amount": amount,
                "fee": EWA_FEE,
                "net": amount - EWA_FEE,
            },
        }
    except Exception:
        logger.exception("Unexpected error in request_ewa_advance")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}
