import queue

instructions = [i.split() for i in open("input.txt", "r").read().splitlines()]


def parse():
    actions = queue.Queue()

    actions.put(0)

    for i in instructions:
        # Takes 2 cycles to fulfill so put a spacer
        actions.put(0)
        cmd = i[0]
        if cmd == "addx":
            actions.put(int(i[1]))
    return actions


def p1():
    actions = parse()
    t, x = 1, 1
    checkpts = {20, 60, 100, 140, 180, 220}
    signals = []
    for _ in range(actions.qsize()):
        dx = actions.get()
        x += dx
        if t in checkpts:
            signals.append(t * x)
        t += 1
    return sum(signals)


def p2():
    actions = parse()
    t, x = 1, 1
    render = []
    for _ in range(actions.qsize()):
        dx = actions.get()
        x += dx
        pos = (t - 1) % 40
        if abs(x - pos) < 2:
            render.append("#")
        else:
            render.append(".")
        t += 1
    print_render(render)


def print_render(render):
    for i in range(len(render) // 40):
        print("")
        for j in range(40):
            print(render[(i * 40) + j], end="")


print(p1())
p2()
