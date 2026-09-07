# Reproduce the UI demo GIF

The README includes `assets/demo.gif`, recorded from the real Streamlit UI with the three fictional sample PDFs. The recorder checks batch ranking, evidence retrieval, and a separate single-resume upload; failed assertions stop recording.

From the project root, with your virtual environment activated:

```bash
python -m pip install -r requirements-dev.txt
python -m examples.generate_samples
PLAYWRIGHT_BROWSERS_PATH=.cache/ms-playwright python -m playwright install chromium
python -m streamlit run app.py --server.headless true --browser.gatherUsageStats false
```

In another terminal using the same environment:

```bash
PLAYWRIGHT_BROWSERS_PATH=.cache/ms-playwright python -m examples.generate_demo_gif --url http://127.0.0.1:8501 --out assets/demo.gif
```

Outputs: `assets/demo.gif`, desktop `assets/demo.png`, and `assets/mobile.png`. The script launches Chromium headlessly, uploads only fictional samples, and uses the real embedding model. The first model load may take longer. No manual clicking is needed.
