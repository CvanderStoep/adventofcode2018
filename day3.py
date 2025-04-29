import re
from collections import defaultdict


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        claims = [line.strip() for line in f]

    return claims

def process_claim(claim, fabric):
    id, x, y, dx, dy = map(int, re.findall(r'(\d+)', claim))
    for i in range(x, x + dx):
        for j in range(y, y + dy):
            fabric[(i, j)].append(id)

def compute_part_one(file_name: str) -> str:
    claims = read_input_file(file_name)
    fabric = defaultdict(list)
    for claim in claims:
        process_claim(claim, fabric)

    overlap_count = 0
    overlaps = set()
    for z in fabric.values():
        if len(z) > 1:
            overlap_count += 1
            overlaps.update(z)

    print(f'part I: number of overlaps = {overlap_count}')

    for i in range(min(overlaps), max(overlaps) + 1):
        if i not in overlaps:
            print(f'part II: ID {i} does not overlap')



if __name__ == '__main__':
    file_path = 'input/input3.txt'
    compute_part_one(file_path)
