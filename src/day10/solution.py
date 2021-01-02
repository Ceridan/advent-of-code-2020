import os

from typing import List


def part1(adapters: List[int]) -> int:
    voltages = sorted(adapters)
    voltages.append(voltages[len(voltages) - 1] + 3)

    diffs = [0, 0, 0]
    current = 0

    for v in voltages:
        diffs[v - current - 1] += 1
        current = v

    return diffs[0] * diffs[2]


def part2(adapters: List[int]) -> int:
    voltages = sorted(adapters)
    device_adapter_voltage = voltages[len(voltages) - 1] + 3
    voltages = [0] + voltages + [device_adapter_voltage]

    dp = [0] * len(voltages)
    dp[0] = 1

    for i in range(1, len(voltages)):
        j = i - 1
        while j >= 0 and voltages[i] - voltages[j] <= 3:
            dp[i] += dp[j]
            j -= 1

    return dp[len(voltages) - 1]


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(35, part1([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]))
test(220, part1([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
                 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]))


test(8, part2([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]))
test(19208, part2([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
                   38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    input_data = [int(line.strip()) for line in f.readlines()]

    print('Day 10, part 1: %r' % (part1(input_data)))
    print('Day 10, part 2: %r' % (part2(input_data)))
