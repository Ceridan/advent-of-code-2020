import os
import re
from collections import defaultdict

from typing import List, Set, Dict, Tuple


def part1(food_recipes: List[str]) -> int:
    ingredients, allergens = _parse_recipes(food_recipes)

    possible_contain_allergens = set()
    for allergen_ingredients in allergens.values():
        possible_contain_allergens.update(allergen_ingredients)

    good_count = 0
    for ingredient, amount in ingredients.items():
        if ingredient not in possible_contain_allergens:
            good_count += amount

    return good_count


def part2(food_recipes: List[str]) -> str:
    _, allergens = _parse_recipes(food_recipes)

    allergens_count = len(allergens)
    single_ingredient_allergens = {}

    while len(single_ingredient_allergens) < allergens_count:
        for allergen, allergen_ingredients in sorted(allergens.items(), key=lambda item: len(item[1])):
            if len(allergen_ingredients) == 1:
                ingredient = list(allergen_ingredients)[0]
                for other_allergen in allergens:
                    if allergen != other_allergen and ingredient in allergens[other_allergen]:
                        allergens[other_allergen].remove(ingredient)
                single_ingredient_allergens[allergen] = ingredient
                del allergens[allergen]

    bad_ingredients = []

    for allergen, ingredient in sorted(single_ingredient_allergens.items(), key=lambda item: item[0]):
        bad_ingredients.append(ingredient)

    return ','.join(bad_ingredients)


def _parse_recipes(food_recipes: List[str]) -> Tuple[Dict[str, int], Dict[str, Set[str]]]:
    ingredients = defaultdict(int)
    allergens = {}

    for line in food_recipes:
        line = line.strip()

        items = re.findall(r'([a-z]+)', line)
        possible_allergen_ingredients = []
        mode = 0

        for item in items:
            if item == 'contains':
                mode = 1
                continue

            if mode == 0:
                possible_allergen_ingredients.append(item)
                ingredients[item] += 1
            else:
                if item not in allergens:
                    allergens[item] = set(possible_allergen_ingredients)
                else:
                    allergens[item] = allergens[item].intersection(possible_allergen_ingredients)

    return ingredients, allergens


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(5, part1([
    'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
    'trh fvjkl sbzzf mxmxvkd (contains dairy)',
    'sqjhc fvjkl (contains soy)',
    'sqjhc mxmxvkd sbzzf (contains fish)',
]))

test('mxmxvkd,sqjhc,fvjkl', part2([
    'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
    'trh fvjkl sbzzf mxmxvkd (contains dairy)',
    'sqjhc fvjkl (contains soy)',
    'sqjhc mxmxvkd sbzzf (contains fish)',
]))


file_path = os.path.join(os.path.dirname(__file__), 'inputs/day21.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 21, part 1: %r' % (part1(input_data)))
    print('Day 21, part 2: %r' % (part2(input_data)))
