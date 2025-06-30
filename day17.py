import re
from collections import defaultdict, deque
from itertools import count


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content

def print_grid(grid: defaultdict, water_spring: tuple, partly: bool = False) -> None:
    xs = [x for x,y in grid.keys()]
    ys = [y for x,y in grid.keys()]
    xw, yw = water_spring
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    if partly:
        minx, maxx, miny, maxy = 450, 550, 0, 100
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if x == xw and y == yw:
                print('+', end='')
            else:
                print(grid[(x,y)], end='')
        print()
    print()

def transform_input_to_grid(slice: list) -> dict:
    grid = defaultdict(lambda: '.')

    for line in slice:
        a, b, c = map(int, re.findall(r'\d+', line))
        if line[0] == 'x':
            for y in range(b, c+1):
                grid[(a, y)] = '#'
        else:
            for x in range(b, c+1):
                grid[(x, a)] = '#'
    return grid

def find_walls(grid: dict, coordinate: tuple, size: tuple ) -> tuple:
    left_wall, right_wall = None, None
    x, y = coordinate
    # xs, ys = zip(*grid.keys())
    min_x, min_y, max_x, max_y = size #min(xs), min(ys), max(xs), max(ys)
    for i in range(x, min_x-1, -1):
        if grid[(i,y)] == '#':
            left_wall = (i, y)
            break
        if grid[(i,y+1)] == '.':
            break
    for i in range(x, max_x+2):
        if grid[(i,y)] == '#':
            right_wall = (i, y)
            break
        if grid[(i,y+1)] == '.':
            break
    return left_wall, right_wall

def grid_size(grid: dict ) -> tuple:

    xs, ys = zip(*grid.keys())
    min_x, min_y, max_x, max_y = min(xs), min(ys), max(xs), max(ys)
    return min_x, min_y, max_x, max_y



def find_edges(grid: dict, coordinate: tuple, size: tuple ) -> tuple:
    left_edge, right_edge = None, None
    x, y = coordinate
    # xs, ys = zip(*grid.keys())
    min_x, min_y, max_x, max_y = size # min(xs), min(ys), max(xs), max(ys)
    for i in range(x, min_x-2, -1):
        if grid[(i,y)] in '.|' and grid[(i, y+1)] == '#':
            left_edge = (i - 1, y)
            break
    for i in range(x, max_x+2):
        if grid[(i,y)] in '.|' and grid[(i, y+1)] == '#':
            right_edge = (i + 1, y)
            break

    return left_edge, right_edge

def water_count(grid: dict) -> int:
    wc = 0
    for c in grid.values():
        if c in '~|':
            wc += 1
    return wc

def fill_water_layer(grid: dict, left_wall: tuple, right_wall: tuple) -> dict:
    xl, xr = left_wall[0], right_wall[0]
    y = left_wall[1]
    for x in range(xl+1, xr):
        grid[(x,y)] = '~'
    return grid

def fill_running_water(grid: dict, left: tuple, right: tuple) -> dict:
    xl, xr = left[0], right[0]
    y = left[1]
    for x in range(xl, xr+1):
        grid[(x,y)] = '|'
    return grid

def below_max_y_value(grid, coordinate: tuple, size: tuple) -> bool:
    x, y = coordinate
    # xs, ys = zip(*grid.keys())
    min_x, min_y, max_x, max_y = size # min(xs), min(ys), max(xs), max(ys)
    if y > max_y:
        return True

    return False

def compute_part_one(file_name: str) -> str:
    content = read_input_file(file_name)
    water_spring = (500, 0)
    queue = deque([water_spring])
    print(f'{content= }')
    grid = transform_input_to_grid(content)
    # print(grid)
    print_grid(grid, water_spring, partly=False)
    # input()
    size = grid_size(grid)
    print(f'{size =}')

    # put water spring in queue
    # find 2 walls and fill level with water
    # otherwise, put left and/or right edge as water spring in queue
    while queue:
        print(f'{len(queue)= }')
        water_spring = queue.popleft()
        for t in count(1):
            grid[water_spring] = '|'
            water_spring = (water_spring[0], water_spring[1] + 1)
            if below_max_y_value(grid, water_spring, size):
                print('program can stop here')
                print_grid(grid, water_spring)
                print(f'{water_count(grid) -1 = }')
                break

            if grid[water_spring] in '~#':
                # print(t, water_spring, grid[water_spring])
                left_wall, right_wall = find_walls(grid, (water_spring[0], water_spring[1] -1), size)
                if left_wall is not None and right_wall is not None:
                    # print(f'{left_wall, right_wall= }')
                    grid = fill_water_layer(grid, left_wall, right_wall)
                    water_spring = (water_spring[0], water_spring[1] - 2)
                    print_grid(grid, water_spring, partly=False)
                    queue.append(water_spring)
                    break
                else:
                    left_edge, right_edge = find_edges(grid, (water_spring[0], water_spring[1] -1), size)
                    print(f'{left_wall, right_wall= }')
                    print(f'{left_edge, right_edge= }')
                    if left_edge is not None:
                        queue.append(left_edge)
                    if right_edge is not None:
                        queue.append(right_edge)
                    if left_edge is not None and right_edge is not None:
                        fill_running_water(grid, left_edge, right_edge)
                    if left_edge is not None and right_wall is not None:
                        fill_running_water(grid, left_edge, (right_wall[0]-1, right_wall[1]))
                    if left_wall is not None and right_edge is not None:
                        fill_running_water(grid, (left_wall[0] +1, left_wall[1]), right_edge)

                    break









    return "part 1 not yet implemented"


def compute_part_two(file_name: str) -> str:
    content = read_input_file(file_name)
    return "part 2 not yet implemented"


if __name__ == '__main__':
    file_path = 'input/input17.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")