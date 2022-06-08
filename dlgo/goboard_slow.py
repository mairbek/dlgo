import copy

from dlgo.gotypes import Player

class Move():
    def __init__(self, point=None, is_pass=False, is_resignation=False):
        assert (point is not None) ^ is_pass ^ is_resignation
        self.point = point
        self.is_pass = is_pass
        self.is_resignation = is_resignation

    @classmethod
    def play(cls, point):
        return Move(point)

    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        return Move(is_resignation=True)

    @property
    def is_play(self):
        return not self.is_pass and not self.is_resignation

class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self, go_string):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones
        )

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties


class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

    def is_on_grid(self, point):
        return point.row >= 1 and point.row <= self.num_rows and \
            point.col >= 1 and point.col <= self.num_cols

    # returns the string given the point or None.
    def get_go_string(self, point):
        return self._grid.get(point)

    # returns the content(color) of the point
    def get(self, point):
        go_string = self.get_go_string(point)
        if go_string is None:
            return None
        return go_string.color

    def place_stone(self, player, point):
        assert self.is_on_grid(point)
        assert self.get_go_string(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self.get_go_string(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = GoString(player, [point], liberties)
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        for stone in new_string.stones:
            self._grid[stone] = new_string
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)

    def _remove_string(self, go_string):
        for point in go_string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string == go_string:
                    continue
                neighbor_string.add_liberty(point)
            self._grid[point] = None


class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board= board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    def apply_move(self, move):
        next_board = self.board
        if move.is_play:
            # check if it is an empty point
            assert self.board.get(move.point) is None
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        return GameState(next_board, self.next_player.other, self, move)

    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resignation:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return second_last_move.is_pass and self.last_move.is_pass

    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        board = copy.deepcopy(self.board)
        board.place_stone(player, move.point)
        go_string = board.get_go_string(move.point)
        return go_string.num_liberties == 0

    @property
    def situation(self):
        return (self.next_player, self.board)

    def does_move_violate_ko(self, player, move):
        if not move.is_play:
            return False
        board = copy.deepcopy(self.board)
        board.place_stone(player, move.point)
        next_situation = (player, board)
        past_state = self.previous_state
        while past_state != None:
            if next_situation == past_state.situation:
                return True
            past_state = past_state.previous_state
        return False

    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resignation:
            return True
        return (
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move)
        )

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)
