import os
import re


from collections import namedtuple
from typing import List, Dict, Set


BagRule = namedtuple('BagRule', 'amount name')


class BagRuleNode:
    def __init__(self, color: str, inner: List[BagRule] = None, outer: List[str] = None):
        self.color = color
        self.inner = inner if inner else []
        self.outer = outer if outer else []

    def __repr__(self):
        return f'Color: {self.color}, outer: {self.outer}, inner: {self.inner}'


def part1(bag_color: str, bag_rules: List[str]) -> int:
    grid = _parse_rules(bag_rules)
    return _outer_dfs(bag_color, grid, set())


def part2(bag_color: str, bag_rules: List[str]) -> int:
    grid = _parse_rules(bag_rules)
    return _inner_dfs(bag_color, grid)


def _outer_dfs(color: str, grid: Dict[str, BagRuleNode], visited: Set[str]) -> int:
    amount = 0

    for outer_color in grid[color].outer:
        if outer_color not in visited:
            visited.add(outer_color)
            amount += _outer_dfs(outer_color, grid, visited) + 1

    return amount


def _inner_dfs(color: str, grid: Dict[str, BagRuleNode]) -> int:
    amount = 0

    for inner_amount, inner_color in grid[color].inner:
        amount += inner_amount * _inner_dfs(inner_color, grid) + inner_amount

    return amount


def _parse_rules(bag_rules: List[str]) -> Dict[str, BagRuleNode]:
    grid = dict()

    for line in bag_rules:
        outer_color = re.findall(r'^([a-z ]+) bags contain', line)[0]
        if outer_color not in grid:
            grid[outer_color] = BagRuleNode(outer_color)

        inner_bags = re.findall(r'(\d+) ([a-z ]+) bag', line)
        for amount, inner_color in inner_bags:
            grid[outer_color].inner.append(BagRule(int(amount), inner_color))

            if inner_color not in grid:
                grid[inner_color] = BagRuleNode(inner_color)
            grid[inner_color].outer.append(outer_color)

    return grid


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(4, part1('shiny gold', [
    'light red bags contain 1 bright white bag, 2 muted yellow bags.',
    'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
    'bright white bags contain 1 shiny gold bag.',
    'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
    'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
    'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
    'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
    'faded blue bags contain no other bags.',
    'dotted black bags contain no other bags.',
]))

test(32, part2('shiny gold', [
    'light red bags contain 1 bright white bag, 2 muted yellow bags.',
    'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
    'bright white bags contain 1 shiny gold bag.',
    'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
    'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
    'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
    'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
    'faded blue bags contain no other bags.',
    'dotted black bags contain no other bags.',
]))

test(126, part2('shiny gold', [
    'shiny gold bags contain 2 dark red bags.',
    'dark red bags contain 2 dark orange bags.',
    'dark orange bags contain 2 dark yellow bags.',
    'dark yellow bags contain 2 dark green bags.',
    'dark green bags contain 2 dark blue bags.',
    'dark blue bags contain 2 dark violet bags.',
    'dark violet bags contain no other bags.',
]))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 07, part 1: %r' % (part1('shiny gold', input_data)))
    print('Day 07, part 2: %r' % (part2('shiny gold', input_data)))
