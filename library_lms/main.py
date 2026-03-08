#!/usr/bin/env python3
"""
Library Management System (LMS) - Main Entry Point

A multi-branch library management system demonstrating:
- Graph data structures for branch networks
- Hash maps for efficient lookups
- Queue data structures for borrow requests
- BFS algorithms for shortest path calculations
- Sorting algorithms for book organization

Author: Generated for DSA Assignment
"""

from managers.library_system import LibrarySystem


def main():
    """Main application entry point."""
    print("=== Library Management System ===")
    print("Initializing system...")

    # Initialize the library system
    library = LibrarySystem()

    # Demo setup - add some sample data
    setup_demo_data(library)

    # Main menu loop
    while True:
        print("\n=== Main Menu ===")
        print("1. Branch Management")
        print("2. Book Management")
        print("3. Member Management")
        print("4. Borrow/Return Books")
        print("5. Reports")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            branch_menu(library)
        elif choice == "2":
            book_menu(library)
        elif choice == "3":
            member_menu(library)
        elif choice == "4":
            borrow_menu(library)
        elif choice == "5":
            report_menu(library)
        elif choice == "6":
            print("Thank you for using Library Management System!")
            break
        else:
            print("Invalid choice. Please try again.")


def setup_demo_data(library):
    """Set up some demo data for testing."""
    print("Setting up demo data...")

    # Add branches
    library.branch_manager.add_branch("B001", "Central Library", "Downtown")
    library.branch_manager.add_branch("B002", "North Branch", "North District")
    library.branch_manager.add_branch("B003", "South Branch", "South District")

    # Connect branches
    library.branch_manager.connect_branches("B001", "B002")
    library.branch_manager.connect_branches("B002", "B003")
    library.branch_manager.connect_branches("B001", "B003")

    # Add books
    library.book_manager.add_book("B001", "9780131103627", "The C Programming Language",
                                 "Kernighan & Ritchie", 1978, 5)
    library.book_manager.add_book("B002", "9780321127426", "Patterns of Enterprise Application Architecture",
                                 "Martin Fowler", 2002, 3)
    library.book_manager.add_book("B003", "9780596517748", "JavaScript: The Good Parts",
                                 "Douglas Crockford", 2008, 2)

    # Add members
    library.member_manager.add_member("M001", "John Doe", "12/ABC(N)123456", "555-0101", "123 Main St")
    library.member_manager.add_member("M002", "Jane Smith", "12/DEF(N)234567", "555-0102", "456 Oak Ave")

    print("Demo data setup complete!")


