# Parse file
file = open("input.txt", "r")
content = file.read().splitlines()

import re

num_regex = "\d+"


def regex_parse(pattern, str):
    content = [int(x) for x in re.findall(pattern, str)]
    print(content)


def solve(fn):
    count = 0
    for i in content:
        regex_parse(num_regex, i)
        # pairs = i.split(",")
        # pair = [[int(x) for x in range.split("-")] for range in pairs]
        # count += fn(pair)
    print(count)


def p1(pair):
    # count if one range is fully within the other
    # 2 < 3, 8 > 7
    if pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1]:
        return 1
    elif pair[1][0] <= pair[0][0] and pair[1][1] >= pair[0][1]:
        return 1
    return 0


def p2(pair):
    # Find overlap
    if not (pair[0][1] < pair[1][0] or pair[1][1] < pair[0][0]):
        return 1
    return 0


solve(p1)
solve(p2)
