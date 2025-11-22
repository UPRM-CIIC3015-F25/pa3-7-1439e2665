import json
from Cards.Card import Card

class GameSaver:
    def __init__(self, filename="savegame.json"):
        self.filename = filename

    def save_game(self, player_info_obj, hand, deck, activated_jokers):
        """
        Save the game state:
        - player_info_obj: PlayerInfo instance (save only serializable attributes)
        - hand: list of Card objects
        - deck: list of Card objects
        - activated_jokers: set or list of strings
        """
        # Extract serializable attributes from PlayerInfo
        player_info = {
            "roundScore": player_info_obj.roundScore,
            "playerChips": player_info_obj.playerChips,
            "playerMultiplier": player_info_obj.playerMultiplier,
            "amountOfHands": player_info_obj.amountOfHands,
            "amountOfDiscards": player_info_obj.amountOfDiscards,
            "playerMoney": player_info_obj.playerMoney,
            "playerAnte": player_info_obj.playerAnte,
            "round": player_info_obj.round,
            "curHandOfPlayer": player_info_obj.curHandOfPlayer,
            "curAmountJoker": player_info_obj.curAmountJoker,
            "levelFinished": player_info_obj.levelFinished,
            "score": player_info_obj.score,
            "deckType": player_info_obj.deckType,
        }

        # Serialize cards
        hand_data = [card.save_card() for card in hand]
        deck_data = [card.save_card() for card in deck]

        game_state = {
            "player_info": player_info,
            "hand": hand_data,
            "deck": deck_data,
            "activated_jokers": list(activated_jokers)
        }

        with open(self.filename, "w") as f:
            json.dump(game_state, f, indent=4)
        print(f"[GameSaver] Game saved to {self.filename}.")

    def load_game(self, deck_manager):
        """
        Load game state from file and return:
        - player_info dict
        - hand list of Card objects with images
        - deck list of Card objects with images
        - activated_jokers list
        """
        with open(self.filename, "r") as f:
            game_state = json.load(f)

        player_info = game_state.get("player_info", {})

        # Get images from deck manager
        cardImages = deck_manager.load_card_images()
        hcImages = deck_manager.load_card_images(alt=True)

        # Rebuild cards with images
        hand = []
        for c in game_state.get("hand", []):
            card = Card.load_card(c)
            card.image = cardImages.get((card.suit, card.rank))
            card.altImage = hcImages.get((card.suit, card.rank))
            hand.append(card)

        deck = []
        for c in game_state.get("deck", []):
            card = Card.load_card(c)
            card.image = cardImages.get((card.suit, card.rank))
            card.altImage = hcImages.get((card.suit, card.rank))
            deck.append(card)

        activated_jokers = game_state.get("activated_jokers", [])

        print(f"[GameSaver] Game loaded from {self.filename}.")
        return player_info, hand, deck, activated_jokers


