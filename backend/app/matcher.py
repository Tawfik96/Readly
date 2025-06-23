from rapidfuzz import fuzz

def match_transcript_to_pdf(pdf_sentences, user_text, threshold=70):
    best_score = 0
    best_sentence = ""
    best_index = 0

    for i, sentence in enumerate(pdf_sentences):
        score = fuzz.token_set_ratio(user_text.lower(), sentence.lower())
        if score > best_score:
            best_score = score
            best_sentence = sentence
            best_index = i

    return {
        "matched_sentence": best_sentence,
        "score": best_score,
        "is_match": best_score >= threshold,
        "sentence_index": best_index
    }
