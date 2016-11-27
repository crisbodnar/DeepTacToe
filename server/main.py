from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/sendNetworkData', methods=['POST'])
def sendNetworkData():
    callback = request.args.get('callback')
    gBoard = request.data['boardID']
    print(gBoard)
    print(request.data['boardID'])
    response = 5
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug = True)