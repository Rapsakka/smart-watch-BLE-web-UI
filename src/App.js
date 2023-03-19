import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import axios from 'axios';

const ENDPOINT = "http://localhost:5001";
const socket = io(ENDPOINT);

function formatDate(unixTimestamp) {
  const date = new Date(unixTimestamp * 1000);
  return date.toLocaleString();
}

function App() {
  const [sessionData, setSessionData] = useState([]);

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const response = await axios.get(`${ENDPOINT}/sessions`);
        setSessionData(response.data);
      } catch (error) {
        console.log(error);
      }
    };
    fetchSessions();
  }, []);

  useEffect(() => {
    socket.on("sessions", (sessions) => {
      setSessionData(sessions);
    });
  }, []);

    // Sort session data by date
    const sortedSessions = sessionData.sort((a, b) => {
      return new Date(b.sessionStart) - new Date(a.sessionStart);
    });

  return (
    <div className="App">
      <header className="App-header">
        <h1>Hiking Sessions</h1>
      </header>
      <main>
        <ul className="session-list">
          {sortedSessions.map((session, index) => (
            <li key={session.sessionStart} className="session-item">
              <div className="session-info">
                <div className="session-header">
                  <h2>Session {index + 1}</h2>
                  <p>Session Start: {formatDate(session.sessionStart)}</p>
                  <p>Session Stop: {formatDate(session.sessionStop)}</p>
                  <p>Session Time: {((session.sessionStop-session.sessionStart)/60).toFixed(2)} minutes</p>
                </div>
                <div className="session-data">
                  <ul>
                    <li>Average Speed: {session.avgSpeed.toFixed(1)} m/s</li>
                    <li>Distance: {session.hikeDistance.toFixed(1)} meters</li>
                    <li>Steps: {session.stepCount}</li>
                    <li>Step Size: {session.stepSize.toFixed(2)} meters</li>
                    <li>Burned Calories: {session.caloriesBurned} kcal</li>
                    <li>Average Temperature: {session.temperature.toFixed(1)} °C</li>
                  </ul>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </main>
      <footer>
        <p>©2023 Hiking Tracker App</p>
      </footer>
    </div>
  );

}

export default App;
