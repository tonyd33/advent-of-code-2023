file = open('input.txt', 'r')

# sliding window
curr_line = "." + file.readline().rstrip() + "."
next_line = "." + file.readline().rstrip() + "."
prev_line = "." * len(curr_line) # pad top

total = 0
is_EOF = False

#           hit_idx
#              V
# ............12345............................................................
#             ^    ^
#       start_idx end_idx
# get range vs num because dont want to duplicate
def get_num_range(line, hit_idx):
    start_idx = hit_idx
    end_idx = hit_idx
    # expand backward
    while line[start_idx].isdigit():
        start_idx -= 1
    start_idx += 1
    # expand forward
    while line[end_idx].isdigit():
        end_idx += 1
    return start_idx, end_idx

#             idx
#              V
# ..............123............................................................
# .............*234............................................................
# ............345..............................................................
#
def adjacent_nums(prev_line, curr_line, next_line, idx):
    nums = []

    # prev line searches
    search_idx = idx-1
    while search_idx < idx+2:
        if prev_line[search_idx].isdigit():
            start_idx, end_idx = get_num_range(prev_line, search_idx)
            nums.append(int(prev_line[start_idx:end_idx]))
            search_idx = max(search_idx, end_idx)

        search_idx += 1

    # next line searches
    search_idx = idx-1
    while search_idx < idx+2:
        if next_line[search_idx].isdigit():
            start_idx, end_idx = get_num_range(next_line, search_idx)
            nums.append(int(next_line[start_idx:end_idx]))
            search_idx = max(search_idx, end_idx)

        search_idx += 1

    # curr line searches
    if curr_line[idx-1].isdigit():
        start_idx, end_idx = get_num_range(curr_line, idx-1)
        nums.append(int(curr_line[start_idx:end_idx]))
    if curr_line[idx+1].isdigit():
        start_idx, end_idx = get_num_range(curr_line, idx+1)
        nums.append(int(curr_line[start_idx:end_idx]))
    return nums


line = 1
while True:
    #  print(prev_line)
    #  print(curr_line)
    #  print(next_line)
    #  print("")

    line_out = []
    idx = 1 # don't go to padded edges (left)
    end_idx = None

    while idx < len(curr_line) - 1: # don't go to padded edges (right)
        if curr_line[idx] == "*":
            adjacents = adjacent_nums(prev_line, curr_line, next_line, idx)
            if len(adjacents) == 2:
                total += adjacents[0] * adjacents[1]

        idx += 1

    # print("+".join(line_out))
    if is_EOF:
        break

    line += 1
    prev_line = curr_line
    curr_line = next_line
    next_line = file.readline()
    if not next_line:
        is_EOF = True
        next_line = "." * len(curr_line) # pad bottom
    else:
        next_line = "." + next_line.rstrip() + "." # pad left and right

print(total)
