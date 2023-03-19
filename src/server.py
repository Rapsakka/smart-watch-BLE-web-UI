from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

sessions = []

# generate some dummy sessions
for i in range(10):
    time = random.randint(1000000000, 2000000000)
    session = {
        'sessionStart': time,
        'sessionStop': time + 1000*(i+1),
        'caloriesBurned': random.randint(100, 1000),
        'stepCount': random.randint(1000, 10000),
        'hikeDistance': random.uniform(10.0, 10000.0),
        'temperature': random.uniform(20.0, 35.0),
        'stepSize': random.uniform(0.5, 1.0),
        'avgSpeed': random.uniform(3.0, 5.0)
    }
    sessions.append(session)

@app.route('/sessions')
def get_sessions():
    return jsonify(sessions)

@socketio.on('connect')
def handle_connect():
    print("client has connected")
    emit('connected', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True)