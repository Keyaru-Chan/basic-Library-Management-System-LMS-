"""
Borrow Manager for Library Management System

Manages book borrowing and returning operations.
Uses queues (deques) for handling multiple borrow requests when books are unavailable.
"""

from collections import deque
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Deque
from managers.book_manager import BookManager
from managers.member_manager import MemberManager


class BorrowManager:
    """
    Manages book borrowing and returning operations.

    Uses queues for FIFO handling of borrow requests when books are unavailable.
    Maintains borrow history and due dates.
    """

    def __init__(self, book_manager: BookManager, member_manager: MemberManager):
        """
        Initialize borrow manager.

        Args:
            book_manager: Reference to book manager
            member_manager: Reference to member manager
        """
        self.book_manager = book_manager
        self.member_manager = member_manager

        # Waitlist queues: book_id -> deque of member_ids
        self.waitlists: Dict[str, Deque[str]] = {}

        # Borrow history: list of borrow records
        self.borrow_history: List[Dict] = []

        # Borrow period in days
        self.borrow_period_days = 14

        # Fine per day in MMK
        self.fine_per_day = 500.0

    def borrow_book(self, member_id: str, book_id: str) -> str:
        """
        Process a book borrow request.

        If book is available, borrow immediately.
        If not available, add to waitlist queue.

        Args:
            member_id: Member identifier
            book_id: Book identifier

        Returns:
            str: Status message

        Raises:
            ValueError: If member or book not found
        """
        # Validate member exists
        member = self.member_manager.get_member(member_id)
        if not member:
            raise ValueError(f"Member '{member_id}' not found")

        # Find book across all branches
        book_location = None
        book_obj = None

        for branch_id in self.book_manager.branch_books:
            try:
                book_obj = self.book_manager.get_book(branch_id, book_id)
                book_location = branch_id
                break
            except KeyError:
                continue

        if not book_obj:
            raise ValueError(f"Book '{book_id}' not found in any branch")

        # Check if member already has this book
        if member.has_borrowed_book(book_id):
            raise ValueError(f"Member already has borrowed book '{book_id}'")

        # Check if book is available
        if book_obj.is_available():
            # Borrow the book
            return self._borrow_available_book(member, book_obj, book_location)
        else:
            # Add to waitlist
            return self._add_to_waitlist(member_id, book_id)

    def _borrow_available_book(self, member: 'Member', book: 'Book', branch_id: str) -> str:
        """
        Borrow an available book.

        Args:
            member: Member object
            book: Book object
            branch_id: Branch identifier

        Returns:
            str: Success message
        """
        # Decrease quantity
        book.decrease_quantity()

        # Calculate dates
        borrow_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=self.borrow_period_days)).strftime("%Y-%m-%d")

        # Add to member's borrowed books
        member.add_borrowed_book(book.book_id, book.title, borrow_date, due_date)

        # Record in history
        self.borrow_history.append({
            'member_id': member.member_id,
            'book_id': book.book_id,
            'branch_id': branch_id,
            'borrow_date': borrow_date,
            'due_date': due_date,
            'return_date': None,
            'status': 'borrowed'
        })

        return f"Book '{book.title}' borrowed successfully. Due date: {due_date}"

    def _add_to_waitlist(self, member_id: str, book_id: str) -> str:
        """
        Add member to book waitlist.

        Args:
            member_id: Member identifier
            book_id: Book identifier

        Returns:
            str: Waitlist message
        """
        if book_id not in self.waitlists:
            self.waitlists[book_id] = deque()

        # Check if member already in waitlist
        if member_id in self.waitlists[book_id]:
            return f"Member '{member_id}' is already in waitlist for book '{book_id}'"

        self.waitlists[book_id].append(member_id)
        position = len(self.waitlists[book_id])

        return f"Book '{book_id}' is currently unavailable. Added to waitlist at position {position}."

    def return_book(self, member_id: str, book_id: str) -> str:
        """
        Process a book return.

        Increases book quantity and processes waitlist if any.

        Args:
            member_id: Member identifier
            book_id: Book identifier

        Returns:
            str: Status message

        Raises:
            ValueError: If member or book not found, or member doesn't have the book
        """
        # Validate member exists
        member = self.member_manager.get_member(member_id)
        if not member:
            raise ValueError(f"Member '{member_id}' not found")

        # Check if member has borrowed this book
        if not member.has_borrowed_book(book_id):
            raise ValueError(f"Member '{member_id}' has not borrowed book '{book_id}'")

        # Find the book
        book_obj = None
        branch_id = None
        for b_id in self.book_manager.branch_books:
            try:
                book_obj = self.book_manager.get_book(b_id, book_id)
                branch_id = b_id
                break
            except KeyError:
                continue

        if not book_obj:
            raise ValueError(f"Book '{book_id}' not found")

        # Calculate any fines
        return_date = datetime.now()
        fine_amount = self._calculate_fine(member, book_id, return_date)

        # Remove from member's borrowed books
        member.remove_borrowed_book(book_id)

        # Increase book quantity
        book_obj.increase_quantity()

        # Update borrow history
        self._update_borrow_history(member_id, book_id, return_date.strftime("%Y-%m-%d"), fine_amount)

        # Add fine to member
        if fine_amount > 0:
            member.add_fine(fine_amount)

        # Process waitlist
        waitlist_message = self._process_waitlist(book_id)

        fine_msg = f" Fine: {fine_amount} MMK." if fine_amount > 0 else ""
        return f"Book '{book_obj.title}' returned successfully.{fine_msg}{waitlist_message}"

    def _calculate_fine(self, member: 'Member', book_id: str, return_date: datetime) -> float:
        """
        Calculate overdue fine for a returned book.

        Args:
            member: Member object
            book_id: Book identifier
            return_date: Date of return

        Returns:
            float: Fine amount in MMK
        """
        # Find the borrow record
        for book in member.borrowed_books:
            if book['book_id'] == book_id:
                due_date = datetime.strptime(book['due_date'], "%Y-%m-%d")
                if return_date > due_date:
                    days_overdue = (return_date - due_date).days
                    return days_overdue * self.fine_per_day
                break
        return 0.0

    def _update_borrow_history(self, member_id: str, book_id: str, return_date: str, fine: float) -> None:
        """
        Update borrow history with return information.

        Args:
            member_id: Member identifier
            book_id: Book identifier
            return_date: Return date string
            fine: Fine amount
        """
        for record in self.borrow_history:
            if (record['member_id'] == member_id and
                record['book_id'] == book_id and
                record['status'] == 'borrowed' and
                record['return_date'] is None):
                record['return_date'] = return_date
                record['fine'] = fine
                record['status'] = 'returned'
                break

    def _process_waitlist(self, book_id: str) -> str:
        """
        Process waitlist for a returned book.

        Args:
            book_id: Book identifier

        Returns:
            str: Message about waitlist processing
        """
        if book_id not in self.waitlists or not self.waitlists[book_id]:
            return ""

        # Get next member in queue
        next_member_id = self.waitlists[book_id].popleft()

        # Try to borrow for this member
        try:
            result = self.borrow_book(next_member_id, book_id)
            return f" Next member '{next_member_id}' has been assigned the book."
        except Exception as e:
            return f" Could not assign book to next member: {e}"

    def get_borrow_history(self, member_id: str) -> List[Dict]:
        """
        Get borrow history for a member.

        Args:
            member_id: Member identifier

        Returns:
            List[Dict]: List of borrow records
        """
        return [record for record in self.borrow_history if record['member_id'] == member_id]

    def get_overdue_books(self) -> List[Dict]:
        """
        Get all overdue books.

        Returns:
            List[Dict]: List of overdue book records
        """
        overdue = []
        today = datetime.now()

        for record in self.borrow_history:
            if record['status'] == 'borrowed':
                due_date = datetime.strptime(record['due_date'], "%Y-%m-%d")
                if today > due_date:
                    days_overdue = (today - due_date).days
                    record_copy = record.copy()
                    record_copy['days_overdue'] = days_overdue
                    overdue.append(record_copy)

        return overdue

    def __str__(self) -> str:
        """String representation of borrow manager."""
        active_borrows = len([r for r in self.borrow_history if r['status'] == 'borrowed'])
        waitlist_count = sum(len(queue) for queue in self.waitlists.values())
        return f"BorrowManager({active_borrows} active borrows, {waitlist_count} in waitlists)"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"BorrowManager(history={len(self.borrow_history)}, waitlists={len(self.waitlists)})"