# The following library was used to draw the program's GUI: 
# Pygame - https://github.com/pygame/pygame

# Acknowledgement:
# Generative AI (ChatGPT) was used to generate x/y coordinates and dimensions for GUI elements
# of this project to ensure alignment

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
# Allow skipping through screens to quickly see if the elements appear correctly
display_test = False

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# This function for loading system font was adapted from https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

# Colors
RED = (220,50,50)
GREEN = (50,200,50)
BLUE = (50,50,220)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)

# Buttons
red_btn = pygame.Rect(150,450,120,50) # (x, y, width, height)
green_btn = pygame.Rect(350,450,120,50)
blue_btn = pygame.Rect(550,450,120,50)
submit_btn = pygame.Rect(250,520,120,50)
clear_btn = pygame.Rect(450,520,120,50)
ready_btn = pygame.Rect(340,340,120,50)
next_btn = pygame.Rect(680,550,120,50)
guess_btn = pygame.Rect(340,540,120,50)
again_btn = pygame.Rect(330,340,160,50)
rules_btn = pygame.Rect(0,550,120,50)

patterns = ["r_next", "g_next", "b_next", "r_space", "g_space", "b_space"]

states = ["rules", "ready1", "player1", "ready2", "player2", "guess", "result"]
state = "ready1"
prev_state = None

# Max length of a sequence
max_length = 5

# Choose a random pattern for each player
pattern1 = random.choice(patterns)
pattern2 = random.choice(patterns)

# Create blank sequences to be recorded later
sequence = []
sequence1 = []
sequence2 = []

# Premade sequences to be used for test mode
test_sequence1 = ["r", "g", "b", "g", "r"]
test_sequence2 = ["r", "r", "g", "g", "b"]

# Dropdowns
dropdown1_open = False
dropdown2_open = False

guess1_index = None
guess2_index = None

dropdown1 = pygame.Rect(300, 165, 200, 40)
dropdown2 = pygame.Rect(300, 265, 200, 40)

# Result
result = None

# Used for test mode
test_result = "Draw_lose"

# Rules
rules = ["1. Each player will be given a pattern at random",
         "2. You will each take turn to make a sequence",
         "3. The pattern must appear in your sequence once and only once",
         "4. Once both players have submitted their sequence, you will guess",
         " each other's pattern based on the sequence they made",
         "5. A player wins if they correctly guess the other player's pattern",
         "6. If both players correctly or incorrectly guess, then it is a draw",
         "Pattern meaning:",
         "- The first character of your pattern indicate the color you must use:",
         "    + r: red",
         "    + g: green",
         "    + b: blue",
         "- The phrase at the end of your pattern indicate what type of pattern it is:",
         "    + next:  2 of the same color are right next to each other",
         "    + space: 2 of the same color are separated by a color (does not have to be different)",
         "Examples:",
         "- Pattern: r_next, Sequence: grrbb (valid)",
         "- Pattern: b_next, Sequence: rbbbg (invalid, pattern appeared twice)",
         "- Pattern: g_space, Sequence: brgbg (valid)",
         "- Pattern: r_space, Sequence: rrrgg (valid)",
         "- Pattern: g_space, Sequence: ggrrb (invalid, pattern does not appear)"]

# Check if the provided sequence match the provided pattern
# Return:
# - "more" if the pattern appears more than once 
# - "none" if pattern does not appear
# - "valid" if the pattern appears only once
def check_pattern(pattern, sequence):
    if (pattern.endswith("next")):
        pattern_matched = 0
        for i in range(len(sequence)-1):
            # Check if the color on this index is the same as the next color and if they match the pattern's color
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
            # Check if the color on this index is the same as the color 2 index away and if they match the pattern's color
            if (sequence[i] == pattern[0] and sequence[i+2] == pattern[0]): 
                pattern_matched += 1
        if (pattern_matched > 1):
            return "more"
        elif (pattern_matched == 0):
            return "none"
        else:
            return "valid"

# Check if either, both, or none of the players guessed correctly
# Return:
# - "Draw_win" if both players guessed correctly
# - "Draw_lose" if both players guessed incorrectly
# - "Player1" if player 1 guessed correctly but player 2 didn't
# - "Player2" if player 2 guessed correctly but player 1 didn't
def check_guess():
    if (patterns[guess1_index] == pattern2 and patterns[guess2_index] == pattern1):
        return "Draw_win"
    elif (patterns[guess1_index] == pattern2):
        return "Player1"
    elif (patterns[guess2_index] == pattern1):
        return "Player2"
    else:
        return "Draw_lose"

# Reset necessary variables and rerandomize players' patterns
# Does not return (void)
def reset():
    global pattern1
    global pattern2
    global sequence
    global sequence1
    global sequence2
    global state

    pattern1 = random.choice(patterns)
    pattern2 = random.choice(patterns)

    sequence, sequence1, sequence2 = [], [], []
    
    state = "ready1"

# Draw the provided text at a certain x/y position with color (default BLACK) and font (default systemfont)
# Does not return (void)
def draw_text(text, x, y, color = BLACK, font = font):
    # This function for drawing "text" on screen was adapted from https://www.pygame.org/docs/ref/font.html?highlight=render#pygame.font.Font.render
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

# Draw a sequence of colored circles starting at the provided x/y position
# Does not return (void)
def draw_sequence(seq, start_x, start_y):
    for i,color in enumerate(seq):
        if color == "r":
            c = RED
        elif color == "g":
            c = GREEN
        else:
            c = BLUE

        # This function for drawing a circle was adapted from https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle 
        # Every circle is 80 pixels apart
        pygame.draw.circle(screen, c, (start_x + i * 80, start_y), 25)

