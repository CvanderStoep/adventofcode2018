from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any

@dataclass
class Player:
    type: str
    x: int
    y: int
    hp: int = 200
    alive: bool = True
    power: int = 3

    def is_enemy(self, other: "Player") -> bool:
        return self.alive and other.alive and self.type != other.type

class Grid:
    def __init__(self, file_name: str):
        self.grid = self.read_input_file(file_name)
        self.players = self._extract_players()

    def read_input_file(self, file_name: str) -> defaultdict[tuple[int, int], str]:
        grid = defaultdict(str)
        with open(file_name) as f:
            for y, line in enumerate(f.read().splitlines()):
                for x, char in enumerate(line):
                    grid[(x, y)] = char
        return grid

    def _extract_players(self) -> list[Player]:
        return [Player(v, x, y) for (x, y), v in self.grid.items() if v in "GE"]

    def print_grid(self) -> None:
        xs = [x for x, _ in self.grid]
        ys = [y for _, y in self.grid]
        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                print(self.grid[(x, y)], end="")
            print()
        print()

    def play_round(self) -> bool:
        self.players.sort(key=lambda p: (p.y, p.x))
        for player in self.players:
            if not player.alive:
                continue
            targets = [t for t in self.players if player.is_enemy(t)]
            if not targets:
                return False

            squares = {xy for t in targets for xy in self.adjacent_open(t.x, t.y)}
            if (player.x, player.y) in squares:
                self.attack(player)
                continue


            reachable = []
            for sq in squares:
                reachable_result = self.is_reachable(player, sq)
                if reachable_result[0]:
                    reachable.append((sq, reachable_result[1]))

            if reachable:
                min_steps = min(dist for _, dist in reachable)
                nearest = sorted([sq for sq, d in reachable if d == min_steps], key=lambda xy: (xy[1], xy[0]))
                next_pos = self.shortest_path(player, nearest[0])[1]
                self.make_move(player, next_pos)
                if (player.x, player.y) in squares:
                    self.attack(player)
        return True

    def adjacent_open(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(x+dx, y+dy) for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]
                if self.grid[(x+dx, y+dy)] in ".GE"]

    def is_reachable(self, player: Player, target: tuple[int, int]) -> tuple[bool, int | None]:
        queue, visited = deque([(0, (player.x, player.y))]), set()
        while queue:
            steps, (x, y) = queue.popleft()
            if (x, y) == target:
                return True, steps
            if (x, y) not in visited:
                visited.add((x, y))
                for nx, ny in self.adjacent_open(x, y):
                    if self.grid[(nx, ny)] == "." and (nx, ny) not in visited:
                        queue.append((steps + 1, (nx, ny)))
        return False, None

    def shortest_path(self, player: Player, target: tuple[int, int]) -> list[tuple[int, int]]:
        queue, visited = deque([((player.x, player.y), [(player.x, player.y)])]), set()
        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == target:
                return path
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in [(0,-1), (-1,0), (1,0), (0,1)]:
                nx, ny = x + dx, y + dy
                if self.grid[(nx, ny)] == '.' and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return []

    def make_move(self, player: Player, next_pos: tuple[int, int]) -> None:
        self.grid[(player.x, player.y)] = '.'
        player.x, player.y = next_pos
        self.grid[next_pos] = player.type

    def attack(self, attacker: Player) -> None:
        adj = [(attacker.x + dx, attacker.y + dy) for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]]
        enemies = [p for p in self.players if p.alive and (p.x, p.y) in adj and p.type != attacker.type]
        if not enemies:
            return
        target = min([e for e in enemies if e.hp == min(en.hp for en in enemies)], key=lambda p: (p.y, p.x))
        target.hp -= attacker.power
        if target.hp <= 0:
            target.alive = False
            self.grid[(target.x, target.y)] = '.'

    def cleanup(self) -> None:
        self.players = [p for p in self.players if p.alive]

    def check_game_over(self) -> bool:
        return len({p.type for p in self.players if p.alive}) <= 1

    def compute_battle(self) -> tuple[int, int, int]:
        rounds = 0
        while True:
            print(f'{rounds= }')
            if not self.play_round():
                break
            self.cleanup()
            if self.check_game_over():
                break
            rounds += 1
        hp = sum(p.hp for p in self.players if p.alive)
        return rounds, hp, rounds * hp

if __name__ == "__main__":
    grid = Grid("input/input15.txt")
    grid.print_grid()
    result = grid.compute_battle()
    print(f"Part I: {result}")
