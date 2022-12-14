def parse():
    return [
        [tuple([int(x) for x in j.split(",")]) for j in i.split(" -> ")]
        for i in open("input.txt").read().splitlines()
    ]


def print_grid(grid):
    for row in grid:
        row_str = "".join(["." if i == 0 else "#" if i == -1 else "o" for i in row])
        print(row_str)


def draw_grid(lines, is_p2=False):
    # Find min and max xy and populate grid relative to it
    x = tuple(coord[0] for line in lines for coord in line)
    y = tuple(coord[1] for line in lines for coord in line)
    min_x, max_x = min(x), max(x)
    # 0 has to be min y since that's where the origin is
    min_y, max_y = min(min(y), 0), max(y)
    bounds = (min_x, min_y, max_x, max_y)

    grid_x = max_x - min_x + 1
    grid_y = max_y - min_y + 1

    # P2
    if is_p2:
        # y is 2 over max y
        y = max_y - min_y + 1 + 2
        # x must be enough to block until origin
        x = 1
        for i in range(y):
            x += 2
        x += 2
        grid_x = x
        grid_y = y
        # Center x to 500
        min_x = 500 - (x // 2)
        bounds = (min_x, min_y, max_x, max_y)

    grid = [[0 for j in range(grid_y)] for i in range(grid_x)]

    # P2
    if is_p2:
        # Draw boundaries at the bottom level
        for x in grid:
            x[-1] = -1

    # Draw lines
    for line in lines:
        # At least 2 coords in a line
        for i in range(1, len(line)):
            start, end = line[i - 1], line[i]
            # Horizontal
            if start[1] == end[1]:
                trend = -1 if start[0] < end[0] else 1
                r_start, r_end = min(start[0], end[0]), max(start[0], end[0])
                for i in range(r_start - min_x, r_end - min_x + 1):
                    grid[i][start[1] - min_y] = -1
            # Vertical
            else:
                trend = -1 if start[1] < end[1] else 1
                r_start, r_end = min(start[1], end[1]), max(start[1], end[1])
                for i in range(r_start - min_y, r_end - min_y + 1):
                    grid[start[0] - min_x][i] = -1
    return bounds, grid


def add_sand(bounds, grid):
    min_x, min_y, max_x, max_y = bounds
    origin = (500 - min_x, 0 - min_y)

    blocked = False
    x, y = origin
    # x: 494 to 503 or 0 to 8 y: 0 to 9
    while not blocked:
        # If origin is blocked
        if grid[origin[0]][origin[1]] != 0:
            return False
        # Not blocked but out of bounds; Cannot add sand
        if x < 0 or x >= len(grid) or y >= len(grid[0]) - 1:
            return False
        # Lookup y ahead
        target = grid[x][y + 1]
        if target == 0:
            # Empty; free to fall
            y += 1
        else:
            # Occupied, need to move horizontally
            # Move left first
            if x == 0:
                # Moving left will bring it out of bounds
                return False
            else:
                target = grid[x - 1][y + 1]
                if target == 0:
                    y += 1
                    x -= 1
                else:
                    # Cannot move left
                    # Already at the rightmost boundary; will fall out of bounds
                    if x == len(grid) - 1:
                        return False
                    else:
                        target = grid[x + 1][y + 1]
                        if target == 0:
                            y += 1
                            x += 1
                        else:
                            # Nowhere to go; blocked
                            blocked = True
    grid[x][y] = 1
    return True


def sand_sim(bounds, grid):
    count = 0
    contained = True
    while contained:
        contained = add_sand(bounds, grid)
        if contained:
            count += 1
    print_grid(grid)
    return count


def solve(is_p2=False):
    lines = parse()
    bounds, grid = draw_grid(lines, is_p2)
    return sand_sim(bounds, grid)


print("Part 1: ")
print(solve(is_p2=False))
print("Part 2: ")
print(solve(is_p2=True))
