from player import Player
from districts import Colors

def assassin_power(player, game):
    targetable_roles = list()
    for role in game.available_roles:
        if role.num != 1:
            targetable_roles.append(role)
    choice = player.choose_a_role(targetable_roles)
    if choice == Player.CHOICE_CANCEL:
        return False
    game.send_message('Assassin has targeted {}', choice)
    game.assassinated_role = choice
    return True

def thief_power(player, game):
    targetable_roles = list()
    for role in game.available_roles:
        if role.num > 2 and role != game.assassinated_role:
            targetable_roles.append(role)
    choice = player.choose_a_role(targetable_roles)
    if choice == Player.CHOICE_CANCEL:
        return False
    game.send_message('Thief has targeted {}', choice.name)
    game.thieved_role = choice
    return True

def magician_power(player, game):
    choice = player.choose_magician_action()
    if choice == Player.CHOICE_MAGIC_PLAYER:
        targetable_players = [target_player.num for target_player
                              in game.players if player != target_player]
        choice = player.choose_player(targetable_players)
        for target_player in game.players:
            if target_player.num == choice:
                game.send_message(
                    'Magician swapping cards with player {}', target_player)
                temp_hand = target_player.hand
                target_player.hand = player.hand
                player.hand = temp_hand
                return True
        return False 
    elif choice == Player.CHOICE_MAGIC_DECK:
        choice = player.choose_cards_in_hand()
        num_cards = sum([1 for i in choice if i])
        game.send_message(
            'Magician swapping {} cards with deck'.format(num_cards))
        if choice == Player.CHOICE_CANCEL:
            return False
        removed_cards = list()
        kept_cards = list()
        for i in range(len(player.hand)):
            if choice[i]:
                removed_cards.append(player.hand[i])
            else:
                kept_cards.append(player.hand[i])
        player.hand = kept_cards
        new_cards = game.districts.draw(len(removed_cards))
        for card in new_cards:
            player.add_to_hand(card)
        game.districts.put_on_bottom(removed_cards)
        return True
    else:
        return False

def gold_for_colored_district_power(color):
    def power(player, game):
        game.send_message('Gaining 1 gold for each {} district'.format(color))
        matching_districts = [district for district in player.city
                              if (district.color == color or
                                  district.name == 'School of Magic')]
        player.gold += len(matching_districts)
        return True
    return power

def warlord_targets(player, target_player):
    targetable_districts = list()
    has_great_wall = target_player.has_district('Great Wall')
    for district in target_player.city:
        cost = district.cost - 1
        if has_great_wall and district.name != 'Great Wall':
            cost += 1
        if (cost <= player.gold and district.name != 'Keep'):
            targetable_districts.append(district)
    return targetable_districts

def warlord_extra_power(player, game):
    if player.choose_binary('Pay gold to destroy a district'):
        targetable_players = list()
        for target_player in game.players:
            if (target_player.role.name != 'Bishop' and
                warlord_targets(player, target_player) and
                not target_player.finished_city()):
                targetable_players.append(target_player.num)
        choice = player.choose_player(targetable_players)
        for target_player in game.players:
            if target_player.num == choice:
                game.send_message('Warlord has targeted {}', target_player)
                targetable_districts = warlord_targets(player, target_player)
                choice = player.choose_district(targetable_districts)
                if choice == Player.CHOICE_CANCEL:
                    return False

                cost = choice.cost - 1
                if target_player.has_district('Great Wall'):
                    cost += 1
                player.gold -= cost

                target_player.remove_from_city(choice)
                game.send_message('Warlord has destroyed {}', choice)

                for other_player in game.players:
                    if (other_player.has_district('Graveyard') and
                        other_player != player):
                        if other_player.gold >= 1:
                            choice = other_player.choose_binary(
                                'Pay 1 gold to put {} in your hand', choice)
                            if choice:
                                other_player.gold -= 1
                                other_player.add_to_hand(choice)
                                game.send_message('{} has recovered {}',
                                    other_player, choice)
                                return True
                return True
        return False
    else:
        return True

class Role(object):
    def __init__(self, name, num, power=None):
        self.name = name
        self.num = num
        self.power = power

    def __repr__(self):
        return '({}, {})'.format(self.name, self.num)

role_data = [('Assassin' , 1, assassin_power),
             ('Thief', 2, thief_power),
             ('Magician', 3, magician_power),
             ('King', 4, gold_for_colored_district_power(Colors.Yellow)),
             ('Bishop', 5, gold_for_colored_district_power(Colors.Blue)),
             ('Merchant', 6, gold_for_colored_district_power(Colors.Green)),
             ('Architect', 7),
             ('Warlord', 8, gold_for_colored_district_power(Colors.Red))]

ROLES = [Role(*data) for data in role_data]
