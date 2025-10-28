import re
from dataclasses import dataclass
from typing import List


@dataclass
class Group:
    units: int
    hit_points: int
    weaknesses: List[str]
    immunities: List[str]
    attack_damage: int
    attack_type: str
    initiative: int
    def effective_power(self) -> int:
        return self.units * self.attack_damage

@dataclass
class Army:
    name: str
    groups: List[Group]

def calculate_damage(group1: Group, group2: Group)-> int:
    damage = group1.attack_damage * group1.units
    if group1.attack_type in group2.immunities:
        damage = 0
    elif group1.attack_type in group2.weaknesses:
        damage *=2


    return damage

def read_input_file(file_name: str) -> tuple[Army, Army]:
    with open(file_name) as f:
        content = f.read().splitlines()
    # Initialize armies
    immune_system = Army(name="Immune System", groups=[])
    infection = Army(name="Infection", groups=[])

    # Parsing logic
    current_army = None
    for line in content:
        line = line.strip()
        if not line:
            continue
        if line.endswith(':'):
            current_army = line[:-1]
            continue

        pattern = re.compile(
            r'(?P<units>\d+) units each with (?P<hp>\d+) hit points(?: \((?P<traits>[^)]+)\))? '
            r'with an attack that does (?P<damage>\d+) (?P<atype>\w+) damage at initiative (?P<init>\d+)'
        )
        match = pattern.match(line)
        if match:
            traits = match.group('traits')
            weaknesses = []
            immunities = []
            if traits:
                for part in traits.split(';'):
                    part = part.strip()
                    if part.startswith('weak to '):
                        weaknesses = [w.strip() for w in part[8:].split(',')]
                    elif part.startswith('immune to '):
                        immunities = [i.strip() for i in part[10:].split(',')]

            group = Group(
                units=int(match.group('units')),
                hit_points=int(match.group('hp')),
                weaknesses=weaknesses,
                immunities=immunities,
                attack_damage=int(match.group('damage')),
                attack_type=match.group('atype'),
                initiative=int(match.group('init'))
            )

            if current_army == "Immune System":
                immune_system.groups.append(group)
            elif current_army == "Infection":
                infection.groups.append(group)


    return immune_system, infection


def target_selection(attackers: List[Group], defenders: List[Group]) -> dict:
    # Sort attackers by effective power, then initiative
    attackers_sorted = sorted(attackers, key=lambda g: (-g.effective_power(), -g.initiative))
    chosen = [] # set()
    targets = {}

    for attacker in attackers_sorted:
        best_target = None
        max_damage = 0
        for defender in defenders:
            if defender in chosen:
                continue
            damage = calculate_damage(attacker, defender)
            if damage == 0:
                continue
            if (damage > max_damage or
                (damage == max_damage and defender.effective_power() > best_target.effective_power()) or
                (damage == max_damage and defender.effective_power() == best_target.effective_power() and defender.initiative > best_target.initiative)):
                best_target = defender
                max_damage = damage
        if best_target:
            targets[id(attacker)] = best_target
            chosen.append(best_target)
    return targets

def attack_phase(groups: List[Group], targets: dict):
    # Sort all groups by initiative descending
    for attacker in sorted(groups, key=lambda g: -g.initiative):
        if attacker.units <= 0 or id(attacker) not in targets:
            continue
        defender = targets[id(attacker)]
        damage = calculate_damage(attacker, defender)
        killed_units = min(defender.units, damage // defender.hit_points)
        defender.units -= killed_units

def compute_part_one(file_name: str) -> int:
    immune_system, infection = read_input_file(file_name)

    while immune_system.groups and infection.groups:
        all_groups = immune_system.groups + infection.groups

        # Target selection
        immune_targets = target_selection(immune_system.groups, infection.groups)
        infection_targets = target_selection(infection.groups, immune_system.groups)
        targets = {**immune_targets, **infection_targets}

        # Store units before attack to detect stalemate
        total_units_before = sum(g.units for g in all_groups)

        # Attack phase
        attack_phase(all_groups, targets)

        # Remove dead groups
        immune_system.groups = [g for g in immune_system.groups if g.units > 0]
        infection.groups = [g for g in infection.groups if g.units > 0]

        total_units_after = sum(g.units for g in immune_system.groups + infection.groups)
        if total_units_after == total_units_before:
            # Stalemate detected
            break

    remaining_units = sum(g.units for g in immune_system.groups + infection.groups)
    return remaining_units

def compute_part_two(file_name: str) -> str | None:
    for boost in range(0, 1600):
        immune_system, infection = read_input_file(file_name)
        for g in immune_system.groups:
            g.attack_damage += boost

        while immune_system.groups and infection.groups:
            all_groups = immune_system.groups + infection.groups

            # Target selection
            immune_targets = target_selection(immune_system.groups, infection.groups)
            infection_targets = target_selection(infection.groups, immune_system.groups)
            targets = {**immune_targets, **infection_targets}

            # Store units before attack to detect stalemate
            total_units_before = sum(g.units for g in all_groups)

            # Attack phase
            attack_phase(all_groups, targets)

            # Remove dead groups
            immune_system.groups = [g for g in immune_system.groups if g.units > 0]
            infection.groups = [g for g in infection.groups if g.units > 0]

            total_units_after = sum(g.units for g in immune_system.groups + infection.groups)
            if total_units_after == total_units_before:
                # Stalemate detected
                break

        remaining_units = sum(g.units for g in immune_system.groups + infection.groups)
        remaining_immunities = sum(g.units for g in immune_system.groups)
        remaining_infection = sum(g.units for g in infection.groups)
        if remaining_immunities > 0 and remaining_infection == 0:
            return str(remaining_immunities)
    return None


if __name__ == '__main__':
    file_path = 'input/input24.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")