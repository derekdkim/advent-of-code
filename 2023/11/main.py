file = open('input.txt', 'r').read().splitlines()

def parse_graph(file):
    # Tabulate how many times a galaxy appears in a given x or y
    cols = dict()
    rows = dict()
    galaxies = []

    for y, line in enumerate(file):
        if y not in rows:
            rows[y] = 0
        for x, cell in enumerate(line):
            if x not in cols:
                cols[x] = 0
            
            if cell == '#':
                rows[y] += 1
                cols[x] += 1
                galaxies.append((y, x))
    
    return galaxies, cols, rows

def solve(p2 = False):
    galaxies, cols, rows = parse_graph(file)
    total = 0
    modifier = 1000000 if p2 else 2

    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            # Calculate manhattan distance between g1 and g2
            g1, g2 = galaxies[i], galaxies[j]
            miny, maxy = min(g1[0], g2[0]), max(g1[0], g2[0])
            minx, maxx = min(g1[1], g2[1]), max(g1[1], g2[1])
            dy, dx = 0, 0
            for k in range(miny, maxy):
                dy += modifier if rows[k] == 0 else 1
            for k in range(minx, maxx):
                dx += modifier if cols[k] == 0 else 1
            
            total += dy + dx
    
    return total

print(solve(False))
print(solve(True))