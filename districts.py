import random

class Colors:
    Green = 'Green'
    Blue = 'Blue'
    Red = 'Red'
    Yellow = 'Yellow'
    Purple = 'Purple'   

class District(object):
    def __init__(self, color, name, short_name, cost, power=None):
        self.name = name
        self.short_name = short_name
        self.cost = cost
        self.color = color
        self.power = power

    def __repr__(self):
        return '({}, {})'.format(self.name, self.cost)


class DistrictDeck(object):
    GREEN_DISTRICTS = [(5, 'Tavern', 'Tvrn', 1),
                       (4, 'Market', 'Mrkt', 2),
                       (3, 'Trading Post', 'TPst', 2),
                       (3, 'Docks', 'Dcks', 3),
                       (3, 'Harbor', 'Hrbr', 4),
                       (2, 'Town Hall', 'TwnH', 5)]

    BLUE_DISITRICTS = [(3, 'Temple', 'Tmpl', 1),
                       (3, 'Monastery', 'Mtry', 3),
                       (2, 'Cathedral', 'Ctdl', 5)]

    RED_DISTRICTS = [(3, 'Watchtower', 'Wtwr', 1),
                     (3, 'Prison', 'Prsn', 2),
                     (3, 'Battlefield', 'Btfd', 3),
                     (2, 'Fortress', 'Ftrs', 5)]

    YELLOW_DISTRICTS = [(5, 'Manor', 'Mnr ', 3),
                        (4, 'Castle', 'Cstl', 4),
                        (3, 'Palace', 'Plce', 5)]

    PURPLE_DISTRICTS = [(1, 'Haunted City', 'HnCt', 2),
                        (2, 'Keep', 'Keep', 3),
                        (1, 'Laboratory', 'Lab ', 5),
                        (1, 'Smith', 'Smth', 5),
                        (1, 'Observatory', 'Obty', 5),
                        (1, 'Graveyard', 'Gvyd', 5),
                        (1, 'Dragon Gate', 'DrGt', 6),
                        (1, 'University', 'Uni ', 6),
                        (1, 'Library', 'Lbry', 6),
                        (1, 'Great Wall', 'GtWl', 6),
                        (1, 'School of Magic', 'SchM', 6)]

    def __init__(self):
        self.districts = list()

        district_data = [(self.GREEN_DISTRICTS, Colors.Green),
                         (self.BLUE_DISITRICTS, Colors.Blue),
                         (self.RED_DISTRICTS, Colors.Red),
                         (self.YELLOW_DISTRICTS, Colors.Yellow),
                         (self.PURPLE_DISTRICTS, Colors.Purple)]
        for district_data, color in district_data:
            self.districts.extend(
                self.make_districts(district_data, color))

        random.shuffle(self.districts)

    def make_districts(self, district_data, color):
        districts = list()
        for data in district_data:
            for _ in range(data[0]):
                districts.append(District(color, *(data[1:])))
        return districts

    def draw(self, num):
        cards = self.districts[:num]
        self.districts = self.districts[num:]
        return cards

    def put_on_bottom(self, cards):
        self.districts.extend(cards)
