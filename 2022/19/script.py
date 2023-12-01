from re import findall
from math import ceil
from queue import deque


def parse():
    # 0: ID
    # 1: Ore robot cost (ore)
    # 2: Clay robot cost (ore)
    # 3: Obs cost (ore)
    # 4: Obs cost (clay)
    # 5: Geode cost (ore)
    # 6: Geode cost (obs)
    robot_cost = [
        tuple([int(i) for i in findall("\d+", line)])
        for line in open(
            "/Users/derekdkim/Programming/AdventOfCode/2022/19/input.txt", "r"
        )
        .read()
        .splitlines()
    ]
    blueprints = []
    for blueprint in robot_cost:
        (
            bp_id,
            bot_0_ore,
            bot_1_ore,
            bot_2_ore,
            bot_2_clay,
            bot_3_ore,
            bot_3_obs,
        ) = blueprint
        blueprints.append(
            [
                ((0, bot_0_ore),),
                ((0, bot_1_ore),),
                ((0, bot_2_ore), (1, bot_2_clay)),
                ((0, bot_3_ore), (2, bot_3_obs)),
            ]
        )
    return blueprints


def can_robot_be_built_now(resources, recipe):
    buildable = True
    for res in recipe:
        r_type, qty = res
        if resources[r_type] < qty:
            buildable = False
    return buildable


# Rules:
# Goal, maximize the production of geode miners
# If a geode robot can be built, build it
# If the rate of current obs prod + stored ores is

memo = dict()


def geode_sim(t, bp):
    # Start with 1 ore bot
    bots = {
        # 0: Ore
        0: 1,
        # 1: Clay
        1: 0,
        # 2: Obs
        2: 0,
        # 3: Geode
        3: 0,
    }

    # Player resources
    bots = (1, 0, 0, 0)
    resources = (0, 0, 0, 0)

    # Explore each solution
    deq = deque([(bots, resources, t)])

    # Optimizations
    max_res = [
        max([i[1] for recipe in bp for i in recipe if i[0] == 0]),
        max([i[1] for recipe in bp for i in recipe if i[0] == 1]),
        max([i[1] for recipe in bp for i in recipe if i[0] == 2]),
    ]
    banned = set()

    # Max geodes
    max_g = 0

    while deq:
        # for i in range(30):
        curr_bots, curr_res, t_rem = deq.popleft()
        # if curr_bots == (2, 1, 1, 0):
        if curr_bots == (4, 4, 7, 4):
            print(curr_bots, curr_res, t_rem)
        # Calculate total geode if nothing is built
        # Only do this if we actually have a geode bot
        # print(curr_bots, curr_res, t_rem)
        if curr_bots[3] > 0:
            total_g = curr_res[3] + (curr_bots[3] * t_rem)
            if t_rem == 0:
                total_g += 1
            max_g = max(max_g, total_g)
            # if curr_bots[3] == 2:
            #     print(curr_bots, curr_res, t_rem, total_g)

        # Don't continue if max is more than the number of bots + current reserve:
        if t_rem < t // 2:
            max_potential = ceil(t_rem / 2) * ((2 * curr_bots[3]) + (t_rem - 1))
            if curr_res[3] + max_potential < max_g:
                continue

        if len(banned) < 3:
            # No more robots needed than the max number of resources since only 1 robot can be made at a time
            for b_t, max_bot_count in enumerate(max_res):
                if curr_bots[b_t] >= max_bot_count:
                    banned.add(b_t)

        # if it can be built, calculate the time cost and update state, then add to deq
        if t_rem > 0:
            for bot_tier, recipe in enumerate(bp):
                if bot_tier not in banned:
                    # Only built a robot if its feasible to build up to that resource with current robot count
                    can_be_built = True
                    for res in recipe:
                        r_type, qty = res
                        # No bots to mine said resource; need to build precursor first
                        if curr_bots[r_type] == 0:
                            can_be_built = False
                        # Impossible to build that robot within timeframe
                        # Also, pointless to build at the last minute
                        if curr_res[r_type] + (curr_bots[r_type] * t_rem) < qty:
                            can_be_built = False

                    if can_be_built:
                        new_bots, new_res = [*curr_bots], [*curr_res]
                        # How many potential robots we can build
                        have_enough_to_build = can_robot_be_built_now(curr_res, recipe)

                        # Can build something right away, advance by 1 minute and build one bot
                        if have_enough_to_build:
                            # Collect resources
                            for k, v in enumerate(new_bots):
                                new_res[k] += v
                            # Build bots
                            new_bots[bot_tier] += 1

                            # Remove used resources from stockpile
                            for res in recipe:
                                r_type, qty = res
                                new_res[r_type] -= qty

                            deq.append((tuple(new_bots), tuple(new_res), t_rem - 1))
                        else:
                            # Can only build in the future
                            # Find the limiting reagent and the time it takes to save for the next robot
                            t_req = []
                            for res in recipe:
                                r_type, qty = res
                                t_req.append(
                                    ceil((qty - new_res[r_type]) / new_bots[r_type])
                                )
                                # Pre-subtract the cost from new pool of resources
                                new_res[r_type] -= qty
                            # Gather resources at the end of a minute.
                            # You can only start building once you have resources on hand
                            t_req = max(t_req) + 1

                            # Collect resources
                            for k, v in enumerate(new_bots):
                                new_res[k] += v * t_req

                            # Build that new bot
                            new_bots[bot_tier] += 1

                            if t_rem - t_req >= 0:
                                deq.append(
                                    (tuple(new_bots), tuple(new_res), t_rem - t_req)
                                )

    return max_g


def solve(t, is_part_2=False):
    blueprints = parse()
    results = 0
    if is_part_2:
        blueprints = blueprints[:3]
        results = 1
    n = len(blueprints)
    for i, bp in enumerate(blueprints):
        geode = geode_sim(t, bp)
        if is_part_2:
            results *= geode
        else:
            results += (i + 1) * geode
    # results = geode_sim(t, blueprints[2])

    return results


print(solve(24))
print(solve(32, is_part_2=True))

# (0, 3), (2, 16)
# 7 (6, 18) before creating
# def test():
#     # recipe = parse()[9][3]
#     # print(recipe)
#     # new_bots = [1, 2, 3, 4]
#     # new_res = [15, 0, 16, 0]
#     # t_req = []
#     # for res in recipe:
#     #     r_type, qty = res
#     #     t_req.append(ceil((qty - new_res[r_type]) / new_bots[r_type]))
#     #     # Pre-subtract the cost from new pool of resources
#     #     new_res[r_type] -= qty
#     # # Gather resources at the end of a minute.
#     # # You can only start building once you have resources on hand
#     # t_req = max(t_req) + 1
#     # print(t_req)

#     # t_rem = 4
#     # max_potential = ceil(t_rem / 2) * ((2 * 4) + (t_rem - 1))
#     # print(max_potential)


# test()
