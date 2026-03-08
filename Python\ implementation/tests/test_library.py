#!/usr/bin/env python3
"""
Test Suite for Library Management System

Comprehensive tests demonstrating all features and algorithms.
"""

import unittest
from datetime import datetime, timedelta
from models.book import Book
from models.member import Member
from models.branch import Branch
from managers.branch_manager import BranchManager
from managers.book_manager import BookManager
from managers.member_manager import MemberManager
from managers.borrow_manager import BorrowManager
from managers.report_manager import ReportManager
from managers.library_system import LibrarySystem
from algorithms.sorting import insertion_sort, quick_sort, merge_sort, sort_books_by_title
from algorithms.bfs_search import bfs_shortest_path_branches
from utils.fine_calculator import FineCalculator


class TestBookModel(unittest.TestCase):
    """Test Book model functionality."""

    def test_book_creation(self):
        """Test book creation and validation."""
        book = Book("123", "Test Book", "Test Author", 2020, 5)
        self.assertEqual(book.book_id, "123")
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.quantity, 5)
        self.assertTrue(book.is_available())

    def test_book_quantity_operations(self):
        """Test quantity increase/decrease operations."""
        book = Book("123", "Test Book", "Test Author", 2020, 3)

        # Test decrease
        self.assertTrue(book.decrease_quantity(2))
        self.assertEqual(book.quantity, 1)

        # Test increase
        book.increase_quantity(1)
        self.assertEqual(book.quantity, 2)

        # Test insufficient quantity
        self.assertFalse(book.decrease_quantity(5))
        self.assertEqual(book.quantity, 2)

    def test_invalid_quantity(self):
        """Test invalid quantity handling."""
        with self.assertRaises(ValueError):
            Book("123", "Test Book", "Test Author", 2020, -1)


class TestMemberModel(unittest.TestCase):
    """Test Member model functionality."""

    def test_member_creation(self):
        """Test member creation."""
        member = Member("M001", "John Doe", "12/ABC(N)123456", "555-1234", "123 Main St")
        self.assertEqual(member.member_id, "M001")
        self.assertEqual(member.name, "John Doe")
        self.assertEqual(member.get_borrowed_book_count(), 0)

    def test_borrow_operations(self):
        """Test borrowing operations."""
        member = Member("M001", "John Doe", "12/ABC(N)123456", "555-1234", "123 Main St")

        # Add borrowed book
        member.add_borrowed_book("B001", "Test Book", "2024-01-01", "2024-01-15")
        self.assertEqual(member.get_borrowed_book_count(), 1)
        self.assertTrue(member.has_borrowed_book("B001"))

        # Remove borrowed book
        self.assertTrue(member.remove_borrowed_book("B001"))
        self.assertEqual(member.get_borrowed_book_count(), 0)
        self.assertFalse(member.has_borrowed_book("B001"))

        # Try to remove non-existent book
        self.assertFalse(member.remove_borrowed_book("B999"))


class TestBranchManager(unittest.TestCase):
    """Test Branch Manager functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = BranchManager()

    def test_add_branch(self):
        """Test adding branches."""
        self.manager.add_branch("B001", "Central Library", "Downtown")
        self.assertEqual(len(self.manager.branches), 1)
        self.assertIn("B001", self.manager.branches)

    def test_connect_branches(self):
        """Test connecting branches."""
        self.manager.add_branch("B001", "Central", "Downtown")
        self.manager.add_branch("B002", "North", "North District")

        self.manager.connect_branches("B001", "B002")

        self.assertIn("B002", self.manager.graph["B001"])
        self.assertIn("B001", self.manager.graph["B002"])

    def test_shortest_path(self):
        """Test shortest path calculation."""
        # Create a simple network: A - B - C
        self.manager.add_branch("A", "Branch A", "Loc A")
        self.manager.add_branch("B", "Branch B", "Loc B")
        self.manager.add_branch("C", "Branch C", "Loc C")

        self.manager.connect_branches("A", "B")
        self.manager.connect_branches("B", "C")

        path = self.manager.find_shortest_path("A", "C")
        self.assertEqual(path, ["A", "B", "C"])

        # Test same branch
        path = self.manager.find_shortest_path("A", "A")
        self.assertEqual(path, ["A"])

        # Test no path
        path = self.manager.find_shortest_path("A", "D")  # D doesn't exist
        self.assertIsNone(path)


class TestBookManager(unittest.TestCase):
    """Test Book Manager functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.branch_manager = BranchManager()
        self.book_manager = BookManager(self.branch_manager)

        # Add a branch
        self.branch_manager.add_branch("B001", "Central Library", "Downtown")

    def test_add_book(self):
        """Test adding books."""
        self.book_manager.add_book("B001", "9781234567890", "Test Book", "Test Author", 2020, 5)

        book = self.book_manager.get_book("B001", "9781234567890")
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.quantity, 5)

    def test_search_book(self):
        """Test book search."""
        self.book_manager.add_book("B001", "9781234567890", "Python Programming", "John Doe", 2020, 1)

        result = self.book_manager.search_book("Python")
        self.assertIsNotNone(result)
        branch_id, book = result
        self.assertEqual(branch_id, "B001")
        self.assertEqual(book.title, "Python Programming")

    def test_update_quantity(self):
        """Test updating book quantity."""
        self.book_manager.add_book("B001", "9781234567890", "Test Book", "Author", 2020, 5)
        self.book_manager.update_book_quantity("B001", "9781234567890", 10)

        book = self.book_manager.get_book("B001", "9781234567890")
        self.assertEqual(book.quantity, 10)


