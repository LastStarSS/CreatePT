# Naming scheme:
# - Red: r 
# - Green: g
# - Blue: b 
# Patterns:
# - next: 2 consecutive same colors (rr, bb, gg)
# - space: 2 same colors separated by 1 color (rrr,rgr,rbr)

import random
import pygame

# True = test mode on
# False = test mode off
# Allow skipping through screen to quickly see if the elements appear correctly
display_test = True

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

# Buttons
red_btn = pygame.Rect(150,450,120,50) # (left, top, width, height)
green_btn = pygame.Rect(350,450,120,50)
blue_btn = pygame.Rect(550,450,120,50)
submit_btn = pygame.Rect(250,520,120,50)
clear_btn = pygame.Rect(450,520,120,50)
ready_btn = pygame.Rect(340,540,120,50)
next_btn = pygame.Rect(680,550,120,50)

patterns = ["r_next", "g_next", "b_next", "r_space", "g_space", "b_space"]

states = ["ready1", "player1", "ready2", "player2", "guess", "result"]
state = "ready1"

# Max length of a sequence
max_length = 5

# Choose a random pattern for each player
pattern1 = random.choice(patterns)
pattern2 = random.choice(patterns)

sequence = []
sequence1 = []
sequence2 = []

test_sequence1 = ["r", "g", "b", "g", "r"]
test_sequence2 = ["r", "r", "g", "g", "b"]

# Dropdowns
dropdown1_open = False
dropdown2_open = False

guess1_index = None
guess2_index = None

dropdown1 = pygame.Rect(300, 165, 200, 40)
dropdown2 = pygame.Rect(300, 265, 200, 40)

def check_pattern(pattern, sequence):
    if (pattern.endswith("next")):
        pattern_matched = 0
        for i in range(len(sequence)-1):
            # Check if the color on this index is the same as the next color and if they match the pattern's color
            if (sequence[i] == pattern[0] and sequence[i+1] == pattern[0]): 
                pattern_matched += 1
        # Pattern must only appear once in the sequence
        if (pattern_matched > 1):
            return "more"
        elif (pattern_matched == 0):
            return "none"
        else:
            return "valid"
    elif (pattern.endswith("space")):
        pattern_matched = 0
        for i in range(len(sequence)-2):
            # Check if the color on this index is the same as the color 2 index away and if they match the pattern's color
            if (sequence[i] == pattern[0] and sequence[i+2] == pattern[0]): 
                pattern_matched += 1
        # Pattern must only appear once in the sequence
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

def draw_sequence(seq, start_x=250, start_y=320):
    for i,color in enumerate(seq):
        if color == "r":
            c = RED
        elif color == "g":
            c = GREEN
        else:
            c = BLUE

        # Draw circle syntax from https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle 
        # Every color is 80 pixels apart
        pygame.draw.circle(screen, c, (start_x + i * 80, start_y), 25)

def draw_dropdown():
    if dropdown1_open:
            for i, pattern in enumerate(patterns):
                option = pygame.Rect(
                    dropdown1.x,
                    dropdown1.y + (i+1)*40,
                    dropdown1.width,
                    dropdown1.height
                )
                pygame.draw.rect(screen, GRAY, option)
                draw_text(pattern, option.x + 10, option.y + 5)

    if dropdown2_open:
        for i, pattern in enumerate(patterns):
            option = pygame.Rect(
                dropdown2.x,
                dropdown2.y + (i+1)*40,
                dropdown2.width,
                dropdown2.height
            )
            pygame.draw.rect(screen, GRAY, option)
            draw_text(pattern, option.x + 10, option.y + 5)


def draw_player_screen():
    screen.fill(WHITE)
    if state == "player1":
        draw_text(f"Player 1's Turn", 300,50)
        draw_text("Pattern: " + pattern1, 300,100)
    elif state == "player2":
        draw_text(f"Player 2's Turn", 300,50)
        draw_text("Pattern: " + pattern2, 300,100)

    draw_text("Sequence:", 100,250)

    draw_sequence(sequence)

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
    if (display_test):
        pygame.draw.rect(screen, GRAY, next_btn)
        draw_text("Next", 710, 565)

def draw_guess_screen():
    draw_text("Both sequences submitted!", 250,50)
    
    # Use real sequences from players if display_test is off, use test sequences if on
    draw_text("Player 1 sequence:", 70,360)
    draw_sequence(test_sequence1 if display_test else sequence1, 370, 365)

    draw_text("Player 2 sequence:", 70, 460)
    draw_sequence(test_sequence2 if display_test else sequence2, 370, 465)

    # Player 1 guess
    draw_text("Player 1 guess:", 70,170)
    pygame.draw.rect(screen, GRAY, dropdown1)
    if guess1_index is None:
        draw_text("Guess",355,170)
    else:
        draw_text(patterns[guess1_index], 350, 170)

    # Player 2 guess
    draw_text("Player 2 guess:", 70,270)
    pygame.draw.rect(screen, GRAY, dropdown2)
    if guess2_index is None:
        draw_text("Guess",355,270)
    else:
        draw_text(patterns[guess2_index], 350, 270)

    draw_dropdown()
    # Reusing ready_btn as the guess submit button
    pygame.draw.rect(screen, GREEN, ready_btn)
    draw_text(
        "Guess",
        ready_btn.x + 17,
        ready_btn.y + 10
    )

