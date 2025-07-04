// import React, { useState, useRef, useEffect } from "react";
// import axios from "axios";
// import "./App.css";
import "./Style.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import BookManager from "./pages/BookManager";
import SessionPage from "./pages/SessionPage";
import SessionListPage from "./pages/SessionListPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<BookManager />} />
        <Route path="/session" element={<SessionPage />} />
        <Route path="/sessions" element={<SessionListPage />} />
      </Routes>
    </Router>
  );
}

export default App;
