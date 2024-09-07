import random

def handle_response(message):
    p_message = message.lower()
    if p_message == 'hello':
        return "Hey!"

    if p_message == 'ping':
        return "Pong!"

    if p_message == '!roll':
        return str(random.randint(1,100))









#USE THIS CODE BELOW FROM CS1110 TO MAKE A GAME WITHIN THE DISCORD BOT

#GAME WILL HAVE THE USER FIRST BEGIN A SEQUEUNCE
# IF /blackjack is ON, THEN THESE FUNCTIONS APPLY (DONE)
# ONCE THAT IS SET, MAKE A CODE THAT GENERATES A RANDOM HAND OF 2 CARDS FOR THE USER
# THEN ALSO GENERATE A HAND FOR THE BOT.
# ONCE THAT IS DONE, USE THE hard_score and the soft_score to see WHICH CAN BE USED BETTER (hard is ace being 1) (soft is 11)
# MAKE A CODE TO DETERMINE IF THE USER WANTS TO FOLD/CHECK/HIT
# AFTER DOING THESE COMMANDS, SEE IF THE NEW HAND IS UPDATED TO SEE IF THEY LOSE (over 21)
# ONCE THE RULES ARE DONE, WE SEE IF THEY WIN OR NOT.

#LATER IF WANT, APPLY MONEY SYSTEM THAT ACTUALLY MAKES THIS DOABLE FOR IN-BOT CURRENCY


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

def soft_score(hand):           #same as hard_score but with ACE_COUNT to account for 1st ace
    count = 0
    score = 0
    ace_count = 0
    if len(hand) == 1:
        score = card_to_value(hand)
        return score
    elif len(hand) > 0:
        for i in range(len(hand)):
            if count < len(hand):
                if ace_count == 0 and hand[count] == "A": #allows to consider the first ace
                    score += 11
                    ace_count += 1
                    count += 1
                else:
                    score += (card_to_value(hand[count]))
                    count += 1
            elif count == len(hand):
                score += (card_to_value(hand[-1:]))
    else:
        score = 0
        return score
    return score
