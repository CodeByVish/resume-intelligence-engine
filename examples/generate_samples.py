"""Generate 3 simple PDF resumes for demo purposes.

Requires: reportlab (installed automatically by `examples/demo.sh`)
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")
os.makedirs(SAMPLES_DIR, exist_ok=True)


SAMPLES = [
    {
        "filename": "resume_alice.pdf",
        "text": """
Alice Smith
alice.smith@example.com

Summary
Experienced NLP engineer with 5 years building production NLP pipelines.

Skills
- Python
- NLP
- spaCy
- sentence-transformers
- FAISS

Experience
- Built semantic search for resumes and document retrieval systems.
""",
    },
    {
        "filename": "resume_bob.pdf",
        "text": """
Bob Johnson
bob.johnson@example.com

Summary
Data engineer focused on scalable ETL, SQL, and AWS.

Skills
- SQL
- AWS
- Spark
- Python

Experience
- Designed data pipelines and ETL for analytics platforms.
""",
    },
    {
        "filename": "resume_carol.pdf",
        "text": """
Carol Lee
carol.lee@example.com

Summary
Machine learning engineer with experience deploying models and building dashboards.

Skills
- Python
- Streamlit
- Docker
- ML ops

Experience
- Deployed ML models and built monitoring dashboards.
""",
    },
]


def write_pdf(path: str, text: str):
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    y = height - 72
    for line in text.strip().splitlines():
        c.setFont("Helvetica", 11)
        c.drawString(72, y, line)
        y -= 14
        if y < 72:
            c.showPage()
            y = height - 72
    c.save()


def main():
    print("Generating sample PDFs in examples/samples/")
    for s in SAMPLES:
        path = os.path.join(SAMPLES_DIR, s["filename"])
        write_pdf(path, s["text"])
        print("  ->", path)


if __name__ == "__main__":
    main()
