import os
from collections import namedtuple

from typing import List


Instruction = namedtuple('Instruction', 'id name value')


class VM:
    def __init__(self, program: List[str]):
        self.instructions = self._compile_program(program)
        self.current_position = 0
        self.accumulator = 0

    @property
    def is_terminated(self) -> bool:
        return self.current_position >= len(self.instructions)

    def execute_next(self):
        instruction = self.instructions[self.current_position]

        if instruction.name == 'acc':
            self.accumulator += instruction.value
            self.current_position += 1
        elif instruction.name == 'jmp':
            self.current_position += instruction.value
        elif instruction.name == 'nop':
            self.current_position += 1

    def reset(self):
        self.current_position = 0
        self.accumulator = 0

    def _compile_program(self, program: List[str]) -> List[Instruction]:
        if not program:
            return []

        instructions = []
        for i, line in enumerate(program):
            code, value = line.split()
            instructions.append(Instruction(i, code, int(value)))

        return instructions


def part1(program: List[str]) -> int:
    vm = VM(program)
    executed_ids = set()

    while vm.current_position not in executed_ids:
        executed_ids.add(vm.current_position)
        vm.execute_next()

    return vm.accumulator


def part2(program: List[str]) -> int:
    vm = VM(program)

    for i in range(len(vm.instructions)):
        current = vm.instructions[i]
        if current.name == 'jmp':
            vm.instructions[i] = Instruction(current.id, 'nop', current.value)
        elif current.name == 'nop':
            vm.instructions[i] = Instruction(current.id, 'jmp', current.value)
        else:
            continue

        executed_ids = set()
        while not vm.is_terminated and vm.current_position not in executed_ids:
            executed_ids.add(vm.current_position)
            vm.execute_next()

        if vm.is_terminated:
            return vm.accumulator

        vm.instructions[i] = current
        vm.reset()

    return -1


def test(expected, actual):
    assert expected == actual, f'Expected: {expected}, Actual: {actual}'


test(5, part1([
    'nop +0',
    'acc +1',
    'jmp +4',
    'acc +3',
    'jmp -3',
    'acc -99',
    'acc +1',
    'jmp -4',
    'acc +6',
]))

test(8, part2([
    'nop +0',
    'acc +1',
    'jmp +4',
    'acc +3',
    'jmp -3',
    'acc -99',
    'acc +1',
    'jmp -4',
    'acc +6',
]))


file_path = os.path.join(os.path.dirname(__file__), 'inputs/day08.txt')
with open(file_path, 'r') as f:
    input_data = [line.strip() for line in f.readlines()]

    print('Day 08, part 1: %r' % (part1(input_data)))
    print('Day 08, part 2: %r' % (part2(input_data)))
