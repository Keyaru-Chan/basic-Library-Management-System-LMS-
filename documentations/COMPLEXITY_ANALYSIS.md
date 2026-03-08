# Complexity Analysis Document

## Overview
This document provides detailed asymptotic analysis of all operations in the Library Management System using Big-O notation.

---

## 1. Graph Operations (Branch Network)

### Operation: Add Branch
```
add_branch(branch_id, name, location)

Data Structure: Dictionary (Adjacency List)
Operation: Insert key-value pair in graph dictionary

Time Complexity: O(1) - average case
    Dictionary insertion is O(1) on average
    
Space Complexity: O(1)
    Only one entry added for new branch
```

### Operation: Connect Branches
```
connect_branches(branch_id1, branch_id2)

Data Structure: Adjacency List (Dictionary)
Operation: Append to neighbor lists (undirected edge)

Time Complexity: O(1) - average case
    List append is O(1) amortized
    
Space Complexity: O(1)
    Only two entries added to adjacency lists
```

### Operation: Find Shortest Path (BFS)
```
find_shortest_path(start_id, end_id)

Data Structure: Queue (deque) + Set + Dictionary
Algorithm: Breadth First Search

Time Complexity: O(V + E)
    V = number of branches (vertices)
    E = number of connections (edges)
    
    Each vertex visited once: V iterations
    Each edge processed once: E operations
    Queue operations (push/pop): O(1) each
    Total: O(V + E)
    
Space Complexity: O(V)
    Queue can contain at most V nodes
    Visited set stores at most V nodes
    Path list stores at most V nodes
    
Example:
    5 branches, 6 connections
    Worst case: Visit all 5 branches = O(5 + 6) = O(11)
```

### Operation: List All Branches
```
list_branches()

Data Structure: Dictionary
Operation: Get all values

Time Complexity: O(V)
    V = number of branches
    Iterate through all branches once
    
Space Complexity: O(V)
    Return list contains V elements
```

---

## 2. Hash Map Operations (Books & Members)

### Operation: Add Book
```
add_book(branch_id, book_id, title, author, year, quantity)

Data Structure: Nested HashMap
    branch_books[branch_id][book_id] = Book

Time Complexity: O(1) - average case
    Hash function computation: O(1)
    Dictionary insertion: O(1) average
    Book object creation: O(1)
    
Space Complexity: O(1)
    Single new entry in nested dictionary
```

### Operation: Get Book (Lookup)
```
get_book(branch_id, book_id)

Data Structure: Nested HashMap
Operation: Two consecutive dictionary lookups

Time Complexity: O(1) - average case
    First lookup (branch): O(1)
    Second lookup (book): O(1)
    Total: O(1)
    
Space Complexity: O(1)
    No additional space needed

Worst Case: O(n)
    If hash collisions occur, lookup can degrade
    Linear probing used in case of collision
    n = number of items in hash table
```

### Operation: Update Book Quantity
```
update_book_quantity(branch_id, book_id, new_quantity)

Data Structure: Nested HashMap
Operation: Lookup + modification

Time Complexity: O(1) - average case
    Get operation: O(1)
    Modification: O(1)
    
Space Complexity: O(1)
    No additional space allocated
```

### Operation: Delete Book
```
delete_book(branch_id, book_id)

Data Structure: Nested HashMap
Operation: Dictionary deletion

Time Complexity: O(1) - average case
    Lookup: O(1)
    Deletion: O(1)
    
Space Complexity: O(1)
    Memory freed, not allocated
```

### Operation: Search Book by Title
```
search_book(title)

Data Structure: Nested HashMap (linear search)
Operation: Full table scan

Time Complexity: O(n)
    n = total number of books across all branches
    Must check each book's title
    
Space Complexity: O(1)
    Only comparison variables, no significant extra space
    
Optimization Possible: O(log n) with index
    Create separate title → book mapping
    Trade-off: Extra O(n) space for O(log n) search
```

### Operation: Add Member
```
add_member(member_id, name, nrc, phone, address)

Data Structure: HashMap
    members[member_id] = Member

Time Complexity: O(1) - average case
    Hash computation: O(1)
    Dictionary insertion: O(1)
    Member object creation: O(1)
    
Space Complexity: O(1)
    Single new entry
```

