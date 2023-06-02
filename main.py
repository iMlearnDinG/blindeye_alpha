import pygame
import random


# Define constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GREEN = (0, 128, 0)
table_image = pygame.image.load(f"cards/table.png")

CARD_WIDTH = 79
CARD_HEIGHT = 118

RECT_WIDTH = 80
RECT_HEIGHT = 120

PLAYER2_CARD_AREA_Y = 20
PLAYER2_BET_AREA_Y = 150
DEALER_CARD_AREA_Y = 300
PLAYER1_BET_AREA_Y = 450
PLAYER1_CARD_AREA_Y = 580


# Define the size and position of the text box
TEXTBOX_WIDTH = 300
TEXTBOX_HEIGHT = 90
TEXTBOX_X = 15
TEXTBOX_Y = 625

# Create a surface for the text box
textbox_surface = pygame.Surface((TEXTBOX_WIDTH, TEXTBOX_HEIGHT))


# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blindeye Table")
clock = pygame.time.Clock()

# Load font for counters
font = pygame.font.Font(None, 36)

# Load card images
card_images = {}
suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', ]
for suit in suits:
    for rank in ranks:
        filename = f"cards/{rank}_of_{suit}.png"
        card_images["{} of {}".format(rank.title(), suit.title())] = pygame.image.load(filename.lower())
card_back = pygame.transform.scale(pygame.image.load(f"cards/back.png".lower()), (CARD_WIDTH, CARD_HEIGHT))

# Load the music file
pygame.mixer.music.load(f"cards/music.ogg")
# Load the sound file
sound = pygame.mixer.Sound(f"cards/music.ogg")
carddrop_sound = pygame.mixer.Sound(f"cards/carddrop_sound.ogg")
flipcard_sound = pygame.mixer.Sound(f"cards/flipcard_sound.ogg")
error_sound = pygame.mixer.Sound(f"cards/error_sound.ogg")
# Set the volume to 50%
sound.set_volume(0.2)
carddrop_sound.set_volume(0.4)
flipcard_sound.set_volume(0.3)
error_sound.set_volume(1)
# Start playing the music
sound.play()

# Define card values and suit values
card_values = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13, }
suit_values = {'Hearts': 2, 'Diamonds': 3, 'Clubs': 4, 'Spades': 1}

# Initialize the list of already drawn cards
drawn_cards = []

# Draw the cards in their respective areas without duplicates
cards = []
for i in range(52):
    card = random.choice(list(card_images.keys()))
    while card in drawn_cards:
        card = random.choice(list(card_images.keys()))
    cards.append(card)
    drawn_cards.append(card)

player1_cards = cards[:5]
player2_cards = cards[5:10]
dealer_cards = cards[10:15]

selected_card = None
player1_bet_area = [[] for _ in range(5)]
player2_bet_area = [[] for _ in range(5)]


# Initialize variables
can_exchange_card = False
scoreboard = []
score_round = {'player1': 0, 'player2': 0}


# Exchange Card Button
EXCHANGE_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH / 2 - -220, 620, 160, 40)
EXCHANGE_BUTTON_COLOR = (255, 255, 255)
EXCHANGE_BUTTON_HIGHLIGHT_COLOR = (255, 255, 0)
placed_cards = 0

# New Round Button
NEW_ROUND_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH / 2 - 200, 580, 400, 120)
NEW_ROUND_BUTTON_COLOR = (255, 255, 255)
NEW_ROUND_BUTTON_HIGHLIGHT_COLOR = (255, 255, 0)


# Define card values and suit values
card_values = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13}
suit_values = {'Hearts': 2, 'Diamonds': 3, 'Clubs': 4, 'Spades': 1}

def rank_proximity(player1_card, player2_card):
    rank1 = int(player1_card.split()[0])
    rank2 = int(player2_card.split()[0])
    diff = abs(rank1 - rank2)
    return min(diff, 13 - diff)

def suit_proximity(player_card, dealer_card):
    player_suit = player_card.split()[2]
    dealer_suit = dealer_card.split()[2]
    if player_suit == dealer_suit:
        return 0
    else:
        return abs(suit_values[player_suit] - suit_values[dealer_suit])

