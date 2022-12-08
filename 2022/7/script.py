file = open("input.txt", "r")
content = file.read().splitlines()

# Anything with $ is a command
# dir <X> is a directory with something inside
# ls after a dir shows the content of a dir
# if a dir shows in ls inside of another dir, it's the parent : DISREGARD


def parse():
    # Keeps track of current path
    stack = []
    # Size contained in each dir
    sizes = {}

    for line in content:
        l = line.split()
        # Either command or content output
        if l[0] == "$":
            # command; cd or ls
            cmd = l[1]
            if cmd == "cd":
                dest = l[2]
                # Backtrack
                if dest == "..":
                    stack.pop()
                # Has dest; add to path
                else:
                    stack.append(l[2])
        # Ignore ls, doesn't change anyhting until next traversal
        # All outputs follow the command
        # ignore dir since we can get to it via traversal
        # Add size in every dir leading up to the curr dir
        # "/": 1000, "/-a": 100, "/-b": 900, "/-b-c": 890, "/-b-d": 10
        elif l[0] != "dir":
            # Ignore file name l[1]
            for i in range(len(stack)):
                # Numerical; add to sizes
                full_path = "-".join(stack[: i + 1])
                if full_path not in sizes:
                    sizes[full_path] = 0
                sizes[full_path] += int(l[0])
    return stack, sizes


def p1():
    stack, sizes = parse()
    # Find all dirs greater than 100k size and add together
    return sum([sizes[i] for i in sizes if sizes[i] < 100000])


def p2():
    stack, sizes = parse()
    # Total - currently consumed
    rem = 70000000 - sizes["/"]
    req_space = 30000000 - rem
    # Find smallest dir of ones with space for update
    return min(sizes[i] for i in sizes if sizes[i] >= req_space)


print(p1())
print(p2())
