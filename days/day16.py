import os
import re
from collections import defaultdict

from typing import List, Tuple, Dict, Set


def part1(tickets_data: str) -> int:
    rules, tickets = _parse_data(tickets_data)
    validation_set = _generate_validation_set(rules)
    invalid_fields_sum = 0

    for ticket in tickets[1:]:
        for v in ticket:
            if v not in validation_set:
                invalid_fields_sum += v

    return invalid_fields_sum


def part2(tickets_data: str) -> int:
    rules, tickets = _parse_data(tickets_data)
    valid_tickets = _discard_invalid_tickets(rules, tickets)
    rule_fields = {rule: set(range(0, len(valid_tickets[0]))) for rule in rules.keys()}

    departure_value = 1

    for ticket in valid_tickets:
        for i in range(len(valid_tickets[0])):
            for rule in rules:
                if i in rule_fields[rule] and ticket[i] not in rules[rule]:
                    rule_fields[rule].remove(i)

    for rule, fields in sorted(rule_fields.items(), key=lambda item: len(item[1])):
        field = list(fields)[0]
        for other_rule in rule_fields:
            if rule != other_rule and field in rule_fields[other_rule]:
                rule_fields[other_rule].remove(field)

    for rule, fields in rule_fields.items():
        if rule.startswith('departure'):
            departure_value *= valid_tickets[0][list(fields)[0]]

    return departure_value


def _discard_invalid_tickets(rules: Dict, tickets: List[List[int]]) -> List[List[int]]:
    validation_set = _generate_validation_set(rules)
    valid_tickets = [tickets[0]]

    for ticket in tickets[1:]:
        is_valid = True
        for v in ticket:
            if v not in validation_set:
                is_valid = False
                break
        if is_valid:
            valid_tickets.append(ticket)

    return valid_tickets


def _generate_validation_set(rules: Dict) -> Set[range]:
    validation_set = set()

    for _, rule in rules.items():
        validation_set.update(rule)

    return validation_set


def _parse_data(tickets_data: str) -> Tuple[Dict, List[List[int]]]:
    rules = defaultdict(set)
    tickets = []

    mode = 0
    for line in tickets_data.split('\n'):
        line = line.strip()
        if not line:
            continue

        if line == 'your ticket:':
            mode = 1
            continue

        if line == 'nearby tickets:':
            mode = 2
            continue

        if mode == 0:
            rule, ll, lh, hl, hh = re.findall(r'([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)', line)[0]
            rules[str(rule)].update(range(int(ll), int(lh) + 1))
            rules[str(rule)].update(range(int(hl), int(hh) + 1))
        else:
            tickets.append([int(x) for x in line.split(',')])

    return rules, tickets


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(71, part1("""
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""))

test(143, part2("""
class: 0-1 or 4-19
departure row: 0-5 or 8-19
departure seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""))


file_path = os.path.join(os.path.dirname(__file__), 'inputs/day16.txt')
with open(file_path, 'r') as f:
    input_data = f.read()

    print('Day 16, part 1: %r' % (part1(input_data)))
    print('Day 16, part 2: %r' % (part2(input_data)))
