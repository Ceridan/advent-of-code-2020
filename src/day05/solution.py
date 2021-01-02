import os
from typing import List, Tuple


def part1(seats: List[str]) -> int:
    best_seat_id = 0

    for seat in seats:
        row, column = _calculate_seat(seat)
        seat_id = row * 8 + column
        if seat_id > best_seat_id:
            best_seat_id = seat_id

    return best_seat_id


def part2(seats: List[str]) -> int:
    ids = []
    for seat in seats:
        row, column = _calculate_seat(seat)
        seat_id = row * 8 + column
        ids.append(seat_id)

    min_ = min(ids)
    max_ = max(ids)
    known_seats = set(ids)
    all_seats = set(range(min_, max_ + 1))

    return list(all_seats - known_seats)[0]


def _calculate_seat(seat: str) -> Tuple[int, int]:
    row = _binary_search(seat[:7])
    column = _binary_search(seat[7:])
    return row, column


def _binary_search(partition: str) -> int:
    left = 0
    right = 2 ** len(partition) - 1

    for part in partition:
        mid = (left + right) // 2
        if part in ['F', 'L']:
            right = mid
        else:
            left = mid + 1

    return right


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test((44, 5), _calculate_seat('FBFBBFFRLR'))
test((70, 7), _calculate_seat('BFFFBBFRRR'))
test((14, 7), _calculate_seat('FFFBBBFRRR'))
test((102, 4), _calculate_seat('BBFFBBFRLL'))

test(820, part1([
    'FBFBBFFRLR',
    'BFFFBBFRRR',
    'FFFBBBFRRR',
    'BBFFBBFRLL',
]))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 05, part 1: %r' % (part1(input_data)))
    print('Day 05, part 2: %r' % (part2(input_data)))
