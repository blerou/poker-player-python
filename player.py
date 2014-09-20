import random

converter={'J':11,'Q':12,'K':13,'A':14}

def rankValue(rank):
	if rank.isdigit():
		return int(rank)
	elif rank in converter.keys():
		return converter[rank]

class Player:
    VERSION = "vakvarju brutal player v16"

    def betRequest(self, game_state):
        my = game_state['players'][game_state['in_action']]
        pot = game_state['pot']

        call = game_state['current_buy_in'] - my['bet']
        extra = game_state['minimum_raise']

        ranks = dict()
        suits = dict()
        cards = game_state['community_cards'] + my['hole_cards']
		
        for card in cards:
            rank=rankValue(card['rank'])
            if rank in ranks:
                ranks[rank].append(card['suit'])
            else:
                ranks[rank] = [card['suit']]
            if card['suit'] in suits:
                suits[card['suit']].append(rank)
            else:
                suits[card['suit']] = [rank]

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
        if len(x) >= 5 and x[0] == x[4]:
            return x[4]
        if len(x) >= 6 and x[1] == x[5]:
            return x[5]
        if len(x) == 7 and x[2] == x[6]:
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
