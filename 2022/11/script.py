from collections import deque
import math

operations = {
    "*": (lambda left, right: left * right),
    "+": (lambda left, right: left + right),
    "-": (lambda left, right: left - right),
}

# LCM between divisible numbers
# Any other value will affect item's worry number's properties
def get_lcm(monkeys):
    return math.lcm(*[monkeys[i]["cond"] for i in monkeys])


def parse():
    content = [
        [i.split() for i in line.split("\n")]
        for line in open("input.txt", "r")
        .read()
        .replace(",", "")
        .replace(":", "")
        .split("\n\n")
    ]
    monkeys = dict()
    # 0: Monkey, <key>
    # 1: items: [:2]
    # 2: op: [:3]
    # 3: Div: [-1]
    # 4: True dest: [-1]
    # 5: False dest: [-1]
    for i in content:
        monkey = {"op": [], "items": [], "cond": 0, "t_d": 0, "f_d": 0}
        monkey["items"] = deque([int(num) for num in i[1][2:]])
        monkey["op"] = i[2][3:]
        monkey["cond"] = int(i[3][-1])
        monkey["t_d"] = int(i[4][-1])
        monkey["f_d"] = int(i[5][-1])
        monkeys[int(i[0][1])] = monkey
    return monkeys


def solve(rounds, divisor=1):
    monkeys = parse()
    inspection_count = [0 for _ in range(len(monkeys))]
    lcm = get_lcm(monkeys)
    for t in range(rounds):
        for i in range(len(monkeys)):
            op, cond, t_d, f_d, items = (
                monkeys[i]["op"],
                monkeys[i]["cond"],
                monkeys[i]["t_d"],
                monkeys[i]["f_d"],
                monkeys[i]["items"],
            )
            while len(items) > 0:
                item = items.popleft()

                # Calculate worry
                left, right = [
                    item if var == "old" else int(var) for var in [op[0], op[2]]
                ]
                # Without culling numbers, numbers will get too large for modulo operations
                res = operations[op[1]](left, right) % lcm
                res = res // divisor

                # Send to appropriate monkey
                dest = t_d if res % cond == 0 else f_d
                monkeys[dest]["items"].append(res)

                inspection_count[i] += 1
    max_2 = sorted(inspection_count, reverse=True)[:2]
    return math.prod(max_2)


print("Part 1:", end="")
print(solve(20, 3))
print("Part 2:", end="")
print(solve(10000, 1))
