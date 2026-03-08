// BookManager.java - Book management with HashMap operations

import java.util.*;
import java.util.stream.Collectors;

/**
 * BookManager manages book inventory across all library branches using HashMap.
 * 
 * Data Structure:
 *   branchBooks[branchId][bookId] = Book
 * 
 * Time Complexities:
 * - Add Book: O(1)
 * - Get Book: O(1)
 * - Search by ID: O(1)
 * - Search by Title: O(n) where n = total books
 * - Sort: O(n log n)
 * - Delete: O(1)
 */
public class BookManager {
    private BranchManager branchManager;
    private Map<String, Map<String, Book>> branchBooks;  // Nested HashMap
    
    /**
     * Constructor - initializes book manager.
     * 
     * @param branchManager Reference to branch manager for validation
     */
    public BookManager(BranchManager branchManager) {
        this.branchManager = branchManager;
        this.branchBooks = new HashMap<>();
    }
    
    /**
     * Add a book to a specific branch.
     * 
     * Time Complexity: O(1)
     * 
     * @param branchId Branch identifier
     * @param book Book object to add
     * @throws IllegalArgumentException if branch doesn't exist or book already exists
     */
    public void addBook(String branchId, Book book) {
        // Validate branch exists
        Branch branch = branchManager.getBranch(branchId);
        
        // Initialize branch books if not exists
        if (!branchBooks.containsKey(branchId)) {
            branchBooks.put(branchId, new HashMap<>());
        }
        
        // Check if book already exists
        Map<String, Book> books = branchBooks.get(branchId);
        if (books.containsKey(book.getBookId())) {
            throw new IllegalArgumentException("Book '" + book.getBookId() + 
                                             "' already exists in branch '" + branchId + "'");
        }
        
        // Add book
        books.put(book.getBookId(), book);
        branch.addBook(book);
    }
    
    /**
     * Get a book from a specific branch.
     * 
     * Time Complexity: O(1)
     * 
     * @param branchId Branch identifier
     * @param bookId Book identifier
     * @return Book object
     * @throws NoSuchElementException if branch or book not found
     */
    public Book getBook(String branchId, String bookId) {
        if (!branchBooks.containsKey(branchId)) {
            throw new NoSuchElementException("Branch '" + branchId + "' has no books");
        }
        
        Book book = branchBooks.get(branchId).get(bookId);
        if (book == null) {
            throw new NoSuchElementException("Book '" + bookId + "' not found in branch '" + branchId + "'");
        }
        return book;
    }
    
    /**
     * Update book quantity in a branch.
     * 
     * Time Complexity: O(1)
     * 
     * @param branchId Branch identifier
     * @param bookId Book identifier
     * @param newQuantity New quantity value
     * @throws NoSuchElementException if branch or book not found
     */
    public void updateBookQuantity(String branchId, String bookId, int newQuantity) {
        if (newQuantity < 0) {
            throw new IllegalArgumentException("Quantity cannot be negative");
        }
        
        Book book = getBook(branchId, bookId);
        // Rather than direct assignment, update through the book object
        int currentQty = book.getQuantity();
        if (newQuantity > currentQty) {
            book.increaseQuantity(newQuantity - currentQty);
        } else if (newQuantity < currentQty) {
            book.decreaseQuantity(currentQty - newQuantity);
        }
    }
    
    /**
     * Delete a book from a branch.
     * 
     * Time Complexity: O(1)
     * 
     * @param branchId Branch identifier
     * @param bookId Book identifier
     * @throws NoSuchElementException if branch or book not found
     */
    public void deleteBook(String branchId, String bookId) {
        if (!branchBooks.containsKey(branchId)) {
            throw new NoSuchElementException("Branch '" + branchId + "' has no books");
        }
        
        if (!branchBooks.get(branchId).containsKey(bookId)) {
            throw new NoSuchElementException("Book '" + bookId + "' not found in branch '" + branchId + "'");
        }
        
        branchBooks.get(branchId).remove(bookId);
        branchManager.getBranch(branchId).removeBook(bookId);
    }
    
    /**
     * Search for a book by title across all branches.
     * 
     * Time Complexity: O(n) where n = total books
     * 
     * @param title Book title to search for
     * @return Pair of (branchId, book) if found, null otherwise
     */
    public Map.Entry<String, Book> searchBook(String title) {
        for (Map.Entry<String, Map<String, Book>> branchEntry : branchBooks.entrySet()) {
            for (Book book : branchEntry.getValue().values()) {
                if (book.getTitle().toLowerCase().contains(title.toLowerCase())) {
                    return new AbstractMap.SimpleEntry<>(branchEntry.getKey(), book);
                }
            }
        }
        return null;
    }
    
    /**
     * List all books in a specific branch.
     * 
     * Time Complexity: O(n) where n = books in branch
     * 
     * @param branchId Branch identifier
     * @return List of books in the branch
     */
    public List<Book> listBooksByBranch(String branchId) {
        if (!branchBooks.containsKey(branchId)) {
            return new ArrayList<>();
        }
        return new ArrayList<>(branchBooks.get(branchId).values());
    }
    
    /**
     * Sort books in a branch by title using Merge Sort.
     * 
     * Time Complexity: O(n log n)
     * Space Complexity: O(n)
     * 
     * @param branchId Branch identifier
     * @return Sorted list of books
     */
    public List<Book> sortBooksByTitle(String branchId) {
        List<Book> books = listBooksByBranch(branchId);
        books.sort(Comparator.comparing(b -> b.getTitle().toLowerCase()));
        return books;
    }
    
    /**
     * Get total number of book titles across all branches.
     * 
     * Time Complexity: O(B) where B = total books
     * 
     * @return Total number of books
     */
    public int getTotalBooks() {
        int total = 0;
        for (Map<String, Book> books : branchBooks.values()) {
            total += books.size();
        }
        return total;
    }
    
    /**
     * Get total quantity of all books across all branches.
     * 
     * Time Complexity: O(B)
     * 
     * @return Total quantity
     */
    public int getTotalQuantity() {
        return branchBooks.values().stream()
                         .flatMap(m -> m.values().stream())
                         .mapToInt(Book::getQuantity)
                         .sum();
    }
    
    @Override
    public String toString() {
        return String.format("BookManager(%d branches, %d books, %d quantity)",
                           branchBooks.size(),
                           getTotalBooks(),
                           getTotalQuantity());
    }
}