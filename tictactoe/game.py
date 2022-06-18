from collections import namedtuple

import copy
import enum

class Player(enum.Enum):
    x = 1
    o = 2

    def opposite(self):
        if self == Player.x:
            return Player.o
        return Player.x

class Point(namedtuple('Point', 'row col')):
    pass

def check_winner(i, j, board, size, player):
    win = True
    for jj in range(size):
        if board[i][jj] != player:
            win = False
            break
    if win:
        return True
    win = True
    for ii in range(size):
        if board[ii][j] != player:
            win = False
            break
    if win:
        return True
    win = True
    for ii in range(size):
        if board[ii][ii] != player:
            win = False
            break
    if win:
        return True
    win = True
    for ii in range(size):
        if board[ii][size - 1 - ii] != player:
            win = False
            break
    return win

class GameState():
    def __init__(self, size = 3, board = None, player = Player.x, winner = None):
        self.size = 3
        if board is None:
            board = [[None for i in range(size)] for j in range(size)]
        self.board = board
        self.next_player = player
        self._winner = winner

    def apply_move(self, move):
        i = move.row - 1
        j = move.col - 1
        assert self.board[i][j] is None

        player = self.next_player
        board = copy.deepcopy(self.board)
        board[i][j] = player
        winner = None
        if check_winner(i, j, board, self.size, player):
            winner = player
        return GameState(size = self.size, board = board, player = player.opposite(), winner=winner)

    def winner(self):
        return self._winner

    def is_over(self):
        if self._winner is not None:
            return True
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None:
                    count += 1
        return count == 0

    def legal_moves(self):
        result = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None:
                    result.append(Point(row=i+1, col=j+1))
        return result
