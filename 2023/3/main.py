import re

file = open("input.txt", "r")

lines = file.read().splitlines()

def solve_p1(engine):
    parts_ref, coords = engine
    total = 0

    for coord in coords:
        eligible_part_rows = [*parts_ref[coord[0]]]
        if coord[0] > 0:
            eligible_part_rows = [*eligible_part_rows, *parts_ref[coord[0] - 1]]
        if coord[0] < len(lines) - 1:
            eligible_part_rows = [*eligible_part_rows, *parts_ref[coord[0] + 1]]
        for part in eligible_part_rows:
            start = coord[1] - 1
            end = coord[1] + 1
            # between [x - 1, x + 1]
            if (part[0] >= start and part[0] <= end) or (part[1] >= start and part[1] <= end):
                total += part[2]
    
    print(total)

def solve_p2(engine):
    parts_ref, coords = engine
    total = 0

    for coord in coords:
        if coord[2] != '*':
            continue
        eligible_part_rows = [*parts_ref[coord[0]]]
        if coord[0] > 0:
            eligible_part_rows = [*eligible_part_rows, *parts_ref[coord[0] - 1]]
        if coord[0] < len(lines) - 1:
            eligible_part_rows = [*eligible_part_rows, *parts_ref[coord[0] + 1]]
        found_parts = []
        for part in eligible_part_rows:
            start = coord[1] - 1
            end = coord[1] + 1
            # between [x - 1, x + 1]
            if (part[0] >= start and part[0] <= end) or (part[1] >= start and part[1] <= end):
                found_parts.append(part[2])
        if len(found_parts) == 2:
            total += found_parts[0] * found_parts[1]
    
    print(total)

def parse_engine(lines):
    engine_parts = []
    symbols_indexes = []

    for i, line in enumerate(lines):
        engine_parts.append([])
        num = []
        for j, char in enumerate(line):
            if char.isdigit():
                num.append(char)

                if j == len(line) - 1:
                    engine_parts[i].append((j - len(num), j, int("".join(num))))
            else:
                if char != ".":
                    # Symbol
                    symbols_indexes.append((i, j, char))
                if num:
                    engine_parts[i].append((j - len(num), j - 1, int("".join(num))))
                num = []
    
    return (engine_parts, symbols_indexes)

engine = parse_engine(lines)
solve_p1(engine)
solve_p2(engine)