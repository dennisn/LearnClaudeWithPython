from solutions.easy.sol_001_two_sum import solve


def test_basic_example():
    assert solve([2, 7, 11, 15], 9) == [0, 1]


def test_answer_at_end():
    assert solve([3, 2, 4], 6) == [1, 2]


def test_duplicate_values():
    assert solve([3, 3], 6) == [0, 1]


def test_negative_numbers():
    assert solve([-1, -2, -3, -4, -5], -8) == [2, 4]


def test_single_pair():
    assert solve([1, 9], 10) == [0, 1]
