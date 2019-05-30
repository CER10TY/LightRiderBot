import random
import sys
import math
import copy


class Bot:

    def __init__(self):
        self.game = None
        self.max_depth = 1

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
                val = self.minimax(0, False, float('-inf'), float('inf'))
                sys.stderr.write("DEBUG INFO: %d" % val)
                if val > best_val:
                    best_val = val
                    best_move = chosen
            if best_move == 'pass':
                self.game.issue_order_pass()
            else:
                self.game.issue_order(best_move)

    def minimax(self, depth, maxim, alpha, beta):
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
                best = max(best, self.minimax(depth + 1, not maxim, alpha, beta))
                alpha = max(alpha, best)

                if beta <= alpha:
                    break
            return best
        else:
            best = float('inf')
            for (_, move) in self.game.field.legal_moves(self.game.other_botid, self.game.players):
                best = min(best, self.minimax(depth + 1, not maxim, alpha, beta))
                beta = min(beta, best)

                if beta <= alpha:
                    break
            return best

    def evaluate(self):
        my_legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        other_legal = self.game.field.legal_moves(self.game.other_botid, self.game.players)
        score = 0

        for (row, col), order in my_legal:
            sys.stderr.write("DEBUG INFO, my row: %s" % str(row))
            self.simulate_move(row, col, self.game.my_botid)
            legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
            score += len(legal) * 5
            self.undo_move(row, col, self.game.my_botid)

        for (row, col), order in other_legal:
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

