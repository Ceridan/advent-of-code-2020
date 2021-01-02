import os

from typing import List


def part1(initial_numbers: List[int], turns: int) -> int:
    return _play_numbers(initial_numbers, turns)


def part2(initial_numbers: List[int], turns: int) -> int:
    return _play_numbers(initial_numbers, turns)


def _play_numbers(initial_numbers: List[int], turns: int) -> int:
    numbers = {num: i + 1 for i, num in enumerate(initial_numbers)}
    current = 0

    for turn in range(len(initial_numbers) + 1, turns):
        if current not in numbers:
            numbers[current] = turn
            current = 0
        else:
            next_number = turn - numbers[current]
            numbers[current] = turn
            current = next_number

    print(f'Initial: {initial_numbers}, turns: {turns}, result: {current}. Done.')
    return current


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(436, part1([0, 3, 6], 2020))
test(1, part1([1, 3, 2], 2020))
test(10, part1([2, 1, 3], 2020))
test(27, part1([1, 2, 3], 2020))
test(78, part1([2, 3, 1], 2020))
test(438, part1([3, 2, 1], 2020))
test(1836, part1([3, 1, 2], 2020))

test(175594, part2([0, 3, 6], 30000000))
test(2578, part2([1, 3, 2], 30000000))
test(3544142, part2([2, 1, 3], 30000000))
test(261214, part2([1, 2, 3], 30000000))
test(6895259, part2([2, 3, 1], 30000000))
test(18, part2([3, 2, 1], 30000000))
test(362, part2([3, 1, 2], 30000000))


file_path = os.path.join(os.path.dirname(__file__), 'inputs/day15.txt')
with open(file_path, 'r') as f:
    input_data = [int(x) for x in f.read().split(',')]

    print('Day 15, part 1: %r' % (part1(input_data, turns=2020)))
    print('Day 15, part 2: %r' % (part2(input_data, turns=30000000)))
