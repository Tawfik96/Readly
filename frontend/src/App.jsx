import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [result, setResult] = useState(null);
  const [recordingTime, setRecordingTime] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [startPage, setStartPage] = useState(null);
  const timerRef = useRef(null);
  const audioRef = useRef(null);

  useEffect(() => {
    const fetchStartPage = async () => {
      try {
        const res = await axios.get("http://localhost:8000/get_location");
        setStartPage(res.data);
      } catch (err) {
        console.error("Failed to get location", err);
      }
    };
    fetchStartPage();
  }, []);

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

    setIsLoading(true); // Start loading
    // setResult(null);

    try {
      const formData = new FormData();
      formData.append("pdf", pdfFile);
      formData.append("audio", audioBlob, "recording.wav");

      const res = await axios.post("http://localhost:8000/upload/", formData);
      setResult(res.data);
    } catch (error) {
      console.error("Submission error:", error);
      alert("An error occurred during submission");
    } finally {
      setIsLoading(false); // Stop loading regardless of success/failure
    }
  };

  const handleReflect = async () => {
    if (!result || !result.text) {
      alert("No result to reflect on yet.");
      return;
    }
    setIsLoading(true);
    try {
      const res = await axios.post(
        "http://localhost:8000/generate-questions/",
        { text: result.text }
      );
      console.log("Response from question generation:", res.data);
      console.log("Generated questions:", res.data.questions);
      setQuestions(res.data.questions);
    } catch (err) {
      console.error("Failed to generate questions", err);
      alert("Error generating reflection questions");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">📖 ReadMe - AI Reading Assistant</h1>
      {startPage !== null && (
        <p className="location-label">📍 Start Page: {startPage}</p>
      )}
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
      <button
        onClick={handleSubmit}
        className="submit-btn"
        disabled={isLoading}
      >
        {isLoading ? "⏳ Processing..." : "🔍 Submit & Match"}
      </button>
      {isLoading && (
        <div className="loading-indicator">
          <div className="spinner"></div>
          <p>Analyzing your content...</p>
        </div>
      )}
      {result && (
        <div className="result-box">
          <p>
            <strong>📘 End Page:</strong> {result.end_position}
          </p>

          <button
            onClick={handleReflect}
            className="reflect-btn"
            disabled={isLoading}
          >
            ✨ Reflect
          </button>
          {isLoading && (
            <div className="loading-indicator">
              <div className="spinner"></div>
              <p>Reflecting on the content...</p>
            </div>
          )}

          {questions && (
            <div className="reflection-questions">
              <h3>🧠 Reflection Questions:</h3>
              <ul>
                {questions.map((q, i) => (
                  <li key={i}>❓ {q}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
