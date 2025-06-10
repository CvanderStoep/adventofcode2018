from collections import defaultdict
from dataclasses import dataclass
from typing import Any, List


@dataclass
class Cart:
    x: int
    y: int
    direction: tuple
    turn: int
    active: bool = True  # Flag to determine if a cart is still operational



def read_input_file(file_name: str) -> defaultdict[Any, str]:
    with open(file_name) as f:
        content = f.read().splitlines()
    grid = defaultdict(str)
    for y, line in enumerate(content):
        for x, letter in enumerate(line):
            grid[(x, y)] = letter
    return grid


def find_carts(grid: defaultdict) -> List[Cart]:
    directions = {'>': (1, 0), '<': (-1, 0), 'v': (0, 1), '^': (0, -1)}
    carts = []
    for (x, y), value in grid.items():
        if value in directions:
            carts.append(Cart(x, y, directions[value], turn=-1))
            grid[(x, y)] = '-' if value in '<>' else '|'
    return carts

def move_carts(grid: defaultdict, carts: List[Cart]) -> None:
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    carts.sort(key=lambda cart: (cart.y, cart.x))  # Ensure correct move order

    for cart in carts: #sorted_carts:
        if not cart.active:
            continue

        dx, dy = cart.direction
        x, y = cart.x, cart.y
        nx, ny = x + dx, y + dy

        # Collision detection
        if any(c.x == nx and c.y == ny and c.active for c in carts):
            print(f"Collision at {nx},{ny}")
            cart.active = False
            for c in carts:
                if c.x == nx and c.y == ny:
                    c.active = False


        cart.x, cart.y = nx, ny
        track = grid[(nx, ny)]

        curve_map = {
            '\\': {(1, 0): (0, 1), (-1, 0): (0, -1), (0, 1): (1, 0), (0, -1): (-1, 0)},
            '/': {(1, 0): (0, -1), (-1, 0): (0, 1), (0, 1): (-1, 0), (0, -1): (1, 0)}
        }
        if track in curve_map:
            cart.direction = curve_map[track][cart.direction]

        # Handle intersections
        elif track == '+':
            direction_index = directions.index(cart.direction)
            if cart.turn == -1:
                direction_index = (direction_index - 1) % 4  # Left turn
                cart.turn = 0
            elif cart.turn == 0:
                cart.turn = 1  # Continue straight
            elif cart.turn == 1:
                direction_index = (direction_index + 1) % 4  # Right turn
                cart.turn = -1
            cart.direction = directions[direction_index]


def print_grid(grid: defaultdict, carts: list) -> None:
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    for x, y in grid.keys():
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            character = grid[(x,y)]
            for cart in carts:
                if (x, y) == (cart.x, cart.y):
                    character = 'C'
            print(character, end='')
        print()


def compute_part(file_name: str) -> str:
    grid = read_input_file(file_name)
    carts = find_carts(grid)

    while len([c for c in carts if c.active]) > 1:
        move_carts(grid, carts)

    last_cart = next(c for c in carts if c.active)
    return f"Part II: {last_cart.x},{last_cart.y}"




if __name__ == '__main__':
    file_path = 'input/input13.txt'
    print('Part I:')
    print(f"{compute_part(file_path)}")
