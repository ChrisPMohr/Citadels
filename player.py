class Player(object):
    CHOICE_GOLD = 'GOLD'
    CHOICE_CARD = 'CARD'

    CHOICE_STEP = 'STEP'
    CHOICE_POWER = 'POWER'

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

    def can_play(self, district):
        if district.cost > self.gold:
            return False
        for played_district in self.city:
            if district.name == played_district.name:
                return False
        return True

    def finished_city(self):
        return len(self.city) >= 8
