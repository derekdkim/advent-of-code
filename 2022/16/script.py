import re
from queue import deque
from functools import lru_cache


def parse():
    content = open("input.txt").read().splitlines()
    pattern = "[A-Z]{2}"

    content = [
        [re.findall(pattern, line), int(re.search("\d+", line).group(0))]
        for line in content
    ]
    # first elem = pipe
    # subsequent elems, adjacent nodes
    valves = dict()
    for line in content:
        key = line[0][0]
        adj = line[0][1:]
        valves[key] = {"adj": adj, "value": line[1]}

    # Transform valves dict to graph
    neighbours = {
        key: [
            (neighbour, valves[neighbour]["value"]) for neighbour in valves[key]["adj"]
        ]
        for key in valves
    }
    rates = {key: val["value"] for key, val in valves.items()}
    return neighbours, rates


def solve():
    neighbours, rates = parse()

    @lru_cache(maxsize=None)
    def get_all_paths():
        all_paths = {}
        for node in rates:
            deq = deque([(node, 0)])
            paths = {}

            # Calculate the time required to get to each path
            while deq:
                key, dist = deq.popleft()
                for dest in neighbours[key]:
                    dest = dest[0]
                    if dest not in paths:
                        paths[dest] = dist + 2
                        deq.append((dest, dist + 1))
            paths = {key: val for key, val in paths.items() if rates[key] > 0}
            all_paths[node] = paths
        return all_paths

    paths = get_all_paths()

    def p1(start, t):
        max_pressure = 0

        # ((Worker pos 1, worker 1 time remaining), (Worker 2), Total Pressure, Opened)
        deq = deque([(start, t, 0, tuple())])
        while deq:
            key, time, total, opened = deq.popleft()

            # Compute the time cost and potential pressure for each adjacent node
            for dest, cost in paths[key].items():
                if cost <= time and dest not in opened:
                    pressure = rates[dest] * (time - cost)
                    deq.append(
                        (
                            dest,
                            time - cost,
                            total + pressure,
                            (*opened, dest),
                        )
                    )

            max_pressure = max(max_pressure, total)

        return max_pressure

    def p2(t=26):
        max_pressure = float("-inf")
        max_nodes = len(paths["AA"])
        cache = dict()

        # ((Worker pos 1, worker 1 time remaining), (Worker 2), Total Pressure, Opened)
        deq = deque([(("AA", t), ("AA", t), 0, tuple())])
        while deq:
            w1, w2, total, opened = deq.popleft()
            workers = [w1, w2]
            if (w1[1], w2[1], opened) in cache:
                if cache[(w1[1], w2[1], opened)] > total:
                    continue
            cache[(w1[1], w2[1], opened)] = total
            # if total >= max_pressure:
            # max_pressure = total
            if len(opened) < max_nodes:
                next_moves = [[], []]
                for i in range(2):
                    key, time = workers[i]
                    # Compute the time cost and potential pressure for each adjacent node
                    for dest, cost in paths[key].items():
                        if cost <= time and dest not in opened:
                            pressure = rates[dest] * (time - cost)
                            next_moves[i].append(
                                (
                                    dest,
                                    time - cost,
                                    pressure,
                                    (*opened, dest),
                                )
                            )

                # Add next valid moves to the queue
                for m1 in next_moves[0]:
                    for m2 in next_moves[1]:
                        # Prevent them from going to the same place next turn
                        if m1[0] == m2[0]:
                            continue

                        # Combine opened
                        new_opened = tuple(set(m1[3] + m2[3]))
                        new_total = total + m1[2] + m2[2]
                        if new_total > max_pressure * 0.9:
                            deq.append(
                                ((m1[0], m1[1]), (m2[0], m2[1]), new_total, new_opened)
                            )
                # Odd numbered edge case
                m1, m2 = next_moves
                if len(m1) > 0 and len(m2) == 0:
                    move = m1[0]
                    new_opened = (*opened, move[0])
                    new_total = total + move[2]
                    deq.append(((move[0], move[1]), w2, new_total, new_opened))
                if len(m2) > 0 and len(m1) == 0:
                    move = m2[0]
                    new_opened = (*opened, move[0])
                    new_total = total + move[2]
                    deq.append((w1, (move[0], move[1]), new_total, new_opened))
            max_pressure = max(max_pressure, total)

        return max_pressure

    print("Part 1: ", end="")
    print(p1("AA", 30))
    print("Part 2: ", end="")
    print(p2())


solve()
