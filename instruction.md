
# Technical Implementation Guide

## Library Management System (LMS)

### Data Structures and Algorithms Assignment

---

# 1. System Overview

The system is a **multi-branch library management system** that manages:

1. Branch Management
2. Book Inventory
3. Member Management
4. Borrow/Return Management
5. Reporting

Constraints from assignment:

* **No database**
* **No UI**
* **In-memory data structures only**
* Must demonstrate **algorithms + ADT usage**
* Must include **complexity analysis**

The system will be implemented using **Python 3.11+** with **clean modular architecture**.

---

# 2. High Level Architecture

```
                +----------------------+
                |  LibrarySystem       |
                |  (Main Controller)   |
                +----------+-----------+
                           |
        -------------------------------------------
        |          |            |          |       |
   BranchManager  BookManager  MemberMgr  BorrowMgr ReportMgr
        |             |            |          |
        |             |            |          |
      Graph        HashMap      HashMap      Queue
   (branches)      (books)      (members)  (requests)
```

---

# 3. Data Structure Selection (Very Important for Assignment)

### 3.1 Branch Management

We must also calculate **shortest route between branches**.

Best structure:

```
Graph (Adjacency List)
```

Reason:

Libraries form a **network of locations**.

Example

```
Branch A --- Branch B
   |             |
Branch C --- Branch D
```

Adjacency list structure:

```
{
 A: [B,C],
 B: [A,D],
 C: [A,D],
 D: [B,C]
}
```

Why adjacency list?

| Reason             | Explanation              |
| ------------------ | ------------------------ |
| Memory efficiency  | O(V + E)                 |
| Faster traversal   | BFS / DFS                |
| Easy shortest path | BFS for unweighted graph |

Algorithm used:

```
Breadth First Search (BFS)
```

Time complexity:

```
O(V + E)
```

---

### 3.2 Book Inventory

Books must support:

* add
* delete
* update
* search
* sort
* quantity tracking

Best structure:

```
Hash Map (Dictionary)
```

Example:

```
books = {
  "9780131103627": BookObject
}
```

Why Hash Map?

| Reason | Complexity |
| ------ | ---------- |
| search | O(1)       |
| update | O(1)       |
| delete | O(1)       |

Books stored per branch:

```
branch_books = {
   branch_id : { book_id : Book }
}
```

---

### 3.3 Member Management

Members searched by:

* NRC_ID
* Passport
* Member ID

Structure:

```
Hash Map
```

Example:

```
members = {
  member_id : MemberObject
}
```

Why?

Fast lookup when borrowing books.

Complexity:

```
Search = O(1)
```

---

### 3.4 Borrow Queue (Handling multiple requests)

Scenario:

```
Book quantity = 1
Member A requests
Member B requests
```

Structure:

```
Queue
```

Example

```
waitlist = deque()
```

Reason:

First come first serve.

Complexity

```
enqueue O(1)
dequeue O(1)
```

---

### 3.5 Borrow History

Structure:

```
Array List (Python List)
```

Why?

Sequential record storage.

Example

```
borrow_history = []
```

---

# 4. Core Data Models

## Branch

```python
class Branch:
    def __init__(self, branch_id, name, location):
        self.branch_id = branch_id
        self.name = name
        self.location = location
        self.inventory = {}
```

---

## Book

```python
class Book:
    def __init__(self, book_id, title, author, year, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.quantity = quantity
```

---

## Member

```python
class Member:
    def __init__(self, member_id, name, nrc, phone, address):
        self.member_id = member_id
        self.name = name
        self.nrc = nrc
        self.phone = phone
        self.address = address
        self.borrowed_books = []
```

---

# 5. Algorithms Design

---

# 5.1 Search Book Algorithm

Use **DFS or BFS**

Example BFS search across branches.

Pseudo code:

```
function search_book(title):

 queue = all_branches

 while queue not empty:

     branch = queue.pop()

     if book exists in branch:
         return branch

 return NOT_FOUND
```

Complexity

```
O(V + E)
```

---

# 5.2 Shortest Route for Book Transfer

Use **BFS**

Pseudo code

```
function shortest_path(start, target):

 queue = [(start, path)]

 while queue not empty:

   node, path = queue.pop()

   if node == target:
       return path

   for neighbor in graph[node]:
        add to queue
```

Complexity

```
O(V + E)
```

---

# 5.3 Sorting Books

Algorithms required in assignment.

Use:

```
Insertion Sort
Quick Sort
Merge Sort
```

---

### Insertion Sort

Good for small datasets.

Complexity:

| Case    | Complexity |
| ------- | ---------- |
| Best    | O(n)       |
| Average | O(n²)      |
| Worst   | O(n²)      |

