TITLE = "Median of Two Sorted Arrays"
DESCRIPTION = (
    "Given two sorted arrays nums1 of size m and nums2 of size n, "
    "return the median of the two sorted arrays as a float. "
    "The overall run time complexity should be O(log(m+n))."
)
PARAMS = [
    {"name": "nums1", "type": "list[int]", "description": "First sorted array, e.g. [1,3]"},
    {"name": "nums2", "type": "list[int]", "description": "Second sorted array, e.g. [2]"},
]


def solve(nums1: list[int], nums2: list[int]) -> float:
    total_length = len(nums1) + len(nums2)
    median_index = total_length // 2
    is_even = total_length % 2 == 0
    lower_index = median_index - 1 if is_even else median_index
    higher_index = median_index
    idx_1 = 0
    idx_2 = 0
    current_index = 0
    val = None
    while (val is None) or (current_index <= higher_index):
        if idx_1 < len(nums1) and (idx_2 >= len(nums2) or nums1[idx_1] < nums2[idx_2]):
            val = nums1[idx_1]
            idx_1 += 1
        else:
            val = nums2[idx_2]
            idx_2 += 1
            
        if current_index == lower_index:
            lower_val = val
        if current_index == higher_index:
            higher_val = val
        current_index += 1

    if is_even:
        return (lower_val + higher_val) / 2
    else:
        return higher_val