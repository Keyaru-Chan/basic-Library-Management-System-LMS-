"""
Fine Calculator for Library Management System

Calculates overdue fines based on library policies.
"""

from datetime import datetime
from typing import Optional


class FineCalculator:
    """
    Calculates fines for overdue books.

    Uses configurable fine rates and policies.
    """

    def __init__(self, fine_per_day: float = 500.0, grace_period_days: int = 0):
        """
        Initialize fine calculator.

        Args:
            fine_per_day: Fine amount per day in MMK
            grace_period_days: Number of grace period days before fines apply
        """
        self.fine_per_day = fine_per_day
        self.grace_period_days = grace_period_days

    def calculate_fine(self, borrow_date: str, due_date: str, return_date: Optional[str] = None) -> float:
        """
        Calculate fine for a book loan.

        Args:
            borrow_date: Date when book was borrowed (YYYY-MM-DD)
            due_date: Due date for return (YYYY-MM-DD)
            return_date: Actual return date (YYYY-MM-DD), uses today if None

        Returns:
            float: Fine amount in MMK (0 if not overdue)

        Raises:
            ValueError: If dates are invalid
        """
        try:
            borrow_dt = datetime.strptime(borrow_date, "%Y-%m-%d")
            due_dt = datetime.strptime(due_date, "%Y-%m-%d")
            return_dt = datetime.strptime(return_date, "%Y-%m-%d") if return_date else datetime.now()
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        # Calculate days overdue
        days_overdue = (return_dt - due_dt).days

        # Apply grace period
        effective_overdue_days = max(0, days_overdue - self.grace_period_days)

        # Calculate fine
        fine = effective_overdue_days * self.fine_per_day

        return max(0, fine)  # Ensure non-negative

    def is_overdue(self, due_date: str, check_date: Optional[str] = None) -> bool:
        """
        Check if a book is overdue.

        Args:
            due_date: Due date (YYYY-MM-DD)
            check_date: Date to check against (uses today if None)

        Returns:
            bool: True if overdue

        Raises:
            ValueError: If date format is invalid
        """
        try:
            due_dt = datetime.strptime(due_date, "%Y-%m-%d")
            check_dt = datetime.strptime(check_date, "%Y-%m-%d") if check_date else datetime.now()
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        return check_dt > due_dt

    def get_days_overdue(self, due_date: str, check_date: Optional[str] = None) -> int:
        """
        Get number of days a book is overdue.

        Args:
            due_date: Due date (YYYY-MM-DD)
            check_date: Date to check against (uses today if None)

        Returns:
            int: Number of days overdue (0 if not overdue)

        Raises:
            ValueError: If date format is invalid
        """
        try:
            due_dt = datetime.strptime(due_date, "%Y-%m-%d")
            check_dt = datetime.strptime(check_date, "%Y-%m-%d") if check_date else datetime.now()
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        days_overdue = (check_dt - due_dt).days
        return max(0, days_overdue)

    def get_fine_breakdown(self, borrow_date: str, due_date: str, return_date: Optional[str] = None) -> dict:
        """
        Get detailed fine calculation breakdown.

        Args:
            borrow_date: Date when book was borrowed (YYYY-MM-DD)
            due_date: Due date for return (YYYY-MM-DD)
            return_date: Actual return date (YYYY-MM-DD), uses today if None

        Returns:
            dict: Fine calculation details
        """
        try:
            borrow_dt = datetime.strptime(borrow_date, "%Y-%m-%d")
            due_dt = datetime.strptime(due_date, "%Y-%m-%d")
            return_dt = datetime.strptime(return_date, "%Y-%m-%d") if return_date else datetime.now()
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        days_overdue = (return_dt - due_dt).days
        grace_adjusted_days = max(0, days_overdue - self.grace_period_days)
        fine_amount = grace_adjusted_days * self.fine_per_day

        return {
            'borrow_date': borrow_date,
            'due_date': due_date,
            'return_date': return_dt.strftime("%Y-%m-%d"),
            'days_overdue': max(0, days_overdue),
            'grace_period_days': self.grace_period_days,
            'effective_overdue_days': grace_adjusted_days,
            'fine_per_day': self.fine_per_day,
            'total_fine': max(0, fine_amount)
        }

    def update_fine_rate(self, new_rate: float) -> None:
        """
        Update the fine rate.

        Args:
            new_rate: New fine amount per day

        Raises:
            ValueError: If rate is negative
        """
        if new_rate < 0:
            raise ValueError("Fine rate cannot be negative")
        self.fine_per_day = new_rate

    def update_grace_period(self, days: int) -> None:
        """
        Update the grace period.

        Args:
            days: Number of grace period days

        Raises:
            ValueError: If days is negative
        """
        if days < 0:
            raise ValueError("Grace period cannot be negative")
        self.grace_period_days = days

    def __str__(self) -> str:
        """String representation of fine calculator."""
        return f"FineCalculator(rate={self.fine_per_day} MMK/day, grace={self.grace_period_days} days)"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"FineCalculator(fine_per_day={self.fine_per_day}, grace_period_days={self.grace_period_days})"