#!/usr/bin/env python3
"""
batch_ingest.py — Tier 1 → Tier 2 batch conversion for the corpus ingestion pipeline.

Converts a directory of raw source files to Markdown using MarkItDown and
writes each output with a Tier 2 frontmatter block.

Usage:
    python scripts/batch_ingest.py \
        --input  corpus_ingest/raw/alan_hirsch/ \
        --output corpus_ingest/converted_markdown/alan_hirsch/ \
        --author "Alan Hirsch"

    # With AI image enhancement (requires OPENAI_API_KEY):
    python scripts/batch_ingest.py \
        --input  corpus_ingest/raw/alan_hirsch/slides/ \
        --output corpus_ingest/converted_markdown/alan_hirsch/slides/ \
        --author "Alan Hirsch" \
        --ai-enhance

    # Dry run (show what would be converted without writing):
    python scripts/batch_ingest.py \
        --input  corpus_ingest/raw/alan_hirsch/ \
        --output corpus_ingest/converted_markdown/alan_hirsch/ \
        --author "Alan Hirsch" \
        --dry-run
"""

import argparse
import os
import sys
from datetime import date
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print("ERROR: markitdown is not installed.")
    print("  pip install 'markitdown[all]'")
    sys.exit(1)

# File extensions MarkItDown handles reliably
SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".xls",
    ".html", ".htm", ".csv", ".json", ".xml",
    ".zip", ".epub", ".txt",
    ".jpg", ".jpeg", ".png", ".gif", ".webp",
    ".wav", ".mp3",
}

# Extensions where AI enhancement is particularly valuable
AI_ENHANCE_CANDIDATES = {".pptx", ".jpg", ".jpeg", ".png", ".gif", ".webp"}


def build_frontmatter(
    title: str,
    author: str,
    source_type: str,
    source_file: str,
    ai_enhanced: bool,
    notes: str = "",
) -> str:
    today = date.today().isoformat()
    ai_flag = "true" if ai_enhanced else "false"
    return f"""---
title: "{title}"
author: "{author}"
source_type: {source_type}
source_file: "{source_file}"
source_url: ""
publication_year: ""
conversion_tool: markitdown
conversion_date: "{today}"
ai_enhanced: {ai_flag}
tier: converted_markdown
cleanup_status: raw_conversion
confidence: ""
conversion_notes: "{notes}"
---

"""


def infer_source_type(path: Path) -> str:
    ext = path.suffix.lower()
    mapping = {
        ".pdf": "book",
        ".epub": "book",
        ".docx": "article",
        ".pptx": "slides",
        ".xlsx": "article",
        ".xls": "article",
        ".html": "web",
        ".htm": "web",
        ".mp3": "audio",
        ".wav": "audio",
        ".zip": "zip",
    }
    return mapping.get(ext, "article")


