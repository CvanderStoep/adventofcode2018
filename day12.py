from collections import defaultdict


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        left, right = f.read().split('\n\n')
        left = left.split(' ')[2]
        right = right.splitlines()
    notes = defaultdict(lambda: '.')
    # notes = dict()
    for note in right:
        l, r = note.split(' => ')
        notes[l] = r

    return left, notes

def return_5_elements(state:str, pos: int) -> str:

    if pos ==0:
        elements =  '..'+state[:3]
    elif pos ==1:
        elements =  '.'+state[:4]
    elif pos == len(state) -1:
        elements =  state[pos-2:] + '..'
    elif pos == len(state) -2:
        elements =  state[pos-2:] + '.'
    else:
        elements =  state[pos-2:pos+3]
    if len(elements) !=5:
        print(state, pos, elements)


    return elements


def compute_part_one(file_name: str) -> str:
    state, notes = read_input_file(file_name)
    print(f'{state= }')
    print(f'{notes= }')
    state = '...'+ state + '...'
    left_index = -3
    print(f'{0: } {state}')
    for i in range(1, 21):
        new_state = ''
        for pos in range(len(state)):
            new_state += notes[return_5_elements(state, pos)]
        state = '...' + new_state + '...'
        left_index += -3
        print(f'{i: } {new_state}')


    total_sum = 0
    for i in range(len(state)):
        if state[i] == '#':
            # print(i, i + left_index)
            total_sum += i + left_index
    return(f'{total_sum= }')

def compute_part_two(file_name: str) -> str:
    state, notes = read_input_file(file_name)
    dots = 1000
    state = '.'* dots+ state + '.' * dots
    left_index = -dots
    seen = set()
    seen_dict = dict()
    for i in range(1, 1000 + 1):
        new_state = ''
        for pos in range(len(state)):
            new_state += notes[return_5_elements(state, pos)]
        state = '' + new_state + ''
        left_index += -0
        trimmed = state.rstrip('.').lstrip('.')
        if trimmed in seen:
            pass
            print('seen before at ', i-1)
            repeat = i
            break
        else:
            seen.add(trimmed)
            seen_dict[trimmed] = i


    total_sum = 0
    for i in range(len(state)):
        if state[i] == '#':
            total_sum += i + left_index
    print(f'{total_sum= }')

    n = 50000000000
    # after n == 90, the pattern does not change anymore, it just shifts position
    # value @ 90 = 2370, increasing by 21 for each step
    return f'{(n-repeat) * 21 + total_sum= }'


if __name__ == '__main__':
    file_path = 'input/input12.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")