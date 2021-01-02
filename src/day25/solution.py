import os


def part1(card_public_key: int, door_public_key: int) -> int:
    card_loop_size = _reverse_loop_size(card_public_key, subject_number=7)
    encryption_key = _calculate_encryption_key(loop_size=card_loop_size, subject_number=door_public_key)
    return encryption_key


def _reverse_loop_size(public_key: int, subject_number: int) -> int:
    value = 1
    remainder = 20201227
    loop_size = 0

    while value != public_key:
        value = (value * subject_number) % remainder
        loop_size += 1

    return loop_size


def _calculate_encryption_key(loop_size: int, subject_number: int) -> int:
    value = 1
    remainder = 20201227

    for i in range(loop_size):
        value = (value * subject_number) % remainder

    return value


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(5764801, _calculate_encryption_key(loop_size=8, subject_number=7))
test(17807724, _calculate_encryption_key(loop_size=11, subject_number=7))

test(8, _reverse_loop_size(5764801, subject_number=7))
test(11, _reverse_loop_size(17807724, subject_number=7))

test(14897079, part1(card_public_key=5764801, door_public_key=17807724))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    input_data = [int(line.strip()) for line in f.readlines()]

    print('Day 25, part 1: %r' % (part1(card_public_key=input_data[0], door_public_key=input_data[1])))
    print('Day 25, part 2: -')
