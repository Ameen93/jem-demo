"""Tests for database seeding."""

import tempfile
from contextlib import contextmanager
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.db.models import (
    Base,
    Employee,
    EmploymentStatus,
    EWAStatus,
    EWATransaction,
    LeaveBalance,
    LeaveType,
    Timesheet,
)


@contextmanager
def test_session():
    """Create a temporary in-memory database session for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()


class TestSeedDatabase:
    """Tests for seed_database() function."""

    def test_creates_12_employees(self):
        """AC #1: 12 employees created matching PRD personas."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            employees = session.query(Employee).all()
            assert len(employees) == 12

    def test_employee_ids_format(self):
        """AC #1: Correct employee IDs EMP001-EMP012."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            ids = sorted([e.id for e in session.query(Employee).all()])
            expected = [f"EMP{str(i).zfill(3)}" for i in range(1, 13)]
            assert ids == expected

    def test_employee_names_match_prd(self):
        """AC #1: Names match PRD personas."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            sipho = session.get(Employee, "EMP001")
            assert sipho is not None
            assert sipho.name == "Sipho Dlamini"
            thandiwe = session.get(Employee, "EMP002")
            assert thandiwe.name == "Thandiwe Nkosi"

    def test_preferred_languages_set(self):
        """AC #1: Language codes set per persona."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            sipho = session.get(Employee, "EMP001")
            assert sipho.preferred_language == "zu"
            johan = session.get(Employee, "EMP003")
            assert johan.preferred_language == "af"
            nomvula = session.get(Employee, "EMP005")
            assert nomvula.preferred_language == "en"

    def test_lerato_in_probation(self):
        """AC #1: Lerato (EMP004) is in probation."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            lerato = session.get(Employee, "EMP004")
            assert lerato.employment_status == EmploymentStatus.PROBATION.value

    def test_leave_balances_created(self):
        """AC #2: Each employee has leave balances."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            for emp_id in [f"EMP{str(i).zfill(3)}" for i in range(1, 13)]:
                balances = (
                    session.query(LeaveBalance)
                    .filter_by(employee_id=emp_id)
                    .all()
                )
                types = {b.leave_type for b in balances}
                assert LeaveType.ANNUAL.value in types, f"{emp_id} missing annual"
                assert LeaveType.SICK.value in types, f"{emp_id} missing sick"
                assert LeaveType.FAMILY.value in types, f"{emp_id} missing family"

    def test_johan_low_annual_leave(self):
        """AC #2: Johan has low annual leave (used most)."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            annual = (
                session.query(LeaveBalance)
                .filter_by(employee_id="EMP003", leave_type=LeaveType.ANNUAL.value)
                .first()
            )
            assert annual.balance_days <= 3

    def test_timesheet_entries_created(self):
        """AC #3: Each employee has timesheet entries."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            for emp_id in [f"EMP{str(i).zfill(3)}" for i in range(1, 13)]:
                ts = (
                    session.query(Timesheet)
                    .filter_by(employee_id=emp_id)
                    .all()
                )
                assert len(ts) >= 1, f"{emp_id} missing timesheet"

    def test_sipho_88_hours(self):
        """AC #3: Sipho has 88 hours worked."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            ts = (
                session.query(Timesheet)
                .filter_by(employee_id="EMP001")
                .first()
            )
            assert ts.hours_worked == 88

    def test_timesheet_status_approved(self):
        """AC #3: All timesheets approved."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            timesheets = session.query(Timesheet).all()
            for ts in timesheets:
                assert ts.status == "approved"

    def test_thandiwe_outstanding_ewa(self):
        """AC #4: Thandiwe has R800 outstanding EWA."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            txns = (
                session.query(EWATransaction)
                .filter_by(employee_id="EMP002", status=EWAStatus.DISBURSED.value)
                .all()
            )
            total = sum(t.amount for t in txns)
            assert total == 800

    def test_idempotency(self):
        """Running seed_database twice doesn't duplicate data."""
        from src.db.seed import seed_database

        with test_session() as session:
            seed_database(session)
            seed_database(session)
            employees = session.query(Employee).all()
            assert len(employees) == 12
