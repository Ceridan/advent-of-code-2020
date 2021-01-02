import os


# References:
# 1. Chinese remainder theorem (https://en.wikipedia.org/wiki/Chinese_remainder_theorem)
# 2. Extended Euclidean algorithm (https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm)
# 3. Modular multiplicative inverse (https://en.wikipedia.org/wiki/Modular_multiplicative_inverse)
# 4. Finding the modular inverse for every number modulo m in linear time (https://cp-algorithms.com/algebra/module-inverse.html)


def part1(earliest_timestamp: int, bus_schedule: str) -> int:
    ids = [int(bus_id) for bus_id in bus_schedule.split(',') if bus_id != 'x']
    modulo_ids = [-earliest_timestamp % bus_id for bus_id in ids]

    best_diff = min(modulo_ids)
    best_id = ids[modulo_ids.index(best_diff)]

    return best_id * best_diff


def part2(bus_schedule: str) -> int:
    all_ids = [int(bus_id) if bus_id != 'x' else 0 for bus_id in bus_schedule.split(',')]
    known_ids = [bus_id for bus_id in all_ids if bus_id > 0]

    modulo = 1
    for bus_id in known_ids:
        modulo *= bus_id

    modulas = [modulo // bus_id for bus_id in known_ids]
    modular_inverses = [_modular_inverse(modulo, bus_id) for modulo, bus_id in zip(modulas, known_ids)]

    t = 0
    j = 0
    for i, bus_id in enumerate(all_ids):
        if bus_id == 0:
            continue
        t += (bus_id - i) * modulas[j] * modular_inverses[j]
        j += 1

    return t % modulo


def _gcd_extended(a, b):
    if a == 0:
        return b, 0, 1

    gcd, x_, y_ = _gcd_extended(b % a, a)

    x = y_ - (b // a) * x_
    y = x_

    return gcd, x, y


def _modular_inverse(a, m):
    gcd, x, y = _gcd_extended(a, m)
    if gcd != 1:
        raise ValueError('No solutions: both "a" and "m" should be prime numbers.')

    x = (x % m + m) % m
    return x


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(295, part1(939, '7,13,x,x,59,x,31,19'))

test(6, part2('3, 7'))
test(174, part2('3, 7, 11'))
test(1068781, part2('7,13,x,x,59,x,31,19'))
test(3417, part2('17,x,13,19'))
test(754018, part2('67,7,59,61'))
test(779210, part2('67,x,7,59,61'))
test(1261476, part2('67,7,x,59,61'))
test(1202161486, part2('1789,37,47,1889'))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    timestamp = int(f.readline().strip())
    input_data = f.readline().strip()

    print('Day 13, part 1: %r' % (part1(timestamp, input_data)))
    print('Day 13, part 2: %r' % (part2(input_data)))
