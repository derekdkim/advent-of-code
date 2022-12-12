import queue


def parse():
    content = [[*i] for i in open("input.txt").read().splitlines()]
    start, end = (0, 0), (0, 0)
    for i in range(len(content)):
        for j in range(len(content[i])):
            if content[i][j] == "S":
                start = (i, j)
                content[i][j] = 0
            elif content[i][j] == "E":
                end = (i, j)
                content[i][j] = ord("z") - ord("a")
            else:
                content[i][j] = ord(content[i][j]) - ord("a")
    return start, end, content


def add_adj(i, j, steps, grid, deq, visited):
    prev = grid[i][j]
    # N
    if i < len(grid) - 1 and (i + 1, j) not in visited:
        deq.append((i + 1, j, prev, steps))
    # E
    if j < len(grid[i]) - 1 and (i, j + 1) not in visited:
        deq.append((i, j + 1, prev, steps))
    # S
    if i > 0 and (i - 1, j) not in visited:
        deq.append((i - 1, j, prev, steps))
    # W
    if j > 0 and (i, j - 1) not in visited:
        deq.append((i, j - 1, prev, steps))


def bfs(start, end, grid, visited, p2=False):
    deq = queue.deque()
    res = 100000
    # Add first set of nodes
    add_adj(start[0], start[1], 1, grid, deq, visited)
    while len(deq) > 0:
        i, j, prev, steps = deq.popleft()
        # Valid movement
        # Can cross at max one higher, equal, or lower
        # This means prev cannot be greater than the new by more than 1
        if prev - grid[i][j] <= 1 and (i, j) not in visited:
            visited.add((i, j))

            # Target found
            # Part 2 ADD: or grid[i][j] == 0
            if (i, j) == end or (p2 and grid[i][j] == 0):
                res = min(res, steps)
            else:
                add_adj(i, j, steps + 1, grid, deq, visited)
    return res


def solve(is_p2=False):
    start, end, grid = parse()
    visited = set()

    return bfs(end, start, grid, visited, is_p2)


print(solve())
print(solve(True))
