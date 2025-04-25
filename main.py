def get_common_letters(s1: str, s2: str) -> str:
    """Returns common characters between two strings, excluding the differing one."""
    return ''.join(c1 for c1, c2 in zip(s1, s2) if c1 == c2)

# Example usage:
s1 = "fghij"
s2 = "fguij"
print(get_common_letters(s1, s2))  # Output: "fgij"
