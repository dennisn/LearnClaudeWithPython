from solutions.medium.sol_001_add_two_numbers import solve


def test_basic_example():
    # 342 + 465 = 807
    assert solve([2, 4, 3], [5, 6, 4]) == [7, 0, 8]


def test_both_zero():
    assert solve([0], [0]) == [0]


def test_carry_propagation():
    # 9999999 + 9999 = 10009998
    assert solve([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9]) == [8, 9, 9, 9, 0, 0, 0, 1]


def test_different_lengths():
    # 99 + 1 = 100
    assert solve([9, 9], [1]) == [0, 0, 1]


def test_single_digit_carry():
    # 5 + 5 = 10
    assert solve([5], [5]) == [0, 1]
