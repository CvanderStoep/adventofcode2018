from collections import defaultdict, deque
from typing import Any
import heapq


def read_input_file(file_name: str) -> tuple[int, int, int]:
    with open(file_name) as f:
        lines = f.readlines()

    # Parse the lines
    depth_line = next(line for line in lines if line.startswith("depth:"))
    target_line = next(line for line in lines if line.startswith("target:"))

    # Extract values
    depth = int(depth_line.split(":")[1].strip())
    x, y = map(int, target_line.split(":")[1].split(","))

    return depth, x, y

def calculate_geological_index_and_erosion_level(geological_index, erosion_level, x_target, y_target, depth) -> \
defaultdict[Any, int]:

    buffer = 100  # extra space to allow detours
    max_x, max_y = x_target + buffer, y_target + buffer

    region_type = defaultdict(int)
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if x == y == 0:
                geological_index[(x, y)] = 0
            elif x == x_target and y == y_target:
                geological_index[(x, y)] = 0
            elif y == 0:
                geological_index[(x, y)] = x * 16807
            elif x == 0:
                geological_index[(x, y)] = y * 48271
            else:
                geological_index[(x, y)] = erosion_level[(x-1, y)] * erosion_level[(x, y-1)]

            erosion_level[(x, y)] = (geological_index[(x, y)] + depth) % 20183
            region_type[(x,y)] = erosion_level[(x, y)] % 3
    return region_type

def compute_part_one(file_name: str) -> str:
    depth, x_target, y_target = read_input_file(file_name)
    geological_index = defaultdict(int)
    erosion_level = defaultdict(int)
    region_type = calculate_geological_index_and_erosion_level(geological_index, erosion_level, x_target, y_target, depth)
    x, y = (0, 0)

    total_risk = 0
    for x in range(x_target + 1):
        for y in range(y_target + 1):
            # total_risk += erosion_level[(x, y)] % 3
            total_risk += region_type[(x, y)]

    return f'{total_risk=}'

def compute_part_two(file_name: str) -> str:
    depth, x_target, y_target = read_input_file(file_name)

    geological_index = defaultdict(int)
    erosion_level = defaultdict(int)
    region_type = calculate_geological_index_and_erosion_level(
        geological_index, erosion_level, x_target, y_target, depth
    )
    # Allowed gear per region type
    allowed = {
        0: {1, 2},  # Rocky: Torch, Climbing Gear
        1: {0, 2},  # Wet: Neither, Climbing Gear
        2: {0, 1},  # Narrow: Neither, Torch
    }

    # Priority queue: (time, x, y, gear)
    heap = [(0, 0, 0, 1)]  # Start with Torch
    visited = {}

    while heap:
        # print(len(heap))
        time, x, y, gear = heapq.heappop(heap)

        if (x, y, gear) in visited and visited[(x, y, gear)] <= time:
            continue
        visited[(x, y, gear)] = time

        if (x, y) == (x_target, y_target) and gear == 1:
            return f"Minimum time to reach target with torch: {time} minutes"

        # Try moving to adjacent cells
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0 or (nx, ny) not in region_type:
                continue
            if gear in allowed[region_type[(nx, ny)]]:
                heapq.heappush(heap, (time + 1, nx, ny, gear))

        # Try switching gear
        for new_gear in allowed[region_type[(x, y)]]:
            if new_gear != gear:
                heapq.heappush(heap, (time + 7, x, y, new_gear))

    return "No path found"


if __name__ == '__main__':
    file_path = 'input/input22.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")
