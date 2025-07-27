This project uses Generative AI (via Mistral LLM from Ollama) to generate Multiple-Choice Questions (MCQs) from a selected range of pages in a PDF file. It’s a simple web app powered by Flask on the backend and HTML/CSS/JS on the frontend.

🚀 Features
Upload a PDF and select specific page range

Generate MCQs based only on the selected content

User sets number of questions

LLM-powered question generation using Mistral via Ollama

🧠 Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

LLM: Mistral via Ollama

PDF Processing: pdfplumber (fitz)

🛠️ Requirements
Python 3.7+

Ollama (installed and configured)

Mistral model pulled in Ollama (ollama pull mistral)


Setup & Run

1. Clone the repository

git clone https://github.com/your-username/pdf-quiz-generator.git
cd pdf-quiz-generator

2. Install dependencies

pip install flask requests PyMuPDF

3. Pull the Mistral model using Ollama

ollama pull mistral

4. Start the Ollama LLM server

ollama run mistral

5. Run the Flask App
python app.py
The app will start at http://127.0.0.1:5000.
