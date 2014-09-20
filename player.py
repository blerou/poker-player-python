import random

class Player:
    VERSION = "vakvarju brutal player v14"

    def betRequest(self, game_state):
        my = game_state['players'][game_state['in_action']]
        pot = game_state['pot']

        call = game_state['current_buy_in'] - my['bet']
        extra = game_state['minimum_raise']

        ranks = dict()
        suits = dict()
        cards = game_state['community_cards'] + my['hole_cards']
        for card in cards:
            if card['rank'] in ranks:
                ranks[card['rank']].append(card['suit'])
            else:
                ranks[card['rank']] = [card['suit']]
            if card['suit'] in suits:
                suits[card['suit']].append(card['rank'])
            else:
                suits[card['suit']] = [card['rank']]

        r = random.randint(0, 99)

        if self.has_straight(ranks) or self.has_set(ranks) or self.has_pair(ranks):
            return call + extra
        elif pot > 200 and call > (pot / 3):
            if r < 10:
                return call
            else:
                return 0
        else:
            if r < 10:
                return 0
            elif r < 70:
                return call + extra
            else:
                return call

    def has_straight(self, ranks):
        x = sorted(ranks.keys())
        return len(x) >= 5 and (x[0] == x[4] or x[1] == x[5] or x[2] == x[6])

    def has_set(self, ranks):
        for s in ranks:
            if len(s) == 3:
                return True
        return False

    def has_pair(self, ranks):
        for s in ranks:
            if len(s) == 2:
                return True
        return False

    def showdown(self, game_state):
        pass


def test_bet():
    gs = {
        'pot': 0,
        'in_action': 0,
        'current_buy_in': 100,
        'minimum_raise': 10,
        'players': [
            {
            'bet': 10,
                'hole_cards': [
                    {
                        'rank': 'a',
                        'suit': 'x'
                    },
                    {
                        'rank': 'b',
                        'suit': 'y'
                    }
                ]
            }
        ],
        'community_cards': [
                {
                    'rank': 'a',
                    'suit': 'x'
                },
                {
                    'rank': 'b',
                    'suit': 'y'
                }
        ]
    }

    assert 0 == Player().betRequest(gs)