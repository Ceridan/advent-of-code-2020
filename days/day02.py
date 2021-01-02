import os
import re

from collections import namedtuple
from typing import List, Tuple


Rule = namedtuple('Rule', 'min max symbol')


def part1(passwords_with_rules: List[str]) -> int:
    pwrs = _parse_passwords(passwords_with_rules)
    valid = 0

    for rule, password in pwrs:
        count = sum([1 for ch in password if ch == rule.symbol])
        valid += 1 if rule.min <= count <= rule.max else 0

    return valid


def part2(passwords_with_rules: List[str]) -> int:
    pwrs = _parse_passwords(passwords_with_rules)
    valid = 0

    for rule, password in pwrs:
        n = len(password)
        pos1 = 1 if rule.min <= n and password[rule.min - 1] == rule.symbol else 0
        pos2 = 1 if rule.max <= n and password[rule.max - 1] == rule.symbol else 0
        valid += pos1 ^ pos2

    return valid


def _parse_passwords(passwords_with_rules: List[str]) -> List[Tuple[Rule, str]]:
    parsed_passwords = []

    for pwr in passwords_with_rules:
        min_, max_, symbol, password = re.findall(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', pwr)[0]
        rule = Rule(int(min_), int(max_), symbol)
        parsed_passwords.append((rule, password))

    return parsed_passwords


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(2, part1([
    '1-3 a: abcde',
    '1-3 b: cdefg',
    '2-9 c: ccccccccc',
]))

test(1, part2([
    '1-3 a: abcde',
    '1-3 b: cdefg',
    '2-9 c: ccccccccc',
]))


file_path = os.path.join(os.path.dirname(__file__), 'inputs/day02.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 02, part 1: %r' % (part1(input_data)))
    print('Day 02, part 2: %r' % (part2(input_data)))

_parse_passwords(['12-3 b: cdefg'])
