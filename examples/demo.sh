#!/usr/bin/env bash
set -euo pipefail
# Run from the repository root after installing requirements-dev.txt.
python -m examples.generate_samples
python -m examples.run_quick_demo --pdf examples/samples/resume_alice.pdf examples/samples/resume_bob.pdf examples/samples/resume_carol.pdf --jd "NLP engineer with Python, natural language processing and vector search skills."
