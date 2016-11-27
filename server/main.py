from flask import Flask, render_template, request
from game import *

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/sendNetworkData', methods=['POST'])
def sendNetworkData():
    callback = request.args.get('callback')
    gBoard = request.get_data()
    config_array = [0 for x in range(9)]
    index = 0
    for i in range(17):
        if gBoard[i] != 44:
            print(gBoard[i])
            if gBoard[i] == 95:
                config_array[index]=0
            elif gBoard[i] == 88:
                config_array[index]=1
            else:
                config_array[index]=2
            print(config_array[index])
            index+=1
    response = c1.choose_next_move(config_array)

    print(response)
    return str(response)

if __name__ == '__main__':
    c1 = Game(3, 3, 3)
    c1.start_game()
    app.run(debug = True)