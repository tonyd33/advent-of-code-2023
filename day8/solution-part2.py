# i dont wanna implement crt lol
from sympy.ntheory.modular import crt


# === START: Load file ===
file = open('input.txt', 'r')
instructions = [int(direction) for direction in
        file.readline().rstrip().replace("L", "0").replace("R", "1")]

file.readline() # skip empty line
line = file.readline()

d = {}
curr_nodes = []
while line:
    node = line[:3]
    left = line[7:10]
    right = line[12:15]
    d[node] = (left, right)

    if node[-1] == "A":
        curr_nodes.append(node)

    line = file.readline()
file.close()
# === END: Load file ===


# === START: General util functions ===
# rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
def rotate(l, y):
    if len(l) == 0:
        return l
    y = -y % len(l)
    return l[y:] + l[:y]


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def flatten(l):
    return [item for sublist in l for item in sublist]

# === END: General util functions ===

# === START: Problem helper functions ===
def find_next(node, instr_pos):
    direction = instructions[instr_pos]
    return d[node][direction]

def find_until_cycle(node):
    pos = 0
    curr_node = node
    trail = []
    hashed_trail = set()

    while True:
        trail.append((curr_node, pos))

        if hash((curr_node, pos)) in hashed_trail:
            break
        hashed_trail.add(hash((curr_node, pos)))

        curr_node = find_next(curr_node, pos)
        pos = (pos + 1) % len(instructions)

    return trail

# last el of path is start of cycle
def find_cycle_start(path):
    s = path[-1]
    return path.index(s)


def extract_cycle(path):
    start = find_cycle_start(path)
    return path[start:-1]
# === END: Problem helper functions ===

# keep traversing until found cycle
paths = [find_until_cycle(node) for node in curr_nodes]

# shift cycles to normalize
longest = max([find_cycle_start(path) for path in paths])
normalized_cycles = [
        rotate(extract_cycle(path), find_cycle_start(path) - longest)
        for path in paths
        ]

# get indices of elements ending with Z in cycle
z_indices = []
for cy in normalized_cycles:
    found = False
    for i, elt in enumerate(cy):
        if elt[0][-1] == "Z":
            z_indices.append(i)
            if found:
                # it can be handled, but w/e
                raise Exception("wasnt expecting two z ends in single cycle")
            found = True


prime_facs = [prime_factors(len(cy)) for cy in normalized_cycles]

xs = []
for z_index, pfs in zip(z_indices, prime_facs):
    mo = []
    for pf in pfs:
        mo.append(z_index % pf)
    xs.append(mo)


res = crt(flatten(prime_facs), flatten(xs))[0]

for cy in normalized_cycles:
    print(cy[res % len(cy)])


print(res + longest)




