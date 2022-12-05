import re

# Parse file
file = open("input.txt", "r")
content = file.read().splitlines()


def regex_parse(pattern, str):
    return [tuple([int(y) for y in x.split(",")]) for x in re.findall(pattern, str)]


def init_grid(grid, x, y):
    for _ in range(x + 1):
        grid.append([0 for _ in range(y + 1)])
        # for j in range(y + 1):
        #     grid[i].append(0)


def fill_grid_x(line, grid):
    y = line[0][1]
    intersects = 0
    min_x, max_x = min(line[0][0], line[1][0]), max(line[0][0], line[1][0])
    for x in range(min_x, max_x + 1):
        grid[x][y] += 1
        # Only count towards the intersect once
        if grid[x][y] == 2:
            intersects += 1

    return intersects


def fill_grid_y(line, grid):
    x = line[0][0]
    intersects = 0
    min_y, max_y = min(line[0][1], line[1][1]), max(line[0][1], line[1][1])
    for y in range(min_y, max_y + 1):
        grid[x][y] += 1
        # Only count towards the intersect once
        if grid[x][y] == 2:
            intersects += 1

    return intersects


def fill_diagonal(line, grid):
    intersects = 0
    # The order from origin to destination matters
    x_increasing = line[1][0] - line[0][0] > 0
    y_increasing = line[1][1] - line[0][1] > 0
    y = line[0][1]
    if x_increasing:
        for x in range(line[0][0], line[1][0] + 1):
            grid[x][y] += 1
            if grid[x][y] == 2:
                intersects += 1
            if y_increasing:
                y += 1
            else:
                y -= 1
    else:
        for x in range(line[0][0], line[1][0] - 1, -1):
            grid[x][y] += 1
            if grid[x][y] == 2:
                intersects += 1
            if y_increasing:
                y += 1
            else:
                y -= 1
    return intersects


def p1():
    lines = []
    grid = []
    max_x = 0
    max_y = 0
    intersects = 0
    for i in content:
        pattern = "\d+[,]{1}\d+"
        # Only handle horizontal or vertical lines
        line = regex_parse(pattern, i)

        if line[0][0] == line[1][0] or line[0][1] == line[1][1]:
            lines.append(line)
    max_x = max([max(line[0][0], line[1][0]) for line in lines])
    max_y = max([max(line[0][1], line[1][1]) for line in lines])

    # Set up empty grid
    init_grid(grid, max_x, max_y)

    # fill grid and find intersects
    for line in lines:
        if line[0][0] == line[1][0]:
            # x is constant; range of y
            intersects += fill_grid_y(line, grid)
        elif line[0][1] == line[1][1]:
            # y is constant; range of x
            intersects += fill_grid_x(line, grid)
    print(intersects)


def p2():
    lines = []
    grid = []
    max_x = 0
    max_y = 0
    intersects = 0
    for i in content:
        pattern = "\d+[,]{1}\d+"
        line = regex_parse(pattern, i)
        lines.append(line)
    max_x = max([max(line[0][0], line[1][0]) for line in lines])
    max_y = max([max(line[0][1], line[1][1]) for line in lines])

    # Set up empty grid
    init_grid(grid, max_x, max_y)

    # fill grid and find intersects
    for line in lines:
        if line[0][0] == line[1][0]:
            # x is constant; range of y
            intersects += fill_grid_y(line, grid)
        elif line[0][1] == line[1][1]:
            # y is constant; range of x
            intersects += fill_grid_x(line, grid)
        else:
            intersects += fill_diagonal(line, grid)
    print(intersects)


p1()
p2()
