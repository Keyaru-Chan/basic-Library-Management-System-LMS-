// Member.java - Member model

import java.util.*;

/**
 * Member class represents a library member.
 * 
 * Maintains member information and tracks borrowed books.
 */
public class Member {
    private String memberId;
    private String name;
    private String nrc;               // National Registration Card
    private String phone;
    private String address;
    private List<BorrowRecord> borrowedBooks;  // Currently borrowed
    private double fineAmount;
    
    /**
     * Inner class for tracking borrowed book records.
     */
    public static class BorrowRecord {
        public String bookId;
        public String bookTitle;
        public String borrowDate;
        public String dueDate;
        
        public BorrowRecord(String bookId, String bookTitle, String borrowDate, String dueDate) {
            this.bookId = bookId;
            this.bookTitle = bookTitle;
            this.borrowDate = borrowDate;
            this.dueDate = dueDate;
        }
    }
    
    /**
     * Constructor for Member.
     * 
     * @param memberId Unique member identifier
     * @param name Member full name
     * @param nrc National Registration Card number
     * @param phone Contact phone number
     * @param address Residential address
     */
    public Member(String memberId, String name, String nrc, String phone, String address) {
        if (nrc == null || nrc.isEmpty()) {
            throw new IllegalArgumentException("NRC cannot be empty");
        }
        
        this.memberId = memberId;
        this.name = name;
        this.nrc = nrc;
        this.phone = phone;
        this.address = address;
        this.borrowedBooks = new ArrayList<>();
        this.fineAmount = 0.0;
    }
    
    // Getters
    public String getMemberId() { return memberId; }
    public String getName() { return name; }
    public String getNrc() { return nrc; }
    public String getPhone() { return phone; }
    public String getAddress() { return address; }
    public List<BorrowRecord> getBorrowedBooks() { return borrowedBooks; }
    public double getFineAmount() { return fineAmount; }
    
    /**
     * Add a borrowed book record.
     * 
     * Time Complexity: O(1)
     * 
     * @param bookId Book identifier
     * @param bookTitle Book title
     * @param borrowDate Borrow date
     * @param dueDate Due date
     */
    public void addBorrowedBook(String bookId, String bookTitle, String borrowDate, String dueDate) {
        borrowedBooks.add(new BorrowRecord(bookId, bookTitle, borrowDate, dueDate));
    }
    
    /**
     * Remove a borrowed book record.
     * 
     * Time Complexity: O(k) where k = number of borrowed books
     * 
     * @param bookId Book identifier to remove
     * @return true if book was removed, false if not found
     */
    public boolean removeBorrowedBook(String bookId) {
        return borrowedBooks.removeIf(record -> record.bookId.equals(bookId));
    }
    
    /**
     * Check if member has borrowed a specific book.
     * 
     * Time Complexity: O(k)
     * 
     * @param bookId Book identifier to check
     * @return true if member has borrowed the book
     */
    public boolean hasBorrowedBook(String bookId) {
        return borrowedBooks.stream().anyMatch(record -> record.bookId.equals(bookId));
    }
    
    /**
     * Get number of books currently borrowed.
     * 
     * Time Complexity: O(1)
     * 
     * @return Number of borrowed books
     */
    public int getBorrowedBookCount() {
        return borrowedBooks.size();
    }
    
    /**
     * Add fine amount to member's account.
     * 
     * Time Complexity: O(1)
     * 
     * @param amount Fine amount to add
     */
    public void addFine(double amount) {
        if (amount > 0) {
            fineAmount += amount;
        }
    }
    
    /**
     * Clear all accumulated fines.
     * 
     * Time Complexity: O(1)
     */
    public void clearFine() {
        fineAmount = 0.0;
    }
    
    @Override
    public String toString() {
        return String.format("%s (ID: %s) - Borrowed: %d books, Fine: %.2f",
                           name, memberId, borrowedBooks.size(), fineAmount);
    }
}