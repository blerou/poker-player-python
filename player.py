import random

converter={'J':11,'Q':12,'K':13,'A':14}

def rankValue(rank):
    if rank.isdigit():
        return int(rank)
    elif rank in converter.keys():
        return converter[rank]

def ranks_suites(cards):
    ranks = dict()
    suits = dict()
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
    return ranks, suits



class Player:
    VERSION = "vakvarju brutal player v21"

    def betRequest(self, game_state):
        my = game_state['players'][game_state['in_action']]
        pot = game_state['pot']

        call = game_state['current_buy_in'] - my['bet']
        extra = game_state['minimum_raise'] * random.randint(1, 3)

        comm_cards = game_state['community_cards']
        cards = comm_cards + my['hole_cards']

        ranks, suits = ranks_suites(cards)

        print "ranks", ranks
        print "suits", suits

        if self.has_straight(ranks) or self.has_poker(ranks) or self.has_set(ranks):
            return call + my['stack']


        r = random.randint(0, 99)

        pairs = self.pairs(ranks)

        if pairs and len(pairs) == 2:
            return call + extra

        my_ranks, _ = ranks_suites(my['hole_cards'])

        if self.pairs(my_ranks):
            if pairs[0] < 10:
                if r < 20:
                    return call
                else:
                    return 0
            else:
                return call + extra

        if pot > 200 and call > (pot / 3):
            if r < 10:
                return call
            else:
                return 0

        if r < 10:
            return 0
        elif r < 50:
            return call + extra
        else:
            return call


    def has_straight(self, ranks):
        x = sorted(ranks.keys())
        if len(x) < 5:
            return None
        if len(x) >= 5 and x[0] + 4 == x[4]:
            return x[4]
        if len(x) >= 6 and x[1] + 4 == x[5]:
            return x[5]
        if len(x) == 7 and x[2] + 4 == x[6]:
            return x[6]
        return None

    def has_poker(self, ranks):
        for r, s in ranks.iteritems():
            if len(s) == 4:
                return True
        return False

    def has_set(self, ranks):
        for r, s in ranks.iteritems():
            if len(s) == 3:
                return r
        return None

    def pairs(self, ranks):
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
                        'rank': 'A',
                        'suit': 'x'
                    },
                    {
                        'rank': '4',
                        'suit': 'y'
                    }
                ]
            }
        ],
        'community_cards': [
                {
                    'rank': 'A',
                    'suit': 'x'
                },
                {
                    'rank': '6',
                    'suit': 'y'
                }
        ]
    }

    assert 0 == Player().betRequest(gs)
