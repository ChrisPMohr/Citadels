import random
from player import Player

class RandomPlayer(Player):
    def __init__(self):
       super(RandomPlayer, self).__init__()

    def pick_role(self, roles):
        return random.randint(0, len(roles) - 1)

    def choose_district(self, cards, mandatory=False):
        if cards:
            return random.choice(cards)
        return Player.CHOICE_CANCEL

    def choose_action(self, played_district):
        if random.random() < 0.5 or played_district:
            if self.cards_with_unused_powers():
                return random.choice(self.cards_with_unused_powers())
        return Player.CHOICE_PLAY_DISTRICT

    def choose_resource(self):
        if random.random() < 0.5:
            return Player.CHOICE_GOLD
        else:
            return Player.CHOICE_CARD

    def choose_district_from_hand(self):
        playable_districts = [district for district in 
                              self.hand if self.can_play(district)]
        if playable_districts:
            return self.choose_district(playable_districts)
        else:
            return Player.CHOICE_NONE

    def choose_a_role(self, roles):
        return random.choice(roles)

    def choose_magician_action(self):
       return random.choice([Player.CHOICE_MAGIC_PLAYER, Player.CHOICE_MAGIC_DECK, Player.CHOICE_CANCEL])

    def choose_player(self, player_numbers):
        if player_numbers:
            return random.choice(player_numbers)
        else:
            return Player.CHOICE_CANCEL

    def choose_cards_in_hand(self):
        return [random.randint(0,1) for _ in range(len(self.hand))]

    def choose_binary(self, message, *args):
        if 'destroy' in message:
            return True
        if random.random() < 0.5:
            return True
        else:
            return False

    def update_board(self, players, current_player, starting_player, removed_roles):
        pass

    def send_message(self, message, *args):
        pass
