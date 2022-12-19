from queue import deque


def parse():
    return [
        tuple([int(i) for i in line.split(",")])
        for line in open("input.txt").read().splitlines()
    ]


def check_boundaries(grid, side):
    x, y, z = side
    if (x < 0 or y < 0 or z < 0) or (
        x > len(grid[0][0]) - 1 or y > len(grid[0]) - 1 or z > len(grid) - 1
    ):
        return True
    return False


def get_adjacent_coords(coord):
    x, y, z = coord
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]


def check_adjacent(grid, side):
    s_x, s_y, s_z = side
    # check if any side will go out of bounds:
    if check_boundaries(grid, side):
        return 1
    else:
        if grid[s_z][s_y][s_x] == 0:
            return 1
    return 0


def fill_air_pockets(grid):
    exposed = set()
    visited = set()
    deq = deque([(0, 0, 0)])
    while len(deq) > 0:
        coord = deq.popleft()
        if coord not in visited:
            visited.add(coord)
            adjs = get_adjacent_coords(coord)
            # If any of its adjacents as already in exposed

            for adj in adjs:
                x, y, z = adj
                if adj in exposed or check_boundaries(grid, adj):
                    exposed.add(coord)
                # Blocked; don't continue from this point
                elif grid[z][y][x] == 1:
                    continue
                else:
                    deq.append(adj)

    # Fill every pocket not in exposed
    for z in range(len(grid)):
        for y in range(len(grid[z])):
            for x in range(len(grid[z][y])):
                coord = (x, y, z)
                if grid[z][y][x] == 0:
                    if coord not in exposed:
                        grid[z][y][x] = 1


def solve(p2=False):
    coords = parse()
    max_x = max(coords, key=lambda x: x[0])[0]
    max_y = max(coords, key=lambda x: x[1])[1]
    max_z = max(coords, key=lambda x: x[2])[2]
    grid = [
        [[0 for x in range(max_x + 1)] for y in range(max_y + 1)]
        for z in range(max_z + 1)
    ]

    # Copy cubes into grid
    for cube in coords:
        x, y, z = cube
        grid[z][y][x] = 1

    if p2:
        fill_air_pockets(grid)

    # Find out how many sides are exposed per cube
    exposed_sides = 0
    for cube in coords:
        # 6 sides in a cube
        criteria = get_adjacent_coords(cube)

        for side in criteria:
            exposed_sides += check_adjacent(grid, side)

    return exposed_sides


print("Part 1: ", end="")
print(solve())
print("Part 2: ", end="")
print(solve(p2=True))
