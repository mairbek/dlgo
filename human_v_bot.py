#!/usr/bin/env python3

from dlgo import agent
from dlgo.agent import naive
from dlgo import gotypes
from dlgo import goboard_slow as goboard

from dlgo.utils import print_board, print_move, point_from_coords

import time

def main():
    board_size = 5
    game = goboard.GameState.new_game(board_size)
    bot = agent.naive.RandomBot()

    while not game.is_over():
        time.sleep(1)
        print(chr(27) + '[2J')
        print_board(game.board)
        if game.next_player == gotypes.Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move)
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)

if __name__ == '__main__':
    main()
