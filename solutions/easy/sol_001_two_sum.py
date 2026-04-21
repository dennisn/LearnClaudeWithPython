TITLE = "Two Sum"
DESCRIPTION = "Given an array nums and an integer target, return indices of the two numbers that add up to target."
PARAMS = [
    {"name": "nums",   "type": "list[int]", "description": "Input array e.g. [2,7,11,15]"},
    {"name": "target", "type": "int",       "description": "Target sum e.g. 9"},
]


def solve(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
