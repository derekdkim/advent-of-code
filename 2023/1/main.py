import re

file = open("input.txt", "r")

lines = file.read().splitlines()

num_conv_ref = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

# P2 Solution:
# Standardize all eligible substrings and digits into a (start_index, number) tuple and sort in ascending order.

def solve(arr):
    calibration = 0
    for string in arr:
        idx_num_tuples = []
        add_substr(string, idx_num_tuples)
        add_digits(string, idx_num_tuples)
        idx_num_tuples.sort()
        calibration += int(idx_num_tuples[0][1] + idx_num_tuples[-1][1])
    print(calibration)

def add_substr(string, array):
    # Convert eligible substrings to nums
    for key, value in num_conv_ref.items():
        indexes = [m.start() for m in re.finditer(key, string)]
        for index in indexes:
            if index > -1:
                array.append((index, value))


def add_digits(string, array):
    # Add in substring
    split_str = [*string]
    for (i, x) in enumerate(split_str):
        if x.isdigit():
            array.append((i, x))

solve(lines)
