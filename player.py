
class Player:
    VERSION = "vakvarju brutal player"

    def betRequest(self, game_state):
        x = game_state['current_buy_in'] - game_state['players'][game_state['in_action']]['bet']
        return game_state['pot'] / 2 + x

    def showdown(self, game_state):
        pass

