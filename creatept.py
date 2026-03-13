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

state = "start"

max_length = 5

# Choose a random pattern for each player
pattern1 = random.choice(patterns)
pattern2 = random.choice(patterns)

# TODO: Update to input
sequence = []
sequence1 = ["r", "r", "g", "g", "r"]
sequence2 = ["r", "b", "r", "b", "r"]

def check_pattern(pattern, sequence):
    if (pattern.endswith("next")):
        pattern_matched = 0
        for i in range(len(sequence)-1):
            if (sequence[i] == pattern[0] and sequence[i+1] == pattern[0]): 
                pattern_matched += 1
        if (pattern_matched > 1):
            return "more"
        elif (pattern_matched == 0):
            return "none"
        else:
            return "valid"
    elif (pattern.endswith("space")):
        pattern_matched = 0
        for i in range(len(sequence)-2):
            if (sequence[i] == pattern[0] and sequence[i+2] == pattern[0]): 
                pattern_matched += 1
        if (pattern_matched > 1):
            return "more"
        elif (pattern_matched == 0):
            return "none"
        else:
            return "valid"

def draw_text(text, x, y, color = BLACK):
    # Font render syntax from https://www.pygame.org/docs/ref/font.html?highlight=render#pygame.font.Font.render
    img = font.render(text, True, color)
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
        pygame.draw.circle(screen, c, (250 + i * 80, 320), 25)

def reset():
    screen.fill(WHITE)

    draw_text(f"Player {state}'s Turn", 300,50)

    if state == 1:
        draw_text("Pattern: " + pattern1, 300,100)
    else:
        draw_text("Pattern: " + pattern2, 300,100)

    draw_text("Sequence:", 100,250)

    draw_sequence(sequence)

    # Buttons
    red_btn = pygame.Rect(150,450,120,50) # (left, top, width, height)
    green_btn = pygame.Rect(350,450,120,50)
    blue_btn = pygame.Rect(550,450,120,50)
    submit_btn = pygame.Rect(250,520,120,50)
    clear_btn = pygame.Rect(450,520,120,50)

    pygame.draw.rect(screen, RED, red_btn)
    pygame.draw.rect(screen, GREEN, green_btn)
    pygame.draw.rect(screen, BLUE, blue_btn)
    pygame.draw.rect(screen, GRAY, submit_btn)
    pygame.draw.rect(screen, GRAY, clear_btn)

    draw_text("R",200,460)
    draw_text("G",400,460)
    draw_text("B",600,460)
    draw_text("Submit",260,530)
    draw_text("Clear",472,530)

running = True

while running:
    if (state == "start"):
        screen.fill(WHITE)
        state = 1
    elif (state == 1):
        draw_text(f"Player 1's Turn", 300, 50)
        draw_text("Make sure player 2 don't see the screen!", 50, 300)
    else:
        draw_text(f"Player {state}'s Turn", 300,50)

        if state == 1:
            draw_text("Pattern: " + pattern1, 300,100)
        else:
            draw_text("Pattern: " + pattern2, 300,100)

        draw_text("Sequence:", 100,250)

        draw_sequence(sequence)

        # Buttons
        red_btn = pygame.Rect(150,450,120,50) # (left, top, width, height)
        green_btn = pygame.Rect(350,450,120,50)
        blue_btn = pygame.Rect(550,450,120,50)
        submit_btn = pygame.Rect(250,520,120,50)
        clear_btn = pygame.Rect(450,520,120,50)

        pygame.draw.rect(screen, RED, red_btn)
        pygame.draw.rect(screen, GREEN, green_btn)
        pygame.draw.rect(screen, BLUE, blue_btn)
        pygame.draw.rect(screen, GRAY, submit_btn)
        pygame.draw.rect(screen, GRAY, clear_btn)
        

        draw_text("R",200,460)
        draw_text("G",400,460)
        draw_text("B",600,460)
        draw_text("Submit",260,530)
        draw_text("Clear",472,530)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if a button is pressed https://stackoverflow.com/questions/67063079/how-to-check-if-a-button-is-clicked-in-pygame
            if red_btn.collidepoint(event.pos) and len(sequence) < max_length:
                sequence.append("r")

            if green_btn.collidepoint(event.pos) and len(sequence) < max_length:
                sequence.append("g")

            if blue_btn.collidepoint(event.pos) and len(sequence) < max_length:
                sequence.append("b")
            
            if clear_btn.collidepoint(event.pos):
                sequence = []
                reset()

            if submit_btn.collidepoint(event.pos) and len(sequence) == max_length:
                if state == 1:
                    match check_pattern(pattern1, sequence):
                        case "valid":
                            # Set sequence1 to sequence then reset it for player 2
                            sequence1 = sequence.copy()
                            sequence = []
                            state = 2
                        case "more":
                            reset()
                            draw_text("Pattern must not appear more than once!", 130, 150, RED)
                        case "none":
                            reset()
                            draw_text("Pattern must appear once!", 220, 150, RED)
                else:
                    match check_pattern(pattern2, sequence):
                        case "valid":
                            # Set sequence1 to sequence then reset it for player 2
                            sequence2 = sequence.copy()
                            sequence = []
                            state = 3
                        case "more":
                            reset()
                            draw_text("Pattern must not appear more than once!", 300, 150, RED)
                        case "none":
                            reset()
                            draw_text("Pattern must appear once!", 300, 150)

    if state == 3:

        screen.fill(WHITE)

        draw_text("Both sequences submitted!", 250,200)

        draw_text("Player 1 sequence: " + "".join(sequence1), 200,300)
        draw_text("Player 2 sequence: " + "".join(sequence2), 200,350)

    pygame.display.flip()

pygame.quit()