def card_distance(player1_card, player2_card, dealer_card):
    rank_diff1 = rank_proximity(player1_card, dealer_card)
    rank_diff2 = rank_proximity(player2_card, dealer_card)
    suit_diff1 = suit_proximity(player1_card, dealer_card)
    suit_diff2 = suit_proximity(player2_card, dealer_card)

    if rank_diff1 < rank_diff2:
        return 'player1'
    elif rank_diff1 > rank_diff2:
        return 'player2'
    else:
        if suit_diff1 < suit_diff2:
            return 'player1'
        elif suit_diff1 > suit_diff2:
            return 'player2'
        else:
            return 'tie'


def reset_game(highlight_cards=None):
    global player1_cards, player2_cards, dealer_cards, selected_card, player1_bet_area, player2_bet_area, placed_cards, can_exchange_card
    # Reset the game state
    cards = list(card_images.keys())
    # Shuffle the cards multiple times
    for i in range(5):
        random.shuffle(cards)
    player1_cards = cards[:5]
    player2_cards = cards[5:10]
    dealer_cards = cards[10:15]
    selected_card = None
    player1_bet_area = [[] for _ in range(5)]
    player2_bet_area = [[] for _ in range(5)]
    placed_cards = 0
    can_exchange_card = False

    if highlight_cards is not None:
        for index in highlight_cards:
            x = (SCREEN_WIDTH - RECT_WIDTH * 5) / 2 + RECT_WIDTH * index + index * GAP_SIZE
            y = PLAYER1_CARD_AREA_Y
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT), 4)

def reset_instance():
    global scoreboard, score_round, player1_cards, player2_cards, dealer_cards, selected_card, player1_bet_area, player2_bet_area, can_exchange_card, count
    scoreboard = []
    score_round = {'player1': 0, 'player2': 0}
    cards = set([random.choice(list(card_images.keys())) for _ in range(52)])
    while len(cards) < 15:
        cards.add(random.choice(list(card_images.keys())))
    player1_cards = list(cards)[:5]
    player2_cards = list(cards)[5:10]
    dealer_cards = list(cards)[10:15]
    selected_card = None
    player1_bet_area = [[] for _ in range(5)]
    player2_bet_area = [[] for _ in range(5)]
    can_exchange_card = False
    count = 0


def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)


