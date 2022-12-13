import json
from functools import cmp_to_key


def parse():
    content = [i.split("\n") for i in open("input.txt").read().split("\n\n")]
    # lol parsing JSON actually works
    return [[json.loads(i) for i in x] for x in content]


def convert(p1, p2):
    # If one is integer:
    if isinstance(p1, int):
        p1 = [p1]
    if isinstance(p2, int):
        p2 = [p2]
    return p1, p2


def compare(p1, p2):
    # Type mismatch
    if type(p1) != type(p2):
        p1, p2 = convert(p1, p2)
        return compare(p1, p2)
    else:
        # Same type
        if isinstance(p1, int):
            # Can decide right now
            if p1 < p2:
                return True
            elif p1 > p2:
                return False
            else:
                # None = Draw
                return None
            # Inconclusive
        elif isinstance(p1, list):
            min_len = min(len(p1), len(p2))
            for i in range(min_len):
                res = compare(p1[i], p2[i])
                # Filters out all None values as the root level are always 2 lists
                if res is not None:
                    return res
            # Left ran out of elems first
            if len(p1) < len(p2):
                return True
            elif len(p1) > len(p2):
                return False


def compare_sort_wrapper(x, y):
    res = compare(x, y)
    return 1 if res else -1


def p1():
    content = parse()
    # Find all indices (1-indexed) in the correct order
    right = []
    for ind, pair in enumerate(content):
        is_right = compare(pair[0], pair[1])
        if is_right:
            right.append(ind + 1)
    # Return the sum of all right indices
    return sum(right)


def p2():
    content = parse()
    all_packets = []
    # New divider packets to add
    d_1 = [[2]]
    d_2 = [[6]]
    # Merge all pairs into one unified list
    for i in content:
        all_packets.extend(i)
    # Append the 2 divider packets
    all_packets.append(d_1)
    all_packets.append(d_2)
    # Sort using custom comparison func
    all_packets = sorted(
        all_packets, key=cmp_to_key(compare_sort_wrapper), reverse=True
    )
    # Multiply packet indices (1-indexed)
    d_1_i = all_packets.index(d_1) + 1
    d_2_i = all_packets.index(d_2) + 1
    return d_1_i * d_2_i


print("Part 1: ", end="")
print(p1())
print("Part 2: ", end="")
print(p2())