Pseudo code:

```
for i from 1 to n:
   key = A[i]
   j = i-1

   while j >= 0 and A[j] > key:
        shift A[j]
        j--

   insert key
```

---

### Quick Sort

Divide and conquer.

Average

```
O(n log n)
```

Worst

```
O(n²)
```

---

### Merge Sort

Stable sorting algorithm.

Complexity

```
O(n log n)
```

Space

```
O(n)
```

---

# 6. Borrowing Algorithm

Pseudo code

```
function borrow(member_id, book_id):

  member = find_member()

  branch = find_book_branch()

  if book.quantity == 0:
        add to waitlist
        return "added to queue"

  decrease quantity

  record borrow_date

  due_date = today + 14 days
```

---

# 7. Return Algorithm

```
function return_book(member, book):

 increase book quantity

 remove from borrowed list

 if waitlist not empty:
      next_member gets book
```

---

# 8. Overdue Fine Calculation

Example rule

```
fine_per_day = 500 MMK
```

Algorithm

```
days_overdue = return_date - due_date

fine = days_overdue * daily_rate
```

Example

```
3 days overdue

fine = 3 * 500 = 1500 MMK
```

---

# 9. Error Handling

Examples:

### Book not found

```
raise BookNotFoundError
```

### Member not found

```
raise MemberNotFoundError
```

### No stock

```
raise BookUnavailableError
```

### Duplicate member

```
raise DuplicateMemberError
```

---

# 10. Handling Multiple Borrow Requests

Case

```
Book stock = 1

Member A borrows
Member B requests
```

System behavior

```
Member B added to queue
```

Queue structure

```
waitlist = [MemberB, MemberC]
```

---

# 11. Reporting System

Reports required:

### Borrowed books

```
for member in members:
   show borrowed books
```

Complexity

```
O(n)
```

---

### Overdue Books

```
if today > due_date
```

---

### Fine Report

```
sum(member.fines)
```

---

# 12. Complexity Evaluation (Task 2)

### Asymptotic Analysis

Used to measure algorithm performance when **input size increases**.

Three main notations:

```
Big O     -> Worst case
Omega     -> Best case
Theta     -> Average case
```

Example

Searching in:

Array

```
O(n)
```

Hash table

```
O(1)
```

---

# 13. Two Ways to Measure Efficiency

### 1. Time Complexity

How fast algorithm runs.

Example

```
Merge Sort = O(n log n)
```

---

### 2. Space Complexity

Memory usage.

Example

```
Merge Sort = O(n)
```

---

# 14. Trade-off in ADT

Example:

Hash table vs Array

| Structure | Advantage   | Disadvantage |
| --------- | ----------- | ------------ |
| HashMap   | fast search | more memory  |
| Array     | simple      | slow search  |

Tradeoff:

```
Speed vs Memory
```

---

# 15. Benefits of Implementation Independent Data Structures

Example ADT:

```
Stack
Queue
Graph
```

Benefits:

### 1. Flexibility

ADT can use different internal structures.

Example

```
Queue → Array or Linked List
```

---

### 2. Maintainability

Implementation can change without affecting system.

---

### 3. Reusability

Same ADT usable in multiple systems.

---

# 16. Flowchart (Borrow Process)

```
Member Request
      |
Check Book
      |
Stock Available?
   /        \
 Yes        No
  |          |
Borrow    Add to Queue
  |
Set Due Date
```

---

# 17. Example Project Structure

```
library_lms/

README.md
main.py

models/
    book.py
    member.py
    branch.py

managers/
    branch_manager.py
    book_manager.py
    member_manager.py
    borrow_manager.py
    report_manager.py

algorithms/
    bfs_search.py
    sorting.py

utils/
    errors.py
    fine_calculator.py

tests/
    test_library.py
```

---

# 18. README Architecture Diagram

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

---

# 19. Testing Plan

Test cases:

| Case                  | Expected        |
| --------------------- | --------------- |
| borrow book available | success         |
| borrow book no stock  | queue           |
| return book           | stock increase  |
| overdue book          | fine calculated |
| search book           | correct branch  |

---

# 20. Demo Plan (for Presentation)

Show step by step:

1. Add branches
2. Add books
3. Add members
4. Borrow book
5. Borrow same book again
6. Show queue
7. Return book
8. Next member gets book
9. Show overdue fine

---

If you want, I can also show you **how to make this assignment look like a “distinction / world-class” submission** by adding:

* **system design diagrams**
* **proper algorithm flowcharts**
* **Big-O comparison tables**
* **clean Python implementation (~700 lines)**
* **professional README like a real GitHub project**

That would make your assignment look **far above normal HND level**.
