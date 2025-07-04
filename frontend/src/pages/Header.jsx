// components/Header.jsx
import React from "react";
import { useNavigate, useLocation } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <>
      <div className="app-header">
        <h1>📚 Readly</h1>
        <p>
          Your AI-powered reading companion for deeper learning and reflection
        </p>
      </div>

      <nav className="app-nav">
        <button
          className={`nav-btn ${isActive("/") ? "active" : ""}`}
          onClick={() => navigate("/")}
        >
          📚 Book Manager
        </button>
        {/* <button
          className={`nav-btn ${isActive("/session") ? "active" : ""}`}
          onClick={() => navigate("/session")}
        >
          🎙️ Session
        </button> */}
        <button
          className={`nav-btn ${isActive("/sessions") ? "active" : ""}`}
          onClick={() => navigate("/sessions")}
        >
          📜 History
        </button>
      </nav>
    </>
  );
};

export default Header;
