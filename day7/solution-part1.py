from functools import cmp_to_key
file = open('input.txt', 'r')
def get_counts(s):
    d = {}
    for c in s:
        d[c] = d.get(c, 0) + 1
    return d
test1 = lambda s: len(get_counts(s)) == 1
test2 = lambda s: 4 in get_counts(s).values()
test3 = lambda s: tuple(sorted(get_counts(s).values())) == (2, 3)
test4 = lambda s: tuple(sorted(get_counts(s).values())) == (1, 1, 3)
test5 = lambda s: tuple(sorted(get_counts(s).values())) == (1, 2, 2)
test6 = lambda s: tuple(sorted(get_counts(s).values())) == (1, 1, 1, 2)
test7 = lambda s: len(get_counts(s)) == 5
ev_fns = [test1, test2, test3, test4, test5, test6, test7]
eval_hand = lambda hand: len(ev_fns) - [fn(hand) for fn in ev_fns].index(True)

card_strengths = "AKQJT98765432"

def cmp_hands(hand1, hand2):
    diff = eval_hand(hand1) - eval_hand(hand2)
    if diff != 0:
        return diff

    for c1, c2 in zip(hand1, hand2):
        str1 = len(card_strengths) - card_strengths.index(c1)
        str2 = len(card_strengths) - card_strengths.index(c2)
        diff = str1 - str2
        if diff != 0:
            return diff
    raise Error("Shouldn't get here")

lines = [line.rstrip().split(" ") for line in file.readlines()]
file.close()

lines.sort(key=cmp_to_key(lambda a, b: cmp_hands(a[0], b[0])))
winnings = [(i+1) * int(line[1]) for i, line in enumerate(lines)]
print(sum(winnings))

