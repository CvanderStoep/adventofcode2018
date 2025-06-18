from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any

def print_grid(grid: defaultdict) -> None:
    xs = [x for x,y in grid.keys()]
    ys = [y for x,y in grid.keys()]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print(grid[(x,y)], end='')
        print()
    print()

def read_input_file(file_name: str) -> defaultdict[Any, str]:
    with open(file_name) as f:
        content = f.read().splitlines()
    grid = defaultdict(str)
    for y, line in enumerate(content):
        for x, letter in enumerate(line):
            grid[(x,y)] = letter
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
    return [Player(v, x, y) for (x, y), v in grid.items() if v in "GE"]

def find_targets(player: Player, players: list) -> list:
    return [t for t in players if t.alive and t.type != player.type]

def find_in_range(target: Player, grid: defaultdict) -> list:
    directions = [(0,1), (0,-1), (-1,0), (1,0)]
    return [(target.x + dx, target.y + dy)
            for dx, dy in directions
            if grid[(target.x + dx, target.y + dy)] == '.']

def is_reachable(player: Player, square: tuple, grid: defaultdict) -> tuple[bool, int] | tuple[bool, None]:
    directions = [(0,1), (0,-1), (-1,0), (1,0)]
    visited = set()
    queue = deque([(0, (player.x, player.y))])
    while queue:
        steps, (x, y) = queue.popleft()
        if (x, y) == square:
            return True, steps
        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if grid[(nx, ny)] == '.' and (nx, ny) not in visited:
                    queue.append((steps + 1, (nx, ny)))
    return False, None

def all_shortest_paths2(player, square: tuple, grid: defaultdict) -> list[tuple[int, int]]:
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    start, finish = (player.x, player.y), square
    visited = {}
    queue = deque([(0, start, [])])
    shortest_paths = []
    min_steps = None
    while queue:
        steps, (x, y), path = queue.popleft()
        if min_steps is not None and steps > min_steps:
            break
        if (x, y) == finish:
            if min_steps is None:
                min_steps = steps
            shortest_paths.append(path)
            continue
        if (x, y) in visited and visited[(x, y)] <= steps:
            continue
        visited[(x, y)] = steps
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if grid[(nx, ny)] == '.' or (nx, ny) == finish:
                queue.append((steps + 1, (nx, ny), path + [(nx, ny)]))
    if not shortest_paths:
        return []
    shortest_paths.sort(key=lambda p: (p[0][1], p[0][0]))  # sort by reading order of first step
    return [start] + shortest_paths[0]

def attack_target(player, players, grid) -> None:
    directions = [(0,1), (0,-1), (-1,0), (1,0)]
    adj = [(player.x + dx, player.y + dy) for dx, dy in directions]
    targets = [pl for x, y in adj
               for pl in players
               if (pl.x, pl.y) == (x,y) and pl.alive and pl.type != player.type]
    if not targets:
        return
    min_hp = min(target.hp for target in targets)
    targets = [t for t in targets if t.hp == min_hp]
    target = min(targets, key=lambda t: (t.y, t.x))
    target.hp -= player.power
    if target.hp <= 0:
        target.alive = False

def make_move(player, next_position, grid) -> None:
    grid[(player.x, player.y)] = '.'
    grid[next_position] = player.type
    player.x, player.y = next_position

def play_round(players, grid) -> bool | None:
    players.sort(key=lambda p: (p.y, p.x))
    for player in players:
        if not player.alive:
            continue
        targets = find_targets(player, players)
        if not targets:
            return False
        in_range = set(sq for t in targets for sq in find_in_range(t, grid))
        if (player.x, player.y) in in_range:
            attack_target(player, players, grid)
            continue
        reachable = [(sq, d) for sq in in_range if (r := is_reachable(player, sq, grid))[0] for d in [r[1]]]
        if not reachable:
            continue
        min_dist = min(dist for _, dist in reachable)
        candidates = sorted([sq for sq, dist in reachable if dist == min_dist], key=lambda c: (c[1], c[0]))
        chosen = candidates[0]
        path = all_shortest_paths2(player, chosen, grid)
        if len(path) >= 2:
            make_move(player, path[1], grid)
        if (player.x, player.y) in in_range:
            attack_target(player, players, grid)
    return True

def remove_dead_players(grid, players) -> list:
    new_players = []
    for p in players:
        if not p.alive:
            grid[(p.x, p.y)] = '.'
        else:
            new_players.append(p)
    return new_players

def check_game_status(grid):
    units = set(v for v in grid.values() if v in {'E', 'G'})
    return units == {'E', 'G'}

def compute_part_one(file_name: str) -> str:
    grid = read_input_file(file_name)
    players = return_players(grid)
    rounds = 0
    while True:
        print(f'{rounds= }')
        if not play_round(players, grid):
            break
        players = remove_dead_players(grid, players)
        rounds += 1
        if not check_game_status(grid):
            break
    hp = sum(p.hp for p in players if p.alive)
    return f"Rounds: {rounds}, Sum HP: {hp}, Outcome: {rounds * hp}"

def compute_part_two(file_name: str) -> str:
    return "part 2 not yet implemented"

if __name__ == '__main__':
    file_path = 'input/input15.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")
