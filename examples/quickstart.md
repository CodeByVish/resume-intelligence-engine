# CLI quickstart

From the project root, activate your virtual environment and install the development requirements:

```bash
python -m pip install -r requirements-dev.txt
bash examples/demo.sh
```

The script generates three fictional PDFs and prints ranked results using the same scorer as the Streamlit app. The embedding model downloads on first use.

For your own PDFs:

```bash
python -m examples.run_quick_demo --pdf path/to/resume.pdf --jd "NLP engineer with Python and vector search skills"
```

Run as a module from the project root so Python can find `src`. Processing errors and keyword fallback warnings are printed alongside successful results.
