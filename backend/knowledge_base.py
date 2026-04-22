# backend/knowledge_base.py
# Hardcoded ground truth for CS concepts.
# This is the single source of truth the verification engine checks claims against.

KNOWLEDGE_BASE = {
    "array": {
        "definition": "Contiguous memory block storing fixed-size elements of same type, accessed by index.",
        "constraints": [
            "Fixed size after allocation",
            "Uniform element type and size",
            "Zero-based contiguous indexing"
        ],
        "time_complexity": "Access O(1), Insert/Delete O(n)",
        "space_complexity": "O(n)",
        "properties": [
            "Constant-time random access",
            "Cache-friendly locality",
            "No built-in bounds checking"
        ],
        "operations": {
            "access": "O(1)",
            "insert": "O(n)",
            "delete": "O(n)",
            "search": "O(n)"
        },
        "common_misconceptions": [
            "Dynamic sizing (requires ArrayList)",
            "Indices start at 1",
            "O(1) deletion"
        ],
        "notes": "Static arrays trade flexibility for performance.",
        "source": {
            "name": "MIT 6.006 Introduction to Algorithms",
            "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
        }
    },

    "linked_list": {
        "definition": "Sequence of nodes where each contains data and pointer to next node.",
        "constraints": [
            "Sequential access only",
            "Extra space for pointers",
            "Head pointer required for access"
        ],
        "time_complexity": "Access O(n), Insert/Delete at known pos O(1)",
        "space_complexity": "O(n) + pointer overhead",
        "properties": [
            "Dynamic sizing",
            "Efficient targeted modifications",
            "Poor cache performance"
        ],
        "operations": {
            "insert_head": "O(1)",
            "delete_head": "O(1)",
            "access_index": "O(n)",
            "search": "O(n)"
        },
        "common_misconceptions": [
            "O(1) random access",
            "Backward traversal in singly-linked",
            "Always faster than arrays"
        ],
        "notes": "Doubly-linked adds prev pointers.",
        "source": {
            "name": "MIT 6.006 Introduction to Algorithms",
            "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
        }
    },

    "stack": {
        "definition": "Linear data structure following LIFO principle.",
        "constraints": [
            "Last-in element removed first",
            "Single access point (top)",
            "Finite capacity in array impl"
        ],
        "time_complexity": "Push/Pop/Peek O(1)",
        "space_complexity": "O(n)",
        "properties": [
            "Strict LIFO ordering",
            "Simple amortized analysis",
            "Recursion simulation"
        ],
        "operations": {
            "push": "O(1)",
            "pop": "O(1)",
            "peek": "O(1)",
            "is_empty": "O(1)"
        },
        "common_misconceptions": [
            "FIFO structure",
            "Multiple access points",
            "Efficient random access"
        ],
        "notes": "Array or linked-list implementation.",
        "source": {
            "name": "MIT 6.0001 Intro to CS and Programming",
            "url": "https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/"
        }
    },

    "queue": {
        "definition": "Linear data structure following FIFO principle.",
        "constraints": [
            "First-in element removed first",
            "Enqueue rear, dequeue front",
            "Circular buffer prevents shifting"
        ],
        "time_complexity": "Enqueue/Dequeue O(1)",
        "space_complexity": "O(n)",
        "properties": [
            "Strict FIFO ordering",
            "Breadth-first processing",
            "Producer-consumer pattern"
        ],
        "operations": {
            "enqueue": "O(1)",
            "dequeue": "O(1)",
            "front": "O(1)"
        },
        "common_misconceptions": [
            "LIFO structure",
            "O(1) random access",
            "Same as stack"
        ],
        "notes": "Circular queue implementation optimal.",
        "source": {
            "name": "MIT 6.006 Introduction to Algorithms",
            "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
        }
    },

    "hash_table": {
        "definition": "Key-value store using hash function to compute array indices.",
        "constraints": [
            "Good hash distribution required",
            "Collision resolution mandatory",
            "Load factor < 0.7 typically"
        ],
        "time_complexity": "Avg O(1), Worst O(n)",
        "space_complexity": "O(n)",
        "properties": [
            "Fast average lookups",
            "Dynamic resizing",
            "Amortized analysis"
        ],
        "operations": {
            "insert": "O(1) avg",
            "lookup": "O(1) avg",
            "delete": "O(1) avg"
        },
        "common_misconceptions": [
            "Guaranteed O(1)",
            "No collision handling needed",
            "Order-preserving"
        ],
        "notes": "Chaining or open addressing for collisions.",
        "source": {
            "name": "MIT 6.006 Lecture 4: Hashing",
            "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-4-hashing/"
        }
    },

    "binary_search": {
        "definition": "Finds target in sorted array by halving search interval each step.",
        "constraints": [
            "Array must be sorted",
            "Total ordering required",
            "Random access capability"
        ],
        "time_complexity": "O(log n)",
        "space_complexity": "O(1) iterative",
        "properties": [
            "Optimal sorted search",
            "Information theoretic lower bound",
            "Divide-and-conquer"
        ],
        "operations": {
            "search": "O(log n)"
        },
        "common_misconceptions": [
            "Works on unsorted arrays",
            "Linked list compatible",
            "Linear performance"
        ],
        "notes": "Undefined on unsorted input.",
        "source": {
            "name": "MIT 6.006 Introduction to Algorithms",
            "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
        }
    },

    "merge_sort": {
        "definition": "Divide array, recursively sort halves, merge sorted results.",
        "constraints": [
            "Random access for merging",
            "Extra space for temp arrays",
            "Stable sort required"
        ],
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "properties": [
            "Optimal comparison sort",
            "Guaranteed performance",
            "Parallel friendly"
        ],
        "operations": {
            "sort": "O(n log n)"
        },
        "common_misconceptions": [
            "In-place algorithm",
            "Adaptive performance",
            "Unstable sort"
        ],
        "notes": "Master theorem: T(n)=2T(n/2)+O(n).",
        "source": {
            "name": "MIT 6.006 Introduction to Algorithms",
            "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
        }
    },

    "breadth_first_search": {
        "definition": "Graph traversal visiting nodes level-by-level using queue.",
        "constraints": [
            "Unweighted edges only",
            "Queue-based level order",
            "Connected component discovery"
        ],
        "time_complexity": "O(V+E)",
        "space_complexity": "O(V)",
        "properties": [
            "Shortest path in unweighted graphs",
            "Level-order traversal",
            "BFS tree construction"
        ],
        "operations": {
            "traverse": "O(V+E)",
            "shortest_path": "O(V+E)"
        },
        "common_misconceptions": [
            "Works on weighted graphs",
            "Same as DFS",
            "Stack-based algorithm"
        ],
        "notes": "Queue processes current level completely.",
        "source": {
            "name": "MIT 6.006 Introduction to Algorithms",
            "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
        }
    },

    "depth_first_search": {
        "definition": "Graph traversal exploring as far as possible along each branch using stack/recursion.",
        "constraints": [
            "Stack or recursion implementation",
            "Visits deeper nodes first",
            "Cycle detection capability"
        ],
        "time_complexity": "O(V+E)",
        "space_complexity": "O(V)",
        "properties": [
            "Topological sorting",
            "Cycle detection",
            "Connected components"
        ],
        "operations": {
            "traverse": "O(V+E)",
            "topological_sort": "O(V+E)"
        },
        "common_misconceptions": [
            "Shortest path algorithm",
            "Queue-based",
            "Always produces tree"
        ],
        "notes": "Recursion simulates explicit stack.",
        "source": {
            "name": "MIT 6.006 Introduction to Algorithms",
            "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
        }
    },

    "big_o": {
        "definition": "Asymptotic upper bound: f(n) ≤ c⋅g(n) for sufficiently large n.",
        "constraints": [
            "n → ∞ limit",
            "Constant factors hidden",
            "Worst-case focus"
        ],
        "time_complexity": None,
        "space_complexity": None,
        "properties": [
            "Upper bound notation",
            "Transitive relation",
            "Ignores constants"
        ],
        "operations": None,
        "common_misconceptions": [
            "Exact runtime",
            "Includes constants",
            "Tight bound (that's Θ)",
            "Best case analysis"
        ],
        "notes": "f(n) ∈ O(g(n)) if lim f/g ≤ c.",
        "source": {
            "name": "MIT 6.006 Introduction to Algorithms",
            "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
        }
    },

    "recursion": {
        "definition": "Function solving problem by calling itself on smaller inputs.",
        "constraints": [
            "Base case termination",
            "Progress toward base case",
            "Stack depth limit"
        ],
        "time_complexity": "Depends on recurrence",
        "space_complexity": "O(recursion depth)",
        "properties": [
            "Tree recursion natural",
            "Divide-and-conquer",
            "Tail-call optimizable"
        ],
        "operations": {
            "base_case": "O(1)",
            "recursive_call": "T(n) = aT(n/b) + f(n)"
        },
        "common_misconceptions": [
            "Always slower than loops",
            "Unbounded stack usage",
            "Same space as iteration"
        ],
        "notes": "Tail recursion → iteration.",
        "source": {
            "name": "MIT 6.0001 Intro to CS and Programming",
            "url": "https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/"
        }
    }
}

SUPPORTED_TOPICS = list(KNOWLEDGE_BASE.keys())