class TestSortingAlgorithms(unittest.TestCase):
    """Test sorting algorithms."""

    def setUp(self):
        """Create test books."""
        self.books = [
            Book("1", "C Book", "Author C", 2000, 1),
            Book("2", "A Book", "Author A", 1990, 1),
            Book("3", "B Book", "Author B", 2010, 1)
        ]

    def test_insertion_sort(self):
        """Test insertion sort."""
        sorted_books = insertion_sort(self.books.copy(), key=lambda b: b.title)
        self.assertEqual(sorted_books[0].title, "A Book")
        self.assertEqual(sorted_books[1].title, "B Book")
        self.assertEqual(sorted_books[2].title, "C Book")

    def test_quick_sort(self):
        """Test quick sort."""
        sorted_books = quick_sort(self.books.copy(), key=lambda b: b.title)
        self.assertEqual(sorted_books[0].title, "A Book")
        self.assertEqual(sorted_books[1].title, "B Book")
        self.assertEqual(sorted_books[2].title, "C Book")

    def test_merge_sort(self):
        """Test merge sort."""
        sorted_books = merge_sort(self.books.copy(), key=lambda b: b.title)
        self.assertEqual(sorted_books[0].title, "A Book")
        self.assertEqual(sorted_books[1].title, "B Book")
        self.assertEqual(sorted_books[2].title, "C Book")

    def test_sort_books_by_title(self):
        """Test book sorting by title."""
        sorted_books = sort_books_by_title(self.books.copy())
        self.assertEqual(sorted_books[0].title, "A Book")
        self.assertEqual(sorted_books[1].title, "B Book")
        self.assertEqual(sorted_books[2].title, "C Book")


