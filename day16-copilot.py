# Below code was improved by Copilot after submitting the code in day-16
from typing import Dict
import re
from z3 import *

def read_and_parse_input(file_name: str) -> tuple[list[dict[int, int]], list[dict[int, int]], list[list[int]]]:
    all_registers_before, all_registers_after, all_instructions = [], [], []

    with open(file_name) as f:
        lines = f.read().strip().split('\n')

    i = 0
    while i < len(lines):
        if lines[i].startswith("Before"):
            before = list(map(int, re.findall(r'\d+', lines[i])))
            instr = list(map(int, lines[i+1].split()))
            after = list(map(int, re.findall(r'\d+', lines[i+2])))

            all_registers_before.append({idx: val for idx, val in enumerate(before)})
            all_registers_after.append({idx: val for idx, val in enumerate(after)})
            all_instructions.append(instr)
            i += 3
        else:
            i += 1

    return all_registers_before, all_registers_after, all_instructions

def process_instruction(opcode: str, instructions: list[int], register: Dict[int, int]) -> None:
    A, B, C = instructions[1:]
    ops = {
        'addr': lambda: register[A] + register[B],
        'addi': lambda: register[A] + B,
        'mulr': lambda: register[A] * register[B],
        'muli': lambda: register[A] * B,
        'banr': lambda: register[A] & register[B],
        'bani': lambda: register[A] & B,
        'borr': lambda: register[A] | register[B],
        'bori': lambda: register[A] | B,
        'setr': lambda: register[A],
        'seti': lambda: A,
        'gtir': lambda: int(A > register[B]),
        'gtri': lambda: int(register[A] > B),
        'gtrr': lambda: int(register[A] > register[B]),
        'eqir': lambda: int(A == register[B]),
        'eqri': lambda: int(register[A] == B),
        'eqrr': lambda: int(register[A] == register[B])
    }
    register[C] = ops[opcode]()

def read_test_program_part2(file_name: str) -> list[list[int]]:
    with open(file_name) as f:
        lines = f.read().strip().split('\n')

    for i in range(len(lines)):
        if lines[i].strip() == '' and i + 1 < len(lines) and lines[i + 1].strip() == '':
            return [list(map(int, line.split())) for line in lines[i + 2:] if line.strip()]
    return []

def compute_part_one(file_name: str) -> str:
    befores, afters, instructions_list = read_and_parse_input(file_name)
    opcodes = [
        'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
        'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'
    ]

    count_gt_3 = 0
    for before, after, instr in zip(befores, afters, instructions_list):
        matches = 0
        for opcode in opcodes:
            reg_copy = before.copy()
            process_instruction(opcode, instr, reg_copy)
            if reg_copy == after:
                matches += 1
        if matches >= 3:
            count_gt_3 += 1

    return f'{count_gt_3=}'

def compute_part_two(file_name: str) -> str:
    befores, afters, instructions_list = read_and_parse_input(file_name)
    test_program = read_test_program_part2(file_name)

    opcodes = [
        'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
        'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'
    ]
    opcode_vars = {name: Int(f'op_{i}') for i, name in enumerate(opcodes)}

    solver = Solver()
    constraints = []
    for before, after, instr in zip(befores, afters, instructions_list):
        candidates = []
        for opcode in opcodes:
            reg_copy = before.copy()
            process_instruction(opcode, instr, reg_copy)
            if reg_copy == after:
                candidates.append(opcode_vars[opcode] == instr[0])
        solver.add(Or(*candidates))

    solver.add(Distinct(*opcode_vars.values()))

    if solver.check() != sat:
        return "No solution"

    model = solver.model()
    instr_to_opcode = {model[var].as_long(): name for name, var in opcode_vars.items()}

    register = {0: 0, 1: 0, 2: 0, 3: 0}
    for instr in test_program:
        opcode_name = instr_to_opcode[instr[0]]
        process_instruction(opcode_name, instr, register)

    return f'{register[0]=}'

if __name__ == '__main__':
    file_path = 'input/input16.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")
