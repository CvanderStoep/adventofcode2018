import itertools
from collections import Counter

def read_input_file(file_name: str) -> list[str]:
    """Reads file and returns a list of lines."""
    with open(file_name) as f:
        return f.read().splitlines()

def differ_by_one(s1: str, s2: str) -> bool:
    """Checks if two strings differ by exactly one character."""
    if len(s1) != len(s2):
        return False

    differences = sum(1 for a, b in zip(s1, s2) if a != b)
    return differences == 1

def compute_checksum(file_name: str) -> int:
    """Computes the checksum for the box IDs."""
    content = read_input_file(file_name)
    two_count, three_count = 0, 0

    for word in content:
        letter_counts = Counter(word).values()
        two_count += (2 in letter_counts)
        three_count += (3 in letter_counts)

    return two_count * three_count

def find_box_containing_prototype(file_name: str):
    content = read_input_file(file_name)
    pairs = itertools.combinations(content, 2)
    for word1, word2 in pairs:
        if differ_by_one(word1, word2):
            return ''.join(c1 for c1, c2 in zip(word1, word2) if c1 ==c2)



if __name__ == '__main__':
    file_path = 'input/input2.txt'
    print(f"Checksum: {compute_checksum(file_path)}")
    print(f"Prototype: {find_box_containing_prototype(file_path)}")
