
class Player:
    VERSION = "vakvarju brutal player"

    def betRequest(self, game_state):
        call = game_state['current_buy_in'] - game_state['players'][game_state['in_action']]['bet']
        extra = max(game_state['pot'] / 2, game_state['minimum_raise'])
        return call + extra

    def showdown(self, game_state):
        pass

