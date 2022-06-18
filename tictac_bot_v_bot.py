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
        print("Winner %s" % game_state.winner())

bots = {
    game.Player.x: minimax.MinimaxAgent(),
    game.Player.o: minimax.MinimaxAgent(),
}

print('Go')

game_state = game.GameState()

print_board(game_state)

player = game.Player.x
while True:
    if game_state.is_over():
        print('Over')
        break
    bot = bots[player]
    move = bot.select_move(game_state)
    game_state = game_state.apply_move(move)
    print_board(game_state)
    player = player.opposite()
