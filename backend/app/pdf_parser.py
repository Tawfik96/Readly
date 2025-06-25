import fitz  # PyMuPDF
import io
import re

def extract_text_from_pdf(pdf_bytes):
    """Extracts PDF text in hierarchical structure: page → blocks → sentences"""
    doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
    page_structure = []
    
    for page in doc:
        blocks = page.get_text("blocks")
        page_blocks = []
        
        for block in blocks:
            x0, y0, x1, y1, text, block_no, block_type = block
            if block_type != 0:  # Skip non-text blocks
                continue
                
            # Clean and split into sentences
            text = re.sub(r'\s+', ' ', text).strip()
            if not text:
                continue
                
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            page_blocks.append(sentences)
        
        page_structure.append(page_blocks)
    
    return page_structure



