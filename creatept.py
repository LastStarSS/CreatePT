# Naming scheme:
# - Red: r 
# - Green: g
# - Blue: b 
# Patterns:
# - next: 2 consecutive same colors (rr, bb, gg)
# - space: 2 same colors separated by 1 color (rrr,rgr,rbr)

import random

patterns = ["r_next", "g_next", "b_next", "r_space", "g_space"," b_space"]

# Choose a random pattern for each player
pattern1 = random.choice(patterns)
pattern2 = random.choice(patterns)

# TODO: Update to input
sequence1 = ["r", "r", "g", "g", "r"]
sequence2 = ["r", "b", "r", "b", "r"]

def check_pattern(pattern, sequence):
    # String slicing taken from https://stackoverflow.com/questions/7983820/get-the-last-4-characters-of-a-string
    if (pattern[-4:] == "next"):
        pattern_matched = 0
        for i in range(len(sequence)-1):
            if (sequence[i] == pattern[0] and sequence[i+1] == pattern[0]): 
                pattern_matched += 1
        if (pattern_matched > 1):
            print("Sequence cannot use the pattern more than once")
            return 0
        elif (pattern_matched == 0):
            print("Sequence must use pattern once")
            return 0
        else:
            print("Sequence valid")
            return 1
    elif (pattern[-5:] == "space"):
        pattern_matched = 0
        for i in range(len(sequence)-2):
            if (sequence[i] == pattern[0] and sequence[i+2] == pattern[0]): 
                pattern_matched += 1
        if (pattern_matched > 1):
            print("Sequence cannot use the pattern more than once")
        elif (pattern_matched == 0):
            print("Sequence must use pattern once")
        else:
            print("Sequence valid")

check_pattern("r_next", sequence1)
check_pattern("r_space", sequence2)


            


