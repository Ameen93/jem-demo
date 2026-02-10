"""SQLAlchemy models for Jem HR Demo."""

from datetime import date, datetime
from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class EmploymentStatus(str, Enum):
    """Employee employment status."""

    ACTIVE = "active"
    PROBATION = "probation"
    TERMINATED = "terminated"


class LeaveType(str, Enum):
    """Types of leave available."""

    ANNUAL = "annual"
    SICK = "sick"
    FAMILY = "family"


class TimesheetStatus(str, Enum):
    """Timesheet approval status."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class EWAStatus(str, Enum):
    """EWA transaction status."""

    PENDING = "pending"
    DISBURSED = "disbursed"
    REPAID = "repaid"
    CANCELLED = "cancelled"


class Employee(Base):
    """Employee model with profile information."""

    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    department: Mapped[str] = mapped_column(String(50))
    role: Mapped[str] = mapped_column(String(100))
    hire_date: Mapped[date]
    hourly_rate: Mapped[float]
    preferred_language: Mapped[str] = mapped_column(String(5), default="en")
    bank_account_last4: Mapped[str] = mapped_column(String(4))
    employment_status: Mapped[str] = mapped_column(
        String(20), default=EmploymentStatus.ACTIVE.value
    )

    # Relationships
    leave_balances: Mapped[list["LeaveBalance"]] = relationship(
        back_populates="employee", cascade="all, delete-orphan"
    )
    timesheets: Mapped[list["Timesheet"]] = relationship(
        back_populates="employee", cascade="all, delete-orphan"
    )
    ewa_transactions: Mapped[list["EWATransaction"]] = relationship(
        back_populates="employee", cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        """Convert employee to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "role": self.role,
            "hire_date": self.hire_date.isoformat(),
            "hourly_rate": self.hourly_rate,
            "preferred_language": self.preferred_language,
            "bank_account_last4": self.bank_account_last4,
            "employment_status": self.employment_status,
        }


class LeaveBalance(Base):
    """Leave balance tracking per employee and leave type."""

    __tablename__ = "leave_balances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(
        String(10), ForeignKey("employees.id", ondelete="CASCADE")
    )
    leave_type: Mapped[str] = mapped_column(String(20))
    balance_days: Mapped[float]
    accrued_ytd: Mapped[float] = mapped_column(default=0.0)
    used_ytd: Mapped[float] = mapped_column(default=0.0)

    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="leave_balances")

    def to_dict(self) -> dict:
        """Convert leave balance to dictionary."""
        return {
            "employee_id": self.employee_id,
            "leave_type": self.leave_type,
            "balance_days": self.balance_days,
            "accrued_ytd": self.accrued_ytd,
            "used_ytd": self.used_ytd,
        }


class Timesheet(Base):
    """Timesheet entries for pay period tracking."""

    __tablename__ = "timesheets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(
        String(10), ForeignKey("employees.id", ondelete="CASCADE")
    )
    pay_period_start: Mapped[date]
    pay_period_end: Mapped[date]
    hours_worked: Mapped[float]
    status: Mapped[str] = mapped_column(
        String(20), default=TimesheetStatus.APPROVED.value
    )

    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="timesheets")

    def to_dict(self) -> dict:
        """Convert timesheet to dictionary."""
        return {
            "employee_id": self.employee_id,
            "pay_period_start": self.pay_period_start.isoformat(),
            "pay_period_end": self.pay_period_end.isoformat(),
            "hours_worked": self.hours_worked,
            "status": self.status,
        }


class EWATransaction(Base):
    """Earned Wage Access transaction records."""

    __tablename__ = "ewa_transactions"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    employee_id: Mapped[str] = mapped_column(
        String(10), ForeignKey("employees.id", ondelete="CASCADE")
    )
    amount: Mapped[float]
    fee: Mapped[float] = mapped_column(default=10.0)
    status: Mapped[str] = mapped_column(String(20), default=EWAStatus.PENDING.value)
    requested_at: Mapped[datetime]
    disbursed_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    # Relationships
    employee: Mapped["Employee"] = relationship(back_populates="ewa_transactions")

    def to_dict(self) -> dict:
        """Convert EWA transaction to dictionary."""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "amount": self.amount,
            "fee": self.fee,
            "status": self.status,
            "requested_at": self.requested_at.isoformat(),
            "disbursed_at": self.disbursed_at.isoformat() if self.disbursed_at else None,
        }
