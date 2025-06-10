from collections import defaultdict

def read_input_file(file_name: str) -> tuple:
    with open(file_name) as f:
        left, right = f.read().split('\n\n')
        left = left.split(' ')[2]
        right = right.splitlines()
    notes = {l: r for l, r in (line.split(' => ') for line in right)}
    return left, notes

def compute_plant_growth(file_name: str, generations: int) -> int:
    state, notes = read_input_file(file_name)
    plants = {i for i, c in enumerate(state) if c == '#'}
    prev_offset = 0

    for gen in range(generations):
        new_plants = set()
        min_index, max_index = min(plants) - 2, max(plants) + 2

        for i in range(min_index, max_index + 1):
            segment = ''.join('#' if j in plants else '.' for j in range(i - 2, i + 3))
            if notes.get(segment, '.') == '#':
                new_plants.add(i)

        offset_shift = min(new_plants) - min(plants)
        if new_plants == {p + offset_shift for p in plants}:
            return sum(p + (generations - gen - 1) * offset_shift for p in new_plants)

        plants = new_plants

    return sum(plants)

if __name__ == '__main__':
    file_path = 'input/input12.txt'
    print(f"Part I: {compute_plant_growth(file_path, 20)}")
    print(f"Part II: {compute_plant_growth(file_path, 50000000000)}")
