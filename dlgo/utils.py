from dlgo import gotypes

COLS = 'ABCDEFGHIJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' . ',
    gotypes.Player.white: ' x ',
    gotypes.Player.black: ' o ',
}

def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resignation:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col -1], move.point.row)
    print('%s %s' % (player, move_str))

def point_from_coords(coords):
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)

def print_board(board):
    for row in range(board.num_rows, 0, -1):
        bump = ' ' if row <= 9 else ''
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print('%s%d %s' % (bump, row, ''.join(line)))
    print('     ' + '  '.join(COLS[:board.num_cols]))
