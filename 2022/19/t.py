from heapq import heapify, heappop, heappush


def find_best(ore_robot, clay_robot, obsidian_robot, geode_robot, end):
    t, ore, clay, obsidian, geode = 0, 0, 0, 0, 0
    max_ore = max(x["o"] for x in [ore_robot, clay_robot, obsidian_robot, geode_robot])
    max_clay = max(
        x["c"] if "c" in x else 0
        for x in [ore_robot, clay_robot, obsidian_robot, geode_robot]
    )
    max_obsidian = max(
        x["ob"] if "ob" in x else 0
        for x in [ore_robot, clay_robot, obsidian_robot, geode_robot]
    )
    queue = [
        (
            t,
            ore,
            clay,
            obsidian,
            geode,
            ore_robot["a"],
            clay_robot["a"],
            obsidian_robot["a"],
            geode_robot["a"],
        )
    ]
    heapify(queue)
    best = set()
    while queue:
        q = heappop(queue)
        t, ore, clay, obsidian, geode, ore_a, clay_a, obsidian_a, geode_a = q
        if t > end - 10:
            l = min(
                [
                    geode_robot["ob"] // (obsidian_a or 1),
                    geode_robot["o"] // (ore_a or 1),
                ]
            )
            # if (ore_a, clay_a, obsidian_a, geode_a) == (4, 4, 7, 5):
            #     print(q)
            if geode + (geode_a * (end - t)) + (l * ((end - t) // 2)) < max(
                best or [0]
            ):
                continue
        best.add(geode)
        ore_flag, clay_flag, obsidian_flag, geode_flag = 0, 0, 0, 0
        for t in range(t, end):
            best.add(geode)
            if not ore_flag and ore >= (o := ore_robot["o"]) and ore_a < max_ore:
                heappush(
                    queue,
                    (
                        t + 1,
                        ore - o + ore_a,
                        clay + clay_a,
                        obsidian + obsidian_a,
                        geode + geode_a,
                        ore_a + 1,
                        clay_a,
                        obsidian_a,
                        geode_a,
                    ),
                )
                ore_flag = 1
            if not clay_flag and ore >= (o := clay_robot["o"]) and clay_a < max_clay:
                heappush(
                    queue,
                    (
                        t + 1,
                        ore - o + ore_a,
                        clay + clay_a,
                        obsidian + obsidian_a,
                        geode + geode_a,
                        ore_a,
                        clay_a + 1,
                        obsidian_a,
                        geode_a,
                    ),
                )
                clay_flag = 1
            if (
                not obsidian_flag
                and ore >= (o := obsidian_robot["o"])
                and clay >= (c := obsidian_robot["c"])
                and obsidian_a < max_obsidian
            ):
                heappush(
                    queue,
                    (
                        t + 1,
                        ore - o + ore_a,
                        clay - c + clay_a,
                        obsidian + obsidian_a,
                        geode + geode_a,
                        ore_a,
                        clay_a,
                        obsidian_a + 1,
                        geode_a,
                    ),
                )
                obsidian_flag = 1
            if (
                not geode_flag
                and ore >= (o := geode_robot["o"])
                and obsidian >= (ob := geode_robot["ob"])
            ):
                heappush(
                    queue,
                    (
                        t + 1,
                        ore - o + ore_a,
                        clay + clay_a,
                        obsidian - ob + obsidian_a,
                        geode + geode_a,
                        ore_a,
                        clay_a,
                        obsidian_a,
                        geode_a + 1,
                    ),
                )
                geode_flag = 1
            ore += ore_a
            clay += clay_a
            obsidian += obsidian_a
            geode += geode_a
    print(max(best))
    return max(best)


with open("input.txt", "r") as file:
    data = {
        (z := [int(x) for x in y.split(" ") if x.isdigit()])[0]: [
            {"a": 1, "o": z[1]},
            {"a": 0, "o": z[2]},
            {"a": 0, "o": z[3], "c": z[4]},
            {"a": 0, "o": z[5], "ob": z[6]},
        ]
        for y in file.read().replace(":", " :").splitlines()
    }
    p1, p2 = 0, 1
    for blueprint, (ore_robot, clay_robot, obsidian_robot, geode_robot) in data.items():
        if blueprint < 4:
            p2 *= find_best(
                {**ore_robot}, {**clay_robot}, {**obsidian_robot}, {**geode_robot}, 32
            )
        # p1 += blueprint * find_best(
        #     {**ore_robot}, {**clay_robot}, {**obsidian_robot}, {**geode_robot}, 24
        # )
    print("day 19 :", p1, p2)
