from rapidfuzz import fuzz
import re

# def split_into_sentences(text):
#     """Split text into sentences using basic punctuation rules."""
#     sentences = re.split(r'[.!?]+', text)
#     return [s.strip() for s in sentences if s.strip()]

# def match_transcript_to_pdf(pdf_text_nested, user_text, threshold=70, sentence_threshold=60):
#     """
#     Match user text to PDF content sentence by sentence for precise boundary detection.
    
#     Args:
#         pdf_text_nested: 3D structure [page][block][sentence]
#         user_text: Text to match against PDF
#         threshold: Minimum average similarity score for overall match
#         sentence_threshold: Minimum similarity score for individual sentence matches
    
#     Returns:
#         dict with:
#             - is_match: boolean indicating if match meets threshold
#             - pdf_text: PDF text equivalent to user_text
#             - end_position: dict with page, block, sentence indices where user_text ends
#             - score: average similarity score of the match
#     """
#     # Step 1: Flatten PDF and create index map
#     flat_sentences = []
#     index_map = []
#     for page_i, page in enumerate(pdf_text_nested):
#         for block_i, block in enumerate(page):
#             for sent_i, sentence in enumerate(block):
#                 flat_sentences.append(sentence.strip())
#                 index_map.append((page_i, block_i, sent_i))

#     if not flat_sentences:
#         return {"is_match": False, "pdf_text": "", "end_position": {"page": -1, "block": -1, "sentence": -1}, "score": 0}

#     # Step 2: Split user text into sentences
#     user_sentences = split_into_sentences(user_text)
#     if not user_sentences:
#         return {"is_match": False, "pdf_text": "", "end_position": {"page": -1, "block": -1, "sentence": -1}, "score": 0}

#     # Step 3: Find best sequential match
#     best_start = 0
#     best_end = 0
#     best_score = 0
#     best_matched_count = 0

#     # Try each possible starting position
#     for start_idx in range(len(flat_sentences)):
#         total_score = 0
#         matched_count = 0
#         pdf_idx = start_idx
        
#         # Try to match each user sentence sequentially
#         for user_sentence in user_sentences:
#             if pdf_idx >= len(flat_sentences):
#                 break
                
#             user_clean = user_sentence.strip().lower()
#             if not user_clean:
#                 continue
            
#             # Look ahead up to 3 sentences to find best match
#             best_local_score = 0
#             best_local_idx = pdf_idx
            
#             for lookahead in range(min(3, len(flat_sentences) - pdf_idx)):
#                 pdf_clean = flat_sentences[pdf_idx + lookahead].strip().lower()
#                 if pdf_clean:
#                     score = fuzz.token_set_ratio(user_clean, pdf_clean)
#                     if score > best_local_score:
#                         best_local_score = score
#                         best_local_idx = pdf_idx + lookahead
            
#             # If good enough match found, count it
#             if best_local_score >= sentence_threshold:
#                 total_score += best_local_score
#                 matched_count += 1
#                 pdf_idx = best_local_idx + 1
#             else:
#                 pdf_idx += 1
        
#         # Calculate average score for this attempt
#         if matched_count > 0:
#             avg_score = total_score / matched_count
#             coverage = matched_count / len(user_sentences)
            
#             # Prefer matches with better coverage and score
#             combined_score = avg_score * coverage
            
#             if combined_score > best_score:
#                 best_score = avg_score
#                 best_start = start_idx
#                 best_end = pdf_idx
#                 best_matched_count = matched_count

#     # Step 4: Check if match is good enough
#     coverage_ratio = best_matched_count / len(user_sentences)
#     is_good_match = (best_score >= threshold and coverage_ratio >= 0.5)
    
#     if not is_good_match:
#         return {"is_match": False, "pdf_text": "", "end_position": {"page": -1, "block": -1, "sentence": -1}, "score": best_score}
    
#     # # Step 5: Extract results
#     # pdf_text = " ".join(flat_sentences[best_start:best_end])
#     # end_position = index_map[best_end - 1] if best_end > 0 else (0, 0, 0)

#     # New Step 5: Extract results organized by blocks (paragraphs)
#     matched_sentences_with_positions = []
#     for i in range(best_start, best_end):
#         sentence = flat_sentences[i]
#         position = index_map[i]
#         matched_sentences_with_positions.append((sentence, position))
    
#     # Group sentences by blocks to form paragraphs
#     pdf_text_blocks = []
#     current_block_sentences = []
#     current_page = None
#     current_block = None
    
#     for sentence, (page, block, sent_idx) in matched_sentences_with_positions:
#         # If we're in a new block, finish the previous one
#         if current_page != page or current_block != block:
#             if current_block_sentences:
#                 pdf_text_blocks.append(" ".join(current_block_sentences))
#             current_block_sentences = [sentence]
#             current_page = page
#             current_block = block
#         else:
#             current_block_sentences.append(sentence)
    
#     # Add the last block
#     if current_block_sentences:
#         pdf_text_blocks.append(" ".join(current_block_sentences))
    
#     # Join blocks with double newlines to separate paragraphs
#     pdf_text = "\n\n".join(pdf_text_blocks)
#     end_position = index_map[best_end - 1] if best_end > 0 else (0, 0, 0)
    
#     return {
#         "is_match": True,
#         "pdf_text": pdf_text_blocks,
#         "end_position": {
#             "page": end_position[0],
#             "block": end_position[1], 
#             "sentence": end_position[2]
#         },
#         "score": best_score
#     }

def match_transcript_to_pdf(pdf_text_nested, user_text, threshold=70):
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
        # "matched_blocks": matches,
        "text": result_text,
        "score": min([match["score"] for match in matches]) if matches else 0
    }


def match_transcript_to_pdf_test(pdf_text_nested, user_text, threshold=70):
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