def draw_ready_screen():
    if (state == "ready1"):
        draw_text(f"Player 1's Turn", 300, 50)
        draw_text("Make sure player 2 don't see the screen!", 120, 300)
    elif (state == "ready2"):
        draw_text(f"Player 2's Turn", 300, 50)
        draw_text("Make sure player 1 don't see the screen!", 120, 300)
    pygame.draw.rect(screen, GREEN, ready_btn)
    draw_text("Ready",357,550)


def next_state():
    global state
    print(f"Old state: {state}")
    for i, state_check in enumerate(states):
        if state_check == state:
            state = states[i+1]
            print(f"New state: {state}")
            break

running = True

while running:
    if (state.startswith("ready")):
        screen.fill(WHITE)
        draw_ready_screen()
    elif (state.startswith("player")):
        draw_player_screen()
    elif (state == "guess"):
        screen.fill(WHITE)
        draw_guess_screen()    
    
    if (display_test):
        next_btn = pygame.Rect(680, 550, 120, 50)
        pygame.draw.rect(screen, GRAY, next_btn)
        draw_text("Next", 710, 565)
    for event in pygame.event.get():

        if (event.type == pygame.QUIT):
            running = False

        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (state.startswith("player")):
                # Check if a button is pressed https://stackoverflow.com/questions/67063079/how-to-check-if-a-button-is-clicked-in-pygame
                if (red_btn.collidepoint(event.pos) and len(sequence) < max_length):
                    sequence.append("r")

                if (green_btn.collidepoint(event.pos) and len(sequence) < max_length):
                    sequence.append("g")

                if (blue_btn.collidepoint(event.pos) and len(sequence) < max_length):
                    sequence.append("b")
                
                if (clear_btn.collidepoint(event.pos)):
                    sequence = []
                    draw_player_screen()
                if submit_btn.collidepoint(event.pos) and len(sequence) == max_length:
                    if (state == "player1"):
                        match check_pattern(pattern1, sequence):
                            case "valid":
                                # Set sequence1 to sequence then reset it for player 2
                                sequence1 = sequence.copy()
                                sequence = []
                                next_state()
                            case "more":
                                draw_player_screen()
                                draw_text("Pattern must not appear more than once!", 130, 150, RED)
                            case "none":
                                draw_player_screen()
                                draw_text("Pattern must appear once!", 220, 150, RED)
                    elif (state == "player2"):
                        match check_pattern(pattern2, sequence):
                            case "valid":
                                # Set sequence2 to sequence then reset it 
                                sequence2 = sequence.copy()
                                sequence = []
                                next_state()
                            case "more":
                                draw_player_screen()
                                draw_text("Pattern must not appear more than once!", 300, 150, RED)
                            case "none":
                                draw_player_screen()
                                draw_text("Pattern must appear once!", 300, 150)

            if (state.startswith("ready")):
                if (ready_btn.collidepoint(event.pos)):
                    next_state()

            if (state == "guess"):
                # Toggle dropdowns
                if dropdown1.collidepoint(event.pos) and not dropdown2_open:
                    dropdown1_open = not dropdown1_open
                    dropdown2_open = False
                elif dropdown2.collidepoint(event.pos) and not dropdown1_open:
                    dropdown2_open = not dropdown2_open
                    dropdown1_open = False

                # Select option for dropdown1
                if dropdown1_open:
                    for i, pattern in enumerate(patterns):
                        option = pygame.Rect(
                            dropdown1.x,
                            dropdown1.y + (i+1)*40,
                            dropdown1.width,
                            dropdown1.height
                        )
                        if option.collidepoint(event.pos):
                            guess1_index = i
                            dropdown1_open = False
                            screen.fill(WHITE)
                            draw_guess_screen


                # Select option for dropdown2
                if dropdown2_open:
                    for i, pattern in enumerate(patterns):
                        option = pygame.Rect(
                            dropdown2.x,
                            dropdown2.y + (i+1)*40,
                            dropdown2.width,
                            dropdown2.height
                        )
                        if option.collidepoint(event.pos):
                            guess2_index = i
                            dropdown2_open = False
                            screen.fill(WHITE)
                            draw_guess_screen()
            
            if (next_btn.collidepoint(event.pos)):
                next_state()

        pygame.display.flip()

pygame.quit()