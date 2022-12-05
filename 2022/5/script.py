import re


def parse():
    # Parse file
    file = open("input.txt", "r")
    content = file.read().splitlines()
    stack, instructions = [], []
    newline_found = False
    for line in content:
        if line == "":
            newline_found = True
        else:
            if newline_found:
                instructions.append(line)
            else:
                # one crate = 3 characters
                # 3 char * 9 lanes + 8 spacers = 35
                crates = []
                for i in range(1, 35, 4):
                    #
                    crates.append(line[i])
                stack.append(crates)

    # Organize stacks in hash map
    stacks = {}
    for i in range(1, 10):
        stacks[i] = []

    # Populate stacks
    for i in range(len(stack) - 2, -1, -1):
        level = stack[i]
        counter = 1
        for crate in level:
            if crate != " ":
                stacks[counter].append(crate)
            counter += 1

    # Parse instructions into tuples
    ins = []
    for i in instructions:
        tup = tuple([int(x) for x in re.findall("\d+", i)])
        ins.append(tup)

    return stacks, ins


def print_answer(stacks):
    res = []
    for key in stacks:
        if len(stacks[key]) > 0:
            crate = stacks[key].pop()
            res.append(crate)
    print("".join(res))


def p1():
    stacks, ins = parse()

    # Process instructions
    for i in ins:
        # i[0] is the number of crates
        # i[1] is origin
        # i[2] is dest
        for _ in range(i[0]):
            if len(stacks[i[1]]) > 0:
                crate = stacks[i[1]].pop()
                stacks[i[2]].append(crate)
    print_answer(stacks)


def p2():
    stacks, ins = parse()

    # Process instructions
    for i in ins:
        # i[0] is the number of crates
        # i[1] is origin
        # i[2] is dest
        temp = []
        for _ in range(i[0]):
            if len(stacks[i[1]]) > 0:
                crate = stacks[i[1]].pop()
                temp.append(crate)
        while len(temp) > 0:
            stacks[i[2]].append(temp.pop())

    print_answer(stacks)


p1()
p2()
