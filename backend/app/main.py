import sqlite3
import json
import time
import datetime
from typing import Optional
from fastapi import Query
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.transcriber import transcribe_audio
from app.matcher import match_transcript_to_pdf, match_transcript_to_pdf_test
from app.pdf_parser import extract_text_from_pdf
from app.reflector import questions_generator
from app.db import get_connection, init_db, reset_db
from app.models import BookInput, SessionInput, TextInput
import os
from pathlib import Path

init_db()  # Initialize the database


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)


@app.post("/upload/")
async def upload_files(pdf_path:str="uploads/story.pdf",  audio: UploadFile = File(...)):
    if pdf_path or audio:
        print("Received files:", pdf_path, audio.filename)
    else:
        print("No files received")


    audio_path = os.path.join(UPLOAD_DIR, audio.filename)
    # audio_path = audio.filename
    # with open(audio_path, "wb") as f:
    #     f.write(await audio.read())

    pdf_text = extract_text_from_pdf(pdf_path)
    start_time=  time.time()
    transcript = transcribe_audio(audio_path)
    end_time = time.time()
    duration = end_time - start_time
    duration = round(duration, 2)
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
            "page3": structure[2],
            "page4": structure[3],}
            

#     API to test matching logic
@app.post("/match/")
async def match_text(pdf: UploadFile = File(...), user_text: str = "",audio: UploadFile = File(...)):
    audio_path = os.path.join(UPLOAD_DIR, audio.filename)
    pdf_bytes = await pdf.read()
    pdf_text = extract_text_from_pdf(pdf_bytes)
    if not user_text:
        user_text = transcribe_audio(audio_path)
    match_result = match_transcript_to_pdf_test(pdf_text, user_text)
    return match_result


@app.post("/generate-questions/")
async def generate_questions(data: TextInput):
    text = data.text
    questions = questions_generator(text[:2000])
    return {'questions':questions}

@app.get("/get_location")
async def get_page_location(s :str=""):
    return "0"

#=================================== Book Related APIs=========================================

@app.post("/add_book/")
async def add_book(pdf: UploadFile = File(...)):
    file_path = f"uploads/{pdf.filename}"

    # Save the file
    with open(file_path, "wb") as f:
        f.write(await pdf.read())

    conn = get_connection()
    cursor = conn.cursor()

    # Check if the book exists
    cursor.execute("SELECT id FROM books WHERE pdf_path = ?", (file_path,))
    exists = cursor.fetchone()
    if exists:
        conn.close()
        return {"message": "Book already exists", "pdf_path": file_path}

    # Insert new book
    cursor.execute(
        "INSERT INTO books (pdf_path, pdf_name) VALUES (?, ?)",
        (file_path, pdf.filename)
    )
    conn.commit()
    conn.close()

    return {"message": "Book uploaded and registered", "pdf_path": file_path}


@app.post("/add-session/")
async def add_session(session: SessionInput):
    if session:
        print(session.pdf_path)
    else:
        return {"message": "Session data is missing"}
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM books WHERE pdf_path = ?", (session.pdf_path,))
    book = cursor.fetchone()
    if not book:
        return {"message": "Book not found"}

    book_id = book[0]
    reflection_json = json.dumps(session.reflection)
    current_time = datetime.datetime.now()
    session_date = session.date or current_time.strftime("%Y-%m-%d %H:%M:%S")

    temp_start_page = 0 #should be changed here and the models.py as well
    cursor.execute("""
        INSERT INTO sessions (book_id, start_page,end_page, user_notes, reflection, date)
        VALUES (?, ?, ?, ?, ?,?)
    """, (book_id,temp_start_page, session.end_page, session.user_notes, reflection_json, session_date))

    conn.commit()
    conn.close()
    return {"message": "Session added"}


@app.get("/books/")
async def get_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pdf_path, pdf_name FROM books")
    books = [{"pdf_path": row[0], "pdf_name": row[1]} for row in cursor.fetchall()]
    conn.close()
    return books


@app.get("/sessions/")
async def get_sessions(pdf_path: Optional[str] = Query(None)):
    conn = get_connection()
    cursor = conn.cursor()

    sessions = []

    if pdf_path:
        # Get specific book ID
        cursor.execute("SELECT id FROM books WHERE pdf_path = ?", (pdf_path,))
        book = cursor.fetchone()
        if not book:
            conn.close()
            return {"message": "Book not found"}
        book_id = book[0]

        cursor.execute("""
            SELECT start_page, end_page, user_notes, reflection, date 
            FROM sessions WHERE book_id = ?
        """, (book_id,))
        rows = cursor.fetchall()

        for row in rows:
            sessions.append({
                "start_page": row[0],
                "end_page": row[1],
                "user_notes": row[2],
                "reflection": json.loads(row[3]),
                "date": row[4],
                "pdf_path": pdf_path
            })
    else:
        # Fetch all sessions with associated pdf_path
        cursor.execute("""
            SELECT s.start_page, s.end_page, s.user_notes, s.reflection, s.date, b.pdf_path
            FROM sessions s
            JOIN books b ON s.book_id = b.id
        """)
        rows = cursor.fetchall()

        for row in rows:
            sessions.append({
                "start_page": row[0],
                "end_page": row[1],
                "user_notes": row[2],
                "reflection": json.loads(row[3]),
                "date": row[4],
                "pdf_path": row[5]
            })

    conn.close()
    return sessions