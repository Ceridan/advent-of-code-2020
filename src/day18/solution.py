import os

from typing import List


def part1(expressions: List[str]) -> int:
    calc_sum = 0
    for expression in expressions:
        calc_sum += _calculator_equal_precedence(expression)
    return calc_sum


def part2(expressions: List[str]) -> int:
    calc_sum = 0
    for expression in expressions:
        calc_sum += _calculator_additions_first(expression)
    return calc_sum


def _calculator_equal_precedence(expression: str) -> int:
    expression = expression.replace(' ', '')
    stack = []

    for ch in expression:
        if ch in '(+*':
            stack.append(ch)
            continue

        if ch == ')':
            arg1 = stack.pop()
            stack.pop()
            if stack and stack[-1] != '(':
                op = stack.pop()
                arg2 = stack.pop()
                result = arg1 * arg2 if op == '*' else arg1 + arg2
                stack.append(result)
            else:
                stack.append(arg1)

        if ch.isdigit():
            if not stack or stack[-1] == '(':
                stack.append(int(ch))
                continue
            else:
                arg1 = int(ch)
                op = stack.pop()
                arg2 = stack.pop()
                result = arg1 * arg2 if op == '*' else arg1 + arg2
                stack.append(result)

    return stack[0]


def _calculator_additions_first(expression: str) -> int:
    expression = expression.replace(' ', '')
    stack = []

    for ch in expression:
        if ch in '(+*':
            stack.append(ch)
            continue

        if ch == ')':
            arg1 = stack.pop()
            while stack[-1] != '(':
                op = stack.pop()
                arg2 = stack.pop()
                arg1 = arg1 * arg2 if op == '*' else arg1 + arg2

            stack.pop()

            if stack and stack[-1] != '(' and stack[-1] != '*':
                op = stack.pop()
                arg2 = stack.pop()
                result = arg1 * arg2 if op == '*' else arg1 + arg2
                stack.append(result)
            else:
                stack.append(arg1)

        if ch.isdigit():
            if not stack or stack[-1] == '(':
                stack.append(int(ch))
                continue
            else:
                arg1 = int(ch)
                if stack[-1] == '+':
                    op = stack.pop()
                    arg2 = stack.pop()
                    result = arg1 * arg2 if op == '*' else arg1 + arg2
                    stack.append(result)
                else:
                    stack.append(arg1)

    result = 1

    while stack:
        arg = stack.pop()
        if arg != '*':
            result *= arg

    return result


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(85, part1(['1 + ((2 * (3 + 4) * 2) * 3)']))
test(71, part1(['1 + 2 * 3 + 4 * 5 + 6']))
test(51, part1(['1 + (2 * 3) + (4 * (5 + 6))']))
test(26, part1(['2 * 3 + (4 * 5)']))
test(437, part1(['5 + (8 * 3 + 9 + 3 * 4 * 3)']))
test(12240, part1(['5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))']))
test(13632, part1(['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2']))


test(85, part2(['1 + ((2 * (3 + 4) * 2) * 3)']))
test(231, part2(['1 + 2 * 3 + 4 * 5 + 6']))
test(51, part2(['1 + (2 * 3) + (4 * (5 + 6))']))
test(46, part2(['2 * 3 + (4 * 5)']))
test(1445, part2(['5 + (8 * 3 + 9 + 3 * 4 * 3)']))
test(669060, part2(['5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))']))
test(23340, part2(['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2']))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 18, part 1: %r' % (part1(input_data)))
    print('Day 18, part 2: %r' % (part2(input_data)))

# 15773593539749 - wrong
