"""Exercise the actual app and capture a repeatable demo GIF using fictional PDFs."""
import argparse
from io import BytesIO
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright, expect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8501")
    parser.add_argument("--out", default="assets/demo.gif")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    frames = []
    expect.set_options(timeout=120000)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 980}, device_scale_factor=1, reduced_motion="reduce")
        page.set_default_timeout(120000)
        page.goto(args.url)
        expect(page.get_by_role("button", name="Compare resumes")).to_be_visible()

        def capture():
            page.wait_for_timeout(600)
            assert page.locator('[data-testid="stException"]').count() == 0
            frames.append(Image.open(BytesIO(page.screenshot())).convert("RGB"))

        capture()
        pdfs = sorted((root / "examples/samples").glob("*.pdf"))
        assert len(pdfs) == 3, "Generate the three fictional sample PDFs first"
        page.locator('input[type="file"]').set_input_files([str(p) for p in pdfs])
        expect(page.get_by_text("resume_alice.pdf", exact=True)).to_be_visible()
        capture()
        page.get_by_role("button", name="Compare resumes", exact=True).click()
        expect(page.get_by_text("3. Review the matches", exact=True)).to_be_visible()
        expect(page.get_by_text("Hybrid", exact=True)).to_be_visible()
        page.get_by_text("3. Review the matches", exact=True).scroll_into_view_if_needed()
        capture()
        page.get_by_role("button", name="Find evidence", exact=True).click()
        expect(page.get_by_text("resume_alice.pdf · similarity", exact=False)).to_be_visible()
        page.get_by_role("button", name="Find evidence", exact=True).scroll_into_view_if_needed()
        capture()
        page.locator(".hero").scroll_into_view_if_needed()
        page.screenshot(path=str(output.with_suffix(".png")))

        # Smoke-check the single-resume path and invalidated results too.
        page.close()
        page = browser.new_page(viewport={"width": 1200, "height": 980})
        page.goto(args.url)
        expect(page.get_by_role("button", name="Compare resumes")).to_be_visible()
        page.locator('input[type="file"]').set_input_files([str(pdfs[0])])
        expect(page.get_by_text("3. Review the matches", exact=True)).not_to_be_visible()
        page.get_by_role("button", name="Compare resumes", exact=True).click()
        expect(page.get_by_text("3. Review the matches", exact=True)).to_be_visible()
        assert page.locator('[data-testid="stException"]').count() == 0
        expect(page.locator('[data-testid="stMetricValue"]').first).to_have_text("1")
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator(".hero").scroll_into_view_if_needed()
        page.screenshot(path=str(output.with_name("mobile.png")), full_page=True)
        browser.close()
    frames[0].save(output, save_all=True, append_images=frames[1:], duration=[1800, 1800, 3000, 4000], loop=0, optimize=True)
    print(f"Verified batch ranking, evidence retrieval, and single upload. GIF saved: {output}")


if __name__ == "__main__":
    main()
