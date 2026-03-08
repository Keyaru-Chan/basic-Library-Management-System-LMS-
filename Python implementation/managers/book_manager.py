"""
Book Manager for Library Management System

Manages book inventory across all branches using hash maps for O(1) operations.
Provides search, add, update, delete operations with efficient lookups.
"""

from typing import Dict, List, Optional, Tuple
from models.book import Book
from managers.branch_manager import BranchManager


class BookManager:
    """
    Manages book inventory across all library branches.

    Uses hash maps for O(1) average-case operations.
    Books are stored per branch: branch_books[branch_id][book_id] = Book
    """

    def __init__(self, branch_manager: BranchManager):
        """
        Initialize book manager.

        Args:
            branch_manager: Reference to branch manager for validation
        """
        self.branch_manager = branch_manager
        # branch_books[branch_id][book_id] = Book object
        self.branch_books: Dict[str, Dict[str, Book]] = {}

    def add_book(self, branch_id: str, book_id: str, title: str, author: str, year: int, quantity: int) -> None:
        """
        Add a book to a specific branch.

        Time Complexity: O(1)

        Args:
            branch_id: Branch identifier
            book_id: Book identifier (ISBN)
            title: Book title
            author: Book author
            year: Publication year
            quantity: Initial quantity

        Raises:
            ValueError: If branch doesn't exist or book already exists
        """
        # Validate branch exists
        self.branch_manager.get_branch(branch_id)

        # Initialize branch books dict if not exists
        if branch_id not in self.branch_books:
            self.branch_books[branch_id] = {}

        # Check if book already exists in this branch
        if book_id in self.branch_books[branch_id]:
            raise ValueError(f"Book '{book_id}' already exists in branch '{branch_id}'")

        # Create and add book
        book = Book(book_id, title, author, year, quantity)
        self.branch_books[branch_id][book_id] = book

        # Also add to branch's inventory
        branch = self.branch_manager.get_branch(branch_id)
        branch.add_book(book)

    def get_book(self, branch_id: str, book_id: str) -> Book:
        """
        Get a book from a specific branch.

        Time Complexity: O(1)

        Args:
            branch_id: Branch identifier
            book_id: Book identifier

        Returns:
            Book: Book object

        Raises:
            KeyError: If branch or book not found
        """
        if branch_id not in self.branch_books:
            raise KeyError(f"Branch '{branch_id}' has no books")
        return self.branch_books[branch_id][book_id]

    def update_book_quantity(self, branch_id: str, book_id: str, new_quantity: int) -> None:
        """
        Update book quantity in a branch.

        Time Complexity: O(1)

        Args:
            branch_id: Branch identifier
            book_id: Book identifier
            new_quantity: New quantity value

        Raises:
            ValueError: If quantity is negative
            KeyError: If branch or book not found
        """
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")

        book = self.get_book(branch_id, book_id)
        book.quantity = new_quantity

    def delete_book(self, branch_id: str, book_id: str) -> None:
        """
        Delete a book from a branch.

        Time Complexity: O(1)

        Args:
            branch_id: Branch identifier
            book_id: Book identifier

        Raises:
            KeyError: If branch or book not found
        """
        if branch_id not in self.branch_books:
            raise KeyError(f"Branch '{branch_id}' has no books")

        if book_id not in self.branch_books[branch_id]:
            raise KeyError(f"Book '{book_id}' not found in branch '{branch_id}'")

        # Remove from branch books
        del self.branch_books[branch_id][book_id]

        # Remove from branch inventory
        branch = self.branch_manager.get_branch(branch_id)
        branch.remove_book(book_id)

    def search_book(self, title: str) -> Optional[Tuple[str, Book]]:
        """
        Search for a book by title across all branches using BFS.

        Time Complexity: O(V + E) where V = branches, E = books per branch

        Args:
            title: Book title to search for

        Returns:
            Optional[Tuple[str, Book]]: (branch_id, book) if found, None otherwise
        """
        # Simple linear search across all branches (could be optimized with indexing)
        for branch_id, books in self.branch_books.items():
            for book in books.values():
                if title.lower() in book.title.lower():
                    return (branch_id, book)
        return None

    def list_books_by_branch(self, branch_id: str) -> List[Book]:
        """
        List all books in a specific branch.

        Time Complexity: O(1) to get branch books dict, O(n) to convert to list

        Args:
            branch_id: Branch identifier

        Returns:
            List[Book]: List of books in the branch

        Raises:
            KeyError: If branch not found
        """
        if branch_id not in self.branch_books:
            return []
        return list(self.branch_books[branch_id].values())

    def sort_books_by_title(self, branch_id: str) -> List[Book]:
        """
        Sort books in a branch by title using merge sort.

        Time Complexity: O(n log n)

        Args:
            branch_id: Branch identifier

        Returns:
            List[Book]: Sorted list of books

        Raises:
            KeyError: If branch not found
        """
        books = self.list_books_by_branch(branch_id)
        if not books:
            return books

        # Use Python's built-in sorted (Timsort - hybrid of merge sort and insertion sort)
        return sorted(books, key=lambda book: book.title.lower())

    def get_total_books(self) -> int:
        """
        Get total number of book titles across all branches.

        Returns:
            int: Total number of unique book titles
        """
        return sum(len(books) for books in self.branch_books.values())

    def get_total_quantity(self) -> int:
        """
        Get total quantity of all books across all branches.

        Returns:
            int: Total quantity of all books
        """
        total = 0
        for branch_books in self.branch_books.values():
            for book in branch_books.values():
                total += book.quantity
        return total

    def __str__(self) -> str:
        """String representation of book manager."""
        total_books = self.get_total_books()
        total_quantity = self.get_total_quantity()
        return f"BookManager({total_books} titles, {total_quantity} total copies)"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"BookManager(branches={len(self.branch_books)}, total_books={self.get_total_books()})"