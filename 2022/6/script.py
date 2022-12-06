def parse():
    # Parse file
    file = open("input.txt", "r")
    return file.read()


def solve(length):
    content = parse()
    chars = [*content]
    unique = set()
    pos = 0
    start = 0

    for i in chars:
        pos += 1
        while i in unique:
            unique.remove(chars[start])
            start += 1
        unique.add(i)
        if len(unique) == length:
            return pos


print(solve(4))
print(solve(14))
