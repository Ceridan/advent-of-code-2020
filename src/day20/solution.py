import os
from collections import namedtuple, defaultdict
from copy import deepcopy
from math import sqrt

from typing import List, Dict, Tuple, Set

TileVariants = namedtuple('TileVariants', ['id', 'position'])


class Tile:
    def __init__(self, id_: int, data: List[List[str]]):
        self.id = id_
        self.data = data
        self.borders = {
            'top': int(''.join(self.data[0]), 2),
            'right': int(''.join(list(zip(*self.data))[-1]), 2),
            'bottom': int(''.join(self.data[-1]), 2),
            'left': int(''.join(list(zip(*self.data))[0]), 2),
        }

    @property
    def top(self):
        return self.borders['top']

    @property
    def right(self):
        return self.borders['right']

    @property
    def bottom(self):
        return self.borders['bottom']

    @property
    def left(self):
        return self.borders['left']

    def rotate(self, angle: int) -> 'Tile':
        angle = angle % 360
        data = deepcopy(self.data)

        while angle > 0:
            data = list(zip(*data[::-1]))
            angle -= 90

        return Tile(self.id, data)

    def flip(self) -> 'Tile':
        data = deepcopy(self.data)
        data = data[::-1]
        return Tile(self.id, data)

    def print(self) -> List[str]:
        lines = []
        for line in self.data:
            lines.append(''.join(['#' if ch == '1' else '.' for ch in line]))
        return lines

    def print_without_borders(self) -> List[str]:
        lines = []
        for line in self.data[1:-1]:
            lines.append(''.join(['#' if ch == '1' else '.' for ch in line[1:-1]]))
        return lines

    def __repr__(self):
        return f'{self.id}'


def part1(tile_data: str) -> int:
    tiles = _parse_data(tile_data)
    variants = {}

    for tile in tiles:
        flipped_tile = tile.flip()
        variants[tile.id] = [tile, tile.rotate(90), tile.rotate(180), tile.rotate(270),
                             flipped_tile, flipped_tile.rotate(90), flipped_tile.rotate(180), flipped_tile.rotate(270)]

    neighbors = _possible_neighbors(variants)
    corners = [k for k, v in neighbors.items() if len(v) == 2]

    result = 1
    for tile_id in corners:
        result *= tile_id

    return result


def part2(tile_data: str) -> int:
    tiles = _parse_data(tile_data)
    size = int(sqrt(len(tiles)))
    variants = {}

    for tile in tiles:
        flipped_tile = tile.flip()
        variants[tile.id] = [tile, tile.rotate(90), tile.rotate(180), tile.rotate(270),
                             flipped_tile, flipped_tile.rotate(90), flipped_tile.rotate(180), flipped_tile.rotate(270)]

    neighbors = _possible_neighbors(variants)
    image_tiles = _restore_image(neighbors, variants, size)

    image_repr = '\n'.join(_print_image(image_tiles))
    image = _parse_data(f'Tile 9999:\n{image_repr}\n')[0]
    flipped_image = image.flip()

    image_variants = [image, image.rotate(90), image.rotate(180), image.rotate(270), flipped_image,
                      flipped_image.rotate(90), flipped_image.rotate(180), flipped_image.rotate(270)]

    for variant in image_variants:
        found, habitat = _check_sea_monsters(variant)

        if found:
            return habitat

def _get_sea_monster_offsets() -> List[Tuple[int, int]]:
    sea_monster = """
                  #
#    ##    ##    ###
 #  #  #  #  #  #
    """

    offsets = [
        (-1, 18),
        (0, 0), (0, 5), (0, 6), (0, 11), (0, 12),  (0, 17), (0, 18), (0, 19),
        (1, 1), (1, 4), (1, 7), (1, 10), (1, 13), (1, 16),
    ]

    return offsets


def _check_sea_monsters(image: Tile) -> Tuple[bool, int]:
    habitat = 0
    data = []

    for y in range(len(image.data)):
        data.append([])
        for x in range(len(image.data[0])):
            if image.data[y][x] == '1':
                habitat += 1
                data[y].append('#')
            else:
                data[y].append('.')

    offsets = _get_sea_monster_offsets()
    size = sorted(offsets, key=lambda item: -item[1])[0][1] + 1
    found = False

    for y in range(1, len(data) - 1):
        for x in range(len(data[0]) - size + 1):
            if data[y][x] == '#':
                local_found = True
                for offset in offsets:
                    if data[y + offset[0]][x + offset[1]] != '#':
                        local_found = False
                        break

                if local_found:
                    found = True
                    habitat -= len(offsets)
                    for offset in offsets:
                        data[y + offset[0]][x + offset[1]] = 'O'

    return found, habitat


