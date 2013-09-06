import random
from player import Player
from randomplayer import RandomPlayer
from userplayer import UserPlayer
from districts import Colors, DistrictDeck
from debugger import Debugger
import roles

class Game(object):
    STARTING_GOLD = 2
    STARTING_CARDS = 4

    def main(self):
        self.num_players = 6
        self.available_roles = roles.ROLES
        self.removed_roles = None
        self.game_over = False

        self.districts = DistrictDeck()

        self.initialize_players()
        self.starting_player = random.choice(self.players)

        self.start_game()

    def start_game(self):
        for player in self.players:
            player.gold += Game.STARTING_GOLD
            cards = self.districts.draw(Game.STARTING_CARDS)
            for card in cards:
                player.add_to_hand(card)

        while not self.game_over:
            self.game_loop()
        self.end_game()

    def game_loop(self):
        self.start_turn()
        self.do_drafting()
        self.do_player_turns()
        self.do_end_of_turn()

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

    def do_drafting(self):
        self.roles, self.removed_roles = self.make_role_pack()
        self.update_board(None)

        current_player = self.starting_player
        self.role_players = dict()
        started = False
        while current_player != self.starting_player or not started:
            started = True
            self.draft_role(current_player)
            current_player = current_player.next_player

    def do_player_turns(self):
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
                    self.send_message('{}, the Thief, steals the gold of {}',
                                      self.role_players['Thief'], current_player)
                    self.role_players['Thief'].gold += current_player.gold
                    current_player.gold = 0

                if role.name == 'King':
                    self.send_message(
                        '{} is crowned King and is now starting player',
                        current_player)
                    self.starting_player = current_player

                self.do_turn(current_player)

    def do_end_of_turn(self):
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
        turn_steps = [('Get resources', self.get_resource),
                      ('Play district', self.may_play_district),
                      ('End turn', self.end_turn)]

        player.reset_powers()

        for step_name, step in turn_steps:
            did_step = False
            while not did_step:
                self.update_board(player)
                if player.cards_with_unused_powers():
                    choice = player.choose_step_or_power(step_name)
                    if choice == Player.CHOICE_STEP:
                        did_step = step(player)
                    else:
                        choice.power.used = choice.power(player, self)
                else:
                    did_step = step(player)

    def get_resource(self, player):
        choice = player.choose_resource()
        if choice == Player.CHOICE_GOLD:
            self.send_message('{} chose to take gold', player)
            NUM_GOLD = 2
            player.gold += NUM_GOLD
        elif choice == Player.CHOICE_CARD:
            self.send_message('{} chose to take a card', player)
            
            NUM_CARDS_DRAW = 2
            NUM_CARDS_KEEP = 1
            if player.has_district('Observatory'):
                NUM_CARDS_DRAW += 1
            if player.has_district('Library'):
                NUM_CARDS_KEEP += 1

            cards = self.districts.draw(NUM_CARDS_DRAW)
            for _ in range(NUM_CARDS_KEEP):
                kept_card = player.choose_district(cards, True)
                cards.remove(kept_card)
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

    def may_play_district(self, player):
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
                    player.gold -= choice.cost

                    self.play_district(player, choice)
                    played += 1
        return True

    def play_district(self, player, district):
        player.add_to_city(district)

        if district.name == 'Haunted City':
            district.played_this_turn = True

        self.send_message('{} playing {}', player, district)
        self.update_board(player)
        if not self.game_over and player.finished_city():
            self.send_message('Game will end at the end of this round')
            self.game_over = True
            player.first_to_finish = True

    def end_turn(self, player):
        if player.role.name == 'Warlord':
            used_extra_power = False
            while not used_extra_power:
                self.update_board(player)
                used_extra_power = roles.warlord_extra_power(player, self)
        return True

    def end_game(self):
        self.send_message('Game over')
        scores = list()
        for player in self.players:
            score = sum([card.cost for card in player.city])
            if player.first_to_finish:
                score += 4
            elif player.finished_city():
                score += 2
            if self.has_all_colors(player.city):
                score += 3
            score += player.bonus_points()
            scores.append((score, player))
        scores.sort(reverse=True)
        self.send_score_message(scores)

    def has_all_colors(self, city):
        NEEDED_COLORS = 5
        districts = list(city)
        for district in city:
            if district.name == 'Haunted City' and not district.played_this_turn:
                districts.remove(district)
                NEEDED_COLORS -= 1
                break
        return len(set([district.color for district in districts])) == NEEDED_COLORS

    def start_turn(self):
        self.assassinated_role = None
        self.thieved_role = None
        for player in self.players:
            player.role = None
            for district in player.city:
                if district.name == 'Haunted City':
                    district.played_this_turn = False

    def update_board(self, current_player):
        for player in self.players:
            player.update_board(self.players, current_player,
                                self.starting_player, self.removed_roles)

    def send_message(self, message, *args):
        for player in self.players:
            player.send_message(message, *args)

    def send_score_message(self, scores):
        self.send_message('Winner is {}!', scores[0][1])
        self.send_message(
            '\n'.join(['Scores:'] + 
            ['{}: '+ str(score[0]) for score in scores]),
            *[score[1] for score in scores])
 

game = Game()
game.main()
