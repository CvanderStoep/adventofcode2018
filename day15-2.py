from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any

def print_grid(grid: defaultdict) -> None:
    xs = [x for x, y in grid.keys()]
    ys = [y for x, y in grid.keys()]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print(grid[(x, y)], end='')
        print()
    print()

def read_input_file(file_name: str) -> defaultdict[Any, str]:
    with open(file_name) as f:
        content = f.read().splitlines()
    grid = defaultdict(str)
    for y, line in enumerate(content):
        for x, letter in enumerate(line):
            grid[(x, y)] = letter
    return grid

@dataclass
class Player:
    type: str
    x: int
    y: int
    hp: int = 200
    alive: bool = True
    power: int = 3

def return_players(grid: defaultdict) -> list:
    players = []
    for (x, y), value in grid.items():
        if value in "GE":
            players.append(Player(value, x, y))
    return players

def find_targets(player: Player, players: list) -> list:
    return [target for target in players if target.alive and player.type != target.type]

def get_target_neighbours(target: Player, grid: defaultdict) -> list:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return [
        (target.x + dx, target.y + dy)
        for dx, dy in directions
        if grid[(target.x + dx, target.y + dy)] in '.EG'
    ]

def is_reachable(player: Player, square: tuple, grid: defaultdict) -> tuple[bool, int] | tuple[bool, None]:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    start, finish = (player.x, player.y), square
    visited = set()
    queue = deque([(0, start)])
    while queue:
        steps, (x, y) = queue.popleft()
        if (x, y) == finish:
            return True, steps
        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if grid[(nx, ny)] == '.' and (nx, ny) not in visited:
                    queue.append((steps + 1, (nx, ny)))
    return False, None

def shortest_path(player, square: tuple, grid: defaultdict) -> list[tuple[int, int]] | list[Any]:
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    start, finish = (player.x, player.y), square
    visited = {}
    queue = deque([(0, start, [start])])
    while queue:
        steps, (x, y), path = queue.popleft()
        if (x, y) == finish:
            return path
        if (x, y) in visited and visited[(x, y)] <= steps:
            continue
        visited[(x, y)] = steps
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if grid[(nx, ny)] == '.':
                queue.append((steps + 1, (nx, ny), path + [(nx, ny)]))
    return []

def attack_target(player, players, grid) -> bool:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    adj = []
    for dx, dy in directions:
        nx, ny = player.x + dx, player.y + dy
        if grid[(nx, ny)] in {'E', 'G'}:
            for pl in players:
                if pl.alive and (pl.x, pl.y) == (nx, ny) and pl.type != player.type:
                    adj.append(pl)

    if not adj:
        return False

    min_hp = min(pl.hp for pl in adj)
    targets = [pl for pl in adj if pl.hp == min_hp]
    target = min(targets, key=lambda t: (t.y, t.x))
    target.hp -= player.power

    if target.hp <= 0:
        target.alive = False
        grid[(target.x, target.y)] = '.'
        if target.type == 'E':
            return True  # Elf died
    return False

def play_round(players, grid) -> str | bool:
    players.sort(key=lambda p: (p.y, p.x))
    for player in players:
        if not player.alive:
            continue
        if not any(p.alive and p.type != player.type for p in players):
            return False
        targets = find_targets(player, players)
        in_range = set()
        for target in targets:
            in_range.update(get_target_neighbours(target, grid))
        if (player.x, player.y) in in_range:
            if attack_target(player, players, grid):
                return 'elf_died'
            continue
        reachable = []
        for square in in_range:
            ir, steps = is_reachable(player, square, grid)
            if ir:
                reachable.append((square, steps))
        if reachable:
            min_dist = min(r[1] for r in reachable)
            nearest = sorted([s for s, d in reachable if d == min_dist], key=lambda xy: (xy[1], xy[0]))
            chosen = nearest[0]
            path = shortest_path(player, chosen, grid)
            if len(path) > 1:
                make_move(player, path[1], grid)

            # Re-evaluate attack after move
            if (player.x, player.y) in in_range:
                if attack_target(player, players, grid):
                    return 'elf_died'
    return True

def make_move(player, next_pos, grid) -> None:
    grid[(player.x, player.y)] = '.'
    grid[next_pos] = player.type
    player.x, player.y = next_pos

def remove_dead_players(grid, players) -> list:
    return [p for p in players if p.alive]

def check_game_status(grid):
    return len({v for v in grid.values() if v in 'EG'}) > 1

def compute_part_two(file_name: str):
    original_grid = read_input_file(file_name)
    base_elf_count = sum(1 for v in original_grid.values() if v == 'E')
    elf_power = 3

    while True:
        elf_power += 1
        print(f'{elf_power= }')
        grid = read_input_file(file_name)
        players = return_players(grid)

        for p in players:
            if p.type == 'E':
                p.power = elf_power

        rounds = 0
        while True:
            game_status = play_round(players, grid)
            players = remove_dead_players(grid, players)

            if game_status == 'elf_died':
                break  # Try next higher power

            if game_status is False:
                hp = sum(p.hp for p in players)
                if sum(1 for p in players if p.type == 'E') == base_elf_count:
                    print_grid(grid)
                    return elf_power, rounds, hp, rounds * hp
                break
            rounds += 1

if __name__ == '__main__':
    file_path = 'input/input15.txt'
    print(f"Part Two: {compute_part_two(file_path)}")