def branch_menu(library):
    """Branch management menu."""
    while True:
        print("\n=== Branch Management ===")
        print("1. Add Branch")
        print("2. List Branches")
        print("3. Connect Branches")
        print("4. Find Shortest Path")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            branch_id = input("Enter branch ID: ").strip()
            name = input("Enter branch name: ").strip()
            location = input("Enter location: ").strip()
            try:
                library.branch_manager.add_branch(branch_id, name, location)
                print(f"Branch '{name}' added successfully!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            branches = library.branch_manager.list_branches()
            if branches:
                print("\nBranches:")
                for branch in branches:
                    print(f"- {branch.branch_id}: {branch.name} ({branch.location})")
            else:
                print("No branches found.")

        elif choice == "3":
            from_id = input("Enter source branch ID: ").strip()
            to_id = input("Enter destination branch ID: ").strip()
            try:
                library.branch_manager.connect_branches(from_id, to_id)
                print("Branches connected successfully!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            start_id = input("Enter start branch ID: ").strip()
            end_id = input("Enter end branch ID: ").strip()
            try:
                path = library.branch_manager.find_shortest_path(start_id, end_id)
                if path:
                    print(f"Shortest path: {' -> '.join(path)}")
                else:
                    print("No path found.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def book_menu(library):
    """Book management menu."""
    while True:
        print("\n=== Book Management ===")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Update Book")
        print("4. Delete Book")
        print("5. List Books by Branch")
        print("6. Sort Books")
        print("7. Back to Main Menu")

        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            branch_id = input("Enter branch ID: ").strip()
            book_id = input("Enter book ID (ISBN): ").strip()
            title = input("Enter title: ").strip()
            author = input("Enter author: ").strip()
            try:
                year = int(input("Enter publication year: ").strip())
                quantity = int(input("Enter quantity: ").strip())
                library.book_manager.add_book(branch_id, book_id, title, author, year, quantity)
                print(f"Book '{title}' added successfully!")
            except ValueError:
                print("Invalid year or quantity. Please enter numbers.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            title = input("Enter book title to search: ").strip()
            try:
                result = library.book_manager.search_book(title)
                if result:
                    branch_id, book = result
                    print(f"Found '{book.title}' by {book.author} at branch {branch_id} (Quantity: {book.quantity})")
                else:
                    print("Book not found.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "3":
            branch_id = input("Enter branch ID: ").strip()
            book_id = input("Enter book ID: ").strip()
            try:
                quantity = int(input("Enter new quantity: ").strip())
                library.book_manager.update_book_quantity(branch_id, book_id, quantity)
                print("Book quantity updated successfully!")
            except ValueError:
                print("Invalid quantity. Please enter a number.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            branch_id = input("Enter branch ID: ").strip()
            book_id = input("Enter book ID: ").strip()
            try:
                library.book_manager.delete_book(branch_id, book_id)
                print("Book deleted successfully!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            branch_id = input("Enter branch ID: ").strip()
            try:
                books = library.book_manager.list_books_by_branch(branch_id)
                if books:
                    print(f"\nBooks in branch {branch_id}:")
                    for book in books:
                        print(f"- {book.book_id}: {book.title} by {book.author} (Qty: {book.quantity})")
                else:
                    print("No books found in this branch.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "6":
            branch_id = input("Enter branch ID: ").strip()
            try:
                sorted_books = library.book_manager.sort_books_by_title(branch_id)
                if sorted_books:
                    print(f"\nSorted books in branch {branch_id}:")
                    for book in sorted_books:
                        print(f"- {book.title} by {book.author}")
                else:
                    print("No books found in this branch.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")


def member_menu(library):
    """Member management menu."""
    while True:
        print("\n=== Member Management ===")
        print("1. Add Member")
        print("2. Search Member")
        print("3. List Members")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            member_id = input("Enter member ID: ").strip()
            name = input("Enter name: ").strip()
            nrc = input("Enter NRC: ").strip()
            phone = input("Enter phone: ").strip()
            address = input("Enter address: ").strip()
            try:
                library.member_manager.add_member(member_id, name, nrc, phone, address)
                print(f"Member '{name}' added successfully!")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            member_id = input("Enter member ID: ").strip()
            try:
                member = library.member_manager.get_member(member_id)
                if member:
                    print(f"Member: {member.name}")
                    print(f"NRC: {member.nrc}")
                    print(f"Phone: {member.phone}")
                    print(f"Address: {member.address}")
                    print(f"Borrowed books: {len(member.borrowed_books)}")
                else:
                    print("Member not found.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "3":
            members = library.member_manager.list_members()
            if members:
                print("\nMembers:")
                for member in members:
                    print(f"- {member.member_id}: {member.name}")
            else:
                print("No members found.")

        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


def borrow_menu(library):
    """Borrow/Return menu."""
    while True:
        print("\n=== Borrow/Return Books ===")
        print("1. Borrow Book")
        print("2. Return Book")
        print("3. View Borrow History")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            member_id = input("Enter member ID: ").strip()
            book_id = input("Enter book ID: ").strip()
            try:
                result = library.borrow_manager.borrow_book(member_id, book_id)
                print(result)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            member_id = input("Enter member ID: ").strip()
            book_id = input("Enter book ID: ").strip()
            try:
                result = library.borrow_manager.return_book(member_id, book_id)
                print(result)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "3":
            member_id = input("Enter member ID: ").strip()
            try:
                history = library.borrow_manager.get_borrow_history(member_id)
                if history:
                    print(f"\nBorrow history for member {member_id}:")
                    for record in history:
                        print(f"- {record['book_title']} (Borrowed: {record['borrow_date']}, Due: {record['due_date']})")
                else:
                    print("No borrow history found.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


def report_menu(library):
    """Reports menu."""
    while True:
        print("\n=== Reports ===")
        print("1. Borrowed Books Report")
        print("2. Overdue Books Report")
        print("3. Fine Report")
        print("4. Back to Main Menu")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            report = library.report_manager.generate_borrowed_books_report()
            if report:
                print("\nBorrowed Books Report:")
                for item in report:
                    print(f"- {item['member_name']}: {item['book_title']} (Due: {item['due_date']})")
            else:
                print("No borrowed books found.")

        elif choice == "2":
            report = library.report_manager.generate_overdue_report()
            if report:
                print("\nOverdue Books Report:")
                for item in report:
                    print(f"- {item['member_name']}: {item['book_title']} ({item['days_overdue']} days overdue)")
            else:
                print("No overdue books found.")

        elif choice == "3":
            report = library.report_manager.generate_fine_report()
            if report:
                print("\nFine Report:")
                for item in report:
                    print(f"- {item['member_name']}: {item['total_fine']} MMK")
            else:
                print("No fines found.")

        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()