# Game Loop
running = True
count = 0
messages = []
round_message_added = False
scoreboard_updated = False
while running and count < 9:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if all(player1_bet_area[col] for col in range(5)):
                if not scoreboard_updated:
                    scoreboard.append([score_round['player1'], score_round['player2']])
                    score_round = {'player1': 0, 'player2': 0}
                    player1_total = sum([score[0] for score in scoreboard])
                    player2_total = sum([score[1] for score in scoreboard])
                    print("Player 1 total:", player1_total)
                    print("Player 2 total:", player2_total)
                    if not round_message_added:
                        messages.append("Round " + str(count + 1))
                        round_message_added = True
                    scoreboard_updated = True
                if NEW_ROUND_BUTTON_RECT.collidepoint(x, y):
                    reset_game()
                    scoreboard_updated = False
                    round_message_added = False
                continue
            if round_message_added:
                round_message_added = False
                scoreboard_updated = False


            # Handle mouse clicks
            if EXCHANGE_BUTTON_RECT.collidepoint(x, y) and can_exchange_card:
                if any(player1_bet_area[col] for col in range(4)):
                    # Discard player 1's 5th card and draw a new one
                    selected_card = None
                    card = random.choice(list(set(card_images.keys()) - set(player1_cards + player2_cards + dealer_cards)))
                    player1_bet_area[4].append(card)
                    player1_cards.pop()
                    can_exchange_card = False
                else:
                    print("Cannot exchange card until the first 4 cards are bet.")
                    messages.append("Cannot exchange card until the first 4 cards are bet.")
                    error_sound.play()


            elif selected_card is None and y >= PLAYER1_CARD_AREA_Y and y < PLAYER1_CARD_AREA_Y + CARD_HEIGHT:
                col = int((x - (SCREEN_WIDTH - CARD_WIDTH * 5) / 2) // CARD_WIDTH)
                if col >= 0 and col < len(player1_cards):
                    selected_card = player1_cards.pop(col)
                    can_exchange_card = False  # Disable the Exchange Card button
                    carddrop_sound.play()  # Play the carddrop sound

            elif selected_card is not None and y >= PLAYER1_BET_AREA_Y and y < PLAYER1_BET_AREA_Y + CARD_HEIGHT:
                col = int((x - (SCREEN_WIDTH - CARD_WIDTH * 5) / 2) // CARD_WIDTH)
                if col >= 0 and col < 5:
                    if not player1_bet_area[col]:
                        # Ensure that the selected card is placed in the first 4 columns
                        if col < 4 or (col == 4 and all(player1_bet_area[col] for col in range(4))):
                            player1_bet_area[col].append(selected_card)
                            selected_card = None
                            # Add a card from player2_card_area to player2_bet_area
                            if player2_cards:
                                card_index = random.randint(0, len(player2_cards) - 1)
                                card = player2_cards.pop(card_index)
                                player2_bet_area[col] = [card]
                                if all(player1_bet_area[col] for col in range(4)):
                                    can_exchange_card = True
                            flipcard_sound.play()  # Play the flipcard sound
                        else:
                            print("Cannot place card in column 5 yet")
                            messages.append("Cannot place card in column 5 yet")
                            error_sound.play()
                    else:
                        print("This column is already bet.")
                        # Add a message to the list
                        messages.append("This column is already bet.")
                        error_sound.play()

            elif selected_card is not None and y >= PLAYER1_CARD_AREA_Y and y < PLAYER1_CARD_AREA_Y + CARD_HEIGHT:
                player1_cards.append(selected_card)
                selected_card = None
                can_exchange_card = True  # Enable the Exchange Card button


            elif selected_card is not None and y >= PLAYER1_CARD_AREA_Y and y < PLAYER1_CARD_AREA_Y + CARD_HEIGHT:
                player1_cards.append(selected_card)
                selected_card = None


            elif can_exchange_card and EXCHANGE_BUTTON_RECT.collidepoint(x, y):
                # Check if all columns in player1_bet_area have cards
                if any(player1_bet_area[col] for col in range(4)):
                    # Discard player 1's 5th card and draw a new one
                    selected_card = None
                    card = random.choice(list(set(card_images.keys()) - set(player1_cards + player2_cards + dealer_cards)))
                    player1_bet_area[4].append(card)
                    can_exchange_card = False
                else:
                    print("Cannot exchange card until the first 4 cards are bet.")

            # Move player 2's last card to corresponding bet area column
            if player2_bet_area and len(player2_bet_area[-1]) > 0:
                last_card = player2_bet_area[-1][0]
                if last_card in player2_cards:
                    col = 4 - player1_bet_area.count([])
                    player2_cards.remove(last_card)
                    player2_bet_area[col] = [last_card]

            # Check if all bet areas are filled
            if all(player1_bet_area[col] for col in range(5)):
                # Compare player 1 bet area with dealer cards
                tie = False
                for col in range(5):
                    if not player1_bet_area[col]:
                        continue
                    player1_card = player1_bet_area[col][0]
                    if not player2_bet_area[col]:
                        continue
                    player2_card = player2_bet_area[col][0]
                    dealer_card = dealer_cards[col]
                    player1_distance = rank_proximity(player1_card, dealer_card)
                    player2_distance = rank_proximity(player2_card, dealer_card)
                    if player1_distance < player2_distance:
                        print(f"Player 1 wins on column {col + 1}")
                        messages.append(f"Player 1 wins on column {col + 1}")
                        score_round['player1'] += 1
                    elif player1_distance > player2_distance:
                        print(f"Player 2 wins on column {col + 1}")
                        messages.append(f"Player 2 wins on column {col + 1}")
                        score_round['player2'] += 1
                    else:
                        # Compare player 1 bet area with dealer cards by suit
                        player1_suit = player1_card.split()[2]
                        dealer_suit = dealer_card.split()[2]
                        player2_suit = player2_card.split()[2]
                        suit_distance1 = suit_proximity(player1_card, dealer_card)
                        suit_distance2 = suit_proximity(player2_card, dealer_card)
                        if suit_distance1 < suit_distance2:
                            print(f"Player 1 wins on column {col + 1}")
                            messages.append(f"Player 1 wins on column {col + 1}")
                            score_round['player1'] += 1
                        elif suit_distance1 > suit_distance2:
                            print(f"Player 2 wins on column {col + 1}")
                            messages.append(f"Player 2 wins on column {col + 1}")
                            score_round['player2'] += 1
                        else:
                            print(f"Rolling dice to break tie in column {col + 1}")
                            messages.append(f"Rolling dice to break tie in column {col + 1}")
                            player1_dice = roll_dice()
                            player2_dice = roll_dice()
                            if player1_dice > player2_dice:
                                print(f"Player 1 wins on column {col + 1} with dice roll {player1_dice} vs {player2_dice}")
                                messages.append(f"Player 1 wins on column {col + 1} with dice roll {player1_dice} vs {player2_dice}")
                                score_round['player1'] += 1
                            elif player1_dice < player2_dice:
                                print(f"Player 2 wins on column {col + 1} with dice roll {player2_dice} vs {player1_dice}")
                                messages.append(f"Player 2 wins on column {col + 1} with dice roll {player2_dice} vs {player1_dice}")
                                score_round['player1'] += 1
                            else:
                                print(f"Column {col + 1} is a tie even after rolling dice")
                                messages.append(f"Column {col + 1} is a tie even after rolling dice")
                                tie = True

                    # Automatically place Player 2's cards in the Player 2 bet area
                    if player2_cards:
                        card_index = random.randint(0, len(player2_cards) - 1)
                        card = player2_cards.pop(card_index)
                        for col in range(5):
                            if not player2_bet_area[col]:
                                player2_bet_area[col].append(card)
                                break

                count += 1
                if count == 9:
                    reset_instance()
                break

    # Set the gap size between rectangles
    GAP_SIZE = 5
    GAP_SIZE2 = 10

    # Convert image to same format as screen
    table_image = table_image.convert(screen)

    # Fill screen with white color
    screen.fill((255, 255, 255))

    # Draw background image
    screen.blit(table_image, (-5, -89))


    # Draw the player 2 bet area
    all_bets_filled = all(player2_bet_area[col] for col in range(5))
    for col in range(5):
        x = (SCREEN_WIDTH - CARD_WIDTH * 5) / 2 + CARD_WIDTH * col + col * GAP_SIZE
        y = PLAYER2_BET_AREA_Y + 15
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT), 2)

        # Highlight the winning cards when all bet areas are filled
        if all_bets_filled:
            dealer_card = dealer_cards[col]
            player1_card = player1_bet_area[col][-1] if player1_bet_area[col] else None
            player2_card = player2_bet_area[col][-1] if player2_bet_area[col] else None
            if player2_card and card_distance(player1_card, player2_card, dealer_card) == 'player2':
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x - 2, y - 2, CARD_WIDTH + 4, CARD_HEIGHT + 4), 5)
            elif player1_card and card_distance(player1_card, player2_card, dealer_card) == 'player1':
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x - 2, y - 2, CARD_WIDTH + 4, CARD_HEIGHT + 4), 5)

    # Draw cards in player 2 bet area
    if all(player2_bet_area[col] for col in range(5)):
        for col, card_list in enumerate(player2_bet_area):
            for row, card in enumerate(card_list):
                x = (SCREEN_WIDTH - CARD_WIDTH * 5) / 2 + CARD_WIDTH * col + col * GAP_SIZE
                y = PLAYER2_BET_AREA_Y + CARD_HEIGHT * (row + 0) + 15
                if card in card_images:
                    card_img = pygame.transform.scale(card_images[card], (CARD_WIDTH, CARD_HEIGHT))
                    screen.blit(card_img, (x, y))
    else:
        for col, card_list in enumerate(player2_bet_area):
            for row, card in enumerate(card_list):
                x = (SCREEN_WIDTH - CARD_WIDTH * 5) / 2 + CARD_WIDTH * col + col * GAP_SIZE
                y = PLAYER2_BET_AREA_Y + CARD_HEIGHT * (row + 0) + 15
                if card in card_images:
                    card_img = pygame.transform.scale(card_back, (CARD_WIDTH, CARD_HEIGHT))
                    screen.blit(card_img, (x, y))

    # Draw cards in player 2 card area
    for col, card in enumerate(player2_cards):
        x = (SCREEN_WIDTH - CARD_WIDTH * 5) / 2 + CARD_WIDTH * col + col * GAP_SIZE
        y = PLAYER2_CARD_AREA_Y
        card_img = pygame.transform.scale(card_back, (CARD_WIDTH, CARD_HEIGHT))
        screen.blit(card_img, (x, y))

    # Draw the dealer card area
    for col in range(5):
        x = (SCREEN_WIDTH - CARD_WIDTH * 5) / 2 + CARD_WIDTH * col + col * GAP_SIZE
        y = DEALER_CARD_AREA_Y
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT), 2)

    # Draw cards in dealer card area
    for col, card in enumerate(dealer_cards):
        x = (SCREEN_WIDTH - CARD_WIDTH * 5) / 2 + CARD_WIDTH * col + col * GAP_SIZE
        y = DEALER_CARD_AREA_Y
        if col in [1, 3, 4] and not all(player1_bet_area[:4]):
            card_img = pygame.transform.scale(card_back, (CARD_WIDTH, CARD_HEIGHT))
        else:
            card_img = pygame.transform.scale(card_images[card], (CARD_WIDTH, CARD_HEIGHT))
        screen.blit(card_img, (x, y))

    # Draw the player 1 bet area
    all_bets_filled = all(player1_bet_area[col] for col in range(5))
    for col in range(5):
        x = (SCREEN_WIDTH - CARD_WIDTH * 5) / 2 + CARD_WIDTH * col + col * GAP_SIZE
        y = PLAYER1_BET_AREA_Y + -14
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, RECT_WIDTH, RECT_HEIGHT), 2)

        # Highlight the winning cards when all bet areas are filled
        if all_bets_filled:
            dealer_card = dealer_cards[col]
            player1_card = player1_bet_area[col][0]
            player2_card = player2_bet_area[col][0]
            if card_distance(player1_card, player2_card, dealer_card) == 'player1':
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x - 2, y - 2, CARD_WIDTH + 5, CARD_HEIGHT + 4), 5)
            elif card_distance(player1_card, player2_card, dealer_card) == 'player2':
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x - 2, y - 2, CARD_WIDTH + 5, CARD_HEIGHT + 4), 5)

    # Draw cards in player 1 bet area
    for col, card_list in enumerate(player1_bet_area):
        for row, card in enumerate(card_list):
            x = (SCREEN_WIDTH - CARD_WIDTH * 5) / 2 + CARD_WIDTH * col + col * GAP_SIZE + (RECT_WIDTH - CARD_WIDTH) / 2
            y = PLAYER1_BET_AREA_Y + CARD_HEIGHT * (row + 0) + -15
            card_img = pygame.transform.scale(card_images[card], (CARD_WIDTH, CARD_HEIGHT))
            screen.blit(card_img, (x, y))

    # Draw cards in player 1 card area
    for col, card in enumerate(player1_cards):
        x = (SCREEN_WIDTH - RECT_WIDTH * 5) / 2 + RECT_WIDTH * col + col * GAP_SIZE
        y = PLAYER1_CARD_AREA_Y
        card_img = pygame.transform.scale(card_images[card], (CARD_WIDTH, CARD_HEIGHT))
        screen.blit(card_img, (x, y))
        if selected_card is None:
            if x <= pygame.mouse.get_pos()[0] <= x + CARD_WIDTH and y <= pygame.mouse.get_pos()[1] <= y + CARD_HEIGHT:
                col = int((pygame.mouse.get_pos()[0] - (SCREEN_WIDTH - CARD_WIDTH * 5) / 2) // CARD_WIDTH)
                if col >= 0 and col < len(player1_cards):
                    x = (SCREEN_WIDTH - CARD_WIDTH * 5) / 2 + CARD_WIDTH * col + col * GAP_SIZE
                    y = PLAYER1_CARD_AREA_Y
                    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT), 4)


    # Draw the selected card in the mouse position
    if selected_card is not None:
        x, y = pygame.mouse.get_pos()
        x -= CARD_WIDTH / 2
        y -= CARD_HEIGHT / 2
        card_img = pygame.transform.scale(card_images[selected_card], (CARD_WIDTH, CARD_HEIGHT))
        screen.blit(card_img, (x, y))


    # Draw exchange button
    if all(player1_bet_area[col] for col in range(4)) and not player1_bet_area[4]:
        if can_exchange_card:
            x, y = pygame.mouse.get_pos()
            if EXCHANGE_BUTTON_RECT.collidepoint(x, y):
                pygame.draw.rect(screen, EXCHANGE_BUTTON_HIGHLIGHT_COLOR, EXCHANGE_BUTTON_RECT)
            else:
                pygame.draw.rect(screen, EXCHANGE_BUTTON_COLOR, EXCHANGE_BUTTON_RECT)
            pygame.draw.rect(screen, [255, 255, 0], EXCHANGE_BUTTON_RECT, 2)
            font = pygame.font.Font(None, 20)
            text = font.render("Exchange Card", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (EXCHANGE_BUTTON_RECT.centerx, EXCHANGE_BUTTON_RECT.centery)
            screen.blit(text, text_rect)
        else:
            ...


    # Draw the New Round button
    if all(player1_bet_area[col] for col in range(5)):
        x, y = pygame.mouse.get_pos()
        if NEW_ROUND_BUTTON_RECT.collidepoint(x, y):
            pygame.draw.rect(screen, NEW_ROUND_BUTTON_HIGHLIGHT_COLOR, NEW_ROUND_BUTTON_RECT, 0)
        else:
            pygame.draw.rect(screen, NEW_ROUND_BUTTON_COLOR, NEW_ROUND_BUTTON_RECT, 0)
        pygame.draw.rect(screen, [255, 255, 0], NEW_ROUND_BUTTON_RECT, 2)
        font = pygame.font.Font(None, 20)
        text1 = font.render("New Round", True, (0, 0, 0))
        text_rect1 = text1.get_rect(center=(NEW_ROUND_BUTTON_RECT.centerx, NEW_ROUND_BUTTON_RECT.centery - 10))
        screen.blit(text1, text_rect1)
        text2 = font.render("Click Here", True, (0, 0, 0))
        text_rect2 = text2.get_rect(center=(NEW_ROUND_BUTTON_RECT.centerx, NEW_ROUND_BUTTON_RECT.centery + 10))
        screen.blit(text2, text_rect2)

    # Draw the table
    table_font = pygame.font.Font(None, 20)
    row_text = table_font.render("Round", True, (255, 255, 255))
    row_rect = row_text.get_rect()
    row_rect.left = 20
    row_rect.top = 10
    screen.blit(row_text, row_rect)

    col1_text = table_font.render("Player 1", True, (255, 255, 255))
    col1_rect = col1_text.get_rect()
    col1_rect.left = 80
    col1_rect.top = 10
    screen.blit(col1_text, col1_rect)

    col2_text = table_font.render("Player 2", True, (255, 255, 255))
    col2_rect = col2_text.get_rect()
    col2_rect.left = 140
    col2_rect.top = 10
    screen.blit(col2_text, col2_rect)

    # Draw the Scores
    for row_index in range(9):
        round_text = table_font.render(str(row_index + 1), True, (255, 255, 255))
        round_rect = round_text.get_rect()
        round_rect.left = 35
        round_rect.top = 40 + row_index * 20
        screen.blit(round_text, round_rect)

    color = (255, 255, 0)
    round_text = table_font.render(str(count + 1), True, color)
    round_rect = round_text.get_rect()
    round_rect.left = 35
    round_rect.top = 40 + count * 20
    screen.blit(round_text, round_rect)

    for row_index in range(len(scoreboard)):
        if row_index == count - 1:
            color = (255, 255, 255)
        else:
            color = (255, 255, 255)

        round_score = scoreboard[row_index]
        round_text = table_font.render(str(row_index + 1), True, color)
        round_rect = round_text.get_rect()
        round_rect.left = 35
        round_rect.top = 40 + row_index * 20
        screen.blit(round_text, round_rect)

        player1_text = table_font.render(str(round_score[0]), True, (255, 255, 255))
        player1_rect = player1_text.get_rect()
        player1_rect.left = 96
        player1_rect.top = 40 + row_index * 20
        screen.blit(player1_text, player1_rect)

        player2_text = table_font.render(str(round_score[1]), True, (255, 255, 255))
        player2_rect = player2_text.get_rect()
        player2_rect.left = 156
        player2_rect.top = 40 + row_index * 20
        screen.blit(player2_text, player2_rect)

    # Draw Game Console
    # Clear the text box surface
    textbox_surface.fill((0, 0, 0))
    # Blit the text onto the text box surface
    y = 0
    for message in messages:
        font = pygame.font.Font(None, 20)
        text_surface = font.render(message, True, (255, 255, 0))
        textbox_surface.blit(text_surface, (0, y))
        y += text_surface.get_height()
    # Scroll the text box surface up by the height of the last message
    if y > TEXTBOX_HEIGHT:
        messages.pop(0)
        textbox_surface.scroll(0, -text_surface.get_height())
    # Blit the text box surface onto the main screen
    screen.blit(textbox_surface, (TEXTBOX_X, TEXTBOX_Y))


    # Update the screen
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()

#Details Update