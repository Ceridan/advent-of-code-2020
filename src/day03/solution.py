import os

from collections import namedtuple
from typing import List


SlopeRule = namedtuple('SlopeRule', 'right down')


class TreeGrid:
    def __init__(self, tree_map: List[str]):
        self._grid = tree_map

    @property
    def height(self) -> int:
        return len(self._grid)

    def get(self, x: int, y: int) -> str:
        if y >= self.height:
            raise ValueError(f'Out of bound. y: {y}, height: {self.height}.')

        width = len(self._grid[0])
        return self._grid[y][x % width]


def part1(tree_map: List[str], rule: SlopeRule) -> int:
    grid = TreeGrid(tree_map)
    return _calculate(grid, rule)


def part2(tree_map: List[str], rules: List[SlopeRule]) -> int:
    grid = TreeGrid(tree_map)
    result = 1
    for rule in rules:
        result *= _calculate(grid, rule)
    return result


def _calculate(grid: TreeGrid, rule: SlopeRule) -> int:
    trees_count = 0
    x, y = 0, 0

    while y < grid.height:
        if grid.get(x, y) == '#':
            trees_count += 1
        x += rule.right
        y += rule.down

    return trees_count


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(7, part1([
    '..##.......',
    '#...#...#..',
    '.#....#..#.',
    '..#.#...#.#',
    '.#...##..#.',
    '..#.##.....',
    '.#.#.#....#',
    '.#........#',
    '#.##...#...',
    '#...##....#',
    '.#..#...#.#',
], rule=SlopeRule(3, 1)))


test(336, part2([
    '..##.......',
    '#...#...#..',
    '.#....#..#.',
    '..#.#...#.#',
    '.#...##..#.',
    '..#.##.....',
    '.#.#.#....#',
    '.#........#',
    '#.##...#...',
    '#...##....#',
    '.#..#...#.#',
], rules=[
    SlopeRule(1, 1),
    SlopeRule(3, 1),
    SlopeRule(5, 1),
    SlopeRule(7, 1),
    SlopeRule(1, 2),
]))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 03, part 1: %r' % (part1(input_data, rule=SlopeRule(3, 1))))
    print('Day 03, part 2: %r' % (part2(input_data, rules=[
        SlopeRule(1, 1),
        SlopeRule(3, 1),
        SlopeRule(5, 1),
        SlopeRule(7, 1),
        SlopeRule(1, 2),
    ])))
