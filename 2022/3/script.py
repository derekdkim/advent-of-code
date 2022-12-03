# Parse file
file = open("input.txt", "r")
content = file.read().splitlines()

# 97 - a -> 1
# 65 - A -> 27
def convert_char_to_prio(char):
    code = ord(char)
    # Lowercase
    # [1, 26]
    if code > 97:
        return code - 97 + 1
    # Uppercase
    # [27, 52]
    return code - 65 + 27


def p1():
    sum = 0
    for sack in content:
        arr = [*sack]
        n = len(arr)
        # Split array into 2
        left = arr[: n // 2]
        right = arr[n // 2 :]
        # Find intersect of sets
        inter = list(set(left) & set(right))

        sum += convert_char_to_prio(inter[0])
    print(sum)


def p2():
    sum = 0
    threes = []
    # Group into triplets
    for i in range(0, len(content), 3):
        threes.append((content[i], content[i + 1], content[i + 2]))

    for i in threes:
        # Find intersect of sets
        inter = list(set(i[0]) & set(i[1]) & set(i[2]))
        sum += convert_char_to_prio(inter[0])

    print(sum)


p1()
p2()
