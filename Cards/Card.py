from enum import Enum

class Suit(Enum): # Enumeration for the four card suits
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"

class Rank(Enum): # Enumeration for the thirteen card ranks
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Card:
    def __init__(self, suit: Suit, rank: Rank, image=None,altimage=None): # Represents a single playing card with suit, rank, and optional image
        self.suit = suit
        self.rank = rank
        self.image = image
        self.altImage = altimage
        self.faceDown = False
        self.isSelected = False

        if rank.value <= 10: # Chip value based on rank
            self.chips = rank.value
        elif rank.value < 14:  # Face cards (Jack, Queen, King)
            self.chips = 10
        else:  # Ace
            self.chips = 11

    def __str__(self): # Formated string of the card (Example: Ace♠)
        return f"{self.rank.name.capitalize()}{self.suit.value}"

    def save_card(self):
        return {
            "suit": self.suit.name,
            "rank": self.rank.name,
            "chips": self.chips,
            "faceDown": self.faceDown
        }

    @staticmethod
    def load_card(data):
        card = Card(Suit[data["suit"]], Rank[data["rank"]])
        card.chips = data.get("chips", card.chips)
        card.faceDown = data.get("faceDown", False)
        card.isSelected = data.get("isSelected", False)
        return card