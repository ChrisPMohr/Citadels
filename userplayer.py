from player import Player
from colorama import init, Fore
import os
from districts import District, Colors

ansi_colors = {'Red': Fore.RED,
               'Blue': Fore.BLUE,
               'Yellow': Fore.YELLOW,
               'Green': Fore.GREEN,
               'Purple': Fore.MAGENTA}
init()


def print_lines(format_str, print_list):
    print '\n'.join(format_str.format(*k) for k in print_list)

def print_numbered_lines(format_str, print_list):
    format_str = '{}: ' + format_str
    print '\n'.join(format_str.format(num, *k) for num, k 
                    in enumerate(print_list, 1))

def print_numbered_districts(cards):
    print_numbered_lines(
        '{}{}{} - {}', 
        [(ansi_colors[card.color], card.name, Fore.RESET, card.cost)
         for card in cards])

def format_districts(cards):
    return ' '.join('{}{}{}-{}'.format(
        ansi_colors[card.color], card.name, Fore.RESET, card.cost)
        for card in cards)


class UserPlayer(Player):
    def __init__(self):
       super(UserPlayer, self).__init__()
#       self.city = [District('Town Hall', 'TwnH', 5, Colors.Green),
#                    District('Town Hall', 'TwnH', 5, Colors.Green),
#                    District('Town Hall', 'TwnH', 5, Colors.Green),
#                    District('Town Hall', 'TwnH', 5, Colors.Green),
#                    District('Town Hall', 'TwnH', 5, Colors.Green),
#                    District('Town Hall', 'TwnH', 5, Colors.Green),
#                    District('Town Hall', 'TwnH', 5, Colors.Green)]

    def pick_role(self, roles):
        print_numbered_lines('{}', [(role.name,) for role in roles])
        return int(raw_input('Choose a role: ')) - 1

    def choose_district(self, cards, mandatory=False):
        print_numbered_districts(cards)
        if not mandatory:
            print 'X: Cancel'

        choice = raw_input('Choose a district: ')

        if choice == 'X':
            return Player.CHOICE_CANCEL
        else:
            return int(choice) - 1

    def choose_step_or_power(self, step_name):
        print '1: ' + step_name
        print '2: Role power'

        choice = raw_input('Do step or use power: ')

        if choice == '1':
            return Player.CHOICE_STEP
        else:
            return Player.CHOICE_POWER

    def choose_resource(self):
        print '1: Get 2 gold'
        print '2: Draw two cards and keep one'
        print 'X: Cancel'

        choice = raw_input('Get gold or a card: ')

        if choice == '1':
            return Player.CHOICE_GOLD
        elif choice == '2':
            return Player.CHOICE_CARD
        else:
            return Player.CHOICE_CANCEL

    def choose_district_from_hand(self):
        playable_districts = [district for district in 
                              self.hand if self.can_play(district)]
        print_numbered_districts(playable_districts)
        print 'N: None'
        print 'X: Cancel'

        choice = raw_input('Choose a district from your hand to play: ')

        if choice == 'N':
            return Player.CHOICE_NONE
        elif choice == 'X':
            return Player.CHOICE_CANCEL
        else:
            return playable_districts[int(choice) - 1]

    def choose_a_role(self, roles):
        print_numbered_lines('{}', [(role.name,) for role in roles])
        print 'X: Cancel'

        choice = raw_input('Choose one of the roles listed: ')

        if choice == 'X':
            return Player.CHOICE_CANCEL
        else:
            return roles[int(choice) - 1]

    def choose_magician_action(self):
        print '1: Exchange your hand with the hand of another player'
        print '2: Place any number of cards from your at the bottom of the District Deck, then draw an equal number of cards'
        print 'X: Cancel'

        choice = raw_input('Choose an action: ')

        if choice == 'X':
            return Player.CHOICE_CANCEL
        elif choice == '1':
            return Player.CHOICE_MAGIC_PLAYER
        else:
            return Player.CHOICE_MAGIC_DECK

    def choose_player(self, player_numbers):
        print_lines('{0}: Player {0}', [(num,) for num in player_numbers])
        print 'X: Cancel'
        
        choice = raw_input('Choose one of the listed players: ')

        if choice == 'X':
            return Player.CHOICE_CANCEL
        else:
            return int(choice)

    def choose_cards_in_hand(self):
        choices = list()
        for card in self.hand:
            choice = raw_input('Discard card {}? (Y/N): '.format(card.name))
            if choice == 'Y':
                choices.append(True)
            else:
                choices.append(False)
        return choices

    def choose_use_extra_power(self, name):
        choice = raw_input(
            'Do you want to use {} power? (Y/N): '.format(name))

        return choice == 'Y'

    def update_board(self, players, current_player, starting_player):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        
        # Print board
        for player in players:
            city_info = ' '.join(
                ['{}{}{}{}'.format(ansi_colors[card.color], card.short_name,
                                   card.cost, Fore.RESET)
                 for card in player.city])

            if player == starting_player:
                sp_str = '*'
            else:
                sp_str = ' '

            player_info = '{}{}: G-{:2} C-{:2} '.format(
                sp_str, player.num, player.gold, len(player.hand))
            print player_info + city_info
        print '-'*79

        # Print own info
        if self.role:
            role_name = self.role.name
        else:
            role_name = 'None'
        print 'Role: {:24}Gold: {}'.format(role_name, self.gold)
        print 'Hand: ' + format_districts(self.hand)
        print 'City: ' + format_districts(self.city)
        print '-'*79

        # Print current player info
        if current_player:
            print 'Current player: {}             Role: {}'.format(
                current_player.num, current_player.role.name)

    def send_message(self, message):
        print message
        raw_input()
