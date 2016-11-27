import sys

def evaluate(board_state):
    """Get a rough score for how good we think this board position is for the plus_player. Does this based on number of
    2 in row lines we have.

    Args:
        board_state (3x3 tuple of int): The board state we are evaluating

    Returns:
        int: evaluated score for the position for the plus player, posative is good for the plus player, negative good
            for the minus player
    """
    score = 0
    for x in range(len(board_state)):
        score += _score_line(board_state[x])
    for y in range(len(board_state[0])):
        score += _score_line([i[y] for i in board_state])

    # diagonals
    score += _score_line([board_state[i][i] for i in range(3)])
    score += _score_line([board_state[2 - i][i] for i in range(3)])

    return score
