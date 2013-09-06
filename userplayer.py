import os
import colorama
from player import Player
from districts import District, Colors
from roles import Role

colorama.init()

ansi_colors = {'Red': colorama.Fore.RED,
               'Blue': colorama.Fore.CYAN,
               'Yellow': colorama.Fore.YELLOW,
               'Green': colorama.Fore.GREEN,
               'Purple': colorama.Fore.MAGENTA}

def color(str, color):
    return ansi_colors[color] + str + colorama.Fore.RESET

def print_lines(format_str, print_list):
    out = '\n'.join(format_str.format(*k) for k in print_list)
    if out:
        print out

def print_numbered_lines(format_str, print_list, start=1):
    format_str = '{}: ' + format_str
    out = '\n'.join(format_str.format(num, *k) for num, k 
                    in enumerate(print_list, start))
    if out:
        print out

def print_numbered_districts(cards):
    print_numbered_lines(
        '{} - {}', 
        [(color(card.name, card.color), card.cost)
         for card in cards])

def format_districts(cards):
    return ' '.join(format_object(card) for card in cards)

def format_object(arg):
    if isinstance(arg, Player):
        return 'Player {}'.format(arg.num)
    elif isinstance(arg, District):
        return color('{}-{}'.format(arg.name, arg.cost), arg.color)
    elif isinstance(arg, Role):
        return arg.name
    else:
        return str(arg)

def format_string(message, *args):
    formatted_args = list()
    for arg in args:
        formatted_args.append(format_object(arg))
    return message.format(*formatted_args)


class UserPlayer(Player):
    def __init__(self):
       super(UserPlayer, self).__init__()

    def pick_role(self, roles):
        self.print_board()

        print_numbered_lines('{}', [(role.name,) for role in roles])

        while True:
           choice = raw_input('Choose a role: ')
           try:
                choice = int(choice) - 1
                if choice < 0 or choice >= len(roles):
                    continue
                return choice
           except:
                pass

    def choose_district(self, cards, mandatory=False):
        self.print_board()

        print_numbered_districts(cards)
        if not mandatory:
            print 'X: Cancel'

        while True:
            choice = raw_input('Choose a district: ')
            if choice == 'X':
                return Player.CHOICE_CANCEL
            else:
                try:
                    choice = int(choice) - 1
                    if choice < 0 or choice >= len(cards):
                        continue
                    return cards[choice]
                except:
                    pass

    def choose_action(self, played_district):
        self.print_board()

        cards = self.cards_with_unused_powers()
        answers = list()

        if not played_district:
            print '1: Play a district'
            answers.append(Player.CHOICE_PLAY_DISTRICT)
        print_numbered_lines('Use {} power',
            [(format_object(card),) for card in cards], len(answers) + 1)
        answers.extend(cards)

        print '{}: End the turn'.format(len(answers) + 1)
        answers.append(Player.CHOICE_END_TURN)

        while True:
            choice = raw_input('Choose an action: ')
            try:
                choice = int(choice) - 1
                if choice < 0 or choice >= len(answers):
                    continue
                else:
                    return answers[choice]
            except:
                pass

    def choose_resource(self):
        self.print_board()

        print '1: Get gold'
        print '2: Get card'

        while True:
            choice = raw_input('Get gold or a card: ')
            if choice == '1':
                return Player.CHOICE_GOLD
            elif choice == '2':
                return Player.CHOICE_CARD

    def choose_district_from_hand(self):
        self.print_board()

        playable_districts = [district for district in 
                              self.hand if self.can_play(district)]
        print_numbered_districts(playable_districts)
        print 'N: None'
        print 'X: Cancel'

        while True:
            choice = raw_input('Choose a district from your hand to play: ')
            if choice == 'N':
                return Player.CHOICE_NONE
            elif choice == 'X':
                return Player.CHOICE_CANCEL
            else:
                try:
                    choice = int(choice) - 1
                    if choice < 0 or choice >= len(playable_districts):
                        continue
                    else:
                        return playable_districts[choice]
                except:
                    pass

    def choose_a_role(self, roles):
        self.print_board()

        print_numbered_lines('{}', [(role.name,) for role in roles])
        print 'X: Cancel'

        while True:
            choice = raw_input('Choose one of the roles listed: ')
            if choice == 'X':
                return Player.CHOICE_CANCEL
            else:
                try:
                    choice = int(choice) - 1
                    if choice < 0 or choice >= len(roles):
                        continue
                    else:
                        return roles[choice]
                except:
                    pass

    def choose_magician_action(self):
        self.print_board()

        print '1: Exchange your hand with the hand of another player'
        print '2: Place any number of cards from your hand on the bottom of the District Deck, then draw that many cards'
        print 'X: Cancel'

        while True:
            choice = raw_input('Choose an action: ')
            if choice == 'X':
                return Player.CHOICE_CANCEL
            elif choice == '1':
                return Player.CHOICE_MAGIC_PLAYER
            elif choice == '2':
                return Player.CHOICE_MAGIC_DECK

    def choose_player(self, player_numbers):
        self.print_board()

        print_lines('{0}: Player {0}', [(num,) for num in player_numbers])
        print 'X: Cancel'

        while True:
            choice = raw_input('Choose one of the listed players: ')
            if choice == 'X':
                return Player.CHOICE_CANCEL
            else:
                try:
                    choice = int(choice)
                    if choice in player_numbers:
                        return choice
                except:
                    pass

    def choose_cards_in_hand(self):
        self.print_board()

        choices = list()
        for card in self.hand:
            while True:
                choice = raw_input(format_string('Discard card {}? (Y/N): ', card))
                if choice == 'Y':
                    choices.append(True)
                    break
                elif choice == 'N':
                    choices.append(False)
                    break
        return choices

    def choose_binary(self, message, *args):
        self.print_board()

        while True:
            choice = raw_input(format_string(message + '? (Y/N): ', *args))
            if choice == 'Y':
                return True
            elif choice == 'N':
                return False

    def update_board(self, players, current_player, starting_player, removed_roles):
        self.players = players
        self.current_player = current_player
        self.starting_player = starting_player
        self.removed_roles = removed_roles
        self.print_board()

    def print_board(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        # Print board
        for player in self.players:
            city_info = ' '.join(
                color(card.short_name + str(card.cost), card.color)
                for card in player.city)

            if player == self.starting_player:
                sp_str = '*'
            else:
                sp_str = ' '

            player_info = '{}{}: G-{:<2} C-{:<2} '.format(
                sp_str, player.num, player.gold, len(player.hand))
            print player_info + city_info
        print '-'*79

        if self.removed_roles:
            print 'Removed {}'.format(
                ', '.join(format_object(role) for role in self.removed_roles))
            print '-'*79

        # Print own info
        if self.role:
            role_name = self.role.name
        else:
            role_name = 'None'
        print 'Role: {:34}Gold: {}'.format(role_name, self.gold)
        print 'Hand: ' + format_districts(self.hand)
        print 'City: ' + format_districts(self.city)
        print '-'*79

        # Print current player info
        if self.current_player:
            print format_string(
                'Current player: {:<24}Role: {}',
                self.current_player, self.current_player.role)

    def send_message(self, message, *args):
        raw_input(format_string(message, *args))
