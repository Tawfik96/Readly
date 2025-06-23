import fitz  # PyMuPDF
import io

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
    sentences = []

    for page in doc:
        text = page.get_text()
        for line in text.split('.'):
            if line.strip():
                line.replace('\n', ' ')  # Clean up newlines
                sentences.append(line.strip())

    return sentences