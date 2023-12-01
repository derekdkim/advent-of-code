from copy import deepcopy


def parse():
    return [1 if i == ">" else -1 for i in [*open("input.txt").read()]]


def get_rock(rock_type):
    rocks = {
        0: [
            [2, 3, 4, 5],
        ],
        1: [[-1, 3, -1], [2, 3, 4], [-1, 3, -1]],
        2: [[-1, -1, 4], [-1, -1, 4], [2, 3, 4]],
        3: [[2], [2], [2], [2]],
        4: [[2, 3], [2, 3]],
    }
    return deepcopy(rocks[rock_type])


def init_container():
    return [[-1 for x in range(7)] for y in range(3)]


def print_grid(grid):
    for y in range(len(grid) - 1, -1, -1):
        print(
            "".join(
                [*["." if i == -1 else "#" if 1 else "@" for i in grid[y]], f"{y + 1}"]
            )
        )
    # for y in range(len(grid)):
    #     print("".join([*["." if i == -1 else "#" for i in grid[y]], f"{y + 1}"]))


def move_rock_horizontally(grid, rock, base_height, curr_gust):
    # Check leftmost side or rightmost side first depending on direction of the wind
    # Rock movement is all or nothing; none of the blocks must be blocked in order to move
    blocked = False
    h = base_height + len(rock) - 1
    for i, row in enumerate(rock):
        for j, cell in enumerate(row):
            # -1 is empty space
            if cell >= 0:
                # Check if i + curr_gust will push any cell out of bounds
                if cell + curr_gust < 0 or cell + curr_gust > 6:
                    blocked = True
                    break
                else:
                    # Check if the destination in any column gets in the way
                    cell_y = h - i
                    if grid[cell_y][cell + curr_gust] == 1:
                        blocked = True
                        break
    if not blocked:
        # Not blocked, update the current x axis of all the rock pieces
        for i, row in enumerate(rock):
            for j, cell in enumerate(row):
                # -1 is empty space
                if cell >= 0:
                    # Move cell
                    row[j] = cell + curr_gust


def solve(n):
    gust = parse()
    grid = init_container()
    max_h = 0
    max_h_cache = dict()

    gust_len = len(gust)
    gust_turn = 0

    for i in range(n):
        if max_h + 7 > len(grid):
            # Add 4 rows for every rock
            for _ in range(4):
                grid.append([-1 for _ in range(7)])
        rock = get_rock(i % 5)

        # Set initial coordinates for the rock
        # The bottom of the rock is always 3 y units above the highest point
        rock_base_h = max_h + 3
        moved = True
        while moved:
            # Adjust rock horizontally
            curr_gust = gust[gust_turn % gust_len]
            move_rock_horizontally(grid, rock, rock_base_h, curr_gust)
            gust_turn += 1

            # Attempt to move down
            # Stop if blocked
            # Check the lowest level of the rock
            # Already at the floor; can't move any further
            # Keep looping as long as the rock moved vertically the round before
            # so that the horizontal displacement can happen one last time
            if rock_base_h == 0:
                moved = False
            else:
                h = rock_base_h + len(rock) - 1
                for y in range(len(rock)):
                    for x in range(len(rock[y])):
                        if rock[y][x] != -1:
                            cell_y = h - y
                            if grid[cell_y - 1][rock[y][x]] == 1:
                                moved = False
                                break
                if moved:
                    rock_base_h -= 1

        # Update grid with new rock
        h = rock_base_h + len(rock) - 1
        for i, row in enumerate(rock):
            for j, cell in enumerate(row):
                # -1 is empty space
                if cell >= 0:
                    # Fill in space
                    cell_y = h - i
                    grid[cell_y][cell] = 1

        # Update height
        max_h = max(max_h, h + 1)
        max_h_cache[i] = max_h

    # print_grid(grid)
    return max_h


def p2(n):
    # Find a state where the board has reset
    # Below is the gust index at the start of a new rock at every new rock cycle
    # 0 24 12 | 2 28 15 5 34 21 10 | 2 28 15 5 34 21 10 | 2 28 15 5 34 21 10 | ...
    # The first 3 cycles (of 5 shapes) have unique states, but after that, there's a pattern
    # every 7 cycles, the board effectively resets
    gust = parse()
    grid = init_container()
    max_h = 0
    max_h_cache = dict()

    gust_len = len(gust)
    gust_turn = 0

    # Cycles
    cycle_cache = dict()
    cycle_found = False
    cycle_size = 0
    startup_rounds = 0
    i = 0

    # Find pattern
    while not cycle_found:
        if max_h + 7 > len(grid):
            # Add 4 rows for every rock
            for _ in range(4):
                grid.append([-1 for _ in range(7)])
        rock = get_rock(i % 5)

        if i % 5 == 0:
            curr_gust = gust_turn % gust_len
            if curr_gust in cycle_cache:
                if len(cycle_cache[curr_gust]) == 2:
                    cycle_found = True
                    cycle_size = i - cycle_cache[curr_gust][-1]
                    startup_rounds = i - cycle_size
                else:
                    cycle_cache[curr_gust].append(i)
            else:
                cycle_cache[curr_gust] = [i]

        # Set initial coordinates for the rock
        # The bottom of the rock is always 3 y units above the highest point
        rock_base_h = max_h + 3
        moved = True
        while moved:
            # Adjust rock horizontally
            curr_gust = gust[gust_turn % gust_len]
            move_rock_horizontally(grid, rock, rock_base_h, curr_gust)
            gust_turn += 1

            # Attempt to move down
            # Stop if blocked
            # Check the lowest level of the rock
            # Already at the floor; can't move any further
            # Keep looping as long as the rock moved vertically the round before
            # so that the horizontal displacement can happen one last time
            if rock_base_h == 0:
                moved = False
            else:
                h = rock_base_h + len(rock) - 1
                for y in range(len(rock)):
                    for x in range(len(rock[y])):
                        if rock[y][x] != -1:
                            cell_y = h - y
                            if grid[cell_y - 1][rock[y][x]] == 1:
                                moved = False
                                break
                if moved:
                    rock_base_h -= 1

        # Update grid with new rock
        h = rock_base_h + len(rock) - 1
        for y, row in enumerate(rock):
            for x, cell in enumerate(row):
                # -1 is empty space
                if cell >= 0:
                    # Fill in space
                    cell_y = h - y
                    grid[cell_y][cell] = 1

        # Update height
        max_h = max(max_h, h + 1)
        max_h_cache[i] = max_h
        i += 1

    # Calculate
    start_up_height = max_h_cache[startup_rounds]
    cycle_height = max_h_cache[startup_rounds + cycle_size] - start_up_height
    n = n - startup_rounds
    extrapolated_h = (n // cycle_size) * cycle_height
    remaining = n % cycle_size
    # Remaining is overshot by a full cycle so adjust
    rem_h = max_h_cache[remaining - 5] if remaining > 5 else -1

    return start_up_height + extrapolated_h + rem_h


print("Part 1: ", end="")
print(solve(2022))
print("Part 2: ", end="")
print(p2(1000000000000))