class TestBorrowManager(unittest.TestCase):
    """Test Borrow Manager functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.branch_manager = BranchManager()
        self.book_manager = BookManager(self.branch_manager)
        self.member_manager = MemberManager()
        self.borrow_manager = BorrowManager(self.book_manager, self.member_manager)

        # Setup test data
        self.branch_manager.add_branch("B001", "Central", "Downtown")
        self.book_manager.add_book("B001", "B001", "Test Book", "Author", 2020, 1)
        self.member_manager.add_member("M001", "John Doe", "12/ABC(N)123456", "555-1234", "123 Main St")

    def test_borrow_available_book(self):
        """Test borrowing an available book."""
        result = self.borrow_manager.borrow_book("M001", "B001")
        self.assertIn("borrowed successfully", result)

        # Check member has the book
        member = self.member_manager.get_member("M001")
        self.assertTrue(member.has_borrowed_book("B001"))

        # Check book quantity decreased
        book = self.book_manager.get_book("B001", "B001")
        self.assertEqual(book.quantity, 0)

    def test_borrow_unavailable_book(self):
        """Test borrowing an unavailable book (should queue)."""
        # First borrow the only copy
        self.borrow_manager.borrow_book("M001", "B001")

        # Add another member
        self.member_manager.add_member("M002", "Jane Smith", "12/DEF(N)234567", "555-5678", "456 Oak St")

        # Try to borrow again
        result = self.borrow_manager.borrow_book("M002", "B001")
        self.assertIn("Added to waitlist", result)

    def test_return_book(self):
        """Test returning a book."""
        # Borrow first
        self.borrow_manager.borrow_book("M001", "B001")

        # Return
        result = self.borrow_manager.return_book("M001", "B001")
        self.assertIn("returned successfully", result)

        # Check member no longer has the book
        member = self.member_manager.get_member("M001")
        self.assertFalse(member.has_borrowed_book("B001"))

        # Check book quantity increased
        book = self.book_manager.get_book("B001", "B001")
        self.assertEqual(book.quantity, 1)


class TestFineCalculator(unittest.TestCase):
    """Test Fine Calculator functionality."""

    def setUp(self):
        """Set up fine calculator."""
        self.calculator = FineCalculator(fine_per_day=500.0, grace_period_days=0)

    def test_no_fine_when_on_time(self):
        """Test no fine when book is returned on time."""
        fine = self.calculator.calculate_fine("2024-01-01", "2024-01-15", "2024-01-15")
        self.assertEqual(fine, 0)

    def test_fine_calculation(self):
        """Test fine calculation for overdue books."""
        # 3 days overdue
        fine = self.calculator.calculate_fine("2024-01-01", "2024-01-15", "2024-01-18")
        self.assertEqual(fine, 1500.0)  # 3 days * 500 MMK

    def test_grace_period(self):
        """Test grace period functionality."""
        calculator_with_grace = FineCalculator(fine_per_day=500.0, grace_period_days=2)

        # 3 days overdue but 2 days grace period
        fine = calculator_with_grace.calculate_fine("2024-01-01", "2024-01-15", "2024-01-17")
        self.assertEqual(fine, 0)  # Within grace period

        # 4 days overdue
        fine = calculator_with_grace.calculate_fine("2024-01-01", "2024-01-15", "2024-01-19")
        self.assertEqual(fine, 1000.0)  # 2 effective days * 500 MMK

    def test_is_overdue(self):
        """Test overdue checking."""
        self.assertFalse(self.calculator.is_overdue("2024-01-15", "2024-01-15"))
        self.assertTrue(self.calculator.is_overdue("2024-01-15", "2024-01-16"))


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""

    def setUp(self):
        """Set up complete library system."""
        self.library = LibrarySystem()

    def test_complete_workflow(self):
        """Test complete library workflow."""
        # Add branches
        self.library.branch_manager.add_branch("B001", "Central", "Downtown")
        self.library.branch_manager.add_branch("B002", "North", "North District")

        # Connect branches
        self.library.branch_manager.connect_branches("B001", "B002")

        # Add books
        self.library.book_manager.add_book("B001", "B001", "Python Guide", "John Doe", 2020, 2)
        self.library.book_manager.add_book("B002", "B002", "Java Guide", "Jane Smith", 2021, 1)

        # Add members
        self.library.member_manager.add_member("M001", "Alice Johnson", "12/ABC(N)111111", "555-1111", "111 Main St")
        self.library.member_manager.add_member("M002", "Bob Wilson", "12/DEF(N)222222", "555-2222", "222 Oak St")

        # Test shortest path
        path = self.library.branch_manager.find_shortest_path("B001", "B002")
        self.assertEqual(path, ["B001", "B002"])

        # Borrow books
        result1 = self.library.borrow_manager.borrow_book("M001", "B001")
        self.assertIn("borrowed successfully", result1)

        result2 = self.library.borrow_manager.borrow_book("M002", "B002")
        self.assertIn("borrowed successfully", result2)

        # Try to borrow unavailable book
        result3 = self.library.borrow_manager.borrow_book("M001", "B002")
        self.assertIn("Added to waitlist", result3)

        # Return book and check queue processing
        result4 = self.library.borrow_manager.return_book("M002", "B002")
        self.assertIn("returned successfully", result4)

        # Check that queue was processed (M001 should now have B002)
        member1 = self.library.member_manager.get_member("M001")
        self.assertTrue(member1.has_borrowed_book("B002"))

        # Generate reports
        borrowed_report = self.library.report_manager.generate_borrowed_books_report()
        self.assertEqual(len(borrowed_report), 2)  # Both books borrowed

        overdue_report = self.library.report_manager.generate_overdue_report()
        # Should be empty since books were just borrowed

        stats = self.library.report_manager.get_system_statistics()
        self.assertEqual(stats['total_members'], 2)
        self.assertEqual(stats['total_borrowed_books'], 2)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)