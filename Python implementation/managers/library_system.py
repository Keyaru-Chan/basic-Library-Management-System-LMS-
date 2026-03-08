"""
Library System Main Controller

Coordinates all managers and provides the main interface for the LMS.
"""

from managers.branch_manager import BranchManager
from managers.book_manager import BookManager
from managers.member_manager import MemberManager
from managers.borrow_manager import BorrowManager
from managers.report_manager import ReportManager


class LibrarySystem:
    """
    Main library system controller.

    Coordinates all subsystem managers and provides unified interface.
    """

    def __init__(self):
        """Initialize the library system with all managers."""
        self.branch_manager = BranchManager()
        self.book_manager = BookManager(self.branch_manager)
        self.member_manager = MemberManager()
        self.borrow_manager = BorrowManager(self.book_manager, self.member_manager)
        self.report_manager = ReportManager(self.member_manager, self.borrow_manager)

    def __str__(self) -> str:
        """String representation of the library system."""
        return "Library Management System"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"LibrarySystem(branches={len(self.branch_manager.branches)}, books={self.book_manager.get_total_books()}, members={len(self.member_manager.members)})"