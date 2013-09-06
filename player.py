class Player(object):
    CHOICE_GOLD = 'GOLD'
    CHOICE_CARD = 'CARD'

    CHOICE_PLAY_DISTRICT = 'PLAY DISTRICT'
    CHOICE_END_TURN = 'END TURN'

    CHOICE_CANCEL = 'CANCEL'
    CHOICE_NONE = 'NONE'

    CHOICE_MAGIC_PLAYER = 'MAGIC_PLAYER'
    CHOICE_MAGIC_DECK = 'MAGIC_DECK'

    def __init__(self):
       self.gold = 0
       self.hand = []
       self.role = None
       self.city = []
       self.first_to_finish = False

    def add_to_hand(self, card):
        self.hand.append(card)

    def remove_from_hand(self, card):
        self.hand.remove(card)

    def add_to_city(self, card):
        self.city.append(card)

    def remove_from_city(self, card):
        self.city.remove(card)

    def can_play(self, district):
        if district.cost > self.gold:
            return False
        for played_district in self.city:
            if district.name == played_district.name:
                return False
        return True

    def finished_city(self):
        return len(self.city) >= 8

    def has_district(self, name):
        for district in self.city:
            if district.name == name:
                return True
        return False

    def cards_with_powers(self):
        powers = list()
        if self.role.power:
            powers.append(self.role)
        for district in self.city:
            if district.power:
                powers.append(district)
        return powers

    def cards_with_unused_powers(self):
        unused_powers = list()
        for card in self.cards_with_powers():
            try:
                if not card.power.used:
                    unused_powers.append(card)
            except AttributeError:
                unused_powers.append(card)
        return unused_powers

    def reset_powers(self):
        for card in self.cards_with_powers():
            card.power.used = False

    def bonus_points(self):
        points = 0
        if self.has_district('Dragon Gate'):
            points += 2
        if self.has_district('University'):
            points += 2
        return points
