import random
import sys
import math
import copy


class Bot:

    def __init__(self):
        self.game = None
        self.max_depth = 2

    def setup(self, game):
        self.game = game

    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            best_val = float('-inf')
            best_move = 'pass'
            for (_, chosen) in legal:
                val = self.minimax(0, False)
                if val > best_val:
                    best_val = val
                    best_move = chosen
            self.game.issue_order(best_move)

    def minimax(self, depth, maxim):
        score = self.evaluate()
        if depth == self.max_depth:
            return score
        if score >= 10:
            return score
        if score <= -10:
            return score

        if maxim:
            best = float('-inf')
            for (_, move) in self.game.field.legal_moves(self.game.my_botid, self.game.players):
                best = max(best, self.minimax(depth + 1, not maxim))
            return best
        else:
            best = float('inf')
            for (_, move) in self.game.field.legal_moves(self.game.other_botid, self.game.players):
                best = min(best, self.minimax(depth + 1, not maxim))
            return best

    def evaluate(self):
        me = self.game.players[self.game.my_botid]
        enemy = self.game.players[self.game.other_botid]
        my_adjacent = self.game.field.get_adjacent(me.row, me.col)
        other_adjacent = self.game.field.get_adjacent(enemy.row, enemy.col)
        score = 0

        for (row, col) in my_adjacent:
            self.simulate_move(row, col, self.game.my_botid)
            legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
            score += len(legal) * 5
            self.undo_move(row, col, self.game.my_botid)

        for (row, col) in other_adjacent:
            self.simulate_move(row, col, self.game.other_botid)
            legal = self.game.field.legal_moves(self.game.other_botid, self.game.players)
            score -= len(legal) * 5
            self.undo_move(row, col, self.game.other_botid)

        return score

    def simulate_move(self, row, col, player_id):
        self.game.field.parse_cell(players=self.game.players, row=self.game.players[player_id].row - row,
                                   col=self.game.players[player_id].col - col,
                                   data=['x'])
        self.game.field.parse_cell(players=self.game.players, row=row, col=col, data=[str(player_id)])

    def undo_move(self, row, col, player_id):
        self.game.field.parse_cell(players=self.game.players, row=self.game.players[player_id].row - row,
                                   col=self.game.players[player_id].col - col,
                                   data=[str(player_id)])
        self.game.field.parse_cell(players=self.game.players, row=row, col=col, data=['.'])

