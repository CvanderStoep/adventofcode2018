from collections import defaultdict
import heapq
from typing import Any, Generator


def read_input_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.read().splitlines()


def convert_to_graph(instructions: list[str]) -> tuple[defaultdict[Any, list], defaultdict[Any, list]]:
    dependents, dependencies = defaultdict(list), defaultdict(list)

    for instruction in instructions:
        words = instruction.split(" ")
        left, right = words[1], words[7]
        dependents[left].append(right)
        dependencies[right].append(left)

    return dependents, dependencies


class SortedTopology:
    def __init__(self, dependents: defaultdict[Any, list], dependencies: defaultdict[Any, list]):
        self.dependents = dependents
        self.dependencies = dependencies
        self.queue = []
        for step in dependents.keys():
            if step not in dependencies.keys():
                heapq.heappush(self.queue, step)


    def empty(self) -> bool:
        return len(self.queue) == 0


    def unlock(self, element: str):
        assert not self.dependencies[element]

        for item in self.dependents[element]:
            self.dependencies[item].remove(element)

            if not self.dependencies[item]:
                heapq.heappush(self.queue, item)


    def pop(self) -> str | None:
        if self.empty():
            return None

        element = heapq.heappop(self.queue)
        print(f'Topology: pop {element}')
        return element


def _duration(element) -> int:
    return ord(element) - ord('A') + 61


class Workbench:
    def __init__(self, number_of_workers: int):
        self.workbench: [(str | None, int)] = [(None, None)] * number_of_workers


    def empty(self) -> bool:
        return all(step is None for (step, _) in self.workbench)


    def full(self) -> bool:
        return all(step is not None for (step, _) in self.workbench)


    def push(self, element: str):
        assert not self.full()

        for i in range(len(self.workbench)):
            if self.workbench[i][0] is None:
                self.workbench[i] = (element, _duration(element))
                print(f'Workbench: push {element} into worker {i + 1}')
                return


    def pop(self) -> ((str | None), int):
        minimum_index, minimum_element, minimum_duration = None, None, None

        for index, (step, duration) in enumerate(self.workbench):
            if step is None:
                continue
            if minimum_duration is None or duration < minimum_duration:
                minimum_index, minimum_element, minimum_duration = index, step, duration

        if minimum_index is None:
            return None, 0

        self.workbench = [(element, duration - minimum_duration) if element else (None, None) for (element, duration) in self.workbench]
        self.workbench[minimum_index] = (None, None)

        print(f'Workbench: pop {minimum_element} from worker {minimum_index + 1} after {minimum_duration} seconds')
        return minimum_element, minimum_duration


def compute_part_one(file_name: str) -> Generator[str]:
    content = read_input_file(file_name)
    graph, dependencies = convert_to_graph(content)

    topo = SortedTopology(graph, dependencies)

    while not topo.empty():
        element = topo.pop()
        topo.unlock(element)
        yield element


def compute_part_two(file_name: str) -> Generator[(str, int)]:
    content = read_input_file(file_name)
    dependents, dependencies = convert_to_graph(content)
    number_of_workers = 5

    topology = SortedTopology(dependents, dependencies)
    workbench = Workbench(number_of_workers)

    while not topology.empty() or not workbench.empty():
        while not workbench.full() and not topology.empty():
            workbench.push(topology.pop())

        element, duration = workbench.pop()
        topology.unlock(element)
        yield element, duration


if __name__ == '__main__':
    file_path = 'input/input7.txt'
    print(f"Part I: {''.join(compute_part_one(file_path))}")
    print(f"Part II: {sum([duration for (element, duration) in compute_part_two(file_path)])}")
