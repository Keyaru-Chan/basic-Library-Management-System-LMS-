"""
Member model for Library Management System

Represents a library member with personal information and borrowing history.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Member:
    """
    Member data model.

    Attributes:
        member_id (str): Unique member identifier
        name (str): Member full name
        nrc (str): National Registration Card number
        phone (str): Contact phone number
        address (str): Residential address
        borrowed_books (List[Dict]): List of currently borrowed books with details
        fine_amount (float): Accumulated fines in MMK
    """
    member_id: str
    name: str
    nrc: str
    phone: str
    address: str
    borrowed_books: List[Dict[str, Any]] = field(default_factory=list)
    fine_amount: float = 0.0

    def __post_init__(self):
        """Validate data after initialization."""
        if self.fine_amount < 0:
            raise ValueError("Fine amount cannot be negative")

    def add_borrowed_book(self, book_id: str, book_title: str, borrow_date: str, due_date: str) -> None:
        """
        Add a book to the member's borrowed list.

        Args:
            book_id: Book identifier
            book_title: Book title
            borrow_date: Date when book was borrowed
            due_date: Date when book is due
        """
        borrow_record = {
            'book_id': book_id,
            'book_title': book_title,
            'borrow_date': borrow_date,
            'due_date': due_date
        }
        self.borrowed_books.append(borrow_record)

    def remove_borrowed_book(self, book_id: str) -> bool:
        """
        Remove a book from the member's borrowed list.

        Args:
            book_id: Book identifier to remove

        Returns:
            bool: True if book was found and removed, False otherwise
        """
        for i, book in enumerate(self.borrowed_books):
            if book['book_id'] == book_id:
                self.borrowed_books.pop(i)
                return True
        return False

    def has_borrowed_book(self, book_id: str) -> bool:
        """
        Check if member has borrowed a specific book.

        Args:
            book_id: Book identifier to check

        Returns:
            bool: True if member has borrowed the book
        """
        return any(book['book_id'] == book_id for book in self.borrowed_books)

    def get_borrowed_book_count(self) -> int:
        """
        Get the number of books currently borrowed by the member.

        Returns:
            int: Number of borrowed books
        """
        return len(self.borrowed_books)

    def add_fine(self, amount: float) -> None:
        """
        Add fine amount to member's account.

        Args:
            amount: Fine amount to add
        """
        if amount > 0:
            self.fine_amount += amount

    def clear_fine(self) -> None:
        """Clear all accumulated fines."""
        self.fine_amount = 0.0

    def __str__(self) -> str:
        """String representation of the member."""
        return f"{self.name} (ID: {self.member_id}) - Borrowed: {len(self.borrowed_books)} books"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"Member(id='{self.member_id}', name='{self.name}', borrowed={len(self.borrowed_books)}, fine={self.fine_amount})"