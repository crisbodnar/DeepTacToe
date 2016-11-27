from flask import Flask, render_template, request, jsonify, Response
import json

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/send-network-data', methods=['POST'])

def send_network_data():
    callback = request.args.get('callback')
    return jsonify({'a' : '1'})

if __name__ == '__main__':
    app.run(debug = True)