import random
import responses

def card_to_value(card):
    for each in ["2","3","4","5","6","7","8","9"]:        # sees if the card is any number between 2-9 and makes the value equal to the specific number
        if card == each:
            value = int(each)
    for every in ["T","J","Q","K"]:                      #sees if card is any face card or 10... equals to 10
        if card == every:
            value = 10
    else:
        if card == "A":                                  #if the card is an Ace, then value = 1
            value = 1
    return value


def hard_score(hand):
    count = 0
    hscore = 0
    if len(hand) == 1:                            #if the hand is just 1 card, the score is equal to the card
        hscore = card_to_value(hand)
        return hscore
    elif len(hand) > 0:                     #if hand is more than 1 card, adds all cards together and determines value
        for i in range(len(hand)):
            if count < len(hand):
                hscore += (card_to_value(hand[count]))
                count += 1
            elif count == len(hand):
                hscore += (card_to_value(hand[-1:]))
    else:
        hscore = 0                             #if no cards in hand
        return hscore
    return hscore

def blackjack():
    global dealer
    global player
    global value
    dealer = " "
    player = " "
    value_dealer_hard = 0
    value_dealer_soft = 0
    value_player_hard = 0
    value_player_soft = 0
    ace_count_d = 0
    ace_count_p = 0
    count = 0
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]

    # CREATING THE DECK OF TWO CARDS EACH
    for i in range(2):
        number = random.randint(0, 12)
        dealer = dealer + cards[number]
    for i in range(2):
        number1 = random.randint(0, 12)
        player = player + cards[number1]

    # WINNING/LOSING CONDITIONS

    # DEALER CONDITIONAL
    dealer_value = 0
    if value_dealer_soft == 21 or value_dealer_hard == 21:
        #await interaction.response.send_message("You lose!")
        print("You Lose")
    if value_dealer_soft > 21 and value_dealer_hard > 21:
        #await interaction.response.send_message("You win!")
        print("You win")
    if value_dealer_soft > 21 and value_dealer_hard < 21:
        dealer_value = value_dealer_hard
    if value_dealer_soft < 21 and value_dealer_hard < 21:
        value_dealer_soft = value_dealer_soft
        value_dealer_hard = value_dealer_hard

    # PLAYER CONDITIONAL
    player_value = 0
    if value_player_soft == 21 or value_player_hard == 21:
        #await interaction.response.send_message("You win!")
        print("You win")
    if value_player_soft > 21 and value_player_hard > 21:
        #await interaction.response.send_message("You lose!")
        print("You lose")
    if value_player_soft > 21 and value_player_hard < 21:
        player_value = value_dealer_hard

    # OPTIONS
    """    if option == "hit":
        number1 = random.randint(0, 12)
        number2 = random.randint(0, 12)
        dealer = dealer + cards[number1]
        player = player + cards[number2]
    """


    """
     if option == "fold":
        if value_dealer_soft < 21 and value_dealer_hard < 21:
            if value_dealer_soft > value_dealer_hard:
                dealer_value = value_dealer_soft
            else:
                dealer_value = value_dealer_hard
            if value_player_soft < 21 and value_player_hard < 21:
                player_value = value_dealer_soft
            else:
                player_value = value_player_hard
        await interaction.response.send_message(f"You lose! You had {player_value} and dealer had {dealer_value}")
    """

   # if option == "check":
    number1 = random.randint(0, 12)
    dealer = dealer + cards[number1]

    # CALCULATING THE SCORE VALUES
    for each in dealer:
        for i in range(len(dealer)):
            if ace_count_d == 0 and each == "A":  # allows to consider the first ace
                value_dealer_soft += 11
                ace_count_d += 1
                count += 1
        if each in ["2", "3", "4", "5", "6", "7", "8", "9"]:
            value_dealer_hard += int(each)
            value_dealer_soft += int(each)
        elif each in ["T", "J", "Q", "K"]:
            value_dealer_hard += 10
            value_dealer_soft += 10
        else:
            if each == "A" and ace_count_d == 1:
                value_dealer_hard += 1

    for each in player:
        for i in range(len(player)):
            if ace_count_p == 0 and each == "A":  # allows to consider the first ace
                value_player_soft += 11
                ace_count_p += 1
                count += 1
        if each in ["2", "3", "4", "5", "6", "7", "8", "9"]:
            value_player_hard += int(each)
            value_player_soft += int(each)
        elif each in ["T", "J", "Q", "K"]:
            value_player_hard += 10
            value_player_soft += 10
        else:
            if each == "A" and ace_count_p == 1:
                value_player_hard += 1

    print(dealer_value)
    print(player_value)

blackjack()

