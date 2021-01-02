import os

from typing import Tuple, Dict


def part1(cubes_data: str, cycles: int) -> int:
    dimensions, initial_size = _parse_data(cubes_data, dimension_size=3)

    size = {
        'x': [initial_size[0][0], initial_size[0][1]],
        'y': [initial_size[1][0], initial_size[1][1]],
        'z': [initial_size[2][0], initial_size[2][1]],
    }

    cycle_count = 0
    next_dimensions = {}
    new_size = {'x': [], 'y': [], 'z': []}

    for cycle in range(cycles):
        cycle_count = 0

        if not size['x'] or not size['y'] or not size['z']:
            continue

        z_min, z_max = size['z'][0] - 1, size['z'][1] + 1
        y_min, y_max = size['y'][0] - 1, size['y'][1] + 1
        x_min, x_max = size['x'][0] - 1, size['x'][1] + 1

        for z in range(z_min, z_max + 1):
            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    new_state = _apply_conway_rule_d3((x, y, z), dimensions)

                    if new_state:
                        cycle_count += 1
                        if z not in next_dimensions:
                            next_dimensions[z] = {}
                        if y not in next_dimensions[z]:
                            next_dimensions[z][y] = {}
                        next_dimensions[z][y][x] = 1

                        new_size['x'] = [min(x, new_size['x'][0]), max(x, new_size['x'][1])] if new_size['x'] else [x, x]
                        new_size['y'] = [min(y, new_size['y'][0]), max(y, new_size['y'][1])] if new_size['y'] else [y, y]
                        new_size['z'] = [min(z, new_size['z'][0]), max(x, new_size['z'][1])] if new_size['z'] else [z, z]

        dimensions = next_dimensions
        size = new_size

        next_dimensions = {}
        new_size = {'x': [], 'y': [], 'z': []}

    return cycle_count


def part2(cubes_data: str, cycles: int) -> int:
    dimensions, initial_size = _parse_data(cubes_data, dimension_size=4)

    size = {
        'x': [initial_size[0][0], initial_size[0][1]],
        'y': [initial_size[1][0], initial_size[1][1]],
        'z': [initial_size[2][0], initial_size[2][1]],
        'w': [initial_size[3][0], initial_size[3][1]],
    }

    cycle_count = 0
    next_dimensions = {}
    new_size = {'x': [], 'y': [], 'z': [], 'w': []}

    for cycle in range(cycles):
        cycle_count = 0

        if not size['x'] or not size['y'] or not size['z'] or not size['w']:
            continue

        w_min, w_max = size['w'][0] - 1, size['w'][1] + 1
        z_min, z_max = size['z'][0] - 1, size['z'][1] + 1
        y_min, y_max = size['y'][0] - 1, size['y'][1] + 1
        x_min, x_max = size['x'][0] - 1, size['x'][1] + 1

        for w in range(w_min, w_max + 1):
            for z in range(z_min, z_max + 1):
                for y in range(y_min, y_max + 1):
                    for x in range(x_min, x_max + 1):
                        new_state = _apply_conway_rule_d4((x, y, z, w), dimensions)

                        if new_state:
                            cycle_count += 1
                            if w not in next_dimensions:
                                next_dimensions[w] = {}
                            if z not in next_dimensions[w]:
                                next_dimensions[w][z] = {}
                            if y not in next_dimensions[w][z]:
                                next_dimensions[w][z][y] = {}
                            next_dimensions[w][z][y][x] = 1

                            new_size['x'] = [min(x, new_size['x'][0]), max(x, new_size['x'][1])] if new_size['x'] else [x, x]
                            new_size['y'] = [min(y, new_size['y'][0]), max(y, new_size['y'][1])] if new_size['y'] else [y, y]
                            new_size['z'] = [min(z, new_size['z'][0]), max(x, new_size['z'][1])] if new_size['z'] else [z, z]
                            new_size['w'] = [min(w, new_size['w'][0]), max(w, new_size['w'][1])] if new_size['w'] else [w, w]

        dimensions = next_dimensions
        size = new_size

        next_dimensions = {}
        new_size = {'x': [], 'y': [], 'z': [], 'w': []}

    return cycle_count


def _apply_conway_rule_d3(point: Tuple[int, int, int], dimensions: Dict[int, Dict[int, Dict[int, int]]]) -> int:
    x, y, z = point
    state = dimensions[z][y][x] if z in dimensions and y in dimensions[z] and x in dimensions[z][y] else 0
    active_count = 0 if state == 0 else -1

    for z_ in [z - 1, z, z + 1]:
        if z_ not in dimensions:
            continue
        for y_ in [y - 1, y, y + 1]:
            if y_ not in dimensions[z_]:
                continue
            for x_ in [x - 1, x, x + 1]:
                if x_ not in dimensions[z_][y_]:
                    continue
                active_count += dimensions[z_][y_][x_]

    if state == 0 and active_count == 3:
        return 1
    elif state == 1 and active_count in [2, 3]:
        return 1

    return 0


def _apply_conway_rule_d4(point: Tuple[int, int, int, int], dimensions: Dict) -> int:
    x, y, z, w = point
    state = dimensions[w][z][y][x] if w in dimensions and z in dimensions[w] and y in dimensions[w][z] and x in dimensions[w][z][y] else 0
    active_count = 0 if state == 0 else -1

    for w_ in [w - 1, w, w + 1]:
        if w_ not in dimensions:
            continue
        for z_ in [z - 1, z, z + 1]:
            if z_ not in dimensions[w_]:
                continue
            for y_ in [y - 1, y, y + 1]:
                if y_ not in dimensions[w_][z_]:
                    continue
                for x_ in [x - 1, x, x + 1]:
                    if x_ not in dimensions[w_][z_][y_]:
                        continue
                    active_count += dimensions[w_][z_][y_][x_]

    if state == 0 and active_count == 3:
        return 1
    elif state == 1 and active_count in [2, 3]:
        return 1

    return 0


def _parse_data(cubes_data: str, dimension_size: int) -> Tuple[Dict, Tuple]:
    dimensions = {}
    current_dimension = dimensions
    sizes = []

    for i in range(dimension_size - 2):
        current_dimension[0] = {}
        current_dimension = current_dimension[0]
        sizes.append((0, 0))

    x_size = 0
    y = 0
    for line in cubes_data.split('\n'):
        line = line.strip()
        if not line:
            continue

        current_dimension[y] = {}
        x_size = len(line) - 1

        for x, ch in enumerate(line):
            if ch == '#':
                current_dimension[y][x] = 1

        y += 1

    return dimensions, ((0, x_size), (0, y - 1), *sizes)


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(112, part1("""
.#.
..#
###
""", cycles=6))


test(848, part2("""
.#.
..#
###
""", cycles=6))


file_path = os.path.join(os.path.dirname(__file__), 'inputs/day17.txt')
with open(file_path, 'r') as f:
    input_data = f.read()

    print('Day 17, part 1: %r' % (part1(input_data, cycles=6)))
    print('Day 17, part 2: %r' % (part2(input_data, cycles=6)))
