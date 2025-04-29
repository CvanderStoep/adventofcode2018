def remove_letter_a(text: str) -> str:
    return text.replace('a', '').replace('A', '')

# Example usage:
input_string = "Advent of Code is amazing!"
output_string = remove_letter_a(input_string)
print(output_string)  # "dvent of Code is mzing!"
