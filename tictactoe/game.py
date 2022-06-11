from collections import namedtuple

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

class GameState():
    def __init__(self, size = 3):
        self.size = 3
        self.board = [[None for i in range(size)] for j in range(size)]
        self.next_player = Player.x
        self.winner = None

    def apply_move(self, move):
        i = move.row - 1
        j = move.col - 1
        assert self.board[i][j] is None
        player = self.next_player
        self.next_player = player.opposite()
        self.board[i][j] = player
        # check row
        win = True
        for jj in range(self.size):
            if self.board[i][jj] != player:
                win = False
                break
        if win:
            self.winner = player
            return
        win = True
        for ii in range(self.size):
            if self.board[ii][j] != player:
                win = False
                break
        if win:
            self.winner = player
            return
        win = True
        for ii in range(self.size):
            if self.board[ii][ii] != player:
                win = False
                break
        if win:
            self.winner = player
            return
        win = True
        for ii in range(self.size):
            if self.board[ii][self.size - 1 - ii] != player:
                win = False
                break
        if win:
            self.winner = player
            return

    def winner(self):
        return self.winner


    def legal_moves(self):
        result = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None:
                    result.append(Point(row=i+1, col=j+1))
