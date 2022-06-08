import random

from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.goboard_slow import Move
from dlgo.gotypes import Point

class RandomBot(Agent):
    def select_move(self, game_state):
        """Choose a random valid move that preserves our own eyes."""
        last_move = game_state.last_move
        if last_move and last_move.is_pass:
            return Move.pass_turn()
        candidates = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                if not game_state.is_valid_move(Move.play(candidate)) or \
                   is_point_an_eye(game_state.board, candidate, game_state.next_player):
                    continue
                candidates.append(candidate)
        if not candidates:
            print('No canidates')
            return Move.pass_turn()
        return Move.play(random.choice(candidates))
