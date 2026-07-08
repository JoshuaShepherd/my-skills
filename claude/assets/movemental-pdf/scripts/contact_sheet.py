#!/usr/bin/env python3
"""
Generate a contact-sheet thumbnail grid of all pages of a PDF, for whole-document
visual audit. Useful for catching orphaned headings, awkward whitespace, or
page-break issues across a long document at one glance.

Usage:
  python3 contact_sheet.py path/to/document.pdf
  python3 contact_sheet.py path/to/document.pdf --cols 4 --output sheet.jpg
"""

import argparse, pathlib, subprocess, sys, tempfile


def main():
    parser = argparse.ArgumentParser(description="Render a Movemental PDF as a thumbnail contact sheet.")
    parser.add_argument("pdf", help="path to the PDF")
    parser.add_argument("--cols", type=int, default=6, help="number of columns in the grid (default 6)")
    parser.add_argument("--dpi", type=int, default=90, help="rasterization DPI per page (default 90)")
    parser.add_argument("--scale", type=float, default=1/3, help="thumbnail downscale factor (default 1/3)")
    parser.add_argument("--output", "-o", help="output JPEG path (default: alongside PDF as <stem>_contact.jpg)")
    args = parser.parse_args()

    pdf_path = pathlib.Path(args.pdf).resolve()
    if not pdf_path.exists():
        sys.exit(f"error: {pdf_path} not found")
    output_path = pathlib.Path(args.output).resolve() if args.output else pdf_path.with_name(pdf_path.stem + "_contact.jpg")

    try:
        from PIL import Image
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "Pillow"], check=True, capture_output=True)
        from PIL import Image

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = pathlib.Path(tmpdir)
        subprocess.run(["pdftoppm", "-jpeg", "-r", str(args.dpi), str(pdf_path), str(tmp / "p")], check=True)
        pages = sorted(tmp.glob("p-*.jpg"))
        if not pages:
            sys.exit("error: pdftoppm produced no pages. Is poppler-utils installed?")

        imgs = [Image.open(p) for p in pages]
        cols = args.cols
        rows = (len(imgs) + cols - 1) // cols
        w, h = imgs[0].size
        tw, th = int(w * args.scale), int(h * args.scale)
        canvas = Image.new("RGB", (tw * cols, th * rows), "white")
        for i, im in enumerate(imgs):
            r, c = i // cols, i % cols
            canvas.paste(im.resize((tw, th)), (c * tw, r * th))
        canvas.save(output_path, quality=82)

    print(f"Contact sheet: {output_path} · {len(pages)} pages · {canvas.size[0]}×{canvas.size[1]}")


if __name__ == "__main__":
    main()
