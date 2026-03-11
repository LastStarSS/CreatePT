# Naming scheme:
# - Red: r 
# - Green: g
# - Blue: b 
# Patterns:
# - next: 2 consecutive same colors (rr, bb, gg)
# - space: 2 same colors separated by 1 color (rrr,rgr,rbr)

import random
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pattern Game")

# Load system font syntax from https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont
font = pygame.font.SysFont(None, 40)

# Colors
RED = (220,50,50)
GREEN = (50,200,50)
BLUE = (50,50,220)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)

patterns = ["r_next", "g_next", "b_next", "r_space", "g_space"," b_space"]

# Choose a random pattern for each player
pattern1 = random.choice(patterns)
pattern2 = random.choice(patterns)

# TODO: Update to input
sequence1 = ["r", "r", "g", "g", "r"]
sequence2 = ["r", "b", "r", "b", "r"]

def check_pattern(pattern, sequence):
    if (pattern.endswith("next")):
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
    elif (pattern.endswith("space")):
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

def draw_text(text, x, y):
    # Font render syntax from https://www.pygame.org/docs/ref/font.html?highlight=render#pygame.font.Font.render
    img = font.render(text, True, BLACK)
    screen.blit(img, (x,y))


def draw_sequence(seq):
    for i,color in enumerate(seq):

        if color == "r":
            c = RED
        elif color == "g":
            c = GREEN
        else:
            c = BLUE

        # Draw circle syntax from https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle 
        # Every color is 80 pixels apart
        pygame.draw.circle(screen, c, (150 + i * 80, 300), 25)