# Draw dropdown options when they are opened
# Does not return (void)
def draw_dropdown():
    if dropdown1_open:
            # For every pattern available, draw an option
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

# Draw the ready screen where they are warned to not let the other player see the screen
# Does not return (void)
def draw_ready_screen():
    if (state == "ready1"):
        draw_text("Player 1's Turn", 300, 50)
        draw_text("Make sure player 2 don't see the screen!", 120, 300)
    elif (state == "ready2"):
        draw_text("Player 2's Turn", 300, 50)
        draw_text("Make sure player 1 don't see the screen!", 120, 300)
    pygame.draw.rect(screen, GREEN, ready_btn)
    draw_text("Ready",
              ready_btn.x + 17,
              ready_btn.y + 10)

# Draw the player screen where they are shown their pattern and make their sequence
# Does not return (void) 
def draw_player_screen():
    screen.fill(WHITE)
    if state == "player1":
        draw_text(f"Player 1's Turn", 300,50)
        draw_text("Pattern: " + pattern1, 300,100)
    elif state == "player2":
        draw_text(f"Player 2's Turn", 300,50)
        draw_text("Pattern: " + pattern2, 300,100)

    draw_text("Sequence:", 100,250)

    draw_sequence(sequence, 250, 320)

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

# Draw the guess screen where players guess each other's pattern
# Does not return (void)
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
    pygame.draw.rect(screen, GREEN, guess_btn)
    draw_text(
        "Guess",
        guess_btn.x + 17,
        guess_btn.y + 10
    )

# Draw the result screen where the winner is announced based on players' guess
# Does not return (void)
def draw_result_screen():
    match test_result if display_test else result:
        case "Player1":
            draw_text("Player 1 won!", 320, 190, GREEN)
        case "Player2":
            draw_text("Player 2 won!", 320, 190, GREEN)
        case "Draw_win":
            draw_text("Draw!", 370, 190)
            draw_text("Both players correctly guessed!", 200, 260, GREEN)
        case "Draw_lose":
            draw_text("Draw!", 370, 190)
            draw_text("Both players incorrectly guessed!", 190, 260, RED)
    pygame.draw.rect(screen, GRAY, again_btn)
    draw_text(
        "Play again",
        again_btn.x + 10,
        again_btn.y + 10)

# Change screen to the next screen
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
    # Drawing screens based on the current state
    if (state.startswith("ready")):
        screen.fill(WHITE)
        draw_ready_screen()
    elif (state.startswith("player")):
        draw_player_screen()
    elif (state == "guess"):
        screen.fill(WHITE)
        draw_guess_screen() 
    elif (state == "result"):
        screen.fill(WHITE)
        draw_result_screen()
    elif (state == "rules"):
        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY, rules_btn)
        draw_text("Back", 25, 565)
        draw_text("Rules", 375, 1)
        for i,rule in enumerate(rules):
            draw_text(rule, 10, 30 + 25*i, BLACK, small_font)
    
    # Draw next_btn if test mode is on
    if (display_test):
        next_btn = pygame.Rect(680, 550, 120, 50)
        pygame.draw.rect(screen, GRAY, next_btn)
        draw_text("Next", 710, 565)
    # Draw rules_btn
    if state != "rules":
        pygame.draw.rect(screen, GRAY, rules_btn)
        draw_text("Rules", 20, 565)
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        # This syntax to check if an element is clicked is taken from 
        # https://stackoverflow.com/questions/67063079/how-to-check-if-a-button-is-clicked-in-pygame
        if (event.type == pygame.MOUSEBUTTONDOWN):
            # Move to next state when next_btn is clicked
            if (next_btn.collidepoint(event.pos)):
                next_state()
            
            # If not in rules screen, go to rules screen, if not, go back to previous screen
            if (rules_btn.collidepoint(event.pos)):
                if (state == "rules"):
                    state = prev_state
                else:
                    prev_state = state
                    state = "rules"

            if (state.startswith("player")):
                # Add the corresponding color to sequence when an R/G/B button is clicked and the
                # sequence is not complete
                if (red_btn.collidepoint(event.pos) and len(sequence) < max_length):
                    sequence.append("r")

                if (green_btn.collidepoint(event.pos) and len(sequence) < max_length):
                    sequence.append("g")

                if (blue_btn.collidepoint(event.pos) and len(sequence) < max_length):
                    sequence.append("b")
                
                # Clear the sequence in case there is a misclick
                if (clear_btn.collidepoint(event.pos)):
                    sequence = []
                    draw_player_screen()
                # Submit the sequence if the sequence is valid, if not, a red warning will show
                if (submit_btn.collidepoint(event.pos) and len(sequence) == max_length):
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
                if (dropdown1.collidepoint(event.pos) and not dropdown2_open):
                    dropdown1_open = not dropdown1_open
                    dropdown2_open = False
                elif (dropdown2.collidepoint(event.pos) and not dropdown1_open):
                    dropdown2_open = not dropdown2_open
                    dropdown1_open = False

                # Select option for dropdown1
                if (dropdown1_open):
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
                if (dropdown2_open):
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

                if (guess_btn.collidepoint(event.pos)):
                    result = check_guess()
                    next_state()
            # Restart the game if the play again button is clicked
            if (state == "result"):
                if (again_btn.collidepoint(event.pos)):
                    reset()

        pygame.display.flip()

pygame.quit()