import os
from collections import namedtuple

from typing import List


Action = namedtuple('Action', 'name value')

COMPASS_TO_INT = {'E': 0, 'N': 1, 'W': 2, 'S': 3}
INT_TO_COMPASS = {0: 'E', 1: 'N', 2: 'W', 3: 'S'}


class Ship:
    def __init__(self, actions: List[str], direction: str):
        self._actions = actions
        self._direction = direction
        self._compass = {'E': 0, 'N': 0, 'W': 0, 'S': 0}

    def move(self) -> int:
        for act in self._actions:
            action = Action(act[0], int(act[1:]))
            self._process_single_action(action)

        distance = abs(self._compass['E'] - self._compass['W']) + abs(self._compass['N'] - self._compass['S'])
        return distance

    def _process_single_action(self, action: Action) -> None:
        if action.name == 'F':
            self._compass[self._direction] += action.value
        elif action.name in 'LR':
            pivot = action.value // 90
            pivot = pivot if action.name == 'L' else (4 - pivot)
            pivot = (COMPASS_TO_INT[self._direction] + pivot) % 4
            self._direction = INT_TO_COMPASS[pivot]
        else:
            self._compass[action.name] += action.value


class Waypoint:
    def __init__(self, ew: Action, ns: Action):
        self.EW = ew
        self.NS = ns

    def move(self, action: Action):
        act, val = action

        if act in 'LR':
            pivot = val // 90
            pivot = pivot if act == 'L' else (4 - pivot)
            ew_pivot = (COMPASS_TO_INT[self.EW.name] + pivot) % 4
            ns_pivot = (COMPASS_TO_INT[self.NS.name] + pivot) % 4
            new_ew_action = Action(INT_TO_COMPASS[ew_pivot], self.EW.value)
            new_ns_action = Action(INT_TO_COMPASS[ns_pivot], self.NS.value)
            self.EW = new_ew_action if new_ew_action.name in 'EW' else new_ns_action
            self.NS = new_ns_action if new_ns_action.name in 'NS' else new_ew_action
        elif action.name in 'NS':
            direction = self.NS.name if self.NS.name == act or self.NS.value >= val else act
            value = self.NS.value + val if self.NS.name == act else abs(self.NS.value - val)
            self.NS = Action(direction, value)
        elif action.name in 'EW':
            direction = self.EW.name if self.EW.name == act or self.EW.value >= val else act
            value = self.EW.value + val if self.EW.name == act else abs(self.EW.value - val)
            self.EW = Action(direction, value)


class WaypointShip:
    def __init__(self, actions: List[str], waypoint_ew: Action, waypoint_ns: Action):
        self._actions = actions
        self._waypoint = Waypoint(waypoint_ew, waypoint_ns)
        self._compass = {'E': 0, 'N': 0, 'W': 0, 'S': 0}

    def move(self) -> int:
        for act in self._actions:
            action = Action(act[0], int(act[1:]))
            self._process_single_action(action)

        distance = abs(self._compass['E'] - self._compass['W']) + abs(self._compass['N'] - self._compass['S'])
        return distance

    def _process_single_action(self, action: Action) -> None:
        if action.name == 'F':
            self._compass[self._waypoint.EW.name] += self._waypoint.EW.value * action.value
            self._compass[self._waypoint.NS.name] += self._waypoint.NS.value * action.value
        else:
            self._waypoint.move(action)


def part1(actions: List[str]) -> int:
    ship = Ship(actions, 'E')
    return ship.move()


def part2(actions: List[str]) -> int:
    ship = WaypointShip(actions, waypoint_ew=Action('E', 10), waypoint_ns=Action('N', 1))
    return ship.move()


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(25, part1([
    'F10',
    'N3',
    'F7',
    'R90',
    'F11',
]))


test(286, part2([
    'F10',
    'N3',
    'F7',
    'R90',
    'F11',
]))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 12, part 1: %r' % (part1(input_data)))
    print('Day 12, part 2: %r' % (part2(input_data)))
