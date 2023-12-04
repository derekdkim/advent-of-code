import re

file = open("input.txt", "r").read().splitlines()

def solve_p1(tickets):
    total = 0

    for ticket in tickets:
        matches = 0
        ref, actual = ticket
        actual_set = set(actual)
        for num in ref:
            if num in actual_set:
                matches += 1
        if matches > 0:
            total += pow(2, matches - 1)
    return total

def solve_p2(tickets):
    match_map = dict()

    for index, ticket in enumerate(tickets):
        matches = []
        ref, actual = ticket
        actual_set = set(actual)
        for num in ref:
            if num in actual_set:
                matches.append(num)
        # 1 indexed ticket numbers
        match_map[index + 1] = matches
    
    total = 0
    # Initial card map with 1 instance of each card
    card_map = dict([(i, 1) for i in range(1, len(tickets) + 1)])
    for i, instances in card_map.items():
        matches = len(match_map[i])
        total += instances
        if matches == 0:
            continue
        for j in range(1, matches + 1):
            if not i + j in card_map:
                card_map[i + j] = 0
            card_map[i + j] += 1 * instances
    return total

def parse(lines):
    tickets = []
    for line in lines:
        start_idx = line.find(":")
        parsed = line[start_idx+2:].split("|")
        ref = [x for x in parsed[0].split(" ") if x != ""]
        actual = [x for x in parsed[1].split(" ") if x != ""]
        tickets.append((ref, actual))
    return tickets

tickets = parse(file)
print(solve_p1(tickets))
print(solve_p2(tickets))