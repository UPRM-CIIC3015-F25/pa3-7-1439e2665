from Cards.Card import Card, Rank

# TODO (TASK 3): Implement a function that evaluates a player's poker hand.
#   Loop through all cards in the given 'hand' list and collect their ranks and suits.
#   Use a dictionary to count how many times each rank appears to detect pairs, three of a kind, or four of a kind.
#   Sort these counts from largest to smallest. Use another dictionary to count how many times each suit appears to check
#   for a flush (5 or more cards of the same suit). Remove duplicate ranks and sort them to detect a
#   straight (5 cards in a row). Remember that the Ace (rank 14) can also count as 1 when checking for a straight.
#   If both a straight and a flush occur in the same suit, return "Straight Flush". Otherwise, use the rank counts
#   and flags to determine if the hand is: "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind",
#   "Two Pair", "One Pair", or "High Card". Return a string with the correct hand type at the end.

#helper function bc im not going to create a new sorting code when i alr did it
def SortCards(hands):
    for pases in range(len(hands) - 1):
        for hand in range(len(hands) - 1 - pases):
            if  hands[hand].rank.value > hands[hand + 1].rank.value:
                hands[hand], hands[hand + 1] = hands[hand + 1], hands[hand]

def evaluate_hand(hand: list[Card]):
    hand_org={}
    SortCards(hand)
    values = [card.rank.value for card in hand]
    pair = 0
    straight =True


    if len(hand) == 5:
        flush = True
    else:
        flush = False

    for hands in range(len(hand)):
        hand_org[hand[hands].rank.value]=hand_org.get(hand[hands].rank.value,0)+1
        if hand[0].suit != hand[hands].suit and flush:
            flush = False

    for value in hand_org.values():
        if value == 2:
            pair +=1

###########-----STRAIGHT DETECTION-----###########
    if len(values) == 5:
        if values == [2,3,4,5,14]:
            straight = True
        else:
            for i in range(len(values)-1):
                if values[i]+1 != values[i + 1]:
                    straight = False
                    break



    if 3 in hand_org.values() and 2 in hand_org.values():
        return "Full House"
    elif 4 in hand_org.values():
        return "Four of a Kind"
    elif 3 in hand_org.values():
        return "Three of a Kind"
    elif pair == 1:
        return "One Pair"
    elif pair == 2:
        return "Two Pair"
    if straight and flush:
        return "Straight Flush"
    elif flush:
        return "Flush"
    elif straight:
        return "Straight"

    else:
        return "High Card" # If none of the above, it's High Card
