class Debugger(object):
    def __init__(self, game):
        self.game = game

    def give_districts_hand(self, player, district_names):
        for district_name in district_names:
            for district in self.game.districts.districts:
                if district.name == district_name:
                    self.game.districts.districts.remove(district)
                    player.add_to_hand(district)
                    break

    def give_districts_city(self, player, district_names):
        for district_name in district_names:
            for district in self.game.districts.districts:
                if district.name == district_name:
                    self.game.districts.districts.remove(district)
                    self.game.play_district(player, district)
                    break
