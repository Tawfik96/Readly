from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.transcriber import transcribe_audio
from app.matcher import match_transcript_to_pdf, match_transcript_to_pdf_test
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
    # with open(audio_path, "wb") as f:
    #     f.write(await audio.read())

    pdf_text = extract_text_from_pdf(await pdf.read())
    # transcript = transcribe_audio(await audio.read())
    transcript = transcribe_audio(audio_path)
    match_result = match_transcript_to_pdf(pdf_text, transcript)
    return match_result

@app.post("/extract-pdf/")
async def extract_pdf(pdf: UploadFile = File(...)):
    pdf_bytes = await pdf.read()
    # Call your extract_text_structure function here
    structure = extract_text_from_pdf(pdf_bytes)
    return {
            "length1": len(structure[0]),
            "length2": len(structure[1]),
            "length3": len(structure[2]),
            "page1":structure[0],
            "page2": structure[1],
            "page3": structure[2]}
            

#     API to test matching logic
@app.post("/match/")
async def match_text(pdf: UploadFile = File(...), user_text: str = ""):
    pdf_bytes = await pdf.read()
    pdf_text = extract_text_from_pdf(pdf_bytes)
    match_result = match_transcript_to_pdf_test(pdf_text, user_text)
    return match_result
