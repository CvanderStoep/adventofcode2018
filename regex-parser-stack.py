def parse_regex(expr):
    stack = []
    current = ['']
    i = 0

    while i < len(expr):
        print(i)
        c = expr[i]
        if c == '(':
            stack.append((current, []))  # Save current and alternates
            current = ['']
        elif c == '|':
            prev_current, alternates = stack.pop()
            stack.append((prev_current, alternates + current))
            current = ['']
        elif c == ')':
            prev_current, alternates = stack.pop()
            combined = alternates + current
            current = [p + s for p in prev_current for s in combined]
        else:
            current = [p + c for p in current]
        i += 1

    return current

# Voorbeeldgebruik
if __name__ == "__main__":
    regex = "(NEEE|SSE(EE|N))"
    combos = parse_regex(regex)
    for c in combos:
        print(c)