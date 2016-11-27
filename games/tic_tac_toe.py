"""
Full code for running a game of tic-tac-toe on a 3 by 3 board.
"""
import itertools
import random

from common.base_game_spec import BaseGameSpec
from techniques.min_max import evaluate


def _new_board():
    """Return a emprty tic-tac-toe board we can use for simulating a game.

    Returns:
        3x3 tuple of ints
    """
    return ((0, 0, 0),
            (0, 0, 0),
            (0, 0, 0))


def apply_move(board_state, move, side):
    """Returns a copy of the given board_state with the desired move applied.

    Args:
        board_state (3x3 tuple of int): The given board_state we want to apply the move to.
        move (int, int): The position we want to make the move in.
        side (int): The side we are making this move for, 1 for the first player, -1 for the second player.

    Returns:
        (3x3 tuple of int): A copy of the board_state with the given move applied for the given side.
    """
    move_x, move_y = move

    def get_tuples():
        for x in range(3):
            if move_x == x:
                temp = list(board_state[x])
                temp[move_y] = side
                yield tuple(temp)
            else:
                yield board_state[x]

    return tuple(get_tuples())


def available_moves(board_state):
    """Get all legal moves for the current board_state. For Tic-tac-toe that is all positions that do not currently have
    pieces played.

    Args:
        board_state: The board_state we want to check for valid moves.

    Returns:
        Generator of (int, int): All the valid moves that can be played in this position.
    """
    for x, y in itertools.product(range(3), range(3)):
        if board_state[x][y] == 0:
            yield (x, y)


def _has_3_in_a_line(line):
    return all(x == -1 for x in line) | all(x == 1 for x in line)


def has_winner(board_state):
    """Determine if a player has won on the given board_state.

    Args:
        board_state (3x3 tuple of int): The current board_state we want to evaluate.

    Returns:
        int: 1 if player one has won, -1 if player 2 has won, otherwise 0.
    """
    # check rows
    for x in range(3):
        if _has_3_in_a_line(board_state[x]):
            return board_state[x][0]
    # check columns
    for y in range(3):
        if _has_3_in_a_line([i[y] for i in board_state]):
            return board_state[0][y]

    # check diagonals
    if _has_3_in_a_line([board_state[i][i] for i in range(3)]):
        return board_state[0][0]
    if _has_3_in_a_line([board_state[2 - i][i] for i in range(3)]):
        return board_state[0][2]

    return 0  # no one has won, return 0 for a draw


def play_game(plus_player_func, minus_player_func, log=False):
    """Run a single game of tic-tac-toe until the end, using the provided function args to determine the moves for each
    player.

    Args:
        plus_player_func ((board_state(3 by 3 tuple of int), side(int)) -> move((int, int))): Function that takes the
            current board_state and side this player is playing, and returns the move the player wants to play.
        minus_player_func ((board_state(3 by 3 tuple of int), side(int)) -> move((int, int))): Function that takes the
            current board_state and side this player is playing, and returns the move the player wants to play.
        log (bool): If True progress is logged to console, defaults to False

    Returns:
        int: 1 if the plus_player_func won, -1 if the minus_player_func won and 0 for a draw
    """
    board_state = _new_board()
    player_turn = 1

    while True:
        _available_moves = list(available_moves(board_state))

        if len(_available_moves) == 0:
            # draw
            if log:
                print("no moves left, game ended a draw")
            return 0.
        if player_turn > 0:
            move = plus_player_func(board_state, 1)
        else:
            move = minus_player_func(board_state, -1)

        if move not in _available_moves:
            # if a player makes an invalid move the other player wins
            if log:
                print("illegal move ", move)
            return -player_turn

        board_state = apply_move(board_state, move, player_turn)
        if log:
            print(board_state)

        winner = has_winner(board_state)
        if winner != 0:
            if log:
                print("we have a winner, side: %s" % player_turn)
            return winner
        player_turn = -player_turn


def random_player(board_state, _):
    """A player func that can be used in the play_game method. Given a board state it chooses a move randomly from the
    valid moves in the current state.

    Args:
        board_state (3x3 tuple of int): The current state of the board
        _: the side this player is playing, not used in this function because we are simply choosing the moves randomly

    Returns:
        (int, int): the move we want to play on the current board
    """
    moves = list(available_moves(board_state))
    return random.choice(moves)


class TicTacToeGameSpec(BaseGameSpec):
    def __init__(self):
        self.available_moves = available_moves
        self.has_winner = has_winner
        self.new_board = _new_board
        self.apply_move = apply_move
        self.evaluate = evaluate

    def board_dimensions(self):
        return 3, 3


if __name__ == '__main__':
    # example of playing a game
    play_game(random_player, random_player, log=True)
