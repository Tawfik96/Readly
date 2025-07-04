// pages/BookManager.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Header from "./Header";

function BookManager() {
  const [books, setBooks] = useState([]);
  const [bookFile, setBookFile] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const res = await axios.get("http://localhost:8000/books/");
        setBooks(res.data);
      } catch (err) {
        console.error("Error fetching books:", err);
      }
    };

    fetchBooks();
  }, []);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const res = await axios.post("http://localhost:8000/add_book/", formData);
      alert(res.data.message);
      setBooks([
        ...books,
        { pdf_path: `uploads/${file.name}`, pdf_name: file.name },
      ]);
    } catch (err) {
      console.error("Upload failed:", err);
    }
  };
  const goToHistorySession = (bookPath) => {
    navigate("/sessions", { state: { bookPath } });
  };

  const goToSession = (bookPath) => {
    navigate("/session", { state: { bookPath } });
  };

  return (
    <div className="container">
      <Header />

      <div className="card">
        <h1>📚 Your Library</h1>

        <div className="upload-section">
          <label>📤 Upload New Book</label>
          <p style={{ marginBottom: "1rem", color: "#64748b" }}>
            Add a PDF book to your library to start reading sessions
          </p>
          <input type="file" accept="application/pdf" onChange={handleUpload} />
        </div>

        <h2>📂 Available Books</h2>
        {books.length === 0 ? (
          <p
            style={{ textAlign: "center", color: "#64748b", margin: "2rem 0" }}
          >
            No books uploaded yet. Upload your first book to get started!
          </p>
        ) : (
          <div className="books-grid">
            {books.map((book, idx) => (
              <div key={idx} className="book-card">
                <div
                  style={{
                    fontWeight: "600",
                    color: "#1e293b",
                    marginBottom: "1rem",
                  }}
                >
                  📖 {book.pdf_name}
                </div>
                <button
                  className="btn"
                  onClick={() => goToSession(book.pdf_path)}
                >
                  🎙️ Start Session
                </button>
                <button
                  className="btn"
                  onClick={() => goToHistorySession(book.pdf_path)}
                >
                  View Sessions
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default BookManager;
