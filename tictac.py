#!/usr/bin/env python3

from tictactoe import minimax
from tictactoe import game

def print_board(game_state):
    n = game_state.size
    for i in range(n):
        row = ''
        for j in range(n):
            val = game_state.board[i][j]
            if val == game.Player.x:
                row += 'x'
            elif val == game.Player.o:
                row += 'o'
            else:
                row += '.'
            if j < (n-1):
                row += ' '
        print(row)
    if game_state.winner is not None:
        print("Winner %s" % game_state.winner)

bots = {
    'x': minimax.MinimaxAgent(),
    'o': minimax.MinimaxAgent(),
}

print('Go')

game_state = game.GameState()

game_state = game_state.apply_move(game.Point(col=2, row=2))
game_state = game_state.apply_move(game.Point(col=3, row=2))
game_state = game_state.apply_move(game.Point(col=3, row=1))
game_state = game_state.apply_move(game.Point(col=3, row=3))
game_state = game_state.apply_move(game.Point(col=1, row=3))

print_board(game_state)
