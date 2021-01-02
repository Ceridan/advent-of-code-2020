import itertools
import os
from typing import List


def part1(nums: List[int]) -> int:
    s = set(nums)
    for num in nums:
        if 2020 - num in s:
            return num * (2020 - num)
    return -1


def part2(nums: List[int]) -> int:
    s = set(nums)
    combs = itertools.combinations(nums, 2)
    for a, b in combs:
        if 2020 - a - b in s:
            return a * b * (2020 - a - b)
    return -1


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(514579, part1([1721, 979, 366, 299, 675, 1456]))
test(241861950, part2([1721, 979, 366, 299, 675, 1456]))


file_path = os.path.join(os.path.dirname(__file__), 'inputs/day01.txt')
with open(file_path, 'r') as f:
    input_data = [int(line.strip()) for line in f.readlines()]

    print('Day 01, part 1: %r' % (part1(input_data)))
    print('Day 01, part 2: %r' % (part2(input_data)))
