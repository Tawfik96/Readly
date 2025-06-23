import React, { useState, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [result, setResult] = useState(null);
  const [recordingTime, setRecordingTime] = useState(0);
  const timerRef = useRef(null);
  const audioRef = useRef(null);

  const handlePdfUpload = (e) => {
    setPdfFile(e.target.files[0]);
  };

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    const audioChunks = [];

    recorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    recorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
      setAudioBlob(audioBlob);
      audioRef.current = window.URL.createObjectURL(audioBlob);
      clearInterval(timerRef.current); // Stop timer
      setRecordingTime(0); // Reset time
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
    if (!pdfFile || !audioBlob)
      return alert("Please upload a PDF and record audio.");

    const formData = new FormData();
    formData.append("pdf", pdfFile);
    formData.append("audio", audioBlob, "recording.wav");

    const res = await axios.post("http://localhost:8000/upload/", formData);
    setResult(res.data);
  };

  return (
    <div className="container">
      <h1 className="title">📖 ReadMe - AI Reading Assistant</h1>

      <div className="upload-section">
        <label className="label">Upload PDF:</label>
        <input
          type="file"
          accept="application/pdf"
          onChange={handlePdfUpload}
        />
      </div>

      <div className="recording-buttons">
        <button
          onClick={startRecording}
          disabled={recording}
          className="start-btn"
        >
          🎙 Start Recording
        </button>
        <button
          onClick={stopRecording}
          disabled={!recording}
          className="stop-btn"
        >
          ⏹ Stop Recording
        </button>
      </div>

      {recording && (
          <p className="recording-indicator">Recording in progress...</p>
        ) && (
          <p className="text-gray-700 font-semibold">
            ⏱️ {recordingTime}s elapsed
          </p>
        )}

      {audioRef.current && (
        <audio controls className="audio-player">
          <source src={audioRef.current} type="audio/wav" />
        </audio>
      )}

      <button onClick={handleSubmit} className="submit-btn">
        🔍 Submit & Match
      </button>

      {result && (
        <div className="result-box">
          <h2>📄 Match Result:</h2>
          <p>
            <strong>Matched Sentence:</strong> {result.matched_sentence}
          </p>
          <p>
            <strong>Score:</strong> {result.score}
          </p>
          <p>
            <strong>Status:</strong>{" "}
            {result.is_match ? "✅ Good match" : "❌ Not confident"}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
