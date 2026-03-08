"""
Sorting Algorithms for Library Management System

Implements various sorting algorithms as required for the DSA assignment:
- Insertion Sort
- Quick Sort
- Merge Sort

All algorithms include complexity analysis and are used for sorting books by various criteria.
"""

from typing import List, TypeVar, Callable, Dict

T = TypeVar('T')  # Generic type for sorting


def insertion_sort(arr: List[T], key: Callable[[T], any] = None) -> List[T]:
    """
    Insertion Sort Algorithm.

    Best Case: O(n) - when array is already sorted
    Average Case: O(n²)
    Worst Case: O(n²)
    Space Complexity: O(1) - in-place sorting

    Good for small datasets or nearly sorted data.

    Args:
        arr: List to sort
        key: Optional key function for comparison

    Returns:
        List[T]: Sorted list
    """
    if not arr:
        return arr

    # Create a copy to avoid modifying original
    sorted_arr = arr.copy()

    for i in range(1, len(sorted_arr)):
        key_item = sorted_arr[i]

        # Get comparison key
        key_value = key(key_item) if key else key_item

        # Find insertion position
        j = i - 1
        while j >= 0:
            compare_value = key(sorted_arr[j]) if key else sorted_arr[j]

            if compare_value > key_value:
                sorted_arr[j + 1] = sorted_arr[j]
                j -= 1
            else:
                break

        sorted_arr[j + 1] = key_item

    return sorted_arr


def quick_sort(arr: List[T], key: Callable[[T], any] = None) -> List[T]:
    """
    Quick Sort Algorithm.

    Best Case: O(n log n)
    Average Case: O(n log n)
    Worst Case: O(n²) - when pivot is always the smallest/largest element
    Space Complexity: O(log n) - for recursion stack

    Fastest sorting algorithm in practice for most cases.

    Args:
        arr: List to sort
        key: Optional key function for comparison

    Returns:
        List[T]: Sorted list
    """
    if not arr:
        return arr

    sorted_arr = arr.copy()

    def _partition(low: int, high: int) -> int:
        """Partition helper function."""
        # Choose rightmost element as pivot
        pivot = key(sorted_arr[high]) if key else sorted_arr[high]

        i = low - 1

        for j in range(low, high):
            compare_value = key(sorted_arr[j]) if key else sorted_arr[j]

            if compare_value <= pivot:
                i += 1
                sorted_arr[i], sorted_arr[j] = sorted_arr[j], sorted_arr[i]

        sorted_arr[i + 1], sorted_arr[high] = sorted_arr[high], sorted_arr[i + 1]
        return i + 1

    def _quick_sort_recursive(low: int, high: int) -> None:
        """Recursive quick sort."""
        if low < high:
            # Find pivot position
            pi = _partition(low, high)

            # Sort left and right partitions
            _quick_sort_recursive(low, pi - 1)
            _quick_sort_recursive(pi + 1, high)

    _quick_sort_recursive(0, len(sorted_arr) - 1)
    return sorted_arr


def merge_sort(arr: List[T], key: Callable[[T], any] = None) -> List[T]:
    """
    Merge Sort Algorithm.

    Best Case: O(n log n)
    Average Case: O(n log n)
    Worst Case: O(n log n)
    Space Complexity: O(n) - requires additional space for merging

    Stable sorting algorithm, good for large datasets.

    Args:
        arr: List to sort
        key: Optional key function for comparison

    Returns:
        List[T]: Sorted list
    """
    if not arr:
        return arr

    if len(arr) <= 1:
        return arr.copy()

    def _merge(left: List[T], right: List[T]) -> List[T]:
        """Merge two sorted lists."""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            left_val = key(left[i]) if key else left[i]
            right_val = key(right[j]) if key else right[j]

            if left_val <= right_val:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        # Add remaining elements
        result.extend(left[i:])
        result.extend(right[j:])

        return result

    # Split array into halves
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)

    return _merge(left, right)


def sort_books_by_title(books: List['Book'], algorithm: str = 'merge') -> List['Book']:
    """
    Sort books by title using specified algorithm.

    Args:
        books: List of Book objects
        algorithm: Sorting algorithm ('insertion', 'quick', 'merge')

    Returns:
        List[Book]: Sorted list of books

    Raises:
        ValueError: If algorithm is not supported
    """
    if algorithm == 'insertion':
        return insertion_sort(books, key=lambda book: book.title.lower())
    elif algorithm == 'quick':
        return quick_sort(books, key=lambda book: book.title.lower())
    elif algorithm == 'merge':
        return merge_sort(books, key=lambda book: book.title.lower())
    else:
        raise ValueError(f"Unsupported sorting algorithm: {algorithm}")


def sort_books_by_author(books: List['Book'], algorithm: str = 'merge') -> List['Book']:
    """
    Sort books by author using specified algorithm.

    Args:
        books: List of Book objects
        algorithm: Sorting algorithm ('insertion', 'quick', 'merge')

    Returns:
        List[Book]: Sorted list of books
    """
    if algorithm == 'insertion':
        return insertion_sort(books, key=lambda book: book.author.lower())
    elif algorithm == 'quick':
        return quick_sort(books, key=lambda book: book.author.lower())
    elif algorithm == 'merge':
        return merge_sort(books, key=lambda book: book.author.lower())
    else:
        raise ValueError(f"Unsupported sorting algorithm: {algorithm}")


def sort_books_by_year(books: List['Book'], algorithm: str = 'merge') -> List['Book']:
    """
    Sort books by publication year using specified algorithm.

    Args:
        books: List of Book objects
        algorithm: Sorting algorithm ('insertion', 'quick', 'merge')

    Returns:
        List[Book]: Sorted list of books
    """
    if algorithm == 'insertion':
        return insertion_sort(books, key=lambda book: book.year)
    elif algorithm == 'quick':
        return quick_sort(books, key=lambda book: book.year)
    elif algorithm == 'merge':
        return merge_sort(books, key=lambda book: book.year)
    else:
        raise ValueError(f"Unsupported sorting algorithm: {algorithm}")


# Complexity analysis functions for demonstration

def analyze_sorting_complexity(algorithm: str, n: int) -> Dict[str, str]:
    """
    Analyze time complexity for sorting algorithms.

    Args:
        algorithm: Sorting algorithm name
        n: Input size

    Returns:
        Dict[str, str]: Complexity analysis
    """
    if algorithm == 'insertion':
        return {
            'best_case': 'O(n)',
            'average_case': f'O({n}²)',
            'worst_case': f'O({n}²)',
            'space_complexity': 'O(1)',
            'stability': 'Stable'
        }
    elif algorithm == 'quick':
        return {
            'best_case': f'O({n} log {n})',
            'average_case': f'O({n} log {n})',
            'worst_case': f'O({n}²)',
            'space_complexity': f'O(log {n})',
            'stability': 'Not stable'
        }
    elif algorithm == 'merge':
        return {
            'best_case': f'O({n} log {n})',
            'average_case': f'O({n} log {n})',
            'worst_case': f'O({n} log {n})',
            'space_complexity': f'O({n})',
            'stability': 'Stable'
        }
    else:
        return {'error': 'Unknown algorithm'}