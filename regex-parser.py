def parse_regex(expr):
    def parse(i):
        result = ['']
        while i < len(expr):
            print(i)
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

# Voorbeeldgebruik
if __name__ == "__main__":
    regex = "WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))"
    combos = parse_regex(regex)
    for c in combos:
        print(c)
    from collections import *

    d = defaultdict(lambda: 1e9)
    p = d[0] = 0
    s = []
    for c in regex:
        if '(' == c:
            s.append(p)
        elif ')' == c:
            p = s.pop()
        elif '|' == c:
            p = s[-1]
        else:
            l = p;p += 1j ** 'ESWN'.index(c);d[p] = min(d[p], d[l] + 1)
    v = d.values()
    print(max(v), sum(x >= 1e3 for x in v))