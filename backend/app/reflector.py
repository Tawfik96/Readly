import io
import re
import requests
from collections import Counter


def generate_questions(text):
    # get that key from notes.txt or from your environment variables

    notes_file = io.open("../Notes.txt", "r")
    if notes_file is None:
        raise FileNotFoundError("Notes.txt file not found")
    lines = notes_file.readlines()
    for line in lines:
        if "Oper Router Readly API Key" in line:
            OPENROUTER_API_KEY = line.split(":")[1].strip()
            break
    else:
        raise ValueError("API key not found in Notes.txt")
    # OPENROUTER_API_KEY = 

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    system_prompt = "You are an assistant that creates meaningful and reflective questions from long texts to help readers think deeper."
    user_prompt = f"Generate 2–3 thoughtful, reflective questions from the following passage:\n\n{text}"

    data = {
        "model": "mistralai/mistral-7b-instruct:free",  # You can also try: openrouter/mistral, openrouter/meta-llama-3-8b-instruct
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def questions_generator(text):
    questions = generate_questions(text)
    res=[]
    for q in questions.split('\n'):
        q = q.strip()
        if q:
            # Clean up the question text
            q = re.sub(r'\s+', ' ', q)
            res.append(q)

    return res
