import os
from collections import defaultdict

from typing import List, Tuple, Set


# Coordinates image: http://devmag.org.za/blog/wp-content/uploads/2013/08/screen_136.png
DIRECTIONS_TO_COORDS = {
    'e': (1, 0),
    'se': (1, -1),
    'sw': (0, -1),
    'w': (-1, 0),
    'nw': (-1, 1),
    'ne': (0, 1),
}


def part1(tiles_list: List[str]) -> int:
    black_tiles = _parse_tiles_list(tiles_list)
    return len(black_tiles)


def part2(tiles_list: List[str], days: int) -> int:
    black_tiles = _parse_tiles_list(tiles_list)

    for day in range(1, days + 1):
        black_tiles = _generate_next_state(black_tiles)

    return len(black_tiles)


def _generate_next_state(black_tiles: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    new_black_tiles = set()
    adjacent_white_tiles = defaultdict(int)

    for x, y in black_tiles:
        adjacent = 0
        for v in DIRECTIONS_TO_COORDS.values():
            coord = (x + v[0], y + v[1])
            if coord in black_tiles:
                adjacent += 1
            else:
                adjacent_white_tiles[coord] += 1

        if adjacent == 1 or adjacent == 2:
            new_black_tiles.add((x, y))

    for coord, amount in adjacent_white_tiles.items():
        if amount == 2:
            new_black_tiles.add(coord)

    return new_black_tiles


def _parse_tiles_list(tiles_list: List[str]) -> Set[Tuple[int, int]]:
    black_tiles = set()

    for line in tiles_list:
        x, y, i = 0, 0, 0

        while i < len(line):
            ch = line[i]
            if ch in 'sn':
                i += 1
                ch += line[i]
            dx, dy = DIRECTIONS_TO_COORDS[ch]
            x += dx
            y += dy
            i += 1

        if (x, y) in black_tiles:
            black_tiles.remove((x, y))
        else:
            black_tiles.add((x, y))

    return black_tiles


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test_input_data = [
    'sesenwnenenewseeswwswswwnenewsewsw',
    'neeenesenwnwwswnenewnwwsewnenwseswesw',
    'seswneswswsenwwnwse',
    'nwnwneseeswswnenewneswwnewseswneseene',
    'swweswneswnenwsewnwneneseenw',
    'eesenwseswswnenwswnwnwsewwnwsene',
    'sewnenenenesenwsewnenwwwse',
    'wenwwweseeeweswwwnwwe',
    'wsweesenenewnwwnwsenewsenwwsesesenwne',
    'neeswseenwwswnwswswnw',
    'nenwswwsewswnenenewsenwsenwnesesenew',
    'enewnwewneswsewnwswenweswnenwsenwsw',
    'sweneswneswneneenwnewenewwneswswnese',
    'swwesenesewenwneswnwwneseswwne',
    'enesenwswwswneneswsenwnewswseenwsese',
    'wnwnesenesenenwwnenwsewesewsesesew',
    'nenewswnwewswnenesenwnesewesw',
    'eneswnwswnwsenenwnwnwwseeswneewsenese',
    'neswnwewnwnwseenwseesewsenwsweewe',
    'wseweeenwnesenwwwswnew',
]

test(10, part1(test_input_data))
test(2208, part2(test_input_data, days=100))


file_path = os.path.join(os.path.dirname(__file__), 'inputs/day24.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 24, part 1: %r' % (part1(input_data)))
    print('Day 24, part 2: %r' % (part2(input_data, days=100)))
