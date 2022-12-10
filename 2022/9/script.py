moves = [(i.split()) for i in open("input.txt", "r").read().splitlines()]


def trail_tail(h_x, h_y, t_x, t_y):
    # Follow where the head goes
    print(h_x, h_y, t_x, t_y)

    # # Don't move unless diff between head and tail position is greater than 1
    if abs(h_x - t_x) > 1:
        # Move tail x in direction of head
        if h_x < t_x:
            t_x -= 1
        else:
            t_x += 1
        # If y was also diagonal, move it closer to y
        if h_y != t_y:
            if h_y < t_y:
                t_y -= 1
            else:
                t_y += 1
    if abs(h_y - t_y) > 1:
        if h_y < t_y:
            t_y -= 1
        else:
            t_y += 1
        # if diagonal, move x as well
        if h_x != t_x:
            if h_x < t_x:
                t_x -= 1
            else:
                t_x += 1

    return t_x, t_y


def p1():
    visited = set()
    t_x, t_y = 0, 0
    h_x, h_y = 0, 0
    visited.add((t_x, t_y))

    for i in moves:
        dir, steps = i[0], int(i[1])
        for _ in range(steps):
            # Left
            if dir == "L":
                h_x -= 1
            elif dir == "R":
                h_x += 1
            elif dir == "U":
                h_y += 1
            else:
                h_y -= 1
            t_x, t_y = trail_tail(h_x, h_y, t_x, t_y)
            print(f"new t pos {t_x, t_y}")
            visited.add((t_x, t_y))

    return len(visited)


def p2():
    visited = set()
    knots = [[0, 0] for _ in range(10)]
    visited.add((0, 0))

    for i in moves:
        dir, steps = i[0], int(i[1])
        for _ in range(steps):
            # Left
            if dir == "L":
                knots[0][0] -= 1
            elif dir == "R":
                knots[0][0] += 1
            elif dir == "U":
                knots[0][1] += 1
            else:
                knots[0][1] -= 1
            for i in range(1, 10):
                t_x, t_y = trail_tail(
                    knots[i - 1][0], knots[i - 1][1], knots[i][0], knots[i][1]
                )
                knots[i] = [t_x, t_y]
                if i == 9:
                    visited.add((t_x, t_y))
    return len(visited)


# print(p1())
print(p2())
