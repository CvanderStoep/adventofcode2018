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
    players = []
    for (x,y), value in grid.items():
        if value in "GE":
            players.append(Player(value, x, y))
    return players

def find_targets(player: Player, players: list) -> list:
    targets = []
    for target in players:
        if not target.alive:
            continue
        if player.type != target.type:
            targets.append(target)
    return targets

def get_target_neighbours(target: Player, grid: defaultdict)-> list:
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbours = []
    x, y = target.x, target.y
    for dx, dy in directions:
        nx, ny = x+dx, y+dy
        if grid[(nx,ny)] in '.EG':
            neighbours.append((nx, ny))
    return neighbours

def is_reachable(player: Player, square: tuple, grid: defaultdict)-> tuple[bool, int] | tuple[bool, None]:
    """"can you reach a specific square from the player using BFS"""
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    start = player.x, player.y
    finish = square[0], square[1]
    visited = set()
    steps = 0
    queue = deque([(steps, start)])
    while queue:
        steps, (x,y) = queue.popleft()
        if (x,y) == finish:
            return True, steps
        if (x,y) not in visited:
            visited.add((x,y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if grid[(nx, ny)] =='.' and (nx, ny) not in visited:
                    queue.append((steps + 1, (nx, ny)))
    return False, None

def shortest_path(player, square: tuple, grid: defaultdict) -> list[tuple[int, int]] | list[Any]:
    """"find the shortest path from the player to the square respecting the reading order in case of a tie"""

    directions = [(0, -1 ), (-1, 0), (1, 0), (0, 1)]  # Reading order
    start = (player.x, player.y)
    finish = square
    visited = {}
    queue = deque([(0, start, [start])])
    min_steps = None
    # best_path = None

    while queue:
        steps, (x, y), path = queue.popleft()

        if min_steps is not None and steps > min_steps:
            break  # No shorter path will be found

        if (x, y) == finish:
            if min_steps is None or steps == min_steps:
                # min_steps = steps
                return path  # Return the first path found in reading order
            continue

        if (x, y) in visited and visited[(x, y)] <= steps:
            continue

        visited[(x, y)] = steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if grid[(nx, ny)] == '.':
                queue.append((steps + 1, (nx, ny), path + [(nx, ny)]))

    return []

def attack_target(player, players, grid)-> None:
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    x, y = player.x, player.y
    adj = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if grid[(nx, ny)] == 'E' and player.type == 'G':
            adj.append((nx, ny))
        if grid[(nx, ny)] == 'G' and player.type == 'E':
            adj.append((nx, ny))

    targets = []
    for x, y in adj:
        for pl in players:
            if (pl.x, pl.y) == (x,y) and pl.alive:
                targets.append(pl)

    # sort target by minimum hp
    # select equal target by reading order
    # apply damage to target
    min_hp = min(target.hp for target in targets)

    targets = [target for target in targets if target.hp == min_hp]
    target = min(targets, key=lambda t: (t.y, t.x))

    target.hp -= player.power
    if target.hp <= 0:
        target.alive = False
        # if a target dies, immediately update the grid
        grid[(target.x, target.y)] = '.'

def play_round(players, grid) -> bool | None:
    players.sort(key=lambda player: (player.y, player.x))
    for player in players:
        if not player.alive:
            continue

        # Check for remaining enemies
        targets = [t for t in players if t.alive and t.type != player.type]
        if not targets:
            return False  # End combat early

        targets = find_targets(player, players)
        squares_in_range = set()
        for target in targets:
            squares_in_range.update(get_target_neighbours(target, grid))
        if any(s == (player.x, player.y) for s in squares_in_range):
            attack_target(player, players, grid)
            continue

        reachable = []
        for square in squares_in_range:
            ir, steps = is_reachable(player, square, grid)
            if ir:
                reachable.append((square, steps))
        if reachable:
            min_s = min(reachable, key=lambda item: item[1])[1]
            # get all squares with the minimum distance and sort them in reading order.
            nearest = [xy for xy, s in reachable if s == min_s]
            nearest.sort(key=lambda xy: (xy[1], xy[0]))
            chosen = nearest[0]
            next_position = shortest_path(player, chosen, grid)[1]
            make_move(player, next_position, grid)

            # has made move, now check for attacking possibilities
            targets = find_targets(player, players)
            squares_in_range = set()
            for target in targets:
                squares_in_range.update(get_target_neighbours(target, grid))
            if any(s == (player.x, player.y) for s in squares_in_range):
                attack_target(player, players, grid)
        else:
            pass
    return True

def remove_dead_players(grid, players) -> list[Any]:
    """"remove dead players from the players list and from the grid"""
    new_players = []
    print(players)
    for player in players:
        if not player.alive:
            grid[(player.x, player.y)] = '.'
            print(f'Dead: {player= }')
        else:
            new_players.append(player)
    return new_players

def check_game_status(grid):
    race_set = {v for v in grid.values() if v in {'E', 'G'}}
    if race_set == {'E'}:
        # "The grid contains only Elves."
        return False
    elif race_set == {'G'}:
        # "The grid contains only Goblins."
        return False
    elif race_set == {'E', 'G'}:
        # "The grid contains both Elves and Goblins."
        return True
    else:
        # "No Elves or Goblins found."
        return False

def make_move(player, next_position, grid) -> None:
    grid[next_position] = player.type
    grid[(player.x, player.y)] = '.'
    player.x, player.y = next_position

def compute_part_one(file_name: str) -> tuple[int | Any, int, int | Any]:
    # for all players in reading order
    # get targets
    # get squares in range
    # get reachable squares
    # get nearest squares
    # get nearest square in reading order
    # get all shortest paths
    # get next move in reading order
    grid = read_input_file(file_name)
    print_grid(grid)

    players = return_players(grid)
    players.sort(key=lambda player: (player.y, player.x))

    rounds = 1
    while True:
        print(f'{rounds= }')
        game_status = play_round(players, grid)
        players = remove_dead_players(grid, players)

        if not game_status:
            print('game has ended early at round', rounds -1)
            hp = sum(player.hp for player in players)
            return rounds-1, hp, (rounds-1) * hp

        game_status = check_game_status(grid)

        if game_status:
            # game can go on
            rounds += 1
        else:
            print('game has ended at round', rounds)
            hp = sum(player.hp for player in players)
            return rounds, hp, rounds * hp

def compute_part_two(file_name: str) -> str:
    content = read_input_file(file_name)
    return "part 2 not yet implemented"


if __name__ == '__main__':
    file_path = 'input/input15.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")