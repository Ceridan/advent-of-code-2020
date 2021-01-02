import os
import re

from typing import List, Dict, Tuple


def part1(raw_message: str) -> int:
    rules, messages = _parse_message_data(raw_message)
    rule = _rules_backtrack(rules)[0]

    pattern = re.compile(rf'^{rule}$')

    valid_count = 0
    for message in messages:
        if pattern.match(message):
            valid_count += 1

    return valid_count


def part2(raw_message: str, replacements: Dict[str, str]) -> int:
    rules, messages = _parse_message_data(raw_message, replacements=replacements)
    processed_rules = _rules_backtrack({k: v for k, v in rules.items() if k not in (0, 8, 11)})

    r31 = processed_rules[31]
    r42 = processed_rules[42]

    r8 = f'({r42})+'
    r11 = f'({r42}({r42}({r42}({r42}({r42}({r42}{r31})*{r31})*{r31})*{r31})*{r31})*{r31})'

    rule = f'^({r8}{r11})$'

    pattern = re.compile(rf'^{rule}$')

    valid_count = 0
    for message in messages:
        if pattern.match(message):
            valid_count += 1

    return valid_count


def _rules_backtrack(rules: Dict[int, str]) -> Dict[int, str]:
    apply = set([id_ for id_, val in rules.items() if len(val) == 1])
    next_apply = set()
    unprocessed = set(rules.keys())
    unprocessed.difference_update(apply)

    while unprocessed:
        for unprocessed_id in unprocessed:
            for apply_id in apply:
                rules[unprocessed_id] = rules[unprocessed_id].replace(f'[{apply_id}]', rules[apply_id])
                if '[' not in rules[unprocessed_id]:
                    next_apply.add(unprocessed_id)

        apply = next_apply
        next_apply = set()
        unprocessed.difference_update(apply)

    return rules


def _parse_message_data(raw_message: str, replacements: Dict[str, str] = None) -> Tuple[Dict[int, str], List[str]]:
    rules = {}
    messages = []
    mode = 0

    for line in raw_message.split('\n'):
        if not line and not rules:
            continue

        if not line:
            mode = 1
            continue

        if mode == 1:
            messages.append(line)
            continue

        if replacements and line in replacements:
            line = replacements[line]

        m = re.match(r'(\d+): "([ab])"', line)
        if m:
            rules[int(m.group(1))] = m.group(2)
            continue

        m = re.match(r'(\d+): (\d+)$"', line)
        if m:
            rules[int(m.group(1))] = f'([{m.group(2)}])'
            continue

        splitted = line.split(':')
        id_ = int(splitted[0].strip())
        rule_ids = []
        for r in splitted[1].split('|'):
            rids = []
            for rid in r.strip().split():
                rids.append(f'[{rid.strip()}]')
            rule_ids.append(''.join(rids))

        rules[id_] = f'({"|".join(rule_ids)})'

    return rules, messages


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(2, part1("""
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""))

test(3, part1("""
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""))


test(12, part2("""
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""", replacements={
    '8: 42': '8: 42 | 42 8',
    '11: 42 31': '11: 42 31 | 42 11 31'
}))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    input_data = f.read()

    print('Day 19, part 1: %r' % (part1(input_data)))
    print('Day 19, part 2: %r' % (part2(input_data, replacements={
        '8: 42': '8: 42 | 42 8',
        '11: 42 31': '11: 42 31 | 42 11 31'
    })))
