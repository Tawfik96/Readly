import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

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

  const goToSession = (bookPath) => {
    navigate("/session", { state: { bookPath } });
  };

  return (
    <div className="container">
      <h1>📚 Your Library</h1>
      <div className="upload-section">
        <label>📤 Upload New Book:</label>
        <input type="file" accept="application/pdf" onChange={handleUpload} />
      </div>

      <button onClick={() => navigate("/sessions", { state: {} })}>
        📜 View Sessions
      </button>
      <h2>📂 Available Books</h2>
      {books.length === 0 ? (
        <p>No books uploaded yet.</p>
      ) : (
        <ul>
          {books.map((book, idx) => (
            <li key={idx}>
              {book.pdf_name}{" "}
              <button onClick={() => goToSession(book.pdf_path)}>
                📖 Start Session
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default BookManager;
