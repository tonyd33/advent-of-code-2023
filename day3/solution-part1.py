# hello if ur reading this, this was an aid to check my vim solution.
# however, after writing this in python, i no longer want to do part 2 in vim.
file = open('input.txt', 'r')

# sliding window
curr_line = "." + file.readline().rstrip() + "."
next_line = "." + file.readline().rstrip() + "."
prev_line = "." * len(curr_line) # pad top

total = 0
is_EOF = False

#             idx
#              V
# .............345.............................................................
#                 ^
#              end_idx
def is_adjacent_symbol_free(prev_line, curr_line, next_line, idx, end_idx):
    prev_line_free = prev_line[idx-1:end_idx+1] == "." * (end_idx - idx + 2)
    next_line_free = next_line[idx-1:end_idx+1] == "." * (end_idx - idx + 2)
    curr_line_edges_free = curr_line[idx-1] == "." and curr_line[end_idx] == "."
    return prev_line_free and next_line_free and curr_line_edges_free


while True:
    #  print(prev_line)
    #  print(curr_line)
    #  print(next_line)

    line_out = []
    idx = 1 # don't go to padded edges (left)
    end_idx = None

    while idx < len(curr_line) - 1: # don't go to padded edges (right)
        if curr_line[idx].isdigit():
            end_idx = idx + 1
            # find end of digit
            while curr_line[end_idx].isdigit():
                end_idx += 1
            symbol_free = is_adjacent_symbol_free(prev_line, curr_line, next_line, idx, end_idx)
            if not symbol_free:
                total += int(curr_line[idx:end_idx])
                line_out.append(curr_line[idx:end_idx])

            idx = end_idx

        idx += 1

    # print("+".join(line_out))
    if is_EOF:
        break

    prev_line = curr_line
    curr_line = next_line
    next_line = file.readline()
    if not next_line:
        is_EOF = True
        next_line = "." * len(curr_line) # pad bottom
    else:
        next_line = "." + next_line.rstrip() + "." # pad left and right

print(total)
