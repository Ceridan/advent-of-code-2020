import os

from typing import List


def part1(form_data: str) -> int:
    groups = _parse_form_data(form_data)
    answer_count = 0

    for group in groups:
        answers = set(''.join(group))
        answer_count += len(answers)

    return answer_count


def part2(form_data: str) -> int:
    groups = _parse_form_data(form_data)
    answer_count = 0

    for group in groups:
        answers = set(group[0])
        for i in range(1, len(group)):
            answers.intersection_update(group[i])
            if len(answers) == 0:
                break
        answer_count += len(answers)

    return answer_count


def _parse_form_data(form_data: str) -> List[List[str]]:
    forms = form_data.split('\n\n')
    groups = []

    for group_data in forms:
        group = group_data.strip().split('\n')
        groups.append(group)

    return groups


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(11, part1("""
abc

a
b
c

ab
ac

a
a
a
a

b
"""))

test(6, part2("""
abc

a
b
c

ab
ac

a
a
a
a

b
"""))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    input_data = f.read()

    print('Day 06, part 1: %r' % (part1(input_data)))
    print('Day 06, part 2: %r' % (part2(input_data)))
