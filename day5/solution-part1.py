# this puzzle is lame, i'm just doing it in python and getting it over with.

file = open('input.txt', 'r')

def load_map():
    lines = []
    l = file.readline()
    while l and l != '\n':
        lines.append(l)
        l = file.readline()
    return lines

curr_mapped = [int(x) for x in file.readline().rstrip().replace("seeds: ", "").split(" ")]
file.readline()
m = load_map()
while len(m) > 0:
    m = [tuple(int(x) for x in l.split(" ")) for l in m[1:]]
    next_mapped = []
    for x in curr_mapped:
        for (destination_start, source_start, rang) in m:
            offset = x - source_start
            if 0 <= offset < rang:
                next_mapped.append(destination_start + offset)
                break
        else:
            next_mapped.append(x)

    curr_mapped = next_mapped
    # print(curr_mapped)
    m = load_map()

print(min(curr_mapped))
