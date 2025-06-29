import re
import requests
from collections import Counter


def generate_questions(text):
    OPENROUTER_API_KEY = "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"

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
