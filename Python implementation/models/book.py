"""
Book model for Library Management System

Represents a book in the library inventory with all necessary attributes.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    """
    Book data model.

    Attributes:
        book_id (str): Unique identifier (ISBN)
        title (str): Book title
        author (str): Book author
        year (int): Publication year
        quantity (int): Available quantity
    """
    book_id: str
    title: str
    author: str
    year: int
    quantity: int

    def __post_init__(self):
        """Validate data after initialization."""
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.year < 0 or self.year > 2100:
            raise ValueError("Invalid publication year")

    def decrease_quantity(self, amount: int = 1) -> bool:
        """
        Decrease book quantity.

        Args:
            amount: Amount to decrease (default: 1)

        Returns:
            bool: True if successful, False if insufficient quantity
        """
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False

    def increase_quantity(self, amount: int = 1) -> None:
        """
        Increase book quantity.

        Args:
            amount: Amount to increase (default: 1)
        """
        self.quantity += amount

    def is_available(self) -> bool:
        """
        Check if book is available for borrowing.

        Returns:
            bool: True if quantity > 0
        """
        return self.quantity > 0

    def __str__(self) -> str:
        """String representation of the book."""
        return f"{self.title} by {self.author} ({self.year}) - Qty: {self.quantity}"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"Book(id='{self.book_id}', title='{self.title}', author='{self.author}', year={self.year}, quantity={self.quantity})"