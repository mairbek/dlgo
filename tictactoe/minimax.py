from dlgo.agent.base import Agent

class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3

class MinimaxAgent(Agent):
    def select_move(self, game_state):
        best_result_so_far =  GameResult.loss
        for candidate_move in game_state.legal_moves():
            next_state = game_state.apply_move(candidate_move)
            opponent_best_outcome = best_result(next_state)

    def best_result(self, game_state):
