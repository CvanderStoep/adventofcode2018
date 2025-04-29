from collections import Counter
import re
from collections import defaultdict


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()
    content.sort()

    return content

def process_shift(shifts: list, position: int, guards: dict) -> int:

    guard_id = int(re.findall(r"#(\d+)", shifts[position])[0])
    position += 1
    while 'begins' not in shifts[position]:
        falls_asleep = int(re.findall(r":(\d+)", shifts[position])[0])
        wakes_up = int(re.findall(r":(\d+)", shifts[position+1])[0])
        position += 2
        for i in range(falls_asleep,wakes_up):
            guards[guard_id].append(i)
        if position >= len(shifts):
            return position
    return position

def compute_part_one(file_name: str) -> str:
    shifts = read_input_file(file_name)
    print(f'{shifts= }')
    guards = defaultdict(list)
    position = 0
    while position < len(shifts):
        position = process_shift(shifts, position,guards)

    sleepy_guard_id = 0
    max_sleep = 0
    for guard, sleep in guards.items():
        if len(sleep) > max_sleep:
            sleepy_guard_id = guard
            max_sleep = len(sleep)


    numbers = guards[sleepy_guard_id]
    count_dict = Counter(numbers)
    sorted_counts = dict(sorted(count_dict.items(), key=lambda x: x[1], reverse=True))
    minute, amount = next(iter(sorted_counts.items()))


    return f'{minute * sleepy_guard_id= }'

def compute_part_two(file_name: str) -> str:
    shifts = read_input_file(file_name)
    guards = defaultdict(list)
    position = 0
    while position < len(shifts):
        position = process_shift(shifts, position,guards)

    sleepy_guard_id = 0
    max_sleep_count = 0
    max_sleep_minute = 0
    for guard, sleep in guards.items():
        numbers = guards[guard]
        count_dict = Counter(numbers)
        sorted_counts = dict(sorted(count_dict.items(), key=lambda x: x[1], reverse=True))
        sleep_minute, sleep_count = next(iter(sorted_counts.items()))

        if sleep_count > max_sleep_count:
            sleepy_guard_id = guard
            max_sleep_count = sleep_count
            max_sleep_minute = sleep_minute

    return f'{sleepy_guard_id * max_sleep_minute= }'


if __name__ == '__main__':
    file_path = 'input/input4.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")