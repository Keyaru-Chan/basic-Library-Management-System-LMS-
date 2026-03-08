"""
Branch model for Library Management System

Represents a library branch with location and inventory information.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Branch:
    """
    Branch data model.

    Attributes:
        branch_id (str): Unique branch identifier
        name (str): Branch name
        location (str): Branch location/address
        inventory (Dict[str, Any]): Books inventory (book_id -> Book object)
    """
    branch_id: str
    name: str
    location: str
    inventory: Dict[str, 'Book'] = field(default_factory=dict)  # Forward reference to avoid circular import

    def add_book(self, book: 'Book') -> None:
        """
        Add a book to the branch inventory.

        Args:
            book: Book object to add
        """
        self.inventory[book.book_id] = book

    def remove_book(self, book_id: str) -> bool:
        """
        Remove a book from the branch inventory.

        Args:
            book_id: Book identifier to remove

        Returns:
            bool: True if book was found and removed, False otherwise
        """
        if book_id in self.inventory:
            del self.inventory[book_id]
            return True
        return False

    def get_book(self, book_id: str) -> 'Book':
        """
        Get a book from the branch inventory.

        Args:
            book_id: Book identifier to retrieve

        Returns:
            Book: Book object if found

        Raises:
            KeyError: If book not found in inventory
        """
        return self.inventory[book_id]

    def has_book(self, book_id: str) -> bool:
        """
        Check if branch has a specific book.

        Args:
            book_id: Book identifier to check

        Returns:
            bool: True if book exists in inventory
        """
        return book_id in self.inventory

    def get_total_books(self) -> int:
        """
        Get total number of books in inventory.

        Returns:
            int: Total number of book titles
        """
        return len(self.inventory)

    def get_total_quantity(self) -> int:
        """
        Get total quantity of all books in inventory.

        Returns:
            int: Total quantity across all books
        """
        return sum(book.quantity for book in self.inventory.values())

    def list_books(self) -> list:
        """
        Get list of all books in inventory.

        Returns:
            list: List of Book objects
        """
        return list(self.inventory.values())

    def __str__(self) -> str:
        """String representation of the branch."""
        return f"{self.name} ({self.location}) - {len(self.inventory)} books"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"Branch(id='{self.branch_id}', name='{self.name}', location='{self.location}', books={len(self.inventory)})"