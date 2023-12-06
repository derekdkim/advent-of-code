file = open("input.txt", "r")

lines = file.read().splitlines()

def solve_p2(games):
    powers = 0
    color_keys = {
        'red': 0,
        'green': 1,
        'blue': 2
    }
    for i in range(len(games)):
        game_min_cubes = [0, 0, 0]
        for game_set in games[i]:
            for marble in game_set:
                index = color_keys[marble[1]]
                game_min_cubes[index] = max(game_min_cubes[index], int(marble[0]))
        powers += game_min_cubes[0] * game_min_cubes[1] * game_min_cubes[2]
    print(powers)

def solve_p1(games):
    sum_of_ids = 0
    starting_cubes = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    for i in range(len(games)):
        possible = True
        for game_set in games[i]:
            for marble in game_set:
                if starting_cubes[marble[1]] < int(marble[0]):
                    possible = False
                    break

        if possible:
            sum_of_ids += i + 1
    print(sum_of_ids)

def parse_games(lines):
    games = []
    for index, line in enumerate(lines):
        start_index = line.find(":")
        game_str = line[start_index + 1:]
        game_sets = [game_set.split(", ") for game_set in game_str.split(";")]
        games.append([])
        for set_index, gs in enumerate(game_sets):
            games[index].append([])
            for marble in gs:
                games[index][set_index].append([item for item in marble.split(" ") if item != ''])
        
    return games

games = parse_games(lines)
solve_p1(games)
solve_p2(games)