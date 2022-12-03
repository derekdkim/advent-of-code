# AX = 1, BY = 2, CZ = 3
# Draw = 3, Win = 6, Lose = 0
# p1
p1_outcomes = {
    "X": {"A": 3 + 1, "B": 0 + 1, "C": 6 + 1},
    "Y": {"A": 6 + 2, "B": 3 + 2, "C": 0 + 2},
    "Z": {"A": 0 + 3, "B": 6 + 3, "C": 3 + 3},
}
# p2
p2_outcomes = {
    # Lose
    "X": {
        # Rock, need Scissors to lose
        "A": 3,
        # Paper, need Rock to lose
        "B": 1,
        # Scissors, need paper to lose
        "C": 2,
    },
    # Tie:
    "Y": {"A": 1 + 3, "B": 2 + 3, "C": 3 + 3},
    # Win:
    "Z": {"A": 2 + 6, "B": 3 + 6, "C": 1 + 6},
}

# Parse file
file = open("input.txt", "r")
rounds = file.read().splitlines()


def tally_outcomes(lookup):
    total = 0
    for i in rounds:
        total += lookup[i[2]][i[0]]

    print(total)


tally_outcomes(p1_outcomes)
tally_outcomes(p2_outcomes)
