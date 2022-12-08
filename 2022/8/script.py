import math

# Parse and Build matrix
content = [[*i] for i in open("input.txt", "r").read().splitlines()]

# Look to find how many trees are not completely blocked
def p1():
    count = 0
    for y, row in enumerate(content):
        for x, tree in enumerate(row):
            # Exterior
            if y == 0 or x == 0 or y == len(content) - 1 or x == len(row) - 1:
                count += 1
            else:
                # Interior
                vis = 0
                # North
                max_n = max([content[i][x] for i in range(y)])
                if tree > max_n:
                    vis += 1

                # South
                max_s = max([content[i][x] for i in range(y + 1, len(content))])
                if tree > max_s:
                    vis += 1

                # West
                max_w = max([row[i] for i in range(x)])
                if tree > max_w:
                    vis += 1

                # East
                max_e = max([row[i] for i in range(x + 1, len(row))])
                if tree > max_e:
                    vis += 1

                if vis > 0:
                    count += 1
    return count


# Find the tree that has the most trees visible from its height
def p2():
    max_v = 0
    for y, row in enumerate(content):
        for x, tree in enumerate(row):
            # Ignore Exterior
            if not (y == 0 or x == 0 or y == len(content) - 1 or x == len(row) - 1):
                # Interior

                vis = [0, 0, 0, 0]
                # North
                target = y - 1
                blocked = False
                while target >= 0 and not blocked:
                    vis[0] += 1
                    if content[target][x] >= tree:
                        blocked = True
                    target -= 1

                # South
                target = y + 1
                blocked = False
                while target < len(content) and not blocked:
                    vis[1] += 1
                    if content[target][x] >= tree:
                        blocked = True
                    target += 1

                # West
                target = x - 1
                blocked = False
                while target >= 0 and not blocked:
                    vis[2] += 1
                    if row[target] >= tree:
                        blocked = True
                    target -= 1

                # East
                target = x + 1
                blocked = False
                while target < len(row) and not blocked:
                    vis[3] += 1
                    if row[target] >= tree:
                        blocked = True
                    target += 1

                max_v = max(max_v, math.prod(vis))
    return max_v


print(p1())
print(p2())
