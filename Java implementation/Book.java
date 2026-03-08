// Book.java - Book model for Java implementation

/**
 * Book class represents a book in the library inventory.
 * 
 * Time Complexity:
 * - Construction: O(1)
 * - decrease/increase quantity: O(1)
 * - is_available: O(1)
 */
public class Book {
    private String bookId;      // ISBN
    private String title;
    private String author;
    private int year;
    private int quantity;
    
    /**
     * Constructor for Book
     * 
     * @param bookId Unique book identifier (ISBN)
     * @param title Book title
     * @param author Book author
     * @param year Publication year
     * @param quantity Available quantity
     */
    public Book(String bookId, String title, String author, int year, int quantity) {
        if (quantity < 0) {
            throw new IllegalArgumentException("Quantity cannot be negative");
        }
        if (year < 0 || year > 2100) {
            throw new IllegalArgumentException("Invalid publication year");
        }
        
        this.bookId = bookId;
        this.title = title;
        this.author = author;
        this.year = year;
        this.quantity = quantity;
    }
    
    // Getters
    public String getBookId() { return bookId; }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public int getYear() { return year; }
    public int getQuantity() { return quantity; }
    
    /**
     * Decrease book quantity.
     * 
     * Time Complexity: O(1)
     * 
     * @param amount Amount to decrease
     * @return true if successful, false if insufficient quantity
     */
    public boolean decreaseQuantity(int amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        if (quantity >= amount) {
            quantity -= amount;
            return true;
        }
        return false;
    }
    
    /**
     * Increase book quantity.
     * 
     * Time Complexity: O(1)
     * 
     * @param amount Amount to increase
     */
    public void increaseQuantity(int amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        quantity += amount;
    }
    
    /**
     * Check if book is available for borrowing.
     * 
     * Time Complexity: O(1)
     * 
     * @return true if quantity > 0
     */
    public boolean isAvailable() {
        return quantity > 0;
    }
    
    @Override
    public String toString() {
        return String.format("%s by %s (%d) - Qty: %d", 
                           title, author, year, quantity);
    }
}