### Operation: Get Member (Lookup)
```
get_member(member_id)

Data Structure: HashMap
Operation: Dictionary lookup

Time Complexity: O(1) - average case
    Hash computation: O(1)
    Lookup: O(1) with good hash function
    
Worst Case: O(n)
    n = number of members
    Poor hash function causing collisions
```

### Operation: Search Member by NRC
```
search_member_by_nrc(nrc)

Data Structure: HashMap (linear search)
Operation: Full table scan

Time Complexity: O(m)
    m = number of members
    Must check each member's NRC
    
Space Complexity: O(1)
    Only comparison variables

Optimization: Create secondary index
    nrc_map[nrc] = member_id
    Search time becomes O(1)
    Space penalty: O(m) for index
```

### Operation: List Members
```
list_members()

Data Structure: HashMap
Operation: Get all values

Time Complexity: O(m)
    m = number of members
    Iterate through all members
    
Space Complexity: O(m)
    Return list contains m elements
```

---

## 3. Queue Operations (Waitlists)

### Operation: Enqueue (Add to Waitlist)
```
waitlist[book_id].append(member_id)

Data Structure: Collections.deque
Operation: Append to end

Time Complexity: O(1) amortized
    Deque append is O(1) amortized
    Python uses circular buffer
    
Space Complexity: O(1)
    Single element added
```

### Operation: Dequeue (Remove from Waitlist)
```
waitlist[book_id].popleft()

Data Structure: Collections.deque
Operation: Remove from front

Time Complexity: O(1) amortized
    Deque popleft is O(1) amortized
    
Space Complexity: O(1)
    Memory freed
```

### Operation: Check Queue Length
```
len(waitlist[book_id])

Data Structure: Collections.deque
Operation: Get length

Time Complexity: O(1)
    Deque maintains length counter
    
Space Complexity: O(1)
```

---

## 4. List Operations (Borrow History)

### Operation: Append Record
```
borrow_history.append(record)

Data Structure: Python List
Operation: Append to end

Time Complexity: O(1) amortized
    List uses dynamic array
    Amortized cost O(1) due to geometric growth
    
Space Complexity: O(1)
    Single record added
```

### Operation: Iterate Records
```
for record in borrow_history:

Data Structure: Python List
Operation: Linear iteration

Time Complexity: O(h)
    h = number of historical records
    Visit each record once
    
Space Complexity: O(1)
    No additional space (excluding record objects)
```

### Operation: Find Overdue Books
```
get_overdue_books()

Data Structure: List + filtering
Operation: Linear search with condition

Time Complexity: O(h)
    h = total borrow records
    Must check each record's due date
    Date comparison: O(1)
    
Space Complexity: O(o)
    o = number of overdue books
    Return list stores overdue records
```

---

## 5. Sorting Operations

### Insertion Sort
```
insertion_sort(books, key=lambda book: book.title)

Pseudo-code:
    for i from 1 to n:
        for j from i-1 down to 0:
            if arr[j] > arr[i]:
                shift arr[j]
        insert arr[i]

Best Case: O(n)
    Input is already sorted
    Inner loop never executes
    Only n-1 comparisons
    
Average Case: O(n²)
    Random input
    ~n²/4 comparisons
    
Worst Case: O(n²)
    Input is reverse sorted
    n²/2 comparisons needed
    
Space Complexity: O(1)
    In-place sorting
    Only temporary variables
    
Example (n=5):
    Comparisons: 1, 2, 3, 4, ... = 1+2+3+4 = O(n²)
```

