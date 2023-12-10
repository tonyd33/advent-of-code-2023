from functools import cmp_to_key
file = open('input.txt', 'r')
def get_counts(s):
    d = {}
    for c in s:
        d[c] = d.get(c, 0) + 1
    jc = d.get("J", 0)
    if "J" in d:
        del d["J"]
    return list(sorted(d.values())), jc

def pad_equal(l1, l2):
    if len(l1) > len(l2):
        l2 = [0] * (len(l1) - len(l2)) + list(l2)
    elif len(l1) < len(l2):
        l1 = [0] * (len(l2) - len(l1)) + list(l1)
    return l1, l2

def can_meet(s, crit):
    counts, jc = get_counts(s)
    counts, crit = pad_equal(counts, crit)
    overlay = [a - b for a, b in zip(crit, counts)]
    return jc == sum(overlay) and all((x >= 0 for x in overlay))

evs = [(5,), (1, 4), (2, 3), (1, 1, 3), (1, 2, 2), (1, 1, 1, 2), (1, 1, 1, 1, 1)]

def eval_hand(hand):
    for i, ev in enumerate(evs):
        if can_meet(hand, ev):
            return len(evs) - i
    raise Error("harry potta black magic here")

card_strengths = "AKQT98765432J"

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

