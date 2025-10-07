from collections import Counter
from itertools import count
from typing import Any

def read_input_file(file_name: str) -> dict[tuple[Any, Any], str]:
    with open(file_name) as f:
        content = f.read().splitlines()
    lumber_area = dict()
    for y, line in enumerate(content):
        for x, char in enumerate(line):
            lumber_area[(x,y)] = char
    return lumber_area

def get_neighbors(area: dict, location: tuple) -> list:
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]
    x, y = location
    xs = [x for x,y in area.keys()]
    ys = [y for x,y in area.keys()]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if min_x <= nx <= max_x and min_y <= ny <= max_y:
            neighbors.append((nx, ny))
    return neighbors

def print_area(area: dict) -> None:
    # Extract all x and y coordinates from the area keys
    x_coords = [x for x, _ in area]
    y_coords = [y for _, y in area]

    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # Print the area row by row
    for y in range(min_y, max_y + 1):
        row = ''.join(area.get((x, y), ' ') for x in range(min_x, max_x + 1))
        print(row)
    print()

def update_state(area: dict) -> dict:

    new_area = dict()
    for (x, y) in area.keys():
        neighbors = get_neighbors(area, (x,y))
        surroundings = Counter([area[n] for n in neighbors])
        # print(x, y, surroundings)
        if area[(x, y)] == '.':
            if surroundings['|'] >= 3:
                new_area[(x, y)] = '|'
            else:
                new_area[(x, y)] = area[(x, y)]
        if area[(x, y)] == '|':
            if surroundings['#'] >= 3:
                new_area[(x, y)] = '#'
            else:
                new_area[(x, y)] = area[(x, y)]
        if area[(x, y)] == '#':
            if surroundings['#'] >= 1 and surroundings['|'] >= 1:
                new_area[(x, y)] = area[(x, y)]
            else:
                new_area[(x, y)] = '.'
    return new_area

def compute_part_one(file_name: str) -> str:
    lumber_area = read_input_file(file_name)
    print(f'{lumber_area= }')
    print(get_neighbors(lumber_area, (0,0)))
    print_area(lumber_area)

    for t in range(1, 11):
        lumber_area = update_state(lumber_area)
        print(f'After {t } minutes:')
        print_area(lumber_area)

    counter = Counter(lumber_area.values())
    print(counter)
    wood = counter['|']
    lumberyard = counter['#']

    return f'{wood * lumberyard= }'

def compute_part_two(file_name: str) -> str:
    lumber_area = read_input_file(file_name)
    print(f'{lumber_area= }')
    print(get_neighbors(lumber_area, (0,0)))
    print_area(lumber_area)

    history = []
    seen_states = set()
    for time in count(1):
        lumber_area = update_state(lumber_area)
        print(f'After {time } minutes:')
        # print_area(lumber_area)
        state_key = frozenset(lumber_area.items())
        if state_key in seen_states:
            print(f"Cycle detected at time {time}")
            break
        seen_states.add(state_key)
        history.append((time, lumber_area.copy()))  # store a copy to preserve the state

    counter = Counter(lumber_area.values())
    print(counter)
    wood = counter['|']
    lumberyard = counter['#']

    return f'{wood * lumberyard= }'


if __name__ == '__main__':
    file_path = 'input/input18.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")

