import enum

from dlgo.agent.base import Agent

class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3

class MinimaxAgent(Agent):
    def select_move(self, game_state):
        pass

    def best_result(self, game_state):
        if game_state.is_over():
            if game_state.winner() == game_state.next_player.opposite():
                return GameResult.win
            if game_state.winner() is None:
                return GameResult.draw
            return GameResult.loss
        best_result_so_far = GameResult.loss
        for candidate_move in game_state.legal_moves():
            next_state = game_state.apply_move(candidate_move)
            if next_state.winner() is not None:
                return GameResult.win
            opponent_best_result = best_result(next_state)
            our_result = reverse_game_result(opponent_best_result)
            if our_result.value > best_result_so_far.value:
                best_result_so_far = our_result
        return best_result_so_far
