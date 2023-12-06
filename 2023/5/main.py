import queue
import time

file = open("input.txt", "r").read().splitlines()

def parse_maps(lines):
    maps = []
    curr_map_index = 0
    for line in lines:
        if line == "":
            curr_map_index += 1
            maps.append([])
        else:
            if line.startswith("seeds: "):
                maps.append([])
                seeds = [int(x) for x in line[7:].split(" ")]
                for seed in seeds:
                    maps[curr_map_index].append(seed)
            else:
                if not line.endswith("map:"):
                    entry = line.split(" ")
                    start = int(entry[1])
                    end = start + int(entry[2]) - 1
                    offset = int(entry[0]) - start
                    maps[curr_map_index].append((start, end, offset))
    
    # Sort each entry in ascending order to ensure the first hit is the minimum for that map
    for i, entry in enumerate(maps):
        if i == 0:
            continue
        entry.sort()

    return maps

def solve_p1(maps):
    # Traverse from first array in maps to last
    min_loc = float('inf')
    for seed in maps[0]:
        curr_num = seed
        for i in range(1, len(maps)):
            curr_map = maps[i]
            for entry in curr_map:
                if curr_num >= entry[0] and curr_num <= entry[1]:
                    curr_num += entry[2]
                    break
        min_loc = min(min_loc, curr_num)
    
    return min_loc

def solve_p2(maps):
    min_loc = float('inf')
    q = queue.Queue()

    for i in range(0, len(maps[0]) - 1, 2):
        seed_range = [maps[0][i], maps[0][i] + maps[0][i+1] - 1, 0]
        q.put(seed_range)
    
    while q.qsize() > 0:
        seed_range = q.get()
        for j in range(1, len(maps)):
            if seed_range[2] > j:
                continue
            curr_map = maps[j]
            for start, end, offset in curr_map:
                
                if seed_range[0] >= start and seed_range[0] <= end:
                    seed_range[0] += offset
                    if seed_range[1] <= end:
                        seed_range[1] += offset
                    else:
                        seed_range[1] = end + offset
                        q.put([end + 1, seed_range[1], j])
                    break
                elif seed_range[1] >= start and seed_range[1] <= end:
                    seed_range[1] += offset
                    if seed_range[0] > start:
                        seed_range[0] += offset
                    else:
                        seed_range[0] = start + offset
                        q.put([seed_range[0], start - 1, j])
                    break
        min_loc = min(min_loc, seed_range[0], seed_range[1])
    
    return min_loc

start = time.time()
maps = parse_maps(file)
print(solve_p1(maps))
print(solve_p2(maps))
print("Elapsed time: ", time.time() - start, "s")