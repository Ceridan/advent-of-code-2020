import os
from collections import deque

from typing import List


def part1(nums: List[int], preamble: int) -> int:
    window = deque(nums[:preamble])

    for i in range(preamble, len(nums)):
        current = nums[i]
        found = False
        for v in window:
            diff = current - v
            if diff > 0 and diff in window:
                found = True
                break

        if not found:
            return current

        window.popleft()
        window.append(current)

    return -1


def part2(nums: List[int], preamble: int) -> int:
    invalid_number = part1(nums, preamble)

    l, r = 0, 0
    current = 0

    while r < len(nums):
        current += nums[r]

        while current > invalid_number:
            current -= nums[l]
            l += 1

        if current == invalid_number and r - l >= 2:
            return min(nums[l:r + 1]) + max(nums[l:r + 1])

        r += 1

    return -1


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(127, part1([35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576],
                preamble=5))

test(62, part2([35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576],
               preamble=5))

file_path = os.path.join(os.path.dirname(__file__), 'inputs/day09.txt')
with open(file_path, 'r') as f:
    input_data = [int(line.strip()) for line in f.readlines()]

    print('Day 09, part 1: %r' % (part1(input_data, preamble=25)))
    print('Day 09, part 2: %r' % (part2(input_data, preamble=25)))
