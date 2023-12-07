file = open("input.txt", "r").read().splitlines()
n = len(file)

def parse_hands(lines, p2=False):
    hands = [[] for _ in range(7)]

    letter_map = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 11, # p1
        'T': 10
    }
    if p2:
        letter_map['J'] = 1

    for line in lines:
        segments = [x for x in line.split(" ")]
        hand = [*segments[0]]
        best_hand = get_best_hand(hand, p2)
        values = [letter_map[x] if x in letter_map else int(x) for x in hand]
        hands[best_hand - 1].append([values, int(segments[1])])

    return hands

def get_best_hand(hand, p2=False):
    hand_cp = sorted(hand)
    freq = dict()
    uniques = len(set(hand))
    hand_size = len(hand)

    for card in hand_cp:
        if card in freq:
            freq[card] += 1
        else:
            freq[card] = 1

    if 'J' not in freq or not p2:
        # Five of a kind - 7
        if uniques == 1:
            return 7
        # High Card - 1
        if uniques == hand_size:
            return 1
        # One Pair - 2
        if uniques == hand_size - 1:
            return 2
        if hand_size == 2:
            # Four of a kind - 6
            if any(x == 4 for x in freq.values()):
                return 6
            # Full House - 5
            return 5
        if hand_size == 3:
            # Three of a kind - 4
            if any(x == 3 for x in freq.values()):
                return 4
            # Two Pair - 3
            return 3
    else:
        if uniques < 3:
            # Five of a kind - 7
            # Legit or with joker
            return 7
        if uniques == 3:
            # Four of a kind - 6
            # Full House - 5
            # Legit or with joker
            # AAABJ - Four of a kind
            # AABBJ - Full House
            # AABJJ - Four of a kind
            # ABJJJ - Four of a kind
            # 2 or more jokers - Four of a kind
            if freq['J'] >= 2 or any(x > 2 for x in freq.values()):
                return 6
            else:
                return 5
        if uniques == 4:
            # Three of a kind - 4
            # ABCJJ
            # AABCJ
            # Impossible to get 2 pair
            return 4
        # Left over - 5 unique cards
        # Form a pair with joker
        return 2
            


def solve(hands):
    for bucket in hands:
        bucket.sort(key=lambda x: x[0], reverse=True)
    
    rank = n
    total = 0
    for i in range(len(hands) - 1, -1, -1):
        bucket = hands[i]
        for hand in bucket:
            total += rank * hand[1]
            rank -= 1

    return total

hands = parse_hands(file, False)
print(solve(hands))
hands = parse_hands(file, True)
print(solve(hands))