from rapidfuzz import fuzz
import re

def match_transcript_to_pdf(pdf_text_nested, user_text, threshold=80):
    """
    Match transcript to PDF blocks (paragraphs) and return all blocks above threshold.
    """
    user_text_clean = user_text.strip().lower()
    matches = []

    for page_i, page in enumerate(pdf_text_nested):
        for block_i, block in enumerate(page):
            if len(block) >1:
                block_text = " ".join(block).strip()
                score = fuzz.token_set_ratio(user_text_clean, block_text.lower())

                if score >= threshold:
                    matches.append({
                        "page": page_i,
                        "block": block_i,
                        "text": block_text,
                        "score": round(score, 2)
                    })
    result_text = "\n ".join([match["text"] for match in matches])

    return {
        "is_match": len(matches) > 0,
        "text"  : result_text,
        "mini_text": result_text[:50]+'...'+result_text[-50:],
        "end_position":  matches[-1]["page"] if matches else -1,
        "score": min([match["score"] for match in matches]) if matches else 0
    }


def match_transcript_to_pdf_test(pdf_text_nested, user_text, threshold=80):
    """
    Match transcript to PDF blocks (paragraphs) and return all blocks above threshold.
    """
    user_text_clean = user_text.strip().lower()
    matches = []

    for page_i, page in enumerate(pdf_text_nested):
        for block_i, block in enumerate(page):
            if len(block) >1:
                block_text = " ".join(block).strip()
                score = fuzz.token_set_ratio(user_text_clean, block_text.lower())

                if score >= threshold:
                    matches.append({
                        "page": page_i,
                        "block": block_i,
                        "text": block_text,
                        "score": round(score, 2)
                    })

    return {

        "matched_blocks": matches
    }

