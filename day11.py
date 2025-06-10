def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content

def get_hundreds_digit(number):
    return abs(number) // 100 % 10

def get_power_level(serial, x, y) -> int:

    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id
    power_level = get_hundreds_digit(power_level) -5
    return power_level

def power_grid(serial) -> list:
    power = [[0] * 301 for _ in range(301)]
    for x in range(1, 301):
        for y in range(1, 301):
            power[x][y] = get_power_level(serial, x, y)
    return power


def compute_part_one(file_name: str) -> str:
    serial_number = 9445
    max_power = 0
    power_level = power_grid(serial_number)
    print(power_level[33][45])
    for x in range(1, 298):
        print(f'{x= }')
        for y in range(1, 298):
            for size in range(1, 20): # should go (1, 301), but at some point the power keeps dropping
                # print(f'{size= }')
                power = 0
                if (x + size) > 300 or (y + size) > 300:
                    continue
                for xg in range(size):
                    for yg in range(size):
                        # power += get_power_level(serial_number, x+xg, y+yg)
                        power += power_level[x+xg][y+yg]

                if power > max_power:
                    xm = x
                    ym = y
                    max_size = size
                    max_power= max(max_power, power)

    print(f'{xm, ym, max_size, max_power= }')


    return (f'{xm, ym, max_size, max_power= }')



if __name__ == '__main__':
    file_path = 'input/input11.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    # print(f"Part II: {compute_part_two(file_path)}")