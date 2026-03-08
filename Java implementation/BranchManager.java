// BranchManager.java - Branch management with Graph (Adjacency List)

import java.util.*;

/**
 * BranchManager manages library branches and their connections using a Graph (Adjacency List).
 * 
 * Data Structure: Adjacency List stored in HashMap
 *   graph.get(branchId) returns List<String> of connected branches
 * 
 * Time Complexities:
 * - Add Branch: O(1)
 * - Connect Branches: O(1)
 * - Find Shortest Path (BFS): O(V + E)
 * - List Branches: O(V)
 */
public class BranchManager {
    private Map<String, Branch> branches;              // HashMap for O(1) branch lookup
    private Map<String, List<String>> graph;           // Adjacency List representation
    
    /**
     * Constructor - initializes branch manager with empty graph.
     */
    public BranchManager() {
        this.branches = new HashMap<>();
        this.graph = new HashMap<>();
    }
    
    /**
     * Add a new branch to the system.
     * 
     * Time Complexity: O(1)
     * 
     * @param branchId Unique branch identifier
     * @param name Branch name
     * @param location Branch location
     * @throws IllegalArgumentException if branch already exists
     */
    public void addBranch(String branchId, String name, String location) {
        if (branches.containsKey(branchId)) {
            throw new IllegalArgumentException("Branch '" + branchId + "' already exists");
        }
        
        Branch branch = new Branch(branchId, name, location);
        branches.put(branchId, branch);
        graph.put(branchId, new ArrayList<>());  // Initialize empty adjacency list
    }
    
    /**
     * Connect two branches (undirected edge).
     * 
     * Time Complexity: O(1)
     * 
     * @param branchId1 First branch ID
     * @param branchId2 Second branch ID
     * @throws IllegalArgumentException if either branch doesn't exist
     */
    public void connectBranches(String branchId1, String branchId2) {
        if (!branches.containsKey(branchId1)) {
            throw new IllegalArgumentException("Branch '" + branchId1 + "' does not exist");
        }
        if (!branches.containsKey(branchId2)) {
            throw new IllegalArgumentException("Branch '" + branchId2 + "' does not exist");
        }
        
        // Add undirected edge (both directions)
        List<String> neighbors1 = graph.get(branchId1);
        List<String> neighbors2 = graph.get(branchId2);
        
        if (!neighbors1.contains(branchId2)) {
            neighbors1.add(branchId2);
        }
        if (!neighbors2.contains(branchId1)) {
            neighbors2.add(branchId1);
        }
    }
    
    /**
     * Find shortest path between two branches using BFS.
     * 
     * Time Complexity: O(V + E)
     *   V = number of vertices (branches)
     *   E = number of edges (connections)
     * 
     * @param startId Starting branch ID
     * @param endId Ending branch ID
     * @return List of branch IDs in path, or null if no path exists
     * @throws IllegalArgumentException if start branch doesn't exist
     */
    public List<String> findShortestPath(String startId, String endId) {
        if (!branches.containsKey(startId)) {
            throw new IllegalArgumentException("Start branch '" + startId + "' does not exist");
        }
        if (!branches.containsKey(endId)) {
            return null;  // End branch doesn't exist
        }
        
        if (startId.equals(endId)) {
            return new ArrayList<>(Collections.singletonList(startId));
        }
        
        // BFS Setup
        Queue<PathNode> queue = new LinkedList<>();
        Set<String> visited = new HashSet<>();
        
        queue.add(new PathNode(startId, new ArrayList<>(Collections.singletonList(startId))));
        visited.add(startId);
        
        // BFS Algorithm
        while (!queue.isEmpty()) {
            PathNode current = queue.poll();
            String currentNode = current.node;
            List<String> path = current.path;
            
            // Check all neighbors
            for (String neighbor : graph.get(currentNode)) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    
                    // Create new path
                    List<String> newPath = new ArrayList<>(path);
                    newPath.add(neighbor);
                    
                    if (neighbor.equals(endId)) {
                        return newPath;  // Found target
                    }
                    
                    queue.add(new PathNode(neighbor, newPath));
                }
            }
        }
        
        return null;  // No path found
    }
    
    /**
     * Get a branch by ID.
     * 
     * Time Complexity: O(1)
     * 
     * @param branchId Branch identifier
     * @return Branch object
     * @throws NoSuchElementException if branch not found
     */
    public Branch getBranch(String branchId) {
        Branch branch = branches.get(branchId);
        if (branch == null) {
            throw new NoSuchElementException("Branch '" + branchId + "' not found");
        }
        return branch;
    }
    
    /**
     * Get list of all branches.
     * 
     * Time Complexity: O(V)
     * 
     * @return Collection of all branches
     */
    public Collection<Branch> listBranches() {
        return branches.values();
    }
    
    /**
     * Private helper class for BFS path tracking.
     */
    private static class PathNode {
        String node;
        List<String> path;
        
        PathNode(String node, List<String> path) {
            this.node = node;
            this.path = path;
        }
    }
    
    @Override
    public String toString() {
        return String.format("BranchManager(%d branches, %d connections)",
                           branches.size(), 
                           graph.values().stream().mapToInt(List::size).sum() / 2);
    }
}