from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List


@dataclass
class Player:
    type: str
    x: int
    y: int
    hp: int = 200
    attack_power: int = 3

    def position(self):
        return (self.x, self.y)


def read_input_file(file_name: str) -> defaultdict[tuple[int, int], str]:
    with open(file_name) as f:
        content = f.read().splitlines()
    grid = defaultdict(str)
    for y, line in enumerate(content):
        for x, letter in enumerate(line):
            grid[(x, y)] = letter
    return grid


def return_players(grid: defaultdict[tuple[int, int], str]) -> List[Player]:
    players = []
    for (x, y), value in grid.items():
        if value in "GE":
            players.append(Player(value, x, y))
    return players


def adjacent_squares(x: int, y: int) -> List[tuple[int, int]]:
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]  # Reading order


def move(player: Player, players: List[Player], grid: defaultdict) -> None:
    occupied = {(p.x, p.y) for p in players if p.hp > 0}
    enemies = [p for p in players if p.type != player.type and p.hp > 0]
    if not enemies:
        return

    targets = set()
    for enemy in enemies:
        for adj in adjacent_squares(enemy.x, enemy.y):
            if grid[adj] == '.' and adj not in occupied:
                targets.add(adj)

    visited = set()
    queue = deque([(player.position(), 0, None)])
    reachable = []
    min_steps = None

    while queue:
        (x, y), steps, first_step = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) in targets:
            if min_steps is None or steps <= min_steps:
                min_steps = steps
                reachable.append((steps, first_step or (x, y), (x, y)))
            continue

        for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            nx, ny = x + dx, y + dy
            if grid[(nx, ny)] == '.' and (nx, ny) not in visited and (nx, ny) not in occupied:
                queue.append(((nx, ny), steps + 1, first_step or (nx, ny)))

    if reachable:
        reachable.sort(key=lambda r: (r[0], r[2][1], r[2][0]))
        next_step = reachable[0][1]
        grid[(player.x, player.y)] = '.'
        player.x, player.y = next_step
        grid[(player.x, player.y)] = player.type


def attack(player: Player, players: List[Player], grid: defaultdict) -> None:
    adjacent_enemies = [
        p for p in players
        if p.type != player.type and p.hp > 0 and (p.x, p.y) in adjacent_squares(player.x, player.y)
    ]
    if not adjacent_enemies:
        return

    targets = sorted(adjacent_enemies, key=lambda e: (e.hp, e.y, e.x))
    target = targets[0]
    target.hp -= player.attack_power
    if target.hp <= 0:
        grid[(target.x, target.y)] = '.'

def print_grid(grid: defaultdict) -> None:
    xs = [x for x,y in grid.keys()]
    ys = [y for x,y in grid.keys()]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print(grid[(x,y)], end='')
        print()

def compute_part_one(file_name: str) -> str:
    grid = read_input_file(file_name)
    print_grid(grid)
    players = return_players(grid)
    rounds_completed = 0
    # print(f'{players= }')

    while True:
        players.sort(key=lambda p: (p.y, p.x))
        turn_order = list(players)

        for player in turn_order:
            if player.hp <= 0:
                continue
            if all(p.type == player.type or p.hp <= 0 for p in players):
                total_hp = sum(p.hp for p in players if p.hp > 0)
                print(rounds_completed, total_hp)
                return str(rounds_completed * total_hp)

            move(player, players, grid)
            attack(player, players, grid)
        # print_grid(grid)

        rounds_completed += 1


def compute_part_two(file_name: str) -> str:
    return "Part 2 not yet implemented"


if __name__ == '__main__':
    file_path = 'input/input15.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")
