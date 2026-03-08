"""
BFS Search Algorithm for Library Management System

Implements Breadth First Search for finding books across branches
and calculating shortest paths between branches.
"""

from collections import deque
from typing import Dict, List, Optional, Set, Tuple


def bfs_search_book(branches: Dict[str, List[str]], book_locations: Dict[str, str], start_branch: str, target_book: str) -> Optional[List[str]]:
    """
    Find a book using BFS across branch network.

    Time Complexity: O(V + E) where V = branches, E = connections

    Args:
        branches: Adjacency list of branch connections
        book_locations: book_id -> branch_id mapping
        start_branch: Branch to start search from
        target_book: Book ID to search for

    Returns:
        Optional[List[str]]: Path to branch containing the book, or None if not found
    """
    if target_book not in book_locations:
        return None

    target_branch = book_locations[target_book]

    # If book is in start branch, return immediately
    if start_branch == target_branch:
        return [start_branch]

    # BFS to find shortest path to target branch
    queue = deque([(start_branch, [start_branch])])  # (current_branch, path)
    visited: Set[str] = set([start_branch])

    while queue:
        current_branch, path = queue.popleft()

        # Check neighbors
        for neighbor in branches.get(current_branch, []):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]

                if neighbor == target_branch:
                    return new_path

                queue.append((neighbor, new_path))

    return None


def bfs_shortest_path_branches(branches: Dict[str, List[str]], start_branch: str, end_branch: str) -> Optional[List[str]]:
    """
    Find shortest path between two branches using BFS.

    Time Complexity: O(V + E)

    Args:
        branches: Adjacency list of branch connections
        start_branch: Starting branch ID
        end_branch: Ending branch ID

    Returns:
        Optional[List[str]]: Shortest path as list of branch IDs, or None if no path
    """
    if start_branch not in branches:
        return None
    if end_branch not in branches:
        return None
    if start_branch == end_branch:
        return [start_branch]

    # BFS setup
    queue = deque([(start_branch, [start_branch])])  # (current, path)
    visited: Set[str] = set([start_branch])

    while queue:
        current, path = queue.popleft()

        # Explore neighbors
        for neighbor in branches.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]

                if neighbor == end_branch:
                    return new_path

                queue.append((neighbor, new_path))

    return None


def bfs_traverse_all_branches(branches: Dict[str, List[str]], start_branch: str) -> List[str]:
    """
    Traverse all reachable branches from a starting point using BFS.

    Time Complexity: O(V + E)

    Args:
        branches: Adjacency list of branch connections
        start_branch: Branch to start traversal from

    Returns:
        List[str]: List of all reachable branch IDs in BFS order
    """
    if start_branch not in branches:
        return []

    visited: Set[str] = set()
    queue = deque([start_branch])
    visited.add(start_branch)
    result = [start_branch]

    while queue:
        current = queue.popleft()

        for neighbor in branches.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                result.append(neighbor)

    return result


def calculate_branch_network_diameter(branches: Dict[str, List[str]]) -> int:
    """
    Calculate the diameter of the branch network (longest shortest path).

    Time Complexity: O(V * (V + E))

    Args:
        branches: Adjacency list of branch connections

    Returns:
        int: Network diameter (maximum shortest path length)
    """
    if not branches:
        return 0

    max_distance = 0

    for start_branch in branches:
        # BFS from each branch to find farthest branch
        distances = bfs_distances_from_branch(branches, start_branch)
        if distances:
            max_distance = max(max_distance, max(distances.values()))

    return max_distance


def bfs_distances_from_branch(branches: Dict[str, List[str]], start_branch: str) -> Dict[str, int]:
    """
    Calculate distances from a branch to all other reachable branches.

    Time Complexity: O(V + E)

    Args:
        branches: Adjacency list of branch connections
        start_branch: Branch to calculate distances from

    Returns:
        Dict[str, int]: branch_id -> distance mapping
    """
    if start_branch not in branches:
        return {}

    distances: Dict[str, int] = {}
    queue = deque([(start_branch, 0)])  # (branch, distance)
    visited: Set[str] = set([start_branch])

    while queue:
        current, distance = queue.popleft()
        distances[current] = distance

        for neighbor in branches.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))

    return distances