import os

from typing import List


def part1(seats: List[str]) -> int:
    return _calculate_seats(seats, 1)


def part2(seats: List[str]) -> int:
    return _calculate_seats(seats, 2)


def _calculate_seats(seats: List[str], rules: int) -> int:
    next_state = _next_seat_state_rules_1 if rules == 1 else _next_seat_state_rules_2

    while True:
        next_seats = []
        occupied_count = 0

        for y in range(len(seats)):
            next_seats.append([])
            line = []
            for x in range(len(seats[y])):
                ch = next_state(seats, x, y)
                if ch == '#':
                    occupied_count += 1
                line.append(ch)
            next_seats[y] = ''.join(line)

        if seats == next_seats:
            return occupied_count

        seats = next_seats


def _next_seat_state_rules_1(seats: List[str], x: int, y: int) -> str:
    if seats[y][x] == '.':
        return seats[y][x]

    occupied_count = 0

    for x_ in [-1, 0, 1]:
        for y_ in [-1, 0, 1]:
            if x_ == 0 and y_ == 0:
                continue
            if 0 <= x + x_ < len(seats[0]) and 0 <= y + y_ < len(seats):
                if seats[y + y_][x + x_] == '#':
                    occupied_count += 1

    if seats[y][x] == 'L' and occupied_count == 0:
        return '#'

    if seats[y][x] == '#' and occupied_count >= 4:
        return 'L'

    return seats[y][x]


def _next_seat_state_rules_2(seats: List[str], x: int, y: int) -> str:
    if seats[y][x] == '.':
        return seats[y][x]

    occupied_count = 0

    for x_ in [-1, 0, 1]:
        for y_ in [-1, 0, 1]:
            if x_ == 0 and y_ == 0:
                continue
            xd = x_
            yd = y_
            while 0 <= x + xd < len(seats[0]) and 0 <= y + yd < len(seats):
                if seats[y + yd][x + xd] == '#':
                    occupied_count += 1
                    break
                elif seats[y + yd][x + xd] == 'L':
                    break
                xd += x_
                yd += y_

    if seats[y][x] == 'L' and occupied_count == 0:
        return '#'

    if seats[y][x] == '#' and occupied_count >= 5:
        return 'L'

    return seats[y][x]


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(37, part1([
    'L.LL.LL.LL',
    'LLLLLLL.LL',
    'L.L.L..L..',
    'LLLL.LL.LL',
    'L.LL.LL.LL',
    'L.LLLLL.LL',
    '..L.L.....',
    'LLLLLLLLLL',
    'L.LLLLLL.L',
    'L.LLLLL.LL',
]))

test(26, part2([
    'L.LL.LL.LL',
    'LLLLLLL.LL',
    'L.L.L..L..',
    'LLLL.LL.LL',
    'L.LL.LL.LL',
    'L.LLLLL.LL',
    '..L.L.....',
    'LLLLLLLLLL',
    'L.LLLLLL.L',
    'L.LLLLL.LL',
]))

file_path = os.path.join(os.path.dirname(__file__), 'inputs/day11.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 11, part 1: %r' % (part1(input_data)))
    print('Day 11, part 2: %r' % (part2(input_data)))
