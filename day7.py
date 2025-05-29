from collections import defaultdict
import heapq
from typing import Any


def read_input_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.read().splitlines()


def convert_to_dictionary(instructions: list[str]) -> tuple[defaultdict[Any, list], defaultdict[Any, list], set[Any]]:
    graph, dependencies = defaultdict(list), defaultdict(list)
    all_steps = set()  # Track all steps

    for instruction in instructions:
        words = instruction.split(" ")
        left, right = words[1], words[7]
        graph[left].append(right)
        dependencies[right].append(left)
        all_steps.update([left, right])  # Track all seen steps

    return graph, dependencies, all_steps


def compute_part_one(file_name: str) -> str:
    content = read_input_file(file_name)
    graph, dependencies, all_steps = convert_to_dictionary(content)
    print(graph)
    print(dependencies)
    print(all_steps)

    # Identify starting steps (no dependencies)
    initial_steps = [step for step in all_steps if step not in dependencies]
    print(f'{initial_steps= }')

    queue = []
    for step in initial_steps:
        heapq.heappush(queue, step)  # Use heap to maintain lexicographical order

    correct_order = ''

    while queue:
        element = heapq.heappop(queue)
        correct_order += element

        for item in graph[element]:
            dependencies[item].remove(element)  # Remove dependency

            if not dependencies[item]:  # If all dependencies resolved, add to queue
                heapq.heappush(queue, item)

    return correct_order

if __name__ == '__main__':
    file_path = 'input/input7.txt'
    print(f"Part I: {compute_part_one(file_path)}")
