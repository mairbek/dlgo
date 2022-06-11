#!/usr/bin/env python3

import copy

board = [[None for i in range(3)] for j in range(3)]

def check_player(board, player):
    for i in range(3):
        win = True
        for j in range(3):
            if board[i][j] != player:
                win = False
                break
        if win:
            return True
    for i in range(3):
        win = True
        for j in range(3):
            if board[j][i] != player:
                win = False
                break
        if win:
            return True
    win = True
    for i in range(3):
        if board[i][i] != player:
            win = False
            break
    if win:
        return True
    win = True
    for i in range(3):
        if board[i][2 - i] != player:
            win = False
            break
    return win


def check_draw(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                return False
    return True

def is_over(board):
    return check_player(board, 'x') or check_player(board, 'o') or check_draw(board)

def other(player):
    if player == 'x':
        return 'o'
    return 'x'

def hash_of(board):
    result = ''
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                result += '.'
            else:
                result += board[i][j]
    return result

def compute_all_games(board, player, visited):
    board_hash = hash_of(board)
    if board_hash in visited:
        return visited[board_hash]
    if is_over(board):
        visited[board_hash] = 1
        return 1
    acc = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                new_board = copy.deepcopy(board)
                new_board[i][j] = player
                acc += compute_all_games(new_board, other(player), visited)
    visited[board_hash] = acc
    return acc

print(compute_all_games(board, 'x', {}))
