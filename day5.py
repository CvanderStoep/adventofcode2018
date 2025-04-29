import string

def read_input_file(file_name: str) -> str:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content[0]

def reduce_polymer(polymer: str) -> str:
    reduced = True
    while reduced:
        reduced = False
        for position in range(len(polymer)-1):
            char1 = polymer[position]
            char2 = polymer[position + 1]
            c1 = char1.lower()
            c2 = char2.lower()
            if c1 == c2 and char1 != char2:
                polymer = polymer[:position] + polymer[position+2:]
                reduced = True
                break

    return polymer

def reduce_polymer_fast(polymer: str) -> str:
    stack = []
    for char in polymer:
        if stack and abs(ord(stack[-1]) - ord(char)) == 32:  # Check polarity reaction
            stack.pop()
        else:
            stack.append(char)
    return "".join(stack)


def compute_part_one(file_name: str) -> str:
    polymer = read_input_file(file_name)
    print(f'{polymer= }')
    polymer = reduce_polymer_fast(polymer)
    return f'reduced {len(polymer)= }'


def compute_part_two(file_name: str) -> str:
    polymer = read_input_file(file_name)

    min_length = len(polymer)
    for letter in string.ascii_lowercase:
        modified_polymer = polymer.replace(letter, '').replace(letter.upper(), '')
        modified_polymer = reduce_polymer_fast(modified_polymer)
        min_length = min(min_length, len(modified_polymer))

    return f'polymer reduced minimum length= {min_length}'


if __name__ == '__main__':
    file_path = 'input/input5.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")