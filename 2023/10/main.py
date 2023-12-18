file = open("input.txt", "r").read().splitlines()

# (0, 0)
# ------- +
# |
# |
# +

# (y, x)
connections = {
    '|': [(1, 0), (-1, 0)],
    '-': [(0, 1), (0, -1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)],
}

def parse_graph(file):
    graph = dict()
    origin = None
    for y, line in enumerate(file):
        for x, cell in enumerate(line):
            if cell in connections:
                for pattern in connections[cell]:
                    new_y, new_x = y + pattern[0], x + pattern[1]
                    if new_y < 0 or new_x < 0:
                        continue
                    if new_y >= len(file) or new_x >= len(line):
                        continue
                    if file[new_y][new_x] == '.':
                        continue
                    if (y, x) not in graph:
                        graph[(y, x)] = []
                    graph[(y, x)].append((new_y, new_x))
            if cell == 'S':
                origin = (y, x)
                graph[origin] = []
    
    for cell in graph:
        for neighbour in graph[cell]:
            if neighbour == origin:
                graph[origin].append(cell)
                break

    return graph, origin

def parse_empty_cells(file):
    blanks = dict()
    for y, line in enumerate(file):
        for x, cell in enumerate(line):
            if y not in blanks:
                blanks[y] = []
            blanks[y].append(x)
    
    return blanks

def solve_p1(graph, origin):
    visited = set()
    distances = dict()
    queue = [(origin, 0)]
    while queue:
        cell, dist = queue.pop(0)
        if cell in visited:
            continue
        visited.add(cell)
        
        if cell not in distances:
            distances[cell] = dist
        distances[cell] = min(distances[cell], dist)

        if cell not in graph:
            continue
        for neighbor in graph[cell]:
            queue.append((neighbor, dist + 1))

    end = None
    max_dist = 0
    for cell in distances:
        if max_dist < distances[cell]:
            end = cell
            max_dist = distances[cell]

    # P2: Backtrack to origin to find path
    queue = [(end, max_dist)]
    path = []
    visited = set()
    while queue:
        cell, dist = queue.pop(0)
        if cell in visited:
            continue
        visited.add(cell)

        if distances[cell] != dist:
            continue
        path.append(cell)

        for neighbour in graph[cell]:
            queue.append((neighbour, dist - 1))

    path.sort()
    boundaries = dict() # key y, val x
    for cell in path:
        y, x = cell
        if y not in boundaries:
            boundaries[y] = []
        boundaries[y].append(x)

    blanks = parse_empty_cells(file)
    enclosed_area = 0
    for y in boundaries:
        if y == min(boundaries.keys()) or y == max(boundaries.keys()):
            continue
        if y in blanks:
            for x in blanks[y]:
                ray_crosses = 0
                last_point = None
                for i in boundaries[y]:
                    if i < x and last_point != x - 1:
                        ray_crosses += 1
                    last_point = i
                if ray_crosses % 2 == 1:
                    enclosed_area += 1

    return end, max_dist, enclosed_area

graph, origin = parse_graph(file)
print(solve_p1(graph, origin))
        