def _print_image(image: List[List[Tile]]) -> List[str]:
    lines = []

    for y in range(len(image)):
        reprs = [image[y][x].print_without_borders() for x in range(len(image[y]))]
        for k in range(len(reprs[0])):
            line = []
            for r in range(len(reprs)):
                line.append(reprs[r][k])
            lines.append(''.join(line))

    return lines


def _possible_neighbors(variants: Dict[int, List[Tile]]) -> Dict[int, Set[int]]:
    neighbors = defaultdict(set)
    v_keys = sorted(variants.keys())
    for i in range(0, len(v_keys) - 1):
        tile_id = v_keys[i]
        for j in range(i + 1, len(v_keys)):
            other_tile_id = v_keys[j]
            if tile_id == other_tile_id:
                continue
            is_added = False
            for variant in variants[tile_id]:
                if not is_added:
                    for other_variant in variants[other_tile_id]:
                        if not is_added:
                            for border in variant.borders:
                                if not is_added:
                                    for other_border in other_variant.borders:
                                        if variant.borders[border] == other_variant.borders[other_border]:
                                            neighbors[tile_id].add(other_tile_id)
                                            neighbors[other_tile_id].add(tile_id)
                                            is_added = True
                                            break

    return neighbors


def _find_top_left_corner_tile(neighbors: Dict[int, Set[int]], variants: Dict[int, List[Tile]]) -> Tile:
    corners = {k: v for k, v in neighbors.items() if len(v) == 2}
    corner_id = list(corners.keys())[0]
    nbr_1_id, nbr_2_id = list(neighbors[corner_id])

    for corner_variant in variants[corner_id]:
        for variant_1 in variants[nbr_1_id]:
            for variant_2 in variants[nbr_2_id]:
                if corner_variant.right == variant_1.left and corner_variant.bottom == variant_2.top:
                    return corner_variant
                if corner_variant.right == variant_2.left and corner_variant.bottom == variant_1.top:
                    return corner_variant


def _restore_image(neighbors: Dict[int, Set[int]], variants: Dict[int, List[Tile]], size: int) -> List[List[Tile]]:
    image = [[None for _ in range(size)] for _ in range(size)]
    image[0][0] = _find_top_left_corner_tile(neighbors, variants)
    visited = {image[0][0].id}

    for y in range(size):
        for x in range(size):
            if x == 0 and y == 0:
                continue

            neighbor_ids = neighbors[image[y - 1][x].id] if x == 0 else neighbors[image[y][x - 1].id]

            for neighbor_id in neighbor_ids:
                if neighbor_id in visited:
                    continue

                for neighbor_variant in variants[neighbor_id]:
                    if x == 0:
                        if neighbor_variant.top == image[y - 1][x].bottom:
                            image[y][x] = neighbor_variant
                            visited.add(neighbor_variant.id)
                            break

                    elif y == 0:
                        if neighbor_variant.left == image[y][x - 1].right:
                            image[y][x] = neighbor_variant
                            visited.add(neighbor_variant.id)
                            break

                    elif neighbor_variant.left == image[y][x - 1].right and neighbor_variant.top == image[y - 1][x].bottom:
                        image[y][x] = neighbor_variant
                        visited.add(neighbor_variant.id)
                        break

                if image[y][x]:
                    break

    return image


def _parse_data(tile_data: str) -> List[Tile]:
    tiles = []
    current_tile_id = 0
    current_tile = []

    for line in tile_data.split('\n'):
        if not line:
            continue

        if line.startswith('Tile'):
            if current_tile_id:
                tiles.append(Tile(current_tile_id, current_tile))
            current_tile_id = int(line[5:9])
            current_tile = []
        else:
            current_tile.append(['1' if ch == "#" else '0' for ch in line])

    tiles.append(Tile(current_tile_id, current_tile))
    return tiles


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(20899048083289, part1("""
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""))


test(273, part2("""
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""))


file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(file_path, 'r') as f:
    input_data = f.read()

    print('Day 20, part 1: %r' % (part1(input_data)))
    print('Day 20, part 2: %r' % (part2(input_data)))
