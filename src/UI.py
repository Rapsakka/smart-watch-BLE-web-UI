from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

sessions = []

def updateSessions():
    con = sqlite3.connect('Hiking.db')
    cursor = con.cursor()
    query =cursor.execute(""" SELECT * FROM Hiking""")
    results = query.fetchall()
    for row in results:
	    #data = row.split(",") 
	    start = int( row[0])
	    end = int(row[1])
	    calories = float(row[4])
	    steps = int(row[2])
	    distance = int(row[3])
	    temp = float(row[5])
	    stepSize = int(distance)/int(steps)
	    avgSpeed = 0
	    if end != "0":
		    avgSpeed = int(distance)/( int(end)-int(start) )
	    session = {
	    'sessionStart': start,
	    'sessionStop': end,
	    'caloriesBurned': calories,
	    'stepCount': steps,
	    'hikeDistance': distance,
	    'temperature': temp,
	    'stepSize': stepSize,
	    'avgSpeed': avgSpeed
	    }
	    sessions.append(session)


updateSessions()

@app.route('/sessions')
def get_sessions():
    return jsonify(sessions)

@socketio.on('connect')
def handle_connect():
    print("client has connected")
    emit('connected', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True)

