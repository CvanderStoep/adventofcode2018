from typing import Dict, Any


def read_and_parse_input(file_name: str) -> tuple[int, list[Any]]:
    all_instructions = []

    with open(file_name) as f:
        lines = f.read().strip().split('\n')

    i = 0
    while i < len(lines):
        if lines[i].startswith("#"):
            register_bound = lines[i].split()[1]
        else:
            parts = lines[i].split()
            converted = [parts[0]] + [int(x) for x in parts[1:]]
            all_instructions.append(converted)
        i += 1

    return int(register_bound), all_instructions

def process_instruction(opcode: str, instructions: list, register: Dict) -> None:
    A, B, C = instructions
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


def compute_part_one(file_name: str) -> str:
    register_bound, all_instructions = read_and_parse_input(file_name)
    register = {0: 0, 1: 0, 2: 0, 3: 0, 4:0, 5: 0}

    print(register_bound, all_instructions)
    ip = 0
    while ip < len(all_instructions):
        register[register_bound] = ip
        instruction = all_instructions[ip]
        opcode = instruction[0]
        instructions = instruction[1:]
        process_instruction(opcode, instructions, register)
        ip = register[register_bound]
        ip += 1
        # print(ip)

    print(f"{opcode, instructions, register= }")

    return f'{register[0]= }'

# solution found via reddit & GitHub
# part 2 actually calculated the sum of the factors of a value that is kept in register[3]
def compute_part_two():
    part2_target = 10551408  #this is the value of register[3] after init.
    # Fast mode, sum the factors of the number.
    def get_factors(num):
        factors = []
        for i in range(1, int(num ** .5) + 1):
            if num % i == 0:
                factors.append(i)
                if i != num // i:
                    factors.append(num // i)
        return sorted(factors)

    return sum(get_factors(part2_target))

if __name__ == '__main__':
    file_name = 'input/input19.txt'
    print(f"Part I: {compute_part_one(file_name)}")
    print(f"Part II: {compute_part_two()}")
