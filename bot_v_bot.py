#!/usr/bin/env python3

from dlgo import agent
from dlgo.agent import naive
from dlgo import gotypes
from dlgo import goboard_slow as goboard

from dlgo.utils import print_board, print_move

import time

def main():
    board_size = 5
    game = goboard.GameState.new_game(board_size)
    bots = {
       gotypes.Player.black: agent.naive.RandomBot(),
       gotypes.Player.white: agent.naive.RandomBot(),
    }
    while not game.is_over():
        time.sleep(1)
        print(chr(27) + '[2J')
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)

if __name__ == '__main__':
    main()
