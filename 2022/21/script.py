from functools import lru_cache


def parse():
    monkeys = [
        [x for x in line.replace(":", "").split()]
        for line in open("input.txt", "r").readlines()
    ]
    # Organize monkeys into hash map
    return {monkey[0]: monkey[1:] for monkey in monkeys}


operate = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x // y,
}

# If x is the result, we can always reverse operations
rev_op_x = {
    "+": lambda x, y: x - y,
    "-": lambda x, y: x + y,
    "*": lambda x, y: x // y,
    "/": lambda x, y: x * y,
}

# If y is the result we're trying to find
# z = x // y
# y = x // z
# z = x - y
# y = x - z
rev_op_y = {
    "+": lambda x, y: x - y,
    "-": lambda x, y: y - x,
    "*": lambda x, y: x // y,
    "/": lambda x, y: y // x,
}


def p1():
    mmap = parse()

    @lru_cache(maxsize=None)
    def calc(key):
        # len 1 means its a number
        if len(mmap[key]) == 1:
            return int(mmap[key][0])
        else:
            # All calculations are in the form of [x, operator, y]
            x, op, y = mmap[key]
            return operate[op](calc(x), calc(y))

    return calc("root")


def p2():
    mmap = parse()
    memo = dict()
    call_stack = dict()

    def calc(key):
        if key == "root":
            x, op, y = mmap[key]
            return calc(x), calc(y)
        elif len(mmap[key]) == 1:
            memo[key] = int(mmap[key][0])
        else:
            # All calculations are in the form of [x, operator, y]
            x, op, y = mmap[key]

            # record the order of which keys were called
            curr_stack = [key]
            if key in call_stack:
                curr_stack = [*call_stack[key]]
            call_stack[x] = [*curr_stack, x]
            call_stack[y] = [*curr_stack, y]
            memo[key] = operate[op](calc(x), calc(y))
        return memo[key]

    # Determine which side is affected
    a1, a2 = calc("root")
    # Find the value of the parent of humn
    humn_parent = call_stack["humn"][0]
    affected_val = memo[humn_parent]

    target = a1 if a2 == affected_val else a2

    # Perform reverse operations on the call stack up to humn to get answer
    # Set the value of humn parent to the target num
    result = target
    # Ignore the subtree root because that will be equal to the target
    # Ignore the last because that's humn
    for key in call_stack["humn"][:-1]:
        x, op, y = mmap[key]
        x_val, y_val = memo[x], memo[y]

        if x in call_stack["humn"]:
            result = rev_op_x[op](result, y_val)
        else:
            result = rev_op_y[op](result, x_val)

    return result


print("Part 1: ")
print(p1())
print("Part 2: ")
print(p2())
