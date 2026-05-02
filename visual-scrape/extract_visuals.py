#!/usr/bin/env python3
"""
Extract visuals (images + vector-rendered regions) from a PDF using PyMuPDF.

Usage:
    python3 extract_visuals.py <pdf_path> [--output-dir <dir>] [--min-size <pixels>] [--pages <range>]

Output:
    - Extracted image files in <output-dir>/
    - manifest.json with metadata for each extracted image
"""

import fitz  # PyMuPDF
import json
import sys
import os
import argparse
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text to a filesystem-safe slug."""
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in text.lower()).strip("-")


def parse_page_range(page_range: str, total_pages: int) -> list[int]:
    """Parse a page range string like '1-10' or '5,8,12-15' into page indices (0-based)."""
    pages = set()
    for part in page_range.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = max(0, int(start) - 1)
            end = min(total_pages, int(end))
            pages.update(range(start, end))
        else:
            p = int(part) - 1
            if 0 <= p < total_pages:
                pages.add(p)
    return sorted(pages)


def extract_embedded_images(page, page_num: int, output_dir: Path, min_size: int) -> list[dict]:
    """Extract embedded raster images from a page."""
    results = []
    image_list = page.get_images(full=True)

    for img_idx, img_info in enumerate(image_list):
        xref = img_info[0]
        try:
            base_image = fitz.Pixmap(page.parent, xref)
        except Exception:
            continue

        # Skip tiny images (icons, bullets, decorations)
        if base_image.width < min_size or base_image.height < min_size:
            base_image = None
            continue

        # Ensure the pixmap is saveable as PNG (must be grayscale or RGB)
        try:
            # Always convert to RGB via samples as the most robust path
            samples = base_image.samples
            w, h = base_image.width, base_image.height
            n = base_image.n
            alpha = base_image.alpha

            # Use fitz to create a clean RGB pixmap from the page render instead
            # This avoids all colorspace conversion edge cases
            if n not in (1, 3) or (n == 3 and alpha):
                # Re-extract via page rendering at the image's location
                base_image = fitz.Pixmap(fitz.csRGB, base_image, 0) if alpha else fitz.Pixmap(fitz.csRGB, base_image)
        except Exception:
            base_image = None
            continue

        ext = "png"
        filename = f"page-{page_num:03d}-img-{img_idx:02d}.{ext}"
        filepath = output_dir / filename
        try:
            base_image.save(str(filepath))
        except Exception:
            # Last resort: skip this image
            base_image = None
            continue

        results.append({
            "file": filename,
            "page": page_num,
            "type": "embedded_image",
            "width": base_image.width,
            "height": base_image.height,
        })
        base_image = None

    return results


def extract_vector_regions(page, page_num: int, output_dir: Path, min_size: int) -> list[dict]:
    """
    Detect pages with significant vector drawing content and render them.
    Uses drawing count heuristic to identify diagram-heavy pages.
    """
    results = []
    drawings = page.get_drawings()

    # Heuristic for detecting actual diagrams vs normal page formatting:
    # - Typeset book pages routinely have 50-100+ vector paths from text formatting,
    #   decorative rules, headers, footers, sidebars, and page furniture
    # - Real diagrams (circles, arrows, boxes) typically have very high drawing counts
    #   AND relatively little text on the page
    # Strategy: require high drawing count AND low text-to-drawing ratio
    if len(drawings) < 30:
        return results

    # Check if there are already embedded images on this page
    # If so, the visuals are likely raster — skip vector rendering
    if len(page.get_images(full=True)) > 0:
        return results

    # Count text content — diagram pages have little text relative to drawings
    text = page.get_text("text").strip()
    text_len = len(text)
    text_blocks = page.get_text("blocks")
    text_block_count = sum(1 for b in text_blocks if b[6] == 0)  # type 0 = text

    # Ratio heuristic: on a diagram page, drawings dominate over text
    # Normal text pages: ~50-150 drawings, 500-2000 chars of text
    # Diagram pages: ~30-300 drawings, <300 chars of text (just labels)
    drawing_to_text_ratio = len(drawings) / max(text_len, 1)

    # Skip if it's clearly a text-heavy page
    if text_len > 400 and drawing_to_text_ratio < 0.3:
        return results

    # Skip pages that are mostly text blocks with moderate drawings (footnote pages, etc)
    if text_block_count > 8 and len(drawings) < 150:
        return results

    # Render the full page at 2x resolution for quality
    mat = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=mat)

    if pix.width < min_size or pix.height < min_size:
        pix = None
        return results

    filename = f"page-{page_num:03d}-vector.png"
    filepath = output_dir / filename
    pix.save(str(filepath))

    results.append({
        "file": filename,
        "page": page_num,
        "type": "vector_render",
        "width": pix.width,
        "height": pix.height,
        "drawing_count": len(drawings),
    })
    pix = None

    return results


def main():
    parser = argparse.ArgumentParser(description="Extract visuals from a PDF")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output-dir", "-o", help="Output directory (default: images/<book-slug>/)")
    parser.add_argument("--min-size", type=int, default=100, help="Minimum image dimension in pixels (default: 100)")
    parser.add_argument("--pages", help="Page range to process (e.g., '1-50' or '5,10,20-30')")
    parser.add_argument("--vectors", action="store_true", default=False, help="Also render vector-heavy pages as images")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).resolve()
    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    book_slug = slugify(pdf_path.stem)
    output_dir = Path(args.output_dir) if args.output_dir else Path("images") / book_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)

    if args.pages:
        page_indices = parse_page_range(args.pages, total_pages)
    else:
        page_indices = list(range(total_pages))

    print(f"Processing {len(page_indices)} pages from '{pdf_path.name}' ({total_pages} total)")
    print(f"Output: {output_dir}/")

    manifest = []

    for page_idx in page_indices:
        page = doc[page_idx]
        page_num = page_idx + 1  # 1-based for humans

        # Extract embedded raster images
        images = extract_embedded_images(page, page_num, output_dir, args.min_size)
        manifest.extend(images)

        # Optionally render vector-heavy pages
        if args.vectors:
            vectors = extract_vector_regions(page, page_num, output_dir, args.min_size)
            manifest.extend(vectors)

        if images or (args.vectors and vectors):
            types = [r["type"] for r in images + (vectors if args.vectors else [])]
            print(f"  Page {page_num}: {len(types)} visual(s) — {', '.join(types)}")

    doc.close()

    # Write manifest
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump({
            "source": str(pdf_path),
            "book_slug": book_slug,
            "total_pages": total_pages,
            "pages_processed": len(page_indices),
            "visuals_found": len(manifest),
            "items": manifest,
        }, f, indent=2)

    print(f"\nDone: {len(manifest)} visuals extracted → {output_dir}/")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
