#!/usr/bin/env python3
import random
from dlgo.gotypes import Player, Point

def to_python(player):
    if player is None:
        return 'None'
    elif player == Player.black:
        return 'Player.black'
    return 'Player.white'

MAX_63 = 0xffffffffffffffff

table = {}
empty_board = 0
for row in range(1, 20):
    for col in range (1, 20):
        for state in (Player.black, Player.white):
            code = random.randint(0, MAX_63)
            table[Point(row, col), state] = code

print('from .gotypes import Player, Point')
print('')
print('__all__ = [\'HASH_CODE\', \'EMPTY_BOARD\']')
print('')
print('HASH_CODE={')
for (pt, state), hash_code in table.items():
    print('    (%r, %s): %r,' % (pt, to_python(state), hash_code))
print('}')
