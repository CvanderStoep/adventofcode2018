from dataclasses import dataclass
import re


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    pattern = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")
    bots = []

    for line in content:
        x, y, z, r = map(int, re.findall(pattern, line)[0])
        bots.append(Bot(x, y, z, r))

    return bots

@dataclass
class Bot:
    x: int
    y: int
    z: int
    r: int

    def manhattan_distance(self, other: 'Bot') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def in_range(self, other: 'Bot') -> bool:
        return self.manhattan_distance(other) <= self.r


def find_strongest_bot(bots: list[Bot]) -> Bot:
    return max(bots, key=lambda b: b.r)


def compute_part_one(file_name: str) -> str:
    bots = read_input_file(file_name)
    print(f'{bots= }')

    strongest_bot = find_strongest_bot(bots)
    total = sum(strongest_bot.in_range(bot) for bot in bots)

    return f'{total=}'

def compute_part_two_slow(file_name: str) -> str:
    bots = read_input_file(file_name)
    print(f'{bots= }')
    x_min = min(b.x for b in bots)
    x_max = max(b.x for b in bots)
    y_min = min(b.y for b in bots)
    y_max = max(b.y for b in bots)
    z_min = min(b.z for b in bots)
    z_max = max(b.z for b in bots)


    max_in_range = 0
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            for z in range(z_min, z_max + 1):
                dummy_bot = Bot(x, y, z, 0)
                total = sum(bot.in_range(dummy_bot) for bot in bots)
                if total > max_in_range:
                    max_in_range = total
                    coordinates = x, y, z
    print(coordinates, max_in_range)


    return f'{total=}'


def compute_part_two(file_name: str) -> str:
    bots = read_input_file(file_name)

    def count_in_range(x, y, z):
        return sum(
            abs(bot.x - x) + abs(bot.y - y) + abs(bot.z - z) <= bot.r
            for bot in bots
        )

    # Bounding box
    x_min = min(bot.x for bot in bots)
    x_max = max(bot.x for bot in bots)
    y_min = min(bot.y for bot in bots)
    y_max = max(bot.y for bot in bots)
    z_min = min(bot.z for bot in bots)
    z_max = max(bot.z for bot in bots)

    step = 10_000_000
    best_x = best_y = best_z = 0

    while step >= 1:
        candidates = []
        for x in range(x_min, x_max + 1, step):
            for y in range(y_min, y_max + 1, step):
                for z in range(z_min, z_max + 1, step):
                    in_range = count_in_range(x, y, z)
                    dist_to_origin = abs(x) + abs(y) + abs(z)
                    candidates.append((in_range, dist_to_origin, x, y, z))

        # Sort by most bots in range, then closest to origin
        candidates.sort(key=lambda t: (-t[0], t[1]))
        best_in_range, best_dist, best_x, best_y, best_z = candidates[0]

        # Narrow the search space
        x_min = best_x - step
        x_max = best_x + step
        y_min = best_y - step
        y_max = best_y + step
        z_min = best_z - step
        z_max = best_z + step
        step //= 2

        print(f"Step {step}: Best point ({best_x}, {best_y}, {best_z}) with {best_in_range} bots in range, distance {best_dist}")

    distance = abs(best_x) + abs(best_y) + abs(best_z)
    return f'Manhattan distance to best point: {distance}'




if __name__ == '__main__':
    file_path = 'input/input23.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")