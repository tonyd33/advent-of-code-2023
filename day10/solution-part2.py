file = open('input.txt', 'r')

# index with [y][x]
grid = []
line = file.readline()
line_num = 0

sc = None
while line:
    grid.append(line.rstrip())
    if 'S' in line:
        sc = (line_num, line.index('S'))
    line = file.readline()
    line_num += 1

m = {
    '|': {'U': 'U', 'D': 'D'},
    '-': {'R': 'R', 'L': 'L'},
    'L': {'D': 'R', 'L': 'U'},
    'J': {'D': 'L', 'R': 'U'},
    '7': {'R': 'D', 'U': 'L'},
    'F': {'L': 'D', 'U': 'R'},
}
n = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}
d_to_c1 = {
    'U': n['R'],
    'D': n['L'],
    'L': n['U'],
    'R': n['D'],
}
d_to_c2 = {
    'U': n['L'],
    'D': n['R'],
    'L': n['D'],
    'R': n['U'],
}

def get_path_info(grid, s):
    path_mask = [[0] * len(row) for row in grid]
    # (coord, dir_in, dir_out)
    path_details = []
    curr_pos = s
    la = None

    path_mask[s[0]][s[1]] = 1


    # must be able to start around here
    # right
    if grid[curr_pos[0]][curr_pos[1] + 1] in ('-', '7', 'J'):
        curr_pos = (curr_pos[0], curr_pos[1] + 1)
        la = 'R'
    # left
    elif grid[curr_pos[0]][curr_pos[1] - 1] in ('-', 'F', 'L'):
        curr_pos = (curr_pos[0], curr_pos[1] - 1)
        la = 'L'
    # up
    elif grid[curr_pos[0] - 1][curr_pos[1]] in ('|', '7', 'F'):
        curr_pos = (curr_pos[0] - 1, curr_pos[1])
        la = 'U'
    # down
    elif grid[curr_pos[0] + 1][curr_pos[1]] in ('|', 'J', 'L'):
        curr_pos = (curr_pos[0] + 1, curr_pos[1])
        la = 'D'

    fa = la
    char = grid[curr_pos[0]][curr_pos[1]]
    while char != 'S':
        path_mask[curr_pos[0]][curr_pos[1]] = 1
        na = m[char][la]
        dy, dx = n[na]
        path_details.append((curr_pos, la, na))

        curr_pos = (curr_pos[0] + dy, curr_pos[1] + dx)
        char = grid[curr_pos[0]][curr_pos[1]]
        la = na

    path_details.insert(0, (curr_pos, la, fa))
    return path_mask, path_details

path_mask, path_details = get_path_info(grid, sc)

c1 = set()
c2 = set()

def explore_comp(path_mask, s, cn):
    if s in cn:
        return

    q = [s]
    while len(q) > 0:
        el = q.pop()
        # if out of bounds or touched path
        if not (0 <= el[0] < len(path_mask) and 0 <= el[1] < len(path_mask[0])) or path_mask[el[0]][el[1]]:
            return

        cn.add(el)
        q.append((el[0] - 1, el[1]))
        q.append((el[0] + 1, el[1]))
        q.append((el[0], el[1] - 1))
        q.append((el[0], el[1] + 1))

for pos, din, dout in path_details:
    din_c1 = d_to_c1[din]
    dout_c1 = d_to_c1[dout]
    explore_comp(path_mask, (pos[0] + din_c1[0], pos[1] + din_c1[1]), c1)
    explore_comp(path_mask, (pos[0] + dout_c1[0], pos[1] + dout_c1[1]), c1)

    din_c2 = d_to_c2[din]
    dout_c2 = d_to_c2[dout]
    explore_comp(path_mask, (pos[0] + din_c2[0], pos[1] + din_c2[1]), c2)
    explore_comp(path_mask, (pos[0] + dout_c2[0], pos[1] + dout_c2[1]), c2)

print(len(c1), len(c2))
acc = 0
for row in path_mask:
    for c in row:
        acc += c
print(acc)
