# Plan: Add "Median of Two Sorted Arrays" Hard Solution Framework

## Context
Add LeetCode #4 "Median of Two Sorted Arrays" as the first hard-difficulty solution. The user wants the framework only — stub solve function, full PARAMS/TITLE/DESCRIPTION, and test cases with expected values — NOT the actual implementation. Tests will fail until the user fills in `solve()`.

## Git
Create and check out branch `feature/20260421_MedianOfTwoSortedArrays` before any file changes.

## Files to Create

### 1. `solutions/hard/__init__.py`
Empty file (new package).

### 2. `solutions/hard/sol_001_median_of_two_sorted_arrays.py`
- `TITLE = "Median of Two Sorted Arrays"`
- `DESCRIPTION`: problem summary (given two sorted arrays of size m and n, return the median as a float)
- `PARAMS`: two `list[int]` params (`nums1`, `nums2`)
- `solve(nums1, nums2) -> float`: raises `NotImplementedError` — placeholder for user to implement

### 3. `tests/hard/__init__.py`
Empty file (new package).

### 4. `tests/hard/test_sol_001_median_of_two_sorted_arrays.py`
Five pytest test cases with expected values already filled in (will fail until `solve()` is implemented):

| Test | nums1 | nums2 | Expected | Notes |
|------|-------|-------|----------|-------|
| `test_odd_total` | `[1,3]` | `[2]` | `2.0` | Merged: [1,2,3], median=2 |
| `test_even_total` | `[1,2]` | `[3,4]` | `2.5` | Merged: [1,2,3,4], median=(2+3)/2 |
| `test_all_zeros` | `[0,0]` | `[0,0]` | `0.0` | |
| `test_one_empty` | `[]` | `[1]` | `1.0` | One array empty |
| `test_large_skew` | `[1,2]` | `[3,4,5,6]` | `3.5` | Merged: [1,2,3,4,5,6] |

## Verification
```bash
pytest tests/hard/test_sol_001_median_of_two_sorted_arrays.py -v
```
Expected: all 5 tests **fail** with `NotImplementedError` — confirming the framework is wired up correctly and ready for the user to implement `solve()`.

## PR
After implementation, create a PR from `feature/20260421_MedianOfTwoSortedArrays` → `main`.
