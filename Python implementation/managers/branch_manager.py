"""
Branch Manager for Library Management System

Manages library branches using a graph data structure (adjacency list).
Provides branch operations and shortest path calculations using BFS.
"""

from collections import defaultdict, deque
from typing import Dict, List, Optional
from models.branch import Branch


class BranchManager:
    """
    Manages library branches and their connections.

    Uses adjacency list graph representation for branch network.
    Provides BFS-based shortest path calculations.
    """

    def __init__(self):
        """Initialize branch manager with empty graph."""
        self.branches: Dict[str, Branch] = {}  # branch_id -> Branch object
        self.graph: Dict[str, List[str]] = defaultdict(list)  # adjacency list

    def add_branch(self, branch_id: str, name: str, location: str) -> None:
        """
        Add a new branch to the system.

        Args:
            branch_id: Unique branch identifier
            name: Branch name
            location: Branch location

        Raises:
            ValueError: If branch_id already exists
        """
        if branch_id in self.branches:
            raise ValueError(f"Branch with ID '{branch_id}' already exists")

        branch = Branch(branch_id, name, location)
        self.branches[branch_id] = branch
        # Add node to graph (even if no connections yet)
        self.graph[branch_id]  # This creates the key in defaultdict

    def connect_branches(self, branch_id1: str, branch_id2: str) -> None:
        """
        Connect two branches (undirected edge).

        Args:
            branch_id1: First branch ID
            branch_id2: Second branch ID

        Raises:
            ValueError: If either branch doesn't exist
        """
        if branch_id1 not in self.branches:
            raise ValueError(f"Branch '{branch_id1}' does not exist")
        if branch_id2 not in self.branches:
            raise ValueError(f"Branch '{branch_id2}' does not exist")

        # Add undirected edge
        if branch_id2 not in self.graph[branch_id1]:
            self.graph[branch_id1].append(branch_id2)
        if branch_id1 not in self.graph[branch_id2]:
            self.graph[branch_id2].append(branch_id1)

    def get_branch(self, branch_id: str) -> Branch:
        """
        Get a branch by ID.

        Args:
            branch_id: Branch identifier

        Returns:
            Branch: Branch object

        Raises:
            KeyError: If branch not found
        """
        return self.branches[branch_id]

    def list_branches(self) -> List[Branch]:
        """
        Get list of all branches.

        Returns:
            List[Branch]: List of all branch objects
        """
        return list(self.branches.values())

    def find_shortest_path(self, start_id: str, end_id: str) -> Optional[List[str]]:
        """
        Find shortest path between two branches using BFS.

        Time Complexity: O(V + E) where V = vertices (branches), E = edges (connections)

        Args:
            start_id: Starting branch ID
            end_id: Ending branch ID

        Returns:
            Optional[List[str]]: List of branch IDs in path, or None if no path exists

        Raises:
            ValueError: If start branch doesn't exist
        """
        if start_id not in self.branches:
            raise ValueError(f"Start branch '{start_id}' does not exist")
        if end_id not in self.branches:
            return None

        if start_id == end_id:
            return [start_id]

        # BFS setup
        queue = deque([(start_id, [start_id])])  # (current_node, path_to_current)
        visited = set([start_id])

        while queue:
            current_node, path = queue.popleft()

            # Check all neighbors
            for neighbor in self.graph[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]

                    if neighbor == end_id:
                        return new_path

                    queue.append((neighbor, new_path))

        return None  # No path found

    def get_branch_network_info(self) -> Dict:
        """
        Get information about the branch network.

        Returns:
            Dict: Network statistics
        """
        total_branches = len(self.branches)
        total_connections = sum(len(connections) for connections in self.graph.values()) // 2  # Divide by 2 for undirected

        return {
            'total_branches': total_branches,
            'total_connections': total_connections,
            'graph': dict(self.graph)  # Convert defaultdict to regular dict
        }

    def __str__(self) -> str:
        """String representation of branch manager."""
        return f"BranchManager({len(self.branches)} branches, {sum(len(c) for c in self.graph.values()) // 2} connections)"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"BranchManager(branches={list(self.branches.keys())}, graph={dict(self.graph)})"