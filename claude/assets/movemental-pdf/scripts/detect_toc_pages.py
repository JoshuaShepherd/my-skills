#!/usr/bin/env python3
"""
TOC page-number detector for the Movemental PDF skill.

Workflow:
  1. Render the document once with PG_X string placeholders in the TOC entries.
  2. Run this script against the rendered PDF.
  3. The script prints a Python dict mapping each placeholder to the
     body-relative page number (matches what the reader sees in the footer).
  4. Paste those numbers back into the HTML, replacing each PG_X.
  5. Re-render.

The script ignores the TOC page itself (you can pass --toc-pdf-page N) so that
section titles appearing in the TOC don't produce false matches before reaching
the actual section pages.

You must edit the MARKERS dict below to fit your document. Each marker is a
distinctive opening phrase from the section's BODY prose — NOT the section
title. Section titles recur in the TOC and headers; body prose is unique.
Pick 8–15 words of opening prose that's unmistakable.

Usage:
  python3 detect_toc_pages.py path/to/document.pdf
  python3 detect_toc_pages.py path/to/document.pdf --toc-pdf-page 5
"""

import argparse, sys, pathlib

# Edit this dict to match your document. Each key is the placeholder string
# used in the TOC (e.g., "PG_INTRO"). Each value is a distinctive phrase from
# the opening prose of that section.
MARKERS = {
    "PG_INTRO":  "AI in its present form is a massive organizational",
    "PG_AUTH":   "AI will mirror and amplify the humanity",
    "PG_WHY":    "Safety is the first stage",
    "PG_PROC":   "Before the data, before the architecture of the Guidebook",
    "PG_DATA":   "Six independent studies, released in the last twelve months",
    "PG_ARCH":   "single document with five layers",
    "PG_L1":     "The Statement is the highest-level layer",
    "PG_L2":     "The Policy translates the Statement",
    "PG_L3":     "The Context layer converts unknowns into knowns",
    "PG_L4":     "The Rules layer is where Policy meets reality",
    "PG_L5":     "The Response Plans layer is what your organization activates",
    "PG_SELF":   "Five questions a leadership team can answer together",
    "PG_MIST":   "Three patterns of failure recur",
    "PG_PATH":   "There are two paths to a complete AI Organizational Guidebook",
    "PG_ABOUT":  "Movemental is the company that built the path",
    "PG_CITE":   "Virtuous and Fundraising.AI",
}


def normalize(text: str) -> str:
    """Normalize curly quotes and various apostrophes to plain ASCII."""
    return (text
        .replace("\u2019", "'")  # right single quote
        .replace("\u2018", "'")  # left single quote
        .replace("\u02BC", "'")  # modifier letter apostrophe (sometimes used by pdf extractors)
        .replace("\u201C", '"')
        .replace("\u201D", '"')
        .replace("\n", " ")
    )


def detect(pdf_path: pathlib.Path, toc_pdf_page: int = None) -> dict:
    try:
        from pypdf import PdfReader
    except ImportError:
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "pypdf"], check=True, capture_output=True)
        from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    results = {}

    for i, page in enumerate(reader.pages, start=1):
        # Skip the TOC page itself if specified — section titles in the TOC would otherwise match early
        if toc_pdf_page is not None and i == toc_pdf_page:
            continue
        text = normalize(page.extract_text() or "")
        for placeholder, marker in MARKERS.items():
            if placeholder in results:
                continue
            if normalize(marker) in text:
                # Body-relative page number: cover is PDF page 1 and has no footer number.
                # First body page (PDF page 2) shows footer "1".
                results[placeholder] = i - 1

    return results


def main():
    parser = argparse.ArgumentParser(description="Detect body-relative TOC page numbers in a rendered Movemental PDF.")
    parser.add_argument("pdf", help="path to the rendered PDF (with PG_X placeholders still present in the TOC)")
    parser.add_argument("--toc-pdf-page", type=int, default=None, help="PDF page number that contains the TOC (1-indexed). Skip this page during matching to avoid false hits from section titles listed in the TOC.")
    args = parser.parse_args()

    pdf_path = pathlib.Path(args.pdf)
    if not pdf_path.exists():
        sys.exit(f"error: {pdf_path} not found")

    results = detect(pdf_path, toc_pdf_page=args.toc_pdf_page)

    print("Detected body-relative page numbers:")
    print()
    print("replacements = {")
    for k in MARKERS.keys():
        v = results.get(k)
        v_str = f'"{v:02d}"' if v is not None else "None  # NOT FOUND — check marker phrase"
        print(f'    "{k}": {v_str},')
    print("}")
    print()
    not_found = [k for k in MARKERS if k not in results]
    if not_found:
        print(f"warning: {len(not_found)} placeholder(s) not detected: {', '.join(not_found)}")
        print("Edit MARKERS in detect_toc_pages.py with more distinctive opening phrases.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
