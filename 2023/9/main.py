file = open('input.txt', 'r').read().splitlines()

def extrapolate_diffs(line):
    nums = [int(x) for x in line.split(' ')]
    diffs = [[*nums]]

    diff_index = 0
    at_base_level = False
    while not at_base_level:
        diffs.append([])
        max_diff = 0
        for i in range(1, len(diffs[diff_index])):
            diff = diffs[diff_index][i] - diffs[diff_index][i - 1]
            max_diff = max(max_diff, abs(diff))
            diffs[diff_index + 1].append(diff)
        if max_diff == 0:
            at_base_level = True
        diff_index += 1

    return diffs


def solve_p1(file):
    total = 0
    for line in file:
        diffs = extrapolate_diffs(line)

        # Work back to fill in last value
        for i in range(len(diffs) - 1, 0, -1):
            diffs[i - 1].append(diffs[i][-1] + diffs[i - 1][-1])

        total += diffs[0][-1]

    return total

def solve_p2(file):
    total = 0
    for line in file:
        diffs = extrapolate_diffs(line)

        # Work back to fill in first value
        # Adding at the first index is O(n), so just keep the value temporarily
        curr_val = 0
        for i in range(len(diffs) - 1, 0, -1):
            curr_val = diffs[i - 1][0] - curr_val

        total += curr_val

    return total
print(solve_p1(file))
print(solve_p2(file))