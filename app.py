from flask import Flask, render_template, request
import os
import pdfplumber
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# PDF text extractor
def extract_text(pdf_path, start, end, max_words=2500):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(start - 1, end):
            if i < len(pdf.pages):
                page_text = pdf.pages[i].extract_text()
                if page_text:
                    text += page_text + "\n"
    # Truncate to avoid overloading the LLM
    words = text.split()
    return " ".join(words[:max_words])


# Send prompt to Ollama
def generate_quiz(text, num_questions):
    prompt = f"""
You are an expert quiz generator AI.

🎯 Objective:
From the provided text, generate {num_questions} multiple-choice questions. Each question must:
- Be based ONLY on the given text (no outside knowledge).
- Have exactly 4 options (A, B, C, D).
- NOT mention which option is correct inline.
- Include the correct answer(s) only in the last line as: Answer: A (or A, C if multiple answers).

📝 Required Format:
Q1. [Question]  
A. Option A  
B. Option B  
C. Option C  
D. Option D  
Answer: [Correct Option Letter(s)]

---

Only return the questions and answers in the exact format above. Do NOT mark answers like “(correct)” next to any option. Do NOT include any commentary, explanation, or notes.

--- START OF TEXT ---
{text}
--- END OF TEXT ---
""".strip()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    # Check if the response was successful
    if response.status_code == 200:
        return response.json().get("response", "❌ No response field in API output.")
    else:
        return f"❌ Failed to generate questions. Error: {response.status_code} - {response.text}"




@app.route('/', methods=['GET', 'POST'])
def index():
    quiz = None
    content= None
    if request.method == 'POST':
        pdf = request.files['pdf_file']
        start_page = int(request.form['start_page'])
        end_page = int(request.form['end_page'])
        num_questions = int(request.form['num_questions'])

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
        pdf.save(pdf_path)

        # ✅ Get total pages
        with pdfplumber.open(pdf_path) as pdf_file:
            total_pages = len(pdf_file.pages)

        # ✅ Validate page range
        if start_page < 1 or end_page > total_pages or start_page > end_page:
            quiz = f"❌ Invalid page range. This PDF has only {total_pages} pages."
            return render_template('index.html', quiz=quiz)

        content = extract_text(pdf_path, start_page, end_page)
        quiz = generate_quiz(content, num_questions)


    return render_template('index.html', quiz=quiz, pdf_text=content)


if __name__ == '__main__':
    app.run(debug=True)