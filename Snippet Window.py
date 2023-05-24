# Draw the dealer card area
    dealer_cards = [random.choice(list(card_images.keys())) for _ in range(5)]
    for col, card in enumerate(dealer_cards):
        x = (SCREEN_WIDTH - CARD_WIDTH * 5) / 2 + CARD_WIDTH * col
        y = DEALER_CARD_AREA_Y
        if col == 1 or col == 3 or col == 4:
            screen.blit(card_back, (x, y))
        else:
            card_img = pygame.transform.scale(card_images[card], (CARD_WIDTH, CARD_HEIGHT))
            screen.blit(card_img, (x, y))

########################################################################################################################################################################################################
########################################################################################################################################################################################################

def calculate_round_winner(player_cards, dealer_cards):

    # Calculate the sum of ranks for player cards and dealer cards
    player_ranks_sum = sum([card_values[card.rank] for card in player_cards])
    dealer_ranks_sum = sum([card_values[card.rank] for card in dealer_cards])

    # Calculate the rank differences using a palindrome
    player_rank_diff = abs(player_ranks_sum - dealer_ranks_sum)
    dealer_rank_diff = int(str(player_rank_diff)[::-1])

    # Check if the rank difference is zero, if so, use suit hierarchy to determine the winner
    if player_rank_diff == 0:
        player_suit_rank = sum([suit_values[card.suit] for card in player_cards])
        dealer_suit_rank = sum([suit_values[card.suit] for card in dealer_cards])
        if player_suit_rank > dealer_suit_rank:
            return "Player 1 wins!"
        elif dealer_suit_rank > player_suit_rank:
            return "Dealer wins!"
        else:
            return "It's a tie!"
    # Check if the rank difference is less than or equal to 6, if so, the player wins
    elif player_rank_diff <= 0:
        return "Player 1 wins!"
    elif dealer_rank_diff <= 1:
        return "Player 2 wins!"
    # Otherwise, it's a tie
    else:
        return "It's a tie!"

########################################################################################################################################################################################################
########################################################################################################################################################################################################

if rank_diff == 0:
    return suit_diff
elif rank_diff == 1:
    return 1
elif rank_diff == 2:
    return 3
elif rank_diff == 3:
    return 2
elif rank_diff == 4:
    return 4
elif rank_diff == 5:
    return 5
elif rank_diff == 6:
    return 6
elif card1.split()[0] == card2.split()[0][::-1]:
    return 1
else:
    return 7

################################################################################################################################################################################################################################################################################################################################################################################################################

count += 1
if count == 9:
    running = False

# Print the final score in a table
print("Player 1".ljust(15) + "Player 2".ljust(15))
print(f"{wc1}".ljust(15) + f"{wc2}".ljust(15))

############################################################################################################################################################################

# Draw the Scoreboard
    for row_index in range(9):
        round_text = table_font.render(str(row_index + 1), True, (255, 255, 255))
        round_rect = round_text.get_rect()
        round_rect.left = 20
        round_rect.top = 200 + row_index * 20
        screen.blit(round_text, round_rect)

        # Update the scoreboard only for the current round
        if row_index == count:
            player1_text = table_font.render(str(win_counter1['player1']), True, (255, 255, 255))
            player1_rect = player1_text.get_rect()
            player1_rect.left = 80
            player1_rect.top = 200 + row_index * 20
            screen.blit(player1_text, player1_rect)

            player2_text = table_font.render(str(win_counter2['player2']), True, (255, 255, 255))
            player2_rect = player2_text.get_rect()
            player2_rect.left = 140
            player2_rect.top = 200 + row_index * 20
            screen.blit(player2_text, player2_rect)

########################################################################################################################################################

# Draw player 1 win counter
    player1_text = font.render("Player 1: {}".format(win_counter1), True, (255, 255, 255))
    player1_rect = player1_text.get_rect()
    player1_rect.right = SCREEN_WIDTH - 20
    player1_rect.top = 20
    screen.blit(player1_text, player1_rect)

    # Draw player 2 win counter
    player2_text = font.render("Player 2: {}".format(win_counter2), True, (255, 255, 255))
    player2_rect = player2_text.get_rect()
    player2_rect.right = SCREEN_WIDTH - 20
    player2_rect.top = 60
    screen.blit(player2_text, player2_rect)