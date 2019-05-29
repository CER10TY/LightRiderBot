import random
import sys


class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            chosen = "pass"
            for x, y in legal:
                a = x

            self.game.issue_order(chosen)
