TITLE = "Add Two Numbers"
DESCRIPTION = (
    "You are given two non-empty linked lists representing two non-negative integers. "
    "Digits are stored in reverse order and each node contains a single digit. "
    "Add the two numbers and return the sum as a list of digits in reverse order."
)
PARAMS = [
    {"name": "l1", "type": "list[int]", "description": "Digits in reverse order, e.g. [2,4,3] for 342"},
    {"name": "l2", "type": "list[int]", "description": "Digits in reverse order, e.g. [5,6,4] for 465"},
]


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def _to_linked_list(digits: list[int]) -> ListNode:
    dummy = ListNode()
    cur = dummy
    for d in digits:
        cur.next = ListNode(d)
        cur = cur.next
    return dummy.next


def _to_list(head: ListNode) -> list[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


def solve(l1: list[int], l2: list[int]) -> list[int]:
    node1 = _to_linked_list(l1)
    node2 = _to_linked_list(l2)
    dummy = ListNode()
    cur = dummy
    carry = 0
    while node1 or node2 or carry:
        v1 = node1.val if node1 else 0
        v2 = node2.val if node2 else 0
        carry, digit = divmod(v1 + v2 + carry, 10)
        cur.next = ListNode(digit)
        cur = cur.next
        if node1:
            node1 = node1.next
        if node2:
            node2 = node2.next
    return _to_list(dummy.next)
