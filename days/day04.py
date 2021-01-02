import os
import re


def part1(passport_data: str) -> int:
    passports = [p.replace('\n', ' ') for p in passport_data.split('\n\n')]
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    valid = 0

    for passport in passports:
        fields = set(re.findall(r'([a-z]{3}):', passport))
        if len(required_fields.difference(fields)) == 0:
            valid += 1

    return valid


def part2(passport_data: str) -> int:
    passports = [p.replace('\n', ' ') for p in passport_data.split('\n\n')]
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    valid = 0

    for passport in passports:
        fields = set(re.findall(r'([a-z]{3}):', passport))
        if len(required_fields.difference(fields)) > 0:
            continue

        for field in passport.split():
            fld, val = field.split(':')
            if not _validate(fld, val):
                valid -= 1
                break

        valid += 1

    return valid


def _validate(field: str, value: str) -> bool:
    if field == 'byr':
        return len(value) == 4 and 1920 <= int(value) <= 2002

    if field == 'iyr':
        return len(value) == 4 and 2010 <= int(value) <= 2020

    if field == 'eyr':
        return len(value) == 4 and 2020 <= int(value) <= 2030

    if field == 'hgt':
        return len(value) > 2 and (value[-2:] == 'cm' and 150 <= int(value[:-2]) <= 193
                                   or value[-2:] == 'in' and 59 <= int(value[:-2]) <= 76)

    if field == 'hcl':
        return len(value) == 7 and re.match(r'#[0-9a-f]{6}', value)

    if field == 'ecl':
        return value in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

    if field == 'pid':
        return len(value) == 9 and re.match(r'[0-9]{9}', value)

    if field == 'cid':
        return True


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(2, part1("""
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""))

test(4, part2("""
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""))


file_path = os.path.join(os.path.dirname(__file__), 'inputs/day04.txt')
with open(file_path, 'r') as f:
    input_data = f.read()

    print('Day 04, part 1: %r' % (part1(input_data)))
    print('Day 04, part 2: %r' % (part2(input_data)))
