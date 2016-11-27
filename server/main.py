from flask import Flask, render_template, request
from game import *
from math import sqrt

app = Flask(__name__)

def _has_winning_line(line, winning_length):
    count = 0
    last_side = 0
    for x in line:
        if x == last_side:
            count += 1
            if count == winning_length:
                return last_side
        else:
            count = 1
            last_side = x
    return 0





def has_winner(board_state, winning_length):


    board_width = len(board_state)
    board_height = len(board_state[0])
    # check rows

    for x in range(board_width):
        winner = _has_winning_line(board_state[x], winning_length)
        if winner != 0:
            return winner

    # check columns
    for y in range(board_height):
        winner = _has_winning_line((i[y] for i in board_state), winning_length)
        if winner != 0:
            return winner

    # check diagonals
    diagonals_start = -(board_width - winning_length)
    diagonals_end = (board_width - winning_length)
    for d in range(diagonals_start, diagonals_end + 1):
        winner = _has_winning_line(
            (board_state[i][i + d] for i in range(max(-d, 0), min(board_width, board_height - d))),
            winning_length)
        if winner != 0:
            return winner

    for d in range(diagonals_start, diagonals_end + 1):
        winner = _has_winning_line(
            (board_state[i][board_height - i - d - 1] for i in range(max(-d, 0), min(board_width, board_height - d))),
            winning_length)
        if winner != 0:
            return winner
    return 0  # no one has won, return 0 for a draw

@app.route('/')
def index():
	return render_template('index7x7.html')


@app.route('/sendNetworkData', methods=['POST'])
def sendNetworkData():
    callback = request.args.get('callback')
    gBoard = request.get_data()
    print(gBoard)
    config_array = [0 for x in range(36)]
    index = 0
    for i in range(71):
        if gBoard[i] != 44:
            print(gBoard[i])
            if gBoard[i] == 95:
                config_array[index]=0
            elif gBoard[i] == 88:
                config_array[index]=1
            else:
                config_array[index]=2
            #print(index, " ", config_array[index])
            index+=1
    print(config_array)
    response = c1.choose_next_move(config_array)

    print(response)
    if(response >= 0):
        return str(response)
    else:
        return str(-1)

@app.route('/checkWinner', methods=['POST'])
def checkWinner():
    callback = request.args.get('callback')
    winBoard = request.get_data()
    print(winBoard)
    config_array = [0 for x in range(36)]
    index = 0
    for i in range(97):
        if winBoard[i] != 44:
            print(winBoard[i])
            if winBoard[i] == 95:
                config_array[index] = 0
            elif winBoard[i] == 88:
                config_array[index] = 1
            else:
                config_array[index] = 2
            # print(index, " ", config_array[index])
            index += 1
    winning_array = [[0 for y in range(6)] for x in range(6)]
    for i in range(len(winning_array)):
        for j in range(len(winning_array[i])):
            winning_array[i][j] = config_array[i*len(winning_array[i])+j]
            if winning_array[i][j] == 2:
                winning_array[i][j] = -1
    print(winning_array)
    response = has_winner(winning_array, 4)
    return str(response)

if __name__ == '__main__':
    c1 = Game(3, 3, 3)
    c1.start_game()
    app.run(debug = True)

