from collections import defaultdict
import heapq
from typing import Any, Tuple


def read_input_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.read().splitlines()


def convert_to_dictionary(instructions: list[str]) -> Tuple[defaultdict[Any, list], defaultdict[Any, list], set[Any]]:
    order_tree, finish_steps = defaultdict(list), defaultdict(list)
    all_steps = set()  # Track all steps

    for instruction in instructions:
        words = instruction.split(" ")
        left, right = words[1], words[7]
        order_tree[left].append(right)
        finish_steps[right].append(left)
        all_steps.update([left, right])  # Track all seen steps

    return order_tree, finish_steps, all_steps


def compute_part_two(file_name: str, num_workers: int, base_time: int) -> int:
    content = read_input_file(file_name)
    order_tree, finish_steps, all_steps = convert_to_dictionary(content)

    initial_steps = [step for step in all_steps if step not in finish_steps]
    queue = []
    for step in initial_steps:
        heapq.heappush(queue, step)  # Lexicographical order

    workers = [None] * num_workers  # Track worker tasks
    remaining_times = [0] * num_workers  # Time left for each task
    time_elapsed = 0
    ongoing_tasks = {}  # {step: time_remaining}

    while queue or any(remaining_times):  # While tasks exist or workers are busy
        # Advance time to next event
        min_time = min([t for t in remaining_times if t > 0], default=1)
        time_elapsed += min_time

        # Reduce remaining time for each worker
        for i in range(num_workers):
            if workers[i]:  # If worker is working
                ongoing_tasks[workers[i]] -= min_time
                remaining_times[i] -= min_time
                if remaining_times[i] == 0:  # Task completes
                    completed_task = workers[i]
                    workers[i] = None
                    del ongoing_tasks[completed_task]

                    for dependent in order_tree[completed_task]:
                        finish_steps[dependent].remove(completed_task)
                        if not finish_steps[dependent]:  # Dependencies resolved
                            heapq.heappush(queue, dependent)

        # Assign new tasks to idle workers
        for i in range(num_workers):
            if workers[i] is None and queue:
                new_task = heapq.heappop(queue)
                workers[i] = new_task
                task_time = base_time + (ord(new_task) - ord('A') + 1)  # Duration
                remaining_times[i] = task_time
                ongoing_tasks[new_task] = task_time

    return time_elapsed -1


if __name__ == '__main__':
    file_path = 'input/input7.txt'
    workers = 5  # Adjustable
    base_time = 60  # Adjustable
    print(f"Part II: {compute_part_two(file_path, workers, base_time)}")
