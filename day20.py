from collections import defaultdict



def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()


    return content

def parse_regex(expr):
    def parse(i):
        result = ['']
        while i < len(expr):
            if expr[i] == '(':
                sub_result, i = parse(i + 1)
                result = [r + s for r in result for s in sub_result]
            elif expr[i] == '|':
                alt_result, i = parse(i + 1)
                return result + alt_result, i
            elif expr[i] == ')':
                return result, i + 1
            else:
                result = [r + expr[i] for r in result]
                i += 1
        return result, i

    combinations, _ = parse(0)
    return combinations

def process_route(route: str, maze: defaultdict) -> None:
    # it works, but only for small input
    position = (0, 0)
    for l in route:
        old_position = position
        match l:
            case "E":
                step = (2, 0)
            case "W":
                step = (-2, 0)
            case "N":
                step = (0, 2)
            case "S":
                step = (0, -2)
        position = (position[0] + step[0], position[1] + step[1])
        if maze[position] == 0:
            maze[position] = maze[old_position] + 1
        else:
            maze[position] = min(maze[position], maze[old_position] + 1)

def process_route2(regex: str) -> int:
    # solution from reddit

    position_dictionary = defaultdict(lambda: 1e9)
    position = position_dictionary[0] = 0
    position_stack = []
    for c in regex:
        if '(' == c:
            position_stack.append(position)
        elif ')' == c:
            position = position_stack.pop()
        elif '|' == c:
            position = position_stack[-1]
        else:
            old_position = position
            position += 1j ** 'ESWN'.index(c) # use complex algebra to update the position
            position_dictionary[position] = min(position_dictionary[position], position_dictionary[old_position] + 1)
    v = position_dictionary.values()
    print(max(v), sum(x >= 1000 for x in v))


def compute_part_one(file_name: str) -> str:
    content = read_input_file(file_name)
    print(f'{content= }')
    maze =  defaultdict(int)
    regex = content[0][1:-1]
    print(f'{regex= }')
    process_route2(regex)
    combos = parse_regex(regex)
    for c in combos:
        process_route(c, maze)

    most_doors = max(maze.values())
    print(f'{most_doors= }')

    return "part 1 not yet implemented"


def compute_part_two(file_name: str) -> str:
    content = read_input_file(file_name)
    return "part 2 not yet implemented"


if __name__ == '__main__':
    file_path = 'input/input20.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")