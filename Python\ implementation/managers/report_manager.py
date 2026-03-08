"""
Report Manager for Library Management System

Generates various reports about the library system including borrowed books,
overdue books, and fine reports.
"""

from typing import List, Dict
from managers.member_manager import MemberManager
from managers.borrow_manager import BorrowManager


class ReportManager:
    """
    Generates reports for the library management system.

    Provides various analytical reports about system usage and status.
    """

    def __init__(self, member_manager: MemberManager, borrow_manager: BorrowManager):
        """
        Initialize report manager.

        Args:
            member_manager: Reference to member manager
            borrow_manager: Reference to borrow manager
        """
        self.member_manager = member_manager
        self.borrow_manager = borrow_manager

    def generate_borrowed_books_report(self) -> List[Dict]:
        """
        Generate report of all currently borrowed books.

        Returns:
            List[Dict]: List of borrowed book records with member and book details
        """
        report = []

        for member in self.member_manager.list_members():
            for borrowed_book in member.borrowed_books:
                report.append({
                    'member_id': member.member_id,
                    'member_name': member.name,
                    'book_id': borrowed_book['book_id'],
                    'book_title': borrowed_book['book_title'],
                    'borrow_date': borrowed_book['borrow_date'],
                    'due_date': borrowed_book['due_date']
                })

        return report

    def generate_overdue_report(self) -> List[Dict]:
        """
        Generate report of all overdue books.

        Returns:
            List[Dict]: List of overdue book records
        """
        return self.borrow_manager.get_overdue_books()

    def generate_fine_report(self) -> List[Dict]:
        """
        Generate report of members with outstanding fines.

        Returns:
            List[Dict]: List of members with their total fines
        """
        report = []

        for member in self.member_manager.list_members():
            if member.fine_amount > 0:
                report.append({
                    'member_id': member.member_id,
                    'member_name': member.name,
                    'total_fine': member.fine_amount
                })

        return report

    def generate_branch_inventory_report(self) -> Dict:
        """
        Generate comprehensive branch inventory report.

        Returns:
            Dict: Branch inventory statistics
        """
        # This would require access to branch and book managers
        # For now, return placeholder
        return {
            'total_branches': 0,
            'total_books': 0,
            'total_quantity': 0,
            'branch_details': []
        }

    def generate_popular_books_report(self) -> List[Dict]:
        """
        Generate report of most borrowed books.

        Returns:
            List[Dict]: List of books sorted by borrow frequency
        """
        borrow_counts = {}

        # Count borrows from history
        for record in self.borrow_manager.borrow_history:
            book_id = record['book_id']
            if book_id not in borrow_counts:
                borrow_counts[book_id] = {'count': 0, 'title': record.get('book_title', 'Unknown')}
            borrow_counts[book_id]['count'] += 1

        # Sort by borrow count
        sorted_books = sorted(
            borrow_counts.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )

        return [
            {
                'book_id': book_id,
                'book_title': info['title'],
                'borrow_count': info['count']
            }
            for book_id, info in sorted_books
        ]

    def generate_member_activity_report(self) -> List[Dict]:
        """
        Generate report of member borrowing activity.

        Returns:
            List[Dict]: List of members with their activity statistics
        """
        report = []

        for member in self.member_manager.list_members():
            history = self.borrow_manager.get_borrow_history(member.member_id)
            total_borrows = len(history)
            current_borrows = len(member.borrowed_books)

            report.append({
                'member_id': member.member_id,
                'member_name': member.name,
                'total_borrows': total_borrows,
                'current_borrows': current_borrows,
                'outstanding_fine': member.fine_amount
            })

        return report

    def get_system_statistics(self) -> Dict:
        """
        Get overall system statistics.

        Returns:
            Dict: System-wide statistics
        """
        total_members = self.member_manager.get_member_count()
        borrowed_books_report = self.generate_borrowed_books_report()
        overdue_report = self.generate_overdue_report()
        fine_report = self.generate_fine_report()

        total_borrowed = len(borrowed_books_report)
        total_overdue = len(overdue_report)
        total_fines = sum(item['total_fine'] for item in fine_report)

        return {
            'total_members': total_members,
            'total_borrowed_books': total_borrowed,
            'total_overdue_books': total_overdue,
            'total_outstanding_fines': total_fines,
            'average_books_per_member': total_borrowed / total_members if total_members > 0 else 0
        }

    def __str__(self) -> str:
        """String representation of report manager."""
        return "ReportManager"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return "ReportManager()"