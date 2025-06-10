from collections import deque


def read_input_file(file_name: str) -> tuple[int, int]:
    with open(file_name) as f:
        content = f.read().split(" ")
        n_players, n_marbles = int(content[0]), int(content[6])

    return n_players, n_marbles


def compute_part_one(file_name: str) -> str:
    # this was my original implementation using list manipulation
    # below is an alternative (faster) implementation using deque
    n_players, n_marbles = read_input_file(file_name)
    print(f'{n_players, n_marbles= }')

    circular_list = [0]
    index = 0
    player = 0
    scores = [0] * n_players
    for marble in range(1, n_marbles + 1):
        player += 1
        player = (player-1) % n_players + 1
        if marble % 23 == 0:
            index = (index - 7) % len(circular_list)
            scores[player-1] += marble + circular_list[index]
            circular_list.pop(index)
        else:
            index = (index + 2) % len(circular_list)
            circular_list.insert(index, marble)

    return f'{max(scores)= }'

def play_marble(n_players, n_marbles, multiplier) -> str:
    n_marbles *= multiplier

    circular_list = deque([0])
    player = 0
    scores = [0] * n_players

    for marble in range(1, n_marbles + 1):
        player += 1
        player = (player - 1) % n_players + 1
        if marble % 23 == 0:
            circular_list.rotate(7)  # Move index back 7 positions
            scores[player - 1] += marble + circular_list.pop()
            circular_list.rotate(-1)  # Adjust after removal
        else:
            circular_list.rotate(-1)  # Move index forward
            circular_list.append(marble)
    return max(scores)

def compute_part_one_alter(file_name: str, multiplier = 1) -> str:
    n_players, n_marbles = read_input_file(file_name)
    max_score = play_marble(n_players, n_marbles, multiplier)

    return f'{max_score= }'



if __name__ == '__main__':
    file_path = 'input/input9.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part I: {compute_part_one_alter(file_path)}")
    print(f"Part II: {compute_part_one_alter(file_path, multiplier=100)}")