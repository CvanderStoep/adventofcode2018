def compute_part_one() -> str:
    number_recipes = 147061
    player1, player2 = 0, 1
    recipes = [3, 7]

    while len(recipes) < number_recipes + 10:
        next_recipe = recipes[player1] + recipes[player2]
        recipes.extend(divmod(next_recipe, 10) if next_recipe >= 10 else [next_recipe])

        player1 = (player1 + 1 + recipes[player1]) % len(recipes)
        player2 = (player2 + 1 + recipes[player2]) % len(recipes)

    return ''.join(map(str, recipes[number_recipes:number_recipes + 10]))


def compute_part_two() -> int:
    target = "147061"
    player1, player2 = 0, 1
    recipes = [3, 7]
    recipe_str = "37"

    while True:
        next_recipe = recipes[player1] + recipes[player2]
        for digit in divmod(next_recipe, 10) if next_recipe >= 10 else [next_recipe]:
            recipes.append(digit)
            recipe_str += str(digit)

            if target in recipe_str[-len(target)-1:]:
                return len(recipe_str) - len(target)

        player1 = (player1 + 1 + recipes[player1]) % len(recipes)
        player2 = (player2 + 1 + recipes[player2]) % len(recipes)


if __name__ == "__main__":
    print(f"Part I: {compute_part_one()}")
    print(f"Part II: {compute_part_two()}")
