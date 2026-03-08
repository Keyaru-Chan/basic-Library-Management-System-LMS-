// SortingAlgorithms.java - Sorting implementations for Java

import java.util.*;
import java.util.Comparator;

/**
 * SortingAlgorithms class implements three sorting algorithms for demonstration:
 * - Insertion Sort: O(n²) - good for small datasets
 * - Quick Sort: O(n log n) average - fast divide and conquer
 * - Merge Sort: O(n log n) guaranteed - stable sorting
 */
public class SortingAlgorithms {
    
    /**
     * Insertion Sort Algorithm
     * 
     * Best Case: O(n) - already sorted
     * Average Case: O(n²)
     * Worst Case: O(n²) - reverse sorted
     * Space: O(1) - in-place
     * 
     * Good for:
     * - Small datasets (< 50 elements)
     * - Nearly sorted data
     * - Online sorting (elements added one by one)
     * 
     * @param arr List to sort
     * @param comparator Comparator for elements
     * @return New sorted list
     */
    public static <T> List<T> insertionSort(List<T> arr, Comparator<T> comparator) {
        List<T> sorted = new ArrayList<>(arr);
        
        // Start from second element
        for (int i = 1; i < sorted.size(); i++) {
            T key = sorted.get(i);
            
            // Shift larger elements right
            int j = i - 1;
            while (j >= 0 && comparator.compare(sorted.get(j), key) > 0) {
                sorted.set(j + 1, sorted.get(j));
                j--;
            }
            
            // Insert key at correct position
            sorted.set(j + 1, key);
        }
        
        return sorted;
    }
    
    /**
     * Quick Sort Algorithm
     * 
     * Best Case: O(n log n) - balanced partitions
     * Average Case: O(n log n) - random pivot selection
     * Worst Case: O(n²) - pivot always smallest/largest
     * Space: O(log n) - recursion stack
     * 
     * Advantages:
     * - Very fast in practice (cache-friendly)
     * - In-place sorting with minimal extra space
     * - Works well for large datasets
     * 
     * Disadvantages:
     * - Not stable (equal elements may reorder)
     * - O(n²) worst case (rare)
     * 
     * @param arr List to sort
     * @param comparator Comparator for elements
     * @return New sorted list
     */
    public static <T> List<T> quickSort(List<T> arr, Comparator<T> comparator) {
        if (arr.isEmpty() || arr.size() == 1) {
            return new ArrayList<>(arr);
        }
        
        // Use first element as pivot
        T pivot = arr.get(0);
        List<T> less = new ArrayList<>();
        List<T> equal = new ArrayList<>();
        List<T> greater = new ArrayList<>();
        
        // Partition elements
        for (T element : arr) {
            int cmp = comparator.compare(element, pivot);
            if (cmp < 0) {
                less.add(element);
            } else if (cmp == 0) {
                equal.add(element);
            } else {
                greater.add(element);
            }
        }
        
        // Recursively sort and combine
        List<T> sorted = new ArrayList<>();
        sorted.addAll(quickSort(less, comparator));
        sorted.addAll(equal);
        sorted.addAll(quickSort(greater, comparator));
        
        return sorted;
    }
    
    /**
     * Merge Sort Algorithm
     * 
     * Best Case: O(n log n) - always divide in half
     * Average Case: O(n log n)
     * Worst Case: O(n log n) - GUARANTEED!
     * Space: O(n) - requires temporary arrays
     * Stability: YES - maintains relative order of equal elements
     * 
     * Advantages:
     * - Guaranteed O(n log n) performance
     * - Stable sorting
     * - Predictable runtime for production systems
     * - Parallelizable
     * 
     * Disadvantages:
     * - Requires O(n) extra space
     * - Slower than Quick Sort in practice (more memory access)
     * - Not in-place
     * 
     * @param arr List to sort
     * @param comparator Comparator for elements
     * @return New sorted list
     */
    public static <T> List<T> mergeSort(List<T> arr, Comparator<T> comparator) {
        if (arr.size() <= 1) {
            return new ArrayList<>(arr);
        }
        
        // Divide
        int mid = arr.size() / 2;
        List<T> left = mergeSort(new ArrayList<>(arr.subList(0, mid)), comparator);
        List<T> right = mergeSort(new ArrayList<>(arr.subList(mid, arr.size())), comparator);
        
        // Merge
        return merge(left, right, comparator);
    }
    
    /**
     * Helper method to merge two sorted lists.
     * 
     * Time Complexity: O(n) where n = total elements
     * 
     * @param left First sorted list
     * @param right Second sorted list
     * @param comparator Comparator for elements
     * @return Merged sorted list
     */
    private static <T> List<T> merge(List<T> left, List<T> right, Comparator<T> comparator) {
        List<T> result = new ArrayList<>();
        int i = 0, j = 0;
        
        // Merge while both lists have elements
        while (i < left.size() && j < right.size()) {
            if (comparator.compare(left.get(i), right.get(j)) <= 0) {
                result.add(left.get(i));
                i++;
            } else {
                result.add(right.get(j));
                j++;
            }
        }
        
        // Add remaining elements
        result.addAll(left.subList(i, left.size()));
        result.addAll(right.subList(j, right.size()));
        
        return result;
    }
    
    /**
     * Sort books by title using specified algorithm.
     * 
     * @param books List of books to sort
     * @param algorithm "insertion", "quick", or "merge"
     * @return Sorted list of books
     * @throws IllegalArgumentException if algorithm not recognized
     */
    public static List<Book> sortBooksByTitle(List<Book> books, String algorithm) {
        Comparator<Book> comparator = Comparator.comparing(
            b -> b.getTitle().toLowerCase()
        );
        
        switch (algorithm.toLowerCase()) {
            case "insertion":
                return insertionSort(books, comparator);
            case "quick":
                return quickSort(books, comparator);
            case "merge":
                return mergeSort(books, comparator);
            default:
                throw new IllegalArgumentException("Unknown algorithm: " + algorithm);
        }
    }
    
    /**
     * Provides complexity analysis information for sorting algorithms.
     */
    public static class ComplexityAnalysis {
        public static void printAnalysis(String algorithm) {
            switch (algorithm.toLowerCase()) {
                case "insertion":
                    System.out.println("Insertion Sort:");
                    System.out.println("  Best: O(n) - already sorted");
                    System.out.println("  Average: O(n²)");
                    System.out.println("  Worst: O(n²) - reverse sorted");
                    System.out.println("  Space: O(1) - in-place");
                    break;
                case "quick":
                    System.out.println("Quick Sort:");
                    System.out.println("  Best: O(n log n) - balanced partitions");
                    System.out.println("  Average: O(n log n)");
                    System.out.println("  Worst: O(n²) - poor pivot");
                    System.out.println("  Space: O(log n) - recursion");
                    System.out.println("  Stability: No");
                    break;
                case "merge":
                    System.out.println("Merge Sort:");
                    System.out.println("  Best: O(n log n)");
                    System.out.println("  Average: O(n log n)");
                    System.out.println("  Worst: O(n log n) - GUARANTEED!");
                    System.out.println("  Space: O(n) - temporary arrays");
                    System.out.println("  Stability: Yes");
                    break;
                default:
                    System.out.println("Unknown algorithm");
            }
        }
    }
}