# backend/knowledge_base.py
# Hardcoded ground truth for CS concepts.
# This is the single source of truth the verification engine checks claims against.

KNOWLEDGE_BASE = {
    "binary_search": {
        "definition": (
            "Binary search is an algorithm that finds a target value in a sorted array "
            "by repeatedly halving the search space."
        ),
        "constraints": [
            "The array must be sorted before applying binary search.",
            "Requires random access to elements (e.g., arrays, not linked lists).",
            "Works on one-dimensional data with a defined order.",
        ],
        "time_complexity": "O(log n) average and worst case",
        "space_complexity": "O(1) iterative, O(log n) recursive",
        "notes": (
            "Binary search does NOT work on unsorted arrays. "
            "It does NOT work on linked lists due to lack of random access."
        ),
    },

    "stack": {
        "definition": (
            "A stack is a linear data structure that follows the "
            "Last-In First-Out (LIFO) principle."
        ),
        "ordering": "LIFO — Last In, First Out",
        "operations": {
            "push": "Add an element to the top. O(1).",
            "pop": "Remove the top element. O(1).",
            "peek": "View the top element without removing it. O(1).",
        },
        "use_cases": [
            "Function call management (call stack)",
            "Undo/redo operations",
            "Expression parsing and evaluation",
            "Depth-first search",
        ],
        "notes": (
            "A stack is NOT FIFO. FIFO describes a queue, not a stack. "
            "Stacks operate strictly LIFO."
        ),
    },

    "queue": {
        "definition": (
            "A queue is a linear data structure that follows the "
            "First-In First-Out (FIFO) principle."
        ),
        "ordering": "FIFO — First In, First Out",
        "operations": {
            "enqueue": "Add an element to the rear. O(1).",
            "dequeue": "Remove an element from the front. O(1).",
        },
        "use_cases": [
            "CPU scheduling",
            "Breadth-first search",
            "Print spooling",
            "Message queues",
        ],
        "notes": (
            "A queue is NOT LIFO. LIFO describes a stack. "
            "Queues process elements in the order they arrive."
        ),
    },

    "hash_table": {
        "definition": (
            "A hash table is a data structure that maps keys to values using a hash function "
            "to compute an index into an array of buckets or slots."
        ),
        "average_time_complexity": {
            "search": "O(1)",
            "insert": "O(1)",
            "delete": "O(1)",
        },
        "worst_time_complexity": {
            "search": "O(n)",
            "insert": "O(n)",
            "delete": "O(n)",
        },
        "conditions": (
            "O(1) average case assumes a good hash function with minimal collisions. "
            "Worst case O(n) occurs when all keys hash to the same bucket (all collisions)."
        ),
        "collision_handling": [
            "Chaining (linked lists at each bucket)",
            "Open addressing (linear probing, quadratic probing, double hashing)",
        ],
        "notes": (
            "Hash tables do NOT guarantee O(1) in worst case. "
            "Performance heavily depends on the quality of the hash function."
        ),
    },
}

# Topics the system can match claims to
SUPPORTED_TOPICS = list(KNOWLEDGE_BASE.keys())