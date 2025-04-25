from itertools import cycle


def read_input_file(file_name: str) -> list[int]:
    """Reads the input file and returns a list of integers."""
    with open(file_name) as f:
        return [int(line.strip()) for line in f]


def compute_part_one(file_name: str) -> str:
    """Computes the sum of all frequency changes."""
    content = read_input_file(file_name)
    return f'Sum of frequencies: {sum(content)}'


def compute_part_two(file_name: str) -> str | None:
    """Finds the first repeated frequency using a set for tracking seen values."""
    content = read_input_file(file_name)
    running_total = 0
    seen = set()

    for number in cycle(content):  # Using itertools.cycle for infinite looping
        running_total += number
        if running_total in seen:
            return f'First repeated frequency: {running_total}'
        seen.add(running_total)


if __name__ == '__main__':
    file_path = 'input/input1.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")