def convert_file(
    source_path: Path,
    output_path: Path,
    author: str,
    input_root: Path,
    md_converter: MarkItDown,
    dry_run: bool = False,
) -> tuple[bool, str]:
    """
    Convert a single file from Tier 1 to Tier 2 markdown.
    Returns (success, message).
    """
    rel_source = str(source_path.relative_to(input_root.parent))
    source_type = infer_source_type(source_path)
    title = source_path.stem.replace("-", " ").replace("_", " ").title()

    if dry_run:
        return True, f"[DRY RUN] Would convert: {source_path.name} → {output_path.name}"

    try:
        result = md_converter.convert(str(source_path))
        content = result.text_content or ""

        if not content.strip():
            notes = "WARNING: MarkItDown returned empty content. Check source file."
            confidence_hint = "low"
        else:
            notes = ""
            confidence_hint = ""

        frontmatter = build_frontmatter(
            title=title,
            author=author,
            source_type=source_type,
            source_file=rel_source,
            ai_enhanced=False,
            notes=notes,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(frontmatter + content, encoding="utf-8")

        if confidence_hint == "low":
            return False, f"WARN: Empty extraction — {source_path.name}"
        return True, f"OK: {source_path.name} → {output_path.name}"

    except Exception as exc:
        # Write a stub file so the conversion attempt is recorded
        stub_frontmatter = build_frontmatter(
            title=title,
            author=author,
            source_type=source_type,
            source_file=rel_source,
            ai_enhanced=False,
            notes=f"CONVERSION ERROR: {exc}",
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            stub_frontmatter + f"\n<!-- Conversion failed: {exc} -->\n",
            encoding="utf-8",
        )
        return False, f"ERROR: {source_path.name} — {exc}"


def convert_file_with_ai(
    source_path: Path,
    output_path: Path,
    author: str,
    input_root: Path,
    dry_run: bool = False,
) -> tuple[bool, str]:
    """
    AI-enhanced conversion for slides and image-heavy files.
    Requires OPENAI_API_KEY in environment.
    """
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return False, f"SKIP (no OPENAI_API_KEY): {source_path.name}"

    if dry_run:
        return True, f"[DRY RUN] Would AI-enhance: {source_path.name} → {output_path.name}"

    client = OpenAI(api_key=api_key)
    md = MarkItDown(
        llm_client=client,
        llm_model="gpt-4o",
        llm_prompt=(
            "Describe this image or slide in detail. "
            "Focus on theological concepts, diagrams, key phrases, scripture references, "
            "and any visual structure that conveys meaning."
        ),
    )

    rel_source = str(source_path.relative_to(input_root.parent))
    source_type = infer_source_type(source_path)
    title = source_path.stem.replace("-", " ").replace("_", " ").title()

    try:
        result = md.convert(str(source_path))
        content = result.text_content or ""
        frontmatter = build_frontmatter(
            title=title,
            author=author,
            source_type=source_type,
            source_file=rel_source,
            ai_enhanced=True,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(frontmatter + content, encoding="utf-8")
        return True, f"OK (AI): {source_path.name} → {output_path.name}"
    except Exception as exc:
        return False, f"ERROR (AI): {source_path.name} — {exc}"


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert Tier 1 source files to Tier 2 markdown."
    )
    parser.add_argument("--input", required=True, help="Input directory (Tier 1 raw files)")
    parser.add_argument("--output", required=True, help="Output directory (Tier 2 converted markdown)")
    parser.add_argument("--author", required=True, help='Author name (e.g. "Alan Hirsch")')
    parser.add_argument("--ai-enhance", action="store_true", help="Use AI for image/slide-heavy files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be converted without writing")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files")
    args = parser.parse_args()

    input_root = Path(args.input).resolve()
    output_root = Path(args.output).resolve()

    if not input_root.exists():
        print(f"ERROR: Input directory does not exist: {input_root}")
        sys.exit(1)

    md = MarkItDown()

    source_files = [
        f for f in input_root.rglob("*")
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not source_files:
        print(f"No supported files found in {input_root}")
        sys.exit(0)

    print(f"\nCorpus Ingestion — Batch Convert")
    print(f"  Input:  {input_root}")
    print(f"  Output: {output_root}")
    print(f"  Author: {args.author}")
    print(f"  Files:  {len(source_files)}")
    print(f"  AI:     {'yes' if args.ai_enhance else 'no'}")
    print(f"  Dry run: {'yes' if args.dry_run else 'no'}")
    print()

    ok_count = 0
    fail_count = 0

    for source_path in sorted(source_files):
        # Mirror the directory structure in the output
        rel_path = source_path.relative_to(input_root)
        output_path = output_root / rel_path.with_suffix(".md")

        if output_path.exists() and not args.overwrite and not args.dry_run:
            print(f"  SKIP (exists): {source_path.name}")
            continue

        use_ai = args.ai_enhance and source_path.suffix.lower() in AI_ENHANCE_CANDIDATES

        if use_ai:
            success, msg = convert_file_with_ai(
                source_path, output_path, args.author, input_root, dry_run=args.dry_run
            )
        else:
            success, msg = convert_file(
                source_path, output_path, args.author, input_root, md, dry_run=args.dry_run
            )

        print(f"  {msg}")
        if success:
            ok_count += 1
        else:
            fail_count += 1

    print()
    print(f"Done. {ok_count} succeeded, {fail_count} failed/warned.")
    if fail_count > 0:
        print("Review failed files and check conversion_notes in frontmatter.")
    if not args.dry_run:
        print(f"\nNext step: Inspect files in {output_root}")
        print("  Then clean and normalize before promoting to Tier 3 (corpus/).")


if __name__ == "__main__":
    main()
