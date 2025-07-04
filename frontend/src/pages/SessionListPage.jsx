// src/pages/SessionListPage.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import Header from "./Header";
import "./SessionListPage.css"; // Import the separate CSS file
import { useLocation } from "react-router-dom";

function SessionListPage() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const location = useLocation();
  const selectedBookPath = location.state?.bookPath;

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        if (!selectedBookPath) {
          const res = await axios.get("http://localhost:8000/sessions/");
          setSessions(res.data);
        } else {
          const res = await axios.get(
            `http://localhost:8000/sessions/?pdf_path=${selectedBookPath}`
          );
          setSessions(res.data);
        }
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
      <Header />

      <div className="card">
        <h1>📚 Reading Sessions History</h1>
        <p className="page-description">
          Track your reading progress and reflections across all your books
        </p>

        {loading ? (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Loading your reading sessions...</p>
          </div>
        ) : sessions.length === 0 ? (
          <div className="empty-state">
            <p className="empty-state-title">📖 No reading sessions yet</p>
            <p className="empty-state-subtitle">
              Start your first reading session to see your progress here!
            </p>
          </div>
        ) : (
          <div className="session-list">
            {sessions.map((session, index) => (
              <div key={index} className="session-card">
                <div className="session-header">
                  <div className="session-info">
                    <h3>
                      📘 {session.pdf_path.split("/").pop().replace(".pdf", "")}
                    </h3>
                    <p className="pages-info">
                      📍 Pages {session.start_page} - {session.end_page}
                    </p>
                  </div>
                  <span className="session-date-badge">
                    📅 {new Date(session.date).toLocaleDateString()}
                  </span>
                </div>

                {session.user_notes && (
                  <div className="notes-section">
                    <h4 className="notes-title">📝 Your Notes</h4>
                    <div className="notes-content">
                      <p className="notes-text">"{session.user_notes}"</p>
                    </div>
                  </div>
                )}

                {session.reflection && session.reflection.length > 0 && (
                  <div className="reflection-section">
                    <h4 className="reflection-title">
                      🧠 AI-Generated Reflection Questions
                    </h4>
                    <ul className="reflection-list">
                      {session.reflection.map((question, i) => (
                        <li key={i} className="reflection-item">
                          <span className="reflection-icon">❓</span>
                          <span className="reflection-text">{question}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default SessionListPage;
