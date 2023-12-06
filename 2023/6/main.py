import re

file = open("input.txt", "r").read().splitlines()

def parse_file(lines):
    parsed = []
    for line in lines:
        parsed.append([int(x) for x in re.findall(r'(\d+)', line)])
    return parsed

def parse_part2(lines):
    parsed = parse_file(lines)
    output = [[],[]]

    for i, nums in enumerate(parsed):
        num_str = ""
        for num in nums:
            num_str += str(num)
        output[i].append(int(num_str))
    
    return output

def get_dist(time, hold_time):
    return (time - hold_time) * hold_time

def solve(races):
    ways = []
    for i in range(len(races[0])):
        time = races[0][i]
        goal = races[1][i]
        
        max_hold_time = float('-inf')
        start, end = 0, time
        while start < end:
            mid = (start + end) // 2
            if get_dist(time, mid) > goal:
                max_hold_time = max(max_hold_time, mid)
                start = mid + 1
            else:
                end = mid
        
        min_hold_time = float('inf')
        start, end = 0, time
        while start < end:
            mid = (start + end) // 2
            if get_dist(time, mid) > goal:
                min_hold_time = min(min_hold_time, mid)
                end = mid
            else:
                start = mid + 1
        
        ways.append(max_hold_time - min_hold_time + 1)
    
    total = ways[0]
    for i in range(1, len(ways)):
        total *= ways[i]
    
    return total



parsed = parse_file(file)
print(solve(parsed))
p2 = parse_part2(file)
print(solve(p2))
