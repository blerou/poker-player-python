
class Player:
    VERSION = "vakvarju brutal player v3"

    def betRequest(self, game_state):
        my = game_state['players'][game_state['in_action']]

        call = game_state['current_buy_in'] - my['bet']
        extra = max(game_state['pot'] / 2, game_state['minimum_raise'])

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

        # assert [] == suits

        if len(cards) == 7:
            if self.has_pair(ranks):
                return call + extra
            else:
                return 0
        else:
            if self.has_pair(ranks):
                return call + extra
            else:
                return call


    def has_pair(self, ranks):
        for s in ranks:
            if len(s) >= 2:
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

    assert 0 < Player().betRequest(gs)