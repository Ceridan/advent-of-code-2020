import os
from collections import deque

from typing import List, Tuple, Deque


def part1(deck: List[str]) -> int:
    player1, player2 = _parse_deck(deck)

    while player1 and player2:
        num1 = player1.popleft()
        num2 = player2.popleft()

        winner = player1 if num1 > num2 else player2
        winner.append(max(num1, num2))
        winner.append(min(num1, num2))

    return _calculate_score(player1, player2)


def part2(deck: List[str]) -> int:
    player1, player2 = _parse_deck(deck)
    _recursive_combat(player1, player2)
    return _calculate_score(player1, player2)


def _recursive_combat(player1: Deque[int], player2: Deque[int]) -> bool:
    states = set()

    while player1 and player2:
        current_state = (tuple(player1), tuple(player2))
        if current_state in states:
            return True

        states.add(current_state)

        num1 = player1.popleft()
        num2 = player2.popleft()

        if num1 <= len(player1) and num2 <= len(player2):
            new_player1 = deque(list(player1)[:num1])
            new_player2 = deque(list(player2)[:num2])
            is_p1 = _recursive_combat(new_player1, new_player2)
            winner = player1 if is_p1 else player2
            winner.append(num1 if is_p1 else num2)
            winner.append(num2 if is_p1 else num1)
            continue

        winner = player1 if num1 > num2 else player2
        winner.append(max(num1, num2))
        winner.append(min(num1, num2))

    return len(player1) > 0


def _calculate_score(player1: Deque[int], player2: Deque[int]) -> int:
    winner = player1 if player1 else player2
    n = len(winner)
    score = 0

    for i, num in enumerate(winner):
        score += num * (n - i)
        i += 1

    return score


def _parse_deck(deck: List[str]) -> Tuple[Deque[int], Deque[int]]:
    player1 = deque()
    player2 = deque()
    player = 1

    for line in deck:
        if not line:
            continue

        if line == 'Player 1:':
            continue
        elif line == 'Player 2:':
            player = 2
            continue

        if player == 1:
            player1.append(int(line))
        else:
            player2.append(int(line))

    return player1, player2


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(306, part1([
    'Player 1:',
    '9',
    '2',
    '6',
    '3',
    '1',
    'Player 2:',
    '5',
    '8',
    '4',
    '7',
    '10',
]))

test(105, part2([
    'Player 1:',
    '43',
    '19',
    'Player 2:',
    '2',
    '29',
    '14',
]))

test(291, part2([
    'Player 1:',
    '9',
    '2',
    '6',
    '3',
    '1',
    'Player 2:',
    '5',
    '8',
    '4',
    '7',
    '10',
]))

file_path = os.path.join(os.path.dirname(__file__), 'inputs/day22.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 22, part 1: %r' % (part1(input_data)))
    print('Day 22, part 2: %r' % (part2(input_data)))
