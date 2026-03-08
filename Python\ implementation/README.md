# Library Management System (LMS)

A multi-branch library management system implemented in Python 3.11+ using clean modular architecture and efficient data structures.

## Features

- **Branch Management**: Network of library branches with shortest path calculations
- **Book Inventory**: Efficient book storage and search using hash maps
- **Member Management**: Fast member lookup and management
- **Borrow/Return System**: Queue-based handling of multiple borrow requests
- **Reporting**: Comprehensive reports on borrowed books, overdue items, and fines

## Data Structures Used

- **Graph (Adjacency List)**: For branch network and shortest path calculations using BFS
- **Hash Maps**: For O(1) book and member lookups
- **Queues**: For handling borrow requests when books are unavailable
- **Arrays/Lists**: For borrow history and sequential operations

## Algorithms Implemented

- **Breadth First Search (BFS)**: For shortest path between branches and book search
- **Sorting Algorithms**: Insertion Sort, Quick Sort, Merge Sort for book organization
- **Queue Operations**: FIFO for borrow request management

## Architecture

```
                    LibrarySystem
                         |
        ---------------------------------------
        |         |          |          |
  BranchMgr   BookMgr    MemberMgr   BorrowMgr
        |                     |
      Graph               HashMap
        |
   BFS Shortest Path
```

## Project Structure

```
library_lms/
├── README.md
├── main.py
├── models/
│   ├── book.py
│   ├── member.py
│   └── branch.py
├── managers/
│   ├── branch_manager.py
│   ├── book_manager.py
│   ├── member_manager.py
│   ├── borrow_manager.py
│   └── report_manager.py
├── algorithms/
│   ├── bfs_search.py
│   └── sorting.py
├── utils/
│   ├── errors.py
│   └── fine_calculator.py
└── tests/
    └── test_library.py
```

## Complexity Analysis

| Operation | Data Structure | Time Complexity |
|-----------|----------------|-----------------|
| Book Search | Hash Map | O(1) |
| Member Lookup | Hash Map | O(1) |
| Shortest Path | BFS | O(V + E) |
| Book Sorting | Merge Sort | O(n log n) |
| Queue Operations | Deque | O(1) |

## Installation

1. Ensure Python 3.11+ is installed
2. Clone the repository
3. Run the main application:

```bash
python main.py
```

## Usage

The system provides a command-line interface for:

1. Adding and managing library branches
2. Managing book inventory across branches
3. Registering and managing library members
4. Processing book borrow and return requests
5. Generating reports on system status

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## License

This project is for educational purposes as part of a Data Structures and Algorithms assignment.