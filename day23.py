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

    def manhattan_distance_to(self, other: 'Bot') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def in_range(self, other: 'Bot') -> bool:
        return self.manhattan_distance_to(other) <= self.r


def find_strongest_bot(bots: list[Bot]) -> Bot:
    return max(bots, key=lambda b: b.r)


def compute_part_one(file_name: str) -> str:
    bots = read_input_file(file_name)
    print(f'{bots= }')

    strongest_bot = find_strongest_bot(bots)
    total = sum(strongest_bot.in_range(bot) for bot in bots)

    return f'{total=}'


def compute_part_two(file_name: str) -> str:
    content = read_input_file(file_name)
    return "part 2 not yet implemented"


if __name__ == '__main__':
    file_path = 'input/input23.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")