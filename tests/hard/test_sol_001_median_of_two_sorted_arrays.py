import pytest
from solutions.hard.sol_001_median_of_two_sorted_arrays import solve


def test_odd_total():
    # Merged: [1, 2, 3] → median = 2.0
    assert solve([1, 3], [2]) == 2.0


def test_even_total():
    # Merged: [1, 2, 3, 4] → median = (2+3)/2 = 2.5
    assert solve([1, 2], [3, 4]) == 2.5


def test_all_zeros():
    assert solve([0, 0], [0, 0]) == 0.0


def test_one_empty():
    assert solve([], [1]) == 1.0


def test_large_skew():
    # Merged: [1, 2, 3, 4, 5, 6] → median = (3+4)/2 = 3.5
    assert solve([1, 2], [3, 4, 5, 6]) == 3.5
