def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    return content


def compute_part_one() -> str:
    number_recipes = 147061
    player1 = 0
    player2 = 1
    recipes = [3, 7]
    while len(recipes) < number_recipes + 10:
        next_recipe = recipes[player1] + recipes[player2]
        if next_recipe <= 9:
            recipes.append(next_recipe)
        else:
            recipes.append(1)
            recipes.append(next_recipe%10)
        player1 = (player1 + 1 + recipes[player1]) % len(recipes)
        player2 = (player2 + 1 + recipes[player2]) % len(recipes)
    return ''.join(map(str, recipes[number_recipes: number_recipes + 10]))

def compute_part_two() -> int:
    digits = [1,4,7,0,6,1]
    player1 = 0
    player2 = 1
    recipes = [3, 7]
    while True:
        next_recipe = recipes[player1] + recipes[player2]
        if next_recipe <= 9:
            recipes.append(next_recipe)
        else:
            recipes.append(1)
            recipes.append(next_recipe%10)
        player1 = (player1 + 1 + recipes[player1]) % len(recipes)
        player2 = (player2 + 1 + recipes[player2]) % len(recipes)

    # it matches at the last elements or the turn before, because either 1 or 2 digits are added
    # example: 147061 can match after adding 12 to 14706(12)
        if recipes[-len(digits):] == digits:
            return len(recipes) - len(digits)
        if recipes[-len(digits)-1:-1] == digits:
            return len(recipes) - len(digits) -1






if __name__ == '__main__':
    file_path = 'input/input0.txt'
    print(f"Part I: {compute_part_one()}")
    print(f"Part II: {compute_part_two()}")