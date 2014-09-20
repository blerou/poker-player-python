import random

class Player:
    VERSION = "vakvarju brutal player v15"

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

        print "ranks", ranks
        print "suits", suits

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
        if len(x) < 5:
            return None
        if x[0] == x[4]:
            return x[4]
        if x[1] == x[5]:
            return x[5]
        if x[2] == x[6]:
            return x[6]
        return None

    def has_set(self, ranks):
        for r, s in ranks.iteritems():
            if len(s) == 3:
                return r
        return None

    def has_pair(self, ranks):
        ps = []
        for r, s in ranks.iteritems():
            if len(s) == 2:
                ps.append(r)
        return ps

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