### Quick Sort
```
quick_sort(books, key=lambda book: book.title)

Pseudo-code:
    function partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j from low to high-1:
            if arr[j] <= pivot:
                swap(arr[i], arr[j])
                i++
        swap(arr[i+1], arr[high])
        return i+1
    
    function sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            sort(arr, low, pi-1)
            sort(arr, pi+1, high)

Best Case: O(n log n)
    Perfect pivot selection
    Array divided into equal halves
    log n levels of recursion
    n operations each level
    T(n) = 2T(n/2) + n = O(n log n)
    
Average Case: O(n log n)
    Random pivot selection
    Usually produces balanced partitions
    Empirically n log n
    
Worst Case: O(n²)
    Poor pivot selection (always smallest/largest)
    Similar to insertion sort
    Example: already sorted array, pivot at end
    Becomes: T(n) = T(n-1) + n = O(n²)
    
Space Complexity: O(log n)
    Recursion stack depth
    In-place partitioning used
    
Real-world Performance:
    Cache-friendly algorithm
    Often faster than Merge Sort in practice
    Python uses Timsort (hybrid) as default
```

### Merge Sort
```
merge_sort(books, key=lambda book: book.title)

Pseudo-code:
    function merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i++
            else:
                result.append(right[j])
                j++
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    function sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = sort(arr[:mid])
        right = sort(arr[mid:])
        return merge(left, right)

Best Case: O(n log n)
    Always divides in half
    Merge is always O(n)
    log n levels
    
Average Case: O(n log n)
    Same division strategy
    Consistent performance
    
Worst Case: O(n log n)
    Guaranteed! No pathological cases
    Always O(n log n) regardless of input
    
Space Complexity: O(n)
    Temporary arrays in merge
    Must store extra n elements
    Not in-place
    
Stability: Yes
    Equal elements maintain relative order
    
Trade-off Summary:
    + Guaranteed O(n log n)
    + Stable sorting
    - Requires O(n) extra space
    - Slower than Quick Sort in practice (more memory access)
```

---

## 6. Borrowing Operations

### Operation: Borrow Book
```
borrow_book(member_id, book_id)

Steps:
    1. Validate member exists: O(1) [HashMap lookup]
    2. Find book across branches: O(b) [b = branches, worst case O(b * k) if k books per branch]
    3. Check availability: O(1) [attribute access]
    4. If available:
        - Decrease quantity: O(1)
        - Add to member's borrowed list: O(1)
        - Record in history: O(1)
    5. If unavailable:
        - Add to waitlist queue: O(1)

Time Complexity: O(b) in worst case
    b = number of branches
    Search across all branches for book
    
Complete breakdown:
    Best case O(1): Book found in first branch checked
    Average case O(b/2): Book found at mid-point
    Worst case O(b): Book found in last or no branch
    
Space Complexity: O(1)
    Single new record/entry

Optimization Possible:
    Create global book index
    book_location[book_id] = branch_id
    Lookup becomes O(1)
    Trade-off: Extra O(total_books) space
```

### Operation: Return Book
```
return_book(member_id, book_id)

Steps:
    1. Validate member: O(1)
    2. Check member has book: O(k) [k = books borrowed by member, typically small]
    3. Find book location: O(b)
    4. Calculate fine: O(1)
    5. Update member's list: O(1)
    6. Increase quantity: O(1)
    7. Process waitlist: O(1) per element
    8. Process next member if waiting: recursive call to borrow_book()

Time Complexity: O(b + w)
    b = branches
    w = people waiting (for queue processing)
    
Space Complexity: O(1)
    No significant new allocations

Note: Recursive processing of waitlist could cause O(n) in pathological cases
      Solution: Implement iterative queue processing
```

### Operation: Calculate Fine
```
calculate_fine(borrow_date, due_date, return_date)

Steps:
    1. Parse dates: O(1)
    2. Calculate days overdue: O(1) [date difference]
    3. Apply grace period: O(1)
    4. Multiply by rate: O(1)

Time Complexity: O(1)
    Constant number of operations
    
Space Complexity: O(1)
    Only temporary variables
```

---

## 7. Report Generation

### Report: Borrowed Books
```
generate_borrowed_books_report()

Steps:
    1. Iterate all members: O(m) [m = members]
    2. For each member, iterate their borrowed books: O(k) [k = avg books/member]
    3. Create report entry: O(1)

Time Complexity: O(m + b)
    m = number of members
    b = total borrowed items
    
Space Complexity: O(b)
    Report contains b entries
```

