# Plan: Add "Add Two Numbers" Solution (LeetCode #2)

## Context

The project is a Flask app that lets users run LeetCode solutions in a browser. Solutions live in `solutions/<difficulty>/`, must export `TITLE`, `PARAMS`, and `solve()`, and are auto-discovered at startup. The app only supports `list[int]` as the closest type to a linked list, so inputs/outputs will be represented as digit arrays in reverse order (e.g. `[2,4,3]` = 342). The `solve()` function will handle the internal linked list construction transparently.

Current state on `main`:
- `solutions/easy/sol_001_two_sum.py` exists
- `tests/__init__.py` and `tests/easy/__init__.py` both exist as source files
- This PR adds `solutions/medium/`
- This PR adds `tests/medium/`

---

## Files to Create

### 1. `solutions/medium/__init__.py` — empty
Required so `from solutions.medium.sol_001_add_two_numbers import solve` works in tests.

### 2. `solutions/medium/sol_001_add_two_numbers.py`

```python
TITLE = "Add Two Numbers"
DESCRIPTION = (
    "You are given two non-empty linked lists representing two non-negative integers. "
    "The digits are stored in reverse order (ones digit first). "
    "Add the two numbers and return the sum as a linked list."
)
PARAMS = [
    {"name": "l1", "type": "list[int]", "description": "First number, reverse digit order e.g. [2,4,3] for 342"},
    {"name": "l2", "type": "list[int]", "description": "Second number, reverse digit order e.g. [5,6,4] for 465"},
]


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def _list_to_linked(digits: list[int]) -> "ListNode | None":
    dummy = ListNode()
    current = dummy
    for d in digits:
        current.next = ListNode(d)
        current = current.next
    return dummy.next


def _linked_to_list(head: "ListNode | None") -> list[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


def solve(l1: list[int], l2: list[int]) -> list[int]:
    p1, p2 = _list_to_linked(l1), _list_to_linked(l2)
    dummy = ListNode()
    current = dummy
    carry = 0
    while p1 or p2 or carry:
        val1 = p1.val if p1 else 0
        val2 = p2.val if p2 else 0
        if p1: p1 = p1.next
        if p2: p2 = p2.next
        total = val1 + val2 + carry
        carry, digit = divmod(total, 10)
        current.next = ListNode(digit)
        current = current.next
    return _linked_to_list(dummy.next)
```

### 3. `tests/__init__.py` — empty
Recreates the missing source file (only `.pyc` exists on `main`).

### 4. `tests/medium/__init__.py` — empty

### 5. `tests/medium/test_sol_001_add_two_numbers.py`

```python
from solutions.medium.sol_001_add_two_numbers import solve


def test_basic_example():
    # 342 + 465 = 807
    assert solve([2, 4, 3], [5, 6, 4]) == [7, 0, 8]


def test_carry_propagation():
    # 99 + 1 = 100
    assert solve([9, 9], [1]) == [0, 0, 1]


def test_different_lengths():
    # 1001 + 99 = 1100
    assert solve([1, 0, 0, 1], [9, 9]) == [0, 0, 1, 1]


def test_all_nines_new_digit():
    # 999 + 999 = 1998
    assert solve([9, 9, 9], [9, 9, 9]) == [8, 9, 9, 1]


def test_single_digits_with_carry():
    # 5 + 5 = 10
    assert solve([5], [5]) == [0, 1]
```

---

## No Changes Required

- `app.py` — auto-discovers `solutions/medium/` once the directory exists
- `requirements.txt` — `pytest` already listed
- `solutions/easy/` — untouched

---

## Git Workflow

Per CLAUDE.md, a new feature branch must be created before any file modifications:

```text
feature/20260421_AddTwoNumbersSolution
```

---

## Verification

1. `pytest tests/medium/` — all 5 tests pass
2. `python app.py` — navigate to `/`, confirm "Add Two Numbers" appears under Medium
3. Submit `[2,4,3]` and `[5,6,4]` via the UI — expect result `[7, 0, 8]`
