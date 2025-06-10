def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = list(map(int, f.read().split(" ")))
    return content

def collect_meta_data(numbers: list, index: int, all_meta_data: list) -> int:
    # Base case: If index exceeds the list length, return immediately
    # print(numbers, index)
    if index >= len(numbers):
        return index

    number_children = numbers[index]
    number_metadata = numbers[index + 1]
    index += 2  # Move past the header

    # Recursively process each child node
    for _ in range(number_children):
        index = collect_meta_data(numbers, index, all_meta_data)

    # Collect metadata entries
    meta_data = numbers[index:index + number_metadata]
    all_meta_data.extend(meta_data)
    index += number_metadata  # Move past metadata

    return index

def calculated_node_value(numbers: list, index: int) -> tuple[int, int]:
    # Base case: If index exceeds the list length, return immediately
    if index >= len(numbers):
        return index, 0

    number_children = numbers[index]
    number_metadata = numbers[index + 1]
    index += 2  # Move past the header

    children_values = []

    # Recursively process each child node
    for _ in range(number_children):
        index, child_value = calculated_node_value(numbers, index)
        children_values.append(child_value)
        print(index, children_values)

    # Collect metadata entries
    meta_data = numbers[index:index + number_metadata]
    index += number_metadata  # Move past metadata

    if number_children == 0:
        # If no children, node value is the sum of metadata
        node_value = sum(meta_data)
    else:
        # If children exist, metadata entries refer to children
        node_value = sum(children_values[m - 1] for m in meta_data if 1 <= m <= number_children)

    return index, node_value


def compute_part_one(file_name: str) -> str:
    content = read_input_file(file_name)
    print(f'{content= }')

    all_meta_data = []
    collect_meta_data(content, 0, all_meta_data)  # Start at index 0
    return f'{sum(all_meta_data)= }'


def compute_part_two(file_name: str) -> str:
    content = read_input_file(file_name)
    index, node_value = calculated_node_value(content, 0)  # Start at index 0

    return f'{node_value= }'


if __name__ == '__main__':
    file_path = 'input/input8.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")