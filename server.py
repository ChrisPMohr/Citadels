import random
from player import Player
from randomplayer import RandomPlayer
from userplayer import UserPlayer
from districts import Colors, DistrictDeck
import roles

class Game(object):
    STARTING_GOLD = 2
    STARTING_CARDS = 4

    def main(self):
        self.num_players = 4
        self.available_roles = roles.ROLES
        self.removed_roles = None

        self.initialize_players()
        self.start_game()

    def start_game(self):
        self.districts = DistrictDeck()

        self.finished = False

        for player in self.players:
            player.gold += Game.STARTING_GOLD
            cards = self.districts.draw(Game.STARTING_CARDS)
            for card in cards:
                player.add_to_hand(card)
        self.starting_player = random.choice(self.players)

        while not self.is_game_over():
            self.game_loop()
        self.end_game()

    def game_loop(self):
        self.roles, self.removed_roles = self.make_role_pack()
        self.update_board(None)

        self.initialize_role_variables()

        current_player = self.starting_player
        self.role_players = dict()
        started = False
        while current_player != self.starting_player or not started:
            started = True
            self.draft_role(current_player)
            current_player = current_player.next_player

        for role in self.available_roles:
            self.update_board(None)
            self.send_message('Calling role {}', role)
            if role.name in self.role_players:
                current_player = self.role_players[role.name]
                if role == self.assassinated_role:
                    self.send_message('Silently skipping turn of {} with role {}',
                                      current_player, role)
                    continue

                if role == self.thieved_role:
                    self.send_message('{}, the Thief steals the gold of {}',
                                      self.role_players['Thief'], current_player)
                    self.role_players['Thief'].gold += current_player.gold
                    current_player.gold = 0

                if role.name == 'King':
                    self.send_message(
                        '{} is crowned King and is now starting player',
                        current_player)
                    self.starting_player = current_player

                self.do_turn(current_player)

        self.update_board(None)

        self.send_message('Turn over')

        if (self.assassinated_role and
            self.assassinated_role.name in self.role_players):
            self.send_message('{}, the {}, was assassinated this turn',
                            self.role_players[self.assassinated_role.name],
                            self.assassinated_role)
            if self.assassinated_role.name == 'King':
                king_player = self.role_players['King']
                self.send_message('{} is heir to the assassinated king and '
                                  'is now starting player', king_player)
                self.starting_player = king_player

    def initialize_players(self):
        self.players = [UserPlayer()]
        self.players.extend([RandomPlayer() for _
                             in range(self.num_players - 1)])

        for i, player in enumerate(self.players, 1):
            player.num = i 

        last_player = self.players[0]
        for player in reversed(self.players):
            player.next_player = last_player
            last_player = player

    def make_role_pack(self):
        roles = list(self.available_roles)
        random.shuffle(roles)
        roles = roles[1:]

        num_removed = max(6 - self.num_players, 0)

        for role in roles:
            if role.name == 'King':
                roles.remove(role)
                roles.append(role)

        return roles[num_removed:], roles[:num_removed]

    def draft_role(self, player):
        choice = player.pick_role(self.roles)
        player.role = self.roles.pop(choice)
        self.role_players[player.role.name] = player

    def do_turn(self, player):
        if player.role.power:
            can_use_power = True
        else:
            can_use_power = False

        turn_steps = [('Get resources', self.get_resource),
                      ('Play district', self.play_district),
                      ('End turn', self.end_turn)]

        for step_name, step in turn_steps:
            did_step = False
            while not did_step:
                self.update_board(player)
                if can_use_power:
                    if (player.choose_step_or_power(step_name) ==
                        Player.CHOICE_STEP):
                        did_step = step(player)
                    else:
                        can_use_power = not player.role.power(player, self)
                else:
                    did_step = step(player)

    def get_resource(self, player):
        choice = player.choose_resource()
        if choice == Player.CHOICE_GOLD:
            self.send_message('{} chose to take gold', player)
            ACTION_GOLD = 2
            player.gold += ACTION_GOLD
        elif choice == Player.CHOICE_CARD:
            self.send_message('{} chose to take a card', player)
            ACTION_CARDS = 2
            cards = self.districts.draw(ACTION_CARDS)
            kept_card = cards.pop(player.choose_district(cards, True))
            player.add_to_hand(kept_card)
            self.districts.put_on_bottom(cards)
        else:
            return False

        if player.role.name == 'Merchant':
            player.gold += 1
        if player.role.name == 'Architect':
            cards = self.districts.draw(2)
            for card in cards:
                player.add_to_hand(card)
        return True

    def play_district(self, player):
        ALLOWED_TO_PLAY = 1
        if player.role.name == 'Architect':
            ALLOWED_TO_PLAY += 2
        played = 0
        while played < ALLOWED_TO_PLAY:
            choice = player.choose_district_from_hand()
            if choice == Player.CHOICE_CANCEL:
                if played == 0:
                    return False
                else:
                    break
            elif choice == Player.CHOICE_NONE:
                break
            else:
                if player.can_play(choice):
                    player.remove_from_hand(choice)
                    player.add_to_city(choice)
                    player.gold -= choice.cost
                    # Do whatever rules changes needed

                    self.send_message('Playing {}', choice)
                    self.update_board(player)
                    if not self.finished and player.finished_city():
                        self.send_message('Game will end at the end of this round')
                        self.finished = True
                        player.first_to_finish = True
                    played += 1
        return True

    def end_turn(self, player):
        if player.role.name == 'Warlord':
            used_extra_power = False
            while not used_extra_power:
                self.update_board(player)
                used_extra_power = roles.warlord_extra_power(player, self)
        return True

    def is_game_over(self):
        return self.finished

    def end_game(self):
        self.send_message('Game over')
        scores = list()
        for player in self.players:
            score = sum([card.cost for card in player.city])
            if player.first_to_finish:
                score += 4
            elif player.finished_city():
                score += 2
            scores.append((score, player))
        scores.sort(reverse=True)
        self.send_message('Winner is {}!'.format(scores[0][1]))
        self.send_message('\n'.join(['Scores'] + 
            ['Player {}: {}'.format(score[1], score[0]) for score in scores]))
 
    def initialize_role_variables(self):
        self.assassinated_role = None
        self.thieved_role = None

    def update_board(self, current_player):
        for player in self.players:
            player.update_board(self.players, current_player,
                                self.starting_player, self.removed_roles)

    def send_message(self, message, *args):
        for player in self.players:
            player.send_message(message, *args)

game = Game()
game.main()
