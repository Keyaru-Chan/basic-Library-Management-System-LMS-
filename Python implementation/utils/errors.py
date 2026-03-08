"""
Custom Exceptions for Library Management System

Defines all custom exceptions used throughout the LMS for proper error handling.
"""


class LibraryError(Exception):
    """Base exception class for all library-related errors."""
    pass


class BookError(LibraryError):
    """Base class for book-related errors."""
    pass


class BookNotFoundError(BookError):
    """Raised when a book is not found in the system."""

    def __init__(self, book_id: str, message: str = None):
        self.book_id = book_id
        if message is None:
            message = f"Book with ID '{book_id}' not found"
        super().__init__(message)


class BookUnavailableError(BookError):
    """Raised when a book is not available for borrowing."""

    def __init__(self, book_id: str, message: str = None):
        self.book_id = book_id
        if message is None:
            message = f"Book '{book_id}' is currently unavailable"
        super().__init__(message)


class BookAlreadyExistsError(BookError):
    """Raised when trying to add a book that already exists."""

    def __init__(self, book_id: str, branch_id: str = None, message: str = None):
        self.book_id = book_id
        self.branch_id = branch_id
        if message is None:
            if branch_id:
                message = f"Book '{book_id}' already exists in branch '{branch_id}'"
            else:
                message = f"Book '{book_id}' already exists"
        super().__init__(message)


class MemberError(LibraryError):
    """Base class for member-related errors."""
    pass


class MemberNotFoundError(MemberError):
    """Raised when a member is not found in the system."""

    def __init__(self, member_id: str, message: str = None):
        self.member_id = member_id
        if message is None:
            message = f"Member with ID '{member_id}' not found"
        super().__init__(message)


class DuplicateMemberError(MemberError):
    """Raised when trying to add a member that already exists."""

    def __init__(self, member_id: str, message: str = None):
        self.member_id = member_id
        if message is None:
            message = f"Member with ID '{member_id}' already exists"
        super().__init__(message)


class BranchError(LibraryError):
    """Base class for branch-related errors."""
    pass


class BranchNotFoundError(BranchError):
    """Raised when a branch is not found in the system."""

    def __init__(self, branch_id: str, message: str = None):
        self.branch_id = branch_id
        if message is None:
            message = f"Branch with ID '{branch_id}' not found"
        super().__init__(message)


class DuplicateBranchError(BranchError):
    """Raised when trying to add a branch that already exists."""

    def __init__(self, branch_id: str, message: str = None):
        self.branch_id = branch_id
        if message is None:
            message = f"Branch with ID '{branch_id}' already exists"
        super().__init__(message)


class BorrowError(LibraryError):
    """Base class for borrowing-related errors."""
    pass


class BorrowLimitExceededError(BorrowError):
    """Raised when a member exceeds their borrowing limit."""

    def __init__(self, member_id: str, current_count: int, limit: int, message: str = None):
        self.member_id = member_id
        self.current_count = current_count
        self.limit = limit
        if message is None:
            message = f"Member '{member_id}' has exceeded borrow limit ({current_count}/{limit})"
        super().__init__(message)


class BookAlreadyBorrowedError(BorrowError):
    """Raised when a member tries to borrow a book they already have."""

    def __init__(self, member_id: str, book_id: str, message: str = None):
        self.member_id = member_id
        self.book_id = book_id
        if message is None:
            message = f"Member '{member_id}' has already borrowed book '{book_id}'"
        super().__init__(message)


class InvalidOperationError(LibraryError):
    """Raised when an invalid operation is attempted."""

    def __init__(self, operation: str, reason: str, message: str = None):
        self.operation = operation
        self.reason = reason
        if message is None:
            message = f"Invalid operation '{operation}': {reason}"
        super().__init__(message)


class ValidationError(LibraryError):
    """Raised when input validation fails."""

    def __init__(self, field: str, value: any, reason: str, message: str = None):
        self.field = field
        self.value = value
        self.reason = reason
        if message is None:
            message = f"Validation error for '{field}': {reason} (value: {value})"
        super().__init__(message)