from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.transcriber import transcribe_audio
from app.matcher import match_transcript_to_pdf
from app.pdf_parser import extract_text_from_pdf

import os
from pathlib import Path
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.post("/upload/")
async def upload_files(pdf: UploadFile = File(...), audio: UploadFile = File(...)):


    # Save Audio
    audio_path = os.path.join(UPLOAD_DIR, audio.filename)
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    pdf_text = extract_text_from_pdf(await pdf.read())
    # transcript = transcribe_audio(await audio.read())
    transcript = transcribe_audio(audio_path)
    match_result = match_transcript_to_pdf(pdf_text, transcript)
    return match_result