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

sequence1 = ["r", "b", "g", "g", "r"]
sequence2 = ["g", "b", "g", "b", "r"]

def check_pattern(pattern, sequence):
    if (pattern == "r_next"):
        pattern_matched = 0
        for i in range(len(sequence)):
            if (sequence[i] == "r" and sequence[i+1] == "r"): 
                pattern_matched += 1
            if (pattern_matched > 1):
                print("Sequence cannot use the pattern more than once")
        if (pattern_matched == 0):
            print("Sequence must use pattern once")


            


