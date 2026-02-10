"""Database seeding for Jem HR Demo."""

import logging
from datetime import date, datetime

from sqlalchemy.orm import Session

from .models import (
    Employee,
    EmploymentStatus,
    EWAStatus,
    EWATransaction,
    LeaveBalance,
    LeaveType,
    Timesheet,
    TimesheetStatus,
)

logger = logging.getLogger(__name__)

# Current pay period
PAY_PERIOD_START = date(2026, 2, 1)
PAY_PERIOD_END = date(2026, 2, 15)


EMPLOYEES = [
    {
        "id": "EMP001",
        "name": "Sipho Dlamini",
        "department": "Retail - Checkers Sandton",
        "role": "Sales Assistant",
        "hire_date": date(2024, 3, 15),
        "hourly_rate": 48.50,
        "preferred_language": "zu",
        "bank_account_last4": "4521",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
    {
        "id": "EMP002",
        "name": "Thandiwe Nkosi",
        "department": "Security - Fidelity Rosebank",
        "role": "Security Officer",
        "hire_date": date(2023, 8, 1),
        "hourly_rate": 42.00,
        "preferred_language": "xh",
        "bank_account_last4": "7832",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
    {
        "id": "EMP003",
        "name": "Johan van der Berg",
        "department": "Warehouse - DHL Johannesburg",
        "role": "Warehouse Supervisor",
        "hire_date": date(2022, 1, 10),
        "hourly_rate": 55.00,
        "preferred_language": "af",
        "bank_account_last4": "1156",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
    {
        "id": "EMP004",
        "name": "Lerato Molefe",
        "department": "Call Centre - Vodacom",
        "role": "Customer Service Agent",
        "hire_date": date(2025, 12, 28),
        "hourly_rate": 38.00,
        "preferred_language": "nso",
        "bank_account_last4": "9043",
        "employment_status": EmploymentStatus.PROBATION.value,
    },
    {
        "id": "EMP005",
        "name": "Nomvula Sithole",
        "department": "Hospitality - Hilton Sandton",
        "role": "Front Desk Agent",
        "hire_date": date(2024, 6, 1),
        "hourly_rate": 45.00,
        "preferred_language": "en",
        "bank_account_last4": "3367",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
    {
        "id": "EMP006",
        "name": "Thabo Mokoena",
        "department": "Mining - Anglo American",
        "role": "Shift Foreman",
        "hire_date": date(2020, 5, 15),
        "hourly_rate": 85.00,
        "preferred_language": "st",
        "bank_account_last4": "6210",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
    {
        "id": "EMP007",
        "name": "Precious Ndlovu",
        "department": "Fast Food - McDonald's",
        "role": "Crew Member",
        "hire_date": date(2025, 9, 1),
        "hourly_rate": 35.00,
        "preferred_language": "zu",
        "bank_account_last4": "8874",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
    {
        "id": "EMP008",
        "name": "Pieter Botha",
        "department": "Logistics - Shoprite DC",
        "role": "Dispatch Coordinator",
        "hire_date": date(2023, 2, 20),
        "hourly_rate": 52.00,
        "preferred_language": "af",
        "bank_account_last4": "2590",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
    {
        "id": "EMP009",
        "name": "Lindiwe Khumalo",
        "department": "Healthcare - Netcare",
        "role": "Nursing Assistant",
        "hire_date": date(2023, 11, 5),
        "hourly_rate": 65.00,
        "preferred_language": "xh",
        "bank_account_last4": "5148",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
    {
        "id": "EMP010",
        "name": "David Okonkwo",
        "department": "Manufacturing - Toyota",
        "role": "Assembly Technician",
        "hire_date": date(2022, 7, 12),
        "hourly_rate": 58.00,
        "preferred_language": "en",
        "bank_account_last4": "4396",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
    {
        "id": "EMP011",
        "name": "Ayanda Zulu",
        "department": "Cleaning - Bidvest",
        "role": "Cleaning Operative",
        "hire_date": date(2024, 10, 1),
        "hourly_rate": 32.00,
        "preferred_language": "zu",
        "bank_account_last4": "7021",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
    {
        "id": "EMP012",
        "name": "Maria van Wyk",
        "department": "Restaurant - Spur",
        "role": "Waitress",
        "hire_date": date(2025, 4, 15),
        "hourly_rate": 40.00,
        "preferred_language": "af",
        "bank_account_last4": "1835",
        "employment_status": EmploymentStatus.ACTIVE.value,
    },
]

# Leave balances: {employee_id: {leave_type: (balance, accrued_ytd, used_ytd)}}
LEAVE_BALANCES = {
    "EMP001": {"annual": (12, 15, 3), "sick": (8, 10, 2), "family": (3, 3, 0)},
    "EMP002": {"annual": (10, 15, 5), "sick": (6, 10, 4), "family": (2, 3, 1)},
    "EMP003": {"annual": (2, 15, 13), "sick": (4, 10, 6), "family": (1, 3, 2)},
    "EMP004": {"annual": (1, 1, 0), "sick": (1, 1, 0), "family": (0, 0, 0)},
    "EMP005": {"annual": (9, 12, 3), "sick": (7, 10, 3), "family": (2, 3, 1)},
    "EMP006": {"annual": (15, 20, 5), "sick": (9, 10, 1), "family": (3, 3, 0)},
    "EMP007": {"annual": (4, 5, 1), "sick": (9, 10, 1), "family": (3, 3, 0)},
    "EMP008": {"annual": (11, 15, 4), "sick": (8, 10, 2), "family": (3, 3, 0)},
    "EMP009": {"annual": (8, 12, 4), "sick": (5, 10, 5), "family": (1, 3, 2)},
    "EMP010": {"annual": (14, 18, 4), "sick": (10, 10, 0), "family": (3, 3, 0)},
    "EMP011": {"annual": (6, 8, 2), "sick": (8, 10, 2), "family": (3, 3, 0)},
    "EMP012": {"annual": (5, 6, 1), "sick": (9, 10, 1), "family": (2, 3, 1)},
}

# Hours worked per employee in current pay period
HOURS_WORKED = {
    "EMP001": 88,
    "EMP002": 80,
    "EMP003": 92,
    "EMP004": 60,
    "EMP005": 76,
    "EMP006": 96,
    "EMP007": 72,
    "EMP008": 84,
    "EMP009": 80,
    "EMP010": 100,
    "EMP011": 68,
    "EMP012": 48,
}


def seed_database(session: Session) -> None:
    """Seed the database with 12 SA employee profiles and related data.

    Idempotent: skips seeding if employees already exist.

    Args:
        session: SQLAlchemy session to use for seeding.
    """
    existing = session.query(Employee).count()
    if existing > 0:
        logger.info("Database already seeded (%d employees). Skipping.", existing)
        return

    logger.info("Seeding database with 12 employees...")

    # Create employees
    for emp_data in EMPLOYEES:
        session.add(Employee(**emp_data))
    session.flush()

    # Create leave balances
    for emp_id, balances in LEAVE_BALANCES.items():
        for leave_type, (balance, accrued, used) in balances.items():
            session.add(
                LeaveBalance(
                    employee_id=emp_id,
                    leave_type=leave_type,
                    balance_days=balance,
                    accrued_ytd=accrued,
                    used_ytd=used,
                )
            )
    session.flush()

    # Create timesheets
    for emp_id, hours in HOURS_WORKED.items():
        session.add(
            Timesheet(
                employee_id=emp_id,
                pay_period_start=PAY_PERIOD_START,
                pay_period_end=PAY_PERIOD_END,
                hours_worked=hours,
                status=TimesheetStatus.APPROVED.value,
            )
        )
    session.flush()

    # Create EWA transactions - Thandiwe has R800 outstanding
    session.add(
        EWATransaction(
            id="EWA-20260205-001",
            employee_id="EMP002",
            amount=800,
            fee=10,
            status=EWAStatus.DISBURSED.value,
            requested_at=datetime(2026, 2, 5, 9, 30),
            disbursed_at=datetime(2026, 2, 5, 9, 31),
        )
    )

    session.commit()
    logger.info("Database seeded successfully with 12 employees.")
