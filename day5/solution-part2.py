# "wow this code is a complete pile of dogshit but i got it"
file = open('input.txt', 'r')

def load_map():
    lines = []
    l = file.readline()
    while l and l != '\n':
        lines.append(l)
        l = file.readline()
    if len(lines) > 0:
        return [tuple(int(x) for x in l.split(" ")) for l in lines[1:]]

    return None

def intersect(interval1, interval2):
    s1, e1 = interval1
    s2, e2 = interval2
    if s2 > e1 or s1 > e2:
        return None
    return (max(s1, s2), min(e1, e2))

# returns (interval1 INTERSECT interval2, [interval1 SETMINUS interval2])
def segment_intervals(interval1, interval2):
    s1, e1 = interval1
    s2, e2 = interval2

    intersection = intersect(interval1, interval2)
    others = set()

    if s1 < s2:
        others.add((s1, min(s2 - 1, e1)))
    if e1 > e2:
        others.add((max(s1, e2 + 1), e1))

    return intersection, others


curr = [int(x) for x in file.readline().rstrip().replace("seeds: ", "").split(" ")]
# these are actually intervals (interval_start, interval_len)
curr = [curr[i: i+2] for i in range(0, len(curr), 2)]
# but that's annoying to work with so change it to
# (interval_start, interval_end) (inclusive)
curr = set([(i[0], i[0] + i[1] - 1) for i in curr])
# print(curr)

file.readline() # skip empty line

map_ = load_map()
while map_ is not None:
    # print(map_)
    next_ = set()

    # precondition: the intervals defined in file do NOT overlap
    # so that it doesn't matter what order you process fragmented intervals in
    while len(curr) > 0:
        interval = curr.pop()
        for (destination_start, source_start, interval_len) in map_:
            source_interval = (source_start, source_start + interval_len - 1)
            good_interval, bad_intervals = segment_intervals(interval, source_interval)
            bad_intervals.discard(interval)


            curr = curr.union(bad_intervals)
            if good_interval:
                offset = destination_start - source_start
                mapped_interval = (good_interval[0] + offset, good_interval[1] + offset)
                next_.add(mapped_interval)
                break

        else:
            next_.add(interval)


    curr = set(next_)
    # print(curr)
    map_ = load_map()

print(min([c[0] for c in curr]))
