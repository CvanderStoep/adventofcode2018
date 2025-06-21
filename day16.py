from typing import Dict
import re
from z3 import *



def read_and_parse_input(file_name: str) -> tuple[list[dict[int, int]], list[dict[int, int]], list[list[int]]]:
    all_registers_before = []
    all_registers_after = []
    all_instructions = []

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

def process_instruction(opcode: str, instructions: list, register: Dict) -> None:
    A, B, C = instructions[1:]
    if opcode == 'addr':
        register[C] = register[A] + register[B]
    if opcode == 'addi':
        register[C] = register[A] + B
    if opcode == 'mulr':
        register[C] = register[A] * register[B]
    if opcode == 'muli':
        register[C] = register[A] * B
    if opcode == 'banr':
        register[C] = register[A] & register[B]
    if opcode == 'bani':
        register[C] = register[A] & B
    if opcode == 'borr':
        register[C] = register[A] | register[B]
    if opcode == 'bori':
        register[C] = register[A] | B
    if opcode == 'setr':
        register[C] = register[A]
    if opcode == 'seti':
        register[C] = A
    if opcode == 'gtir':
        register[C] = int(A > register[B])
    if opcode == 'gtri':
        register[C] = int(register[A] > B)
    if opcode == 'gtrr':
        register[C] = int(register[A] > register[B])
    if opcode == 'eqir':
        register[C] = int(A == register[B])
    if opcode == 'eqri':
        register[C] = int(register[A] == B)
    if opcode == 'eqrr':
        register[C] = int(register[A] == register[B])

def read_test_program_part2(file_name: str) -> list[list[int]]:
    with open(file_name) as f:
        lines = f.read().strip().split('\n')

    # Find the index of the first empty line after all samples
    for i in range(len(lines)):
        if lines[i].strip() == '' and i + 1 < len(lines) and lines[i + 1].strip() == '':
            test_program_lines = lines[i + 2:]
            break
    else:
        test_program_lines = []

    # Convert the test program lines into a list of instructions
    test_program = [list(map(int, line.split())) for line in test_program_lines if line.strip()]
    return test_program

def compute_part_one(file_name: str) -> str:
    all_registers_before, all_registers_after, all_instructions = read_and_parse_input(file_name)
    count_gt_3 = 0
    for register_before, register_after, instructions in zip(all_registers_before, all_registers_after, all_instructions):
        matches = 0

        opcodes = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr',
                   'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

        for opcode in opcodes:
            register = register_before.copy()
            process_instruction(opcode, instructions, register)
            if register_after == register:
                matches += 1
        if matches >= 3:
            count_gt_3 += 1

    return f'{count_gt_3= }'

def compute_part_two(file_name: str) -> str:
    all_registers_before, all_registers_after, all_instructions = read_and_parse_input(file_name)
    opcodes = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr',
               'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']
    all_instructions_part2 = read_test_program_part2(file_name)
    opcodes_vars = [Int(opcodes[i]) for i in range(len(opcodes))]
    solver = Solver()

    for register_before, register_after, instructions in zip(all_registers_before, all_registers_after, all_instructions):
        count_opcode = 0

        opcode_possibilities = dict()
        for opcode in opcodes:
            register = register_before.copy()
            process_instruction(opcode, instructions, register)
            if register_after == register:
                count_opcode += 1
                opcode_possibilities[opcode]=instructions[0]
        solver.add(Or(opcodes_vars[opcodes.index(key)] == instructions[0] for key, value in opcode_possibilities.items()))


    if solver.check() == z3.sat:
        model = solver.model()
        instr_to_opcode = {str(var): model[var].as_long() for var in model}
        opcode_to_instr = {v: k for k, v in instr_to_opcode.items()}
    else:
        print("No solution")

    register = {0: 0, 1: 0, 2: 0, 3: 0}
    for instructions in all_instructions_part2:
        process_instruction(opcode_to_instr[instructions[0]], instructions, register)

    return f'{register[0]= }'


if __name__ == '__main__':
    file_name = 'input/input16.txt'
    print(f"Part I: {compute_part_one(file_name)}")
    print(f"Part II: {compute_part_two(file_name)}")