// Branch.java - Branch model

import java.util.*;

/**
 * Branch class represents a library branch with book inventory.
 * 
 * Inventory is stored as HashMap for O(1) lookup by book ID.
 */
public class Branch {
    private String branchId;
    private String name;
    private String location;
    private Map<String, Book> inventory;  // book_id -> Book (HashMap for O(1) operations)
    
    /**
     * Constructor for Branch.
     * 
     * @param branchId Unique branch identifier
     * @param name Branch name
     * @param location Branch location/address
     */
    public Branch(String branchId, String name, String location) {
        this.branchId = branchId;
        this.name = name;
        this.location = location;
        this.inventory = new HashMap<>();
    }
    
    // Getters
    public String getBranchId() { return branchId; }
    public String getName() { return name; }
    public String getLocation() { return location; }
    public Map<String, Book> getInventory() { return inventory; }
    
    /**
     * Add a book to the branch inventory.
     * 
     * Time Complexity: O(1)
     * 
     * @param book Book to add
     */
    public void addBook(Book book) {
        inventory.put(book.getBookId(), book);
    }
    
    /**
     * Remove a book from the inventory.
     * 
     * Time Complexity: O(1)
     * 
     * @param bookId Book identifier to remove
     * @return true if book was removed, false if not found
     */
    public boolean removeBook(String bookId) {
        return inventory.remove(bookId) != null;
    }
    
    /**
     * Get a book from inventory.
     * 
     * Time Complexity: O(1)
     * 
     * @param bookId Book identifier
     * @return Book object if found
     * @throws NoSuchElementException if book not found
     */
    public Book getBook(String bookId) {
        Book book = inventory.get(bookId);
        if (book == null) {
            throw new NoSuchElementException("Book '" + bookId + "' not found in branch '" + branchId + "'");
        }
        return book;
    }
    
    /**
     * Check if branch has a specific book.
     * 
     * Time Complexity: O(1)
     * 
     * @param bookId Book identifier to check
     * @return true if book exists in inventory
     */
    public boolean hasBook(String bookId) {
        return inventory.containsKey(bookId);
    }
    
    /**
     * Get total number of books in inventory.
     * 
     * Time Complexity: O(1)
     * 
     * @return Total number of unique books
     */
    public int getTotalBooks() {
        return inventory.size();
    }
    
    /**
     * Get total quantity of all books.
     * 
     * Time Complexity: O(n) where n = number of books
     * 
     * @return Total quantity across all books
     */
    public int getTotalQuantity() {
        int total = 0;
        for (Book book : inventory.values()) {
            total += book.getQuantity();
        }
        return total;
    }
    
    /**
     * Get list of all books in inventory.
     * 
     * Time Complexity: O(n)
     * 
     * @return List of books
     */
    public List<Book> listBooks() {
        return new ArrayList<>(inventory.values());
    }
    
    @Override
    public String toString() {
        return String.format("%s (%s) - %d books", name, location, inventory.size());
    }
}