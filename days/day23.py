import os

from typing import List, Dict, Tuple


class Cup:
    def __init__(self, val: int, destinations: List[int], next_: 'Cup' = None):
        self.val = val
        self.next = next_
        self.destinations = destinations


def part1(cups_list: str, turns: int) -> str:
    current, cups = _parse_cups_list(cups_list, len(cups_list))
    _play_cups(current, cups, turns)

    nxt = cups[1].next
    result = ''
    while nxt.val != 1:
        result += str(nxt.val)
        nxt = nxt.next

    return result


def part2(cups_list: str, turns: int, cups_amount: int) -> int:
    current, cups = _parse_cups_list(cups_list, cups_amount)
    _play_cups(current, cups, turns)
    return cups[1].next.val * cups[1].next.next.val


def _play_cups(current: Cup, cups: Dict[int, Cup], turns: int) -> None:
    for turn in range(1, turns + 1):
        removed = current.next
        removed_set = {removed.val, removed.next.val, removed.next.next.val}

        destination = None
        for prev_val in cups[current.val].destinations:
            if prev_val not in removed_set:
                destination = cups[prev_val]
                break

        current.next = removed.next.next.next

        removed.next.next.next = destination.next
        destination.next = removed

        current = current.next


def _parse_cups_list(cups_list: str, amount: int) -> Tuple[Cup, Dict[int, Cup]]:
    cups = {}

    for i in range(1, amount + 1):
        destinations = [
           i - 1 if i - 1 > 0 else amount + i - 1,
           i - 2 if i - 2 > 0 else amount + i - 2,
           i - 3 if i - 3 > 0 else amount + i - 3,
           i - 4 if i - 4 > 0 else amount + i - 4,
        ]
        cups[i] = Cup(i, destinations)

    current = None
    nxt = None
    prev = None

    for ch in cups_list:
        nxt = cups[int(ch)]
        if not current:
            current = nxt
        else:
            prev.next = nxt
        prev = nxt

    for i in range(10, amount + 1):
        nxt = cups[i]
        prev.next = nxt
        prev = nxt

    nxt.next = current

    return current, cups


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test('92658374', part1('389125467', turns=10))
test('67384529', part1('389125467', turns=100))
test(149245887792, part2('389125467', turns=10000000, cups_amount=1000000))


file_path = os.path.join(os.path.dirname(__file__), 'inputs/day23.txt')
with open(file_path, 'r') as f:
    input_data = f.read().strip()

    print('Day 23, part 1: %r' % (part1(input_data, turns=100)))
    print('Day 23, part 2: %r' % (part2(input_data, turns=10000000, cups_amount=1000000)))
