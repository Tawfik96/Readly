// src/pages/SessionListPage.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import "./SessionListPage.css"; // Assuming you have a CSS file for styling

function SessionListPage() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const res = await axios.get("http://localhost:8000/sessions/");
        setSessions(res.data);
      } catch (err) {
        console.error("Failed to fetch sessions:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchSessions();
  }, []);

  return (
    <div className="container">
      <h1>📚 All Sessions</h1>
      {loading ? (
        <p>Loading sessions...</p>
      ) : sessions.length === 0 ? (
        <p>No sessions found.</p>
      ) : (
        <ul className="session-list">
          {sessions.map((session, index) => (
            <li key={index} className="session-card">
              <p>
                <strong>📘 Book:</strong> {session.pdf_path}
              </p>
              <p>
                <strong>📍 Pages:</strong> {session.start_page} ---{" "}
                {session.end_page}
              </p>
              <p>
                <strong>📝 Notes:</strong> {session.user_notes}
              </p>
              <p>
                <strong>🧠 Reflection:</strong>
              </p>
              <ul>
                {session.reflection.map((q, i) => (
                  <li key={i}>❓ {q}</li>
                ))}
              </ul>
              <p>
                <strong>📅 Date:</strong>{" "}
                {new Date(session.date).toLocaleDateString()}
              </p>
              <hr />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default SessionListPage;
