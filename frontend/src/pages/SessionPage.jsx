// pages/SessionPage.jsx
import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useLocation } from "react-router-dom";
import Header from "./Header";

function SessionPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const selectedBookPath = location.state?.bookPath;
  const [audioBlob, setAudioBlob] = useState(null);
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [recordingTime, setRecordingTime] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoading_reflect, setIsLoadingReflect] = useState(false);
  const [result, setResult] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [note, setNote] = useState("");
  const [isSavingSession, setIsSavingSession] = useState(false);
  const timerRef = useRef(null);
  const audioRef = useRef(null);

  useEffect(() => {
    if (!selectedBookPath) {
      alert("No book selected!");
    }
  }, [selectedBookPath]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  };

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    const audioChunks = [];

    recorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    recorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: "audio/wav" });
      setAudioBlob(blob);
      audioRef.current = window.URL.createObjectURL(blob);
      clearInterval(timerRef.current);
    };

    recorder.start();
    setMediaRecorder(recorder);
    setRecording(true);

    timerRef.current = setInterval(() => {
      setRecordingTime((prev) => prev + 1);
    }, 1000);
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setRecording(false);
    }
  };

  const handleSubmit = async () => {
    if (!audioBlob || !selectedBookPath) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append("pdf", selectedBookPath);
    formData.append("audio", audioBlob, "recording.wav");

    try {
      const res = await axios.post("http://localhost:8000/upload/", formData);
      setResult(res.data);
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReflect = async () => {
    if (!result?.text) return;

    setIsLoadingReflect(true);
    try {
      const res = await axios.post(
        "http://localhost:8000/generate-questions/",
        {
          text: result.text,
        }
      );
      setQuestions(res.data.questions);
    } catch (err) {
      console.error("Reflection failed:", err);
    } finally {
      setIsLoadingReflect(false);
    }
  };

  const handleSaveSession = async () => {
    if (!selectedBookPath || !result?.end_position) {
      alert("Missing required session data.");
      return;
    }

    setIsSavingSession(true);
    try {
      await axios.post("http://localhost:8000/add-session/", {
        pdf_path: selectedBookPath,
        start_page: 0,
        end_page: result.end_position,
        user_notes: note,
        reflection: questions,
      });
      alert("✅ Session saved successfully!");
      setNote("");
      navigate("/");
    } catch (err) {
      console.error("❌ Failed to save session", err);
      alert("Failed to save session.");
    } finally {
      setIsSavingSession(false);
    }
  };

  return (
    <div className="container">
      <Header />

      <div className="card">
        <h1>🎙️ Reading Session</h1>
        <p style={{ marginBottom: "2rem" }}>
          <strong>Book:</strong> {selectedBookPath || "No book selected"}
        </p>

        <div className="recording-section">
          <h3>Audio Recording</h3>
          <p>Record yourself reading aloud for AI analysis</p>

          <div className="recording-buttons">
            <button
              onClick={startRecording}
              disabled={recording}
              className="btn"
            >
              🎙️ Start Recording
            </button>
            <button
              onClick={stopRecording}
              disabled={!recording}
              className="btn btn-secondary"
            >
              ⏹️ Stop Recording
            </button>
          </div>

          {recording && (
            <div className="recording-indicator">
              🔴 Recording in progress...
            </div>
          )}

          <div className="timer">⏱️ {formatTime(recordingTime)}</div>

          {audioRef.current && (
            <audio controls className="audio-player">
              <source src={audioRef.current} type="audio/wav" />
            </audio>
          )}
        </div>

        <div className="text-center">
          <button
            onClick={handleSubmit}
            className="submit-btn"
            disabled={
              isLoading || !audioBlob || !selectedBookPath || result?.text
            }
          >
            {isLoading ? "⏳ Processing..." : "🔍 Analyze Recording"}
          </button>
        </div>

        {isLoading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Analyzing your content...</p>
          </div>
        )}

        {result && (
          <div className="result">
            <h2>📄 Analysis Results</h2>
            <p>
              You stopped at page: <strong>{result.end_position}</strong>
            </p>

            <button
              onClick={handleReflect}
              className="submit-btn"
              disabled={isLoading_reflect || questions.length > 0}
            >
              {isLoading_reflect
                ? "⏳ Processing..."
                : "✨ Generate Reflection Questions"}
            </button>

            {isLoading_reflect && (
              <div className="loading-indicator">
                <div className="spinner"></div>
                <p>Generating questions...</p>
              </div>
            )}

            {questions.length > 0 && (
              <div>
                <h3>🧠 Reflection Questions</h3>
                <ul>
                  {questions.map((q, i) => (
                    <li key={i}>❓ {q}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="session-notes">
              <label htmlFor="notes">📝 Session Notes</label>
              <textarea
                id="notes"
                placeholder="Write your thoughts, insights, and notes from this reading session..."
                value={note}
                onChange={(e) => setNote(e.target.value)}
              />
            </div>

            <button
              className="submit-btn"
              style={{
                marginTop: "1rem",
                backgroundColor: "#10b981",
              }}
              onClick={handleSaveSession}
              disabled={isSavingSession || !note.trim()}
            >
              {isSavingSession ? "💾 Saving..." : "💾 Save Session"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default SessionPage;