### Report: Overdue Books
```
generate_overdue_report()

Steps:
    1. Iterate all borrow records: O(h) [h = total records]
    2. Check if overdue: O(1) [date comparison]
    3. Add to report if overdue: O(1)

Time Complexity: O(h)
    h = total historical records
    
Space Complexity: O(o)
    o = number of overdue books
```

### Report: Fine Report
```
generate_fine_report()

Steps:
    1. Iterate all members: O(m)
    2. Check if has fine: O(1)
    3. Add to report: O(1)

Time Complexity: O(m)
    m = number of members
    
Space Complexity: O(f)
    f = members with fines
```

### Report: System Statistics
```
get_system_statistics()

Calls multiple report generators
Total Complexity:
    Borrowed books: O(m + b)
    Overdue books: O(h)
    Fine report: O(m)
    Sum fines: O(f)

Total: O(m + b + h + f)
    Dominated by O(m + h) typically

Space Complexity: O(b + o + f)
    All report results stored
```

---

## 8. Complete System Complexity Summary

### Data Structure Sizes
- V = branches
- E = connections between branches
- B = total books across all branches
- M = members
- H = borrow history records
- W = people waiting (all queues combined)

### Key Operations

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Add Branch | O(1) | O(1) | HashMap insert |
| Connect Branches | O(1) | O(1) | List append |
| Shortest Path | O(V+E) | O(V) | BFS algorithm |
| Add Book | O(1) | O(1) | HashMap insert |
| Get Book | O(1) | O(1) | HashMap lookup |
| Search Book by Title | O(B) | O(1) | Linear search |
| Add Member | O(1) | O(1) | HashMap insert |
| Get Member | O(1) | O(1) | HashMap lookup |
| Borrow Book | O(V) | O(1) | Search + queue |
| Return Book | O(V+W) | O(1) | Search + process |
| Calculate Fine | O(1) | O(1) | Date arithmetic |
| Sort Books | O(n log n) | O(n) | Merge sort |
| Generate Report | O(M+H) | O(H) | Full scan |

### Overall System Space
```
Total Space = O(V + E + B + M + H + W)

Approximation for typical library:
- V: 5-20 branches
- B: 1000-10000 books
- M: 100-1000 members
- H: growth proportional to usage
- W: typically < 100

Typical: O(B + M + H) dominant
```

---

## 9. Asymptotic Analysis Notation

### Big-O (Worst Case)
```
Definition: f(n) = O(g(n)) means
           ∃ c > 0, n₀ > 0 : f(n) ≤ c·g(n) for all n ≥ n₀

Example: HashMap lookup is O(1)
        Linear search is O(n)
        BFS is O(V + E)
```

### Big-Θ (Average Case)
```
Definition: f(n) = Θ(g(n)) means
           ∃ c₁, c₂ > 0, n₀ > 0 :
           c₁·g(n) ≤ f(n) ≤ c₂·g(n) for all n ≥ n₀

Example: Quick Sort average is Θ(n log n)
```

### Big-Ω (Best Case)
```
Definition: f(n) = Ω(g(n)) means
           ∃ c > 0, n₀ > 0 : f(n) ≥ c·g(n) for all n ≥ n₀

Example: Insertion Sort best is Ω(n)
```

---

## 10. Practical Implications

### For Small Data (< 100 items)
- Insertion Sort preferred (simple, low overhead)
- Linear search acceptable
- Arrays vs HashMaps: not significant

### For Medium Data (100-10000 items)
- Merge/Quick Sort preferred
- Hash Maps for lookups
- BFS for graph algorithms

### For Large Data (> 10000 items)
- Hash Maps essential for lookups
- Guaranteed O(n log n) algorithms needed
- Consider external sorting for persistence
- Index structures recommended

### Trade-offs in This System
1. **Hash Maps vs Arrays**: Choose Hash Map (O(1) > O(n))
2. **Merge vs Quick Sort**: Choose Merge (guaranteed O(n log n))
3. **Direct Lookup vs Search**: Hash Map when possible

---

## Conclusion

The Library Management System demonstrates efficient use of data structures and algorithms achieving optimal complexity for common operations:
- O(1) for single item operations
- O(V+E) for graph traversal
- O(n log n) for sorting
- O(n) for aggregation/reporting

This provides responsive user experience even with growing data volumes.
