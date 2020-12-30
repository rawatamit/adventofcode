import collections


def play_one_round(decka, deckb):
    a = decka.popleft()
    b = deckb.popleft()

    if a > b:
        decka.append(a)
        decka.append(b)
    else:
        deckb.append(b)
        deckb.append(a)


def play_game(decka, deckb):
    while decka and deckb:
        play_one_round(decka, deckb)
    return decka, deckb


def player_score(deck):
    multipliers = range(len(deck), 0, -1)
    return sum(map(lambda a, b: a * b, deck, multipliers))


def read_player_deck(stream):
    # skip player name
    stream.readline()

    deck = collections.deque()
    line = stream.readline().strip()
    while line:
        deck.append(int(line))
        line = stream.readline().strip()
    return deck


if __name__ == "__main__":
    with open('d22.txt') as fin:
        decka = read_player_deck(fin)
        deckb = read_player_deck(fin)
    
    play_game(decka, deckb)
    print(player_score(decka))

    '''
    decka = collections.deque([9, 2, 6, 3, 1])
    deckb = collections.deque([5, 8, 4, 7, 10])
    play_game(decka, deckb)
    print(decka, deckb)
    print(player_score(decka))
    print(player_score(deckb))
    '''
