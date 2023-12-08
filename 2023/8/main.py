import math

file = open("input.txt", "r").read().splitlines()

def parse_map(lines):
    instr = [*lines[0]]
    map_dict = dict()
    for i in range(2, len(lines)):
        segments = lines[i].split(" = ")
        dirs = segments[1].strip("()").split(", ")
        map_dict[segments[0]] = dirs
    return instr, map_dict

def solve_p1(maps, start="AAA", p2=False):
    instr, map_dict = maps
    curr_loc = start
    count = 0
    while curr_loc[2] != "Z" if p2 else curr_loc != "ZZZ":
        for i in instr:
            curr_loc = map_dict[curr_loc][0 if i == "L" else 1]
            count += 1
    return count

def solve_p2(maps):
    instr, map_dict = maps
    curr_locs = []

    for i in map_dict.keys():
        if i[2] == "A":
            curr_locs.append(i)
    
    counts = [solve_p1(maps, x, True) for x in curr_locs]
    return math.lcm(*counts)

maps = parse_map(file)
print(solve_p1(maps))
print(solve_p2(maps))