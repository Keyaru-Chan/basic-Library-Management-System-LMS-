"""
Member Manager for Library Management System

Manages library members using hash maps for O(1) lookups.
Supports member registration, search, and management operations.
"""

from typing import Dict, List, Optional
from models.member import Member


class MemberManager:
    """
    Manages library members.

    Uses hash map for O(1) average-case member lookups by member_id.
    """

    def __init__(self):
        """Initialize member manager with empty member store."""
        self.members: Dict[str, Member] = {}  # member_id -> Member object

    def add_member(self, member_id: str, name: str, nrc: str, phone: str, address: str) -> None:
        """
        Add a new member to the system.

        Time Complexity: O(1)

        Args:
            member_id: Unique member identifier
            name: Member full name
            nrc: National Registration Card number
            phone: Contact phone number
            address: Residential address

        Raises:
            ValueError: If member_id already exists
        """
        if member_id in self.members:
            raise ValueError(f"Member with ID '{member_id}' already exists")

        member = Member(member_id, name, nrc, phone, address)
        self.members[member_id] = member

    def get_member(self, member_id: str) -> Optional[Member]:
        """
        Get a member by ID.

        Time Complexity: O(1)

        Args:
            member_id: Member identifier

        Returns:
            Optional[Member]: Member object if found, None otherwise
        """
        return self.members.get(member_id)

    def update_member(self, member_id: str, **kwargs) -> None:
        """
        Update member information.

        Time Complexity: O(1)

        Args:
            member_id: Member identifier
            **kwargs: Fields to update (name, phone, address)

        Raises:
            KeyError: If member not found
        """
        member = self.members.get(member_id)
        if not member:
            raise KeyError(f"Member '{member_id}' not found")

        # Update allowed fields
        allowed_fields = {'name', 'phone', 'address'}
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(member, field, value)

    def delete_member(self, member_id: str) -> None:
        """
        Delete a member from the system.

        Time Complexity: O(1)

        Args:
            member_id: Member identifier

        Raises:
            KeyError: If member not found
        """
        if member_id not in self.members:
            raise KeyError(f"Member '{member_id}' not found")

        del self.members[member_id]

    def search_member_by_nrc(self, nrc: str) -> Optional[Member]:
        """
        Search member by NRC number.

        Time Complexity: O(n) - linear search

        Args:
            nrc: NRC number to search for

        Returns:
            Optional[Member]: Member object if found, None otherwise
        """
        for member in self.members.values():
            if member.nrc == nrc:
                return member
        return None

    def list_members(self) -> List[Member]:
        """
        Get list of all members.

        Time Complexity: O(n)

        Returns:
            List[Member]: List of all member objects
        """
        return list(self.members.values())

    def get_members_with_overdue_books(self) -> List[Member]:
        """
        Get members who have overdue books.

        Note: This is a placeholder - actual overdue logic would be in borrow manager

        Returns:
            List[Member]: List of members with overdue books
        """
        # This would be implemented with borrow manager integration
        return []

    def get_member_count(self) -> int:
        """
        Get total number of members.

        Returns:
            int: Total member count
        """
        return len(self.members)

    def __str__(self) -> str:
        """String representation of member manager."""
        return f"MemberManager({len(self.members)} members)"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"MemberManager(members={list(self.members.keys())})"