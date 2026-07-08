#!/usr/bin/env python3
"""
Movemental PDF render script.

Two-pass Playwright Chromium render:
  Pass 1 — cover only, no header/footer, zero margins.
  Pass 2 — body only, with running header/footer, page-numbered.
  Then pypdf concatenates them into the final document.

Usage:
  python3 render.py path/to/document.html
  python3 render.py path/to/document.html --keep-intermediates
  python3 render.py path/to/document.html --output custom.pdf

The HTML file is expected to contain:
  - <section class="cover"> for the title page
  - one or more <section class="page"> for body content
  - A reference to logo.png (relative to the HTML) for the running header

Customize header/footer text by editing the constants below.
"""

import argparse, base64, pathlib, shutil, subprocess, sys
from playwright.sync_api import sync_playwright


# The skill's bundled assets live one level up from this scripts/ directory.
SKILL_ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"


# ============================================================
# Customize these for the document being rendered.
# ============================================================
HEADER_TITLE = "Movemental"                       # right-aligned in the running header
HEADER_KICKER = ""                                # optional small text before the title (e.g., "Field Guide")
FOOTER_LEFT = "movemental.ai"                     # left-aligned footer text
FOOTER_RIGHT_FORMAT = '<span class="pageNumber"></span>'   # right footer; can be 'Page X of Y' with .totalPages

# Body page margins (do NOT also set @page margin in the HTML)
BODY_MARGIN_TOP    = "0.75in"
BODY_MARGIN_BOTTOM = "0.6in"
BODY_MARGIN_LEFT   = "1.0in"
BODY_MARGIN_RIGHT  = "1.0in"


# ============================================================
# Build header/footer HTML templates.
# These render in Chromium's print chrome regions. Note that pageNumber
# is a Chromium-defined class — its text is injected automatically.
# ============================================================
def build_header_template(logo_data_uri: str) -> str:
    return f"""
<div style="
  -webkit-print-color-adjust: exact;
  font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  font-weight: 300; font-size: 7.5pt; color: #6b6b6b;
  width: 100%; padding: 0 {BODY_MARGIN_LEFT} 0 {BODY_MARGIN_LEFT};
  margin: 0; box-sizing: border-box;
  display: flex; align-items: center; justify-content: space-between;
">
  <div style="display:flex;align-items:center;gap:8pt;">
    <img src="{logo_data_uri}" style="height:11pt;width:auto;opacity:0.85;" />
    {f'<span style="letter-spacing:0.18em;text-transform:uppercase;font-weight:500;color:#444;">{HEADER_KICKER}</span>' if HEADER_KICKER else ''}
  </div>
  <div style="letter-spacing:0.20em;text-transform:uppercase;color:#666;">
    {HEADER_TITLE}
  </div>
</div>
"""


def build_footer_template() -> str:
    return f"""
<div style="
  font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  font-weight: 300; font-size: 7.5pt; color: #6b6b6b;
  width: 100%; padding: 0 {BODY_MARGIN_LEFT} 0 {BODY_MARGIN_LEFT};
  margin: 0; box-sizing: border-box;
  display: flex; align-items: center; justify-content: space-between;
">
  <div style="letter-spacing:0.18em;text-transform:uppercase;color:#999;font-weight:500;">
    {FOOTER_LEFT}
  </div>
  <div style="font-variant-numeric:tabular-nums;">{FOOTER_RIGHT_FORMAT}</div>
</div>
"""


def stage_assets(workdir: pathlib.Path) -> None:
    """Copy the skill's bundled logo + fonts next to the HTML if they aren't already there.

    Lets freshly written HTML use the simple local-copy paths (`logo.png`,
    `fonts/inter-300.woff2`) without the author hand-copying anything. Skipped
    entirely when --no-stage is passed (for HTML that points at ../assets/...).
    Existing files are never overwritten.
    """
    if not SKILL_ASSETS.exists():
        return  # nothing bundled to stage; logo resolution below will report if needed

    src_logo = SKILL_ASSETS / "logo.png"
    dst_logo = workdir / "logo.png"
    if src_logo.exists() and not dst_logo.exists():
        shutil.copy2(src_logo, dst_logo)

    src_fonts = SKILL_ASSETS / "fonts"
    dst_fonts = workdir / "fonts"
    if src_fonts.is_dir():
        dst_fonts.mkdir(exist_ok=True)
        for woff in src_fonts.glob("*.woff2"):
            target = dst_fonts / woff.name
            if not target.exists():
                shutil.copy2(woff, target)


def render(html_path: pathlib.Path, output_path: pathlib.Path,
           keep_intermediates: bool = False, stage: bool = True) -> pathlib.Path:
    html_path = html_path.resolve()
    output_path = output_path.resolve()
    workdir = html_path.parent

    if stage:
        stage_assets(workdir)

    cover_pdf = workdir / "_cover.pdf"
    body_pdf = workdir / "_body.pdf"

    # The logo is loaded by the HTML itself; for the header template we also need it
    # as a base64 data URI (Chromium's header templates run in a stripped-down context
    # that may not resolve relative file:// URLs). Prefer the staged copy next to the
    # HTML, then fall back to the skill's bundled asset.
    logo_path = workdir / "logo.png"
    if not logo_path.exists():
        logo_path = SKILL_ASSETS / "logo.png"
    if not logo_path.exists():
        sys.exit(f"error: logo.png not found in {workdir} or {SKILL_ASSETS} "
                 f"(run without --no-stage, or copy it from the skill's assets/ directory)")
    logo_data_uri = "data:image/png;base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")

    header_template = build_header_template(logo_data_uri)
    footer_template = build_footer_template()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context()

        # ---------- Pass 1: cover only ----------
        page = ctx.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.add_style_tag(content="section.page { display: none !important; }")
        # Ensure web fonts are fully loaded before rendering
        page.evaluate("document.fonts && document.fonts.ready")
        page.pdf(
            path=str(cover_pdf),
            format="Letter",
            print_background=True,
            display_header_footer=False,
            margin={"top": "0in", "bottom": "0in", "left": "0in", "right": "0in"},
        )
        page.close()

        # ---------- Pass 2: body only ----------
        page2 = ctx.new_page()
        page2.goto(html_path.as_uri(), wait_until="networkidle")
        page2.add_style_tag(content="section.cover { display: none !important; }")
        page2.evaluate("document.fonts && document.fonts.ready")
        page2.pdf(
            path=str(body_pdf),
            format="Letter",
            print_background=True,
            display_header_footer=True,
            header_template=header_template,
            footer_template=footer_template,
            margin={
                "top": BODY_MARGIN_TOP,
                "bottom": BODY_MARGIN_BOTTOM,
                "left": BODY_MARGIN_LEFT,
                "right": BODY_MARGIN_RIGHT,
            },
        )
        page2.close()
        browser.close()

    # ---------- Merge ----------
    try:
        from pypdf import PdfWriter, PdfReader
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "pypdf"],
            check=True, capture_output=True,
        )
        from pypdf import PdfWriter, PdfReader

    writer = PdfWriter()
    for src in (cover_pdf, body_pdf):
        for pg in PdfReader(str(src)).pages:
            writer.add_page(pg)
    with open(output_path, "wb") as f:
        writer.write(f)

    if not keep_intermediates:
        cover_pdf.unlink(missing_ok=True)
        body_pdf.unlink(missing_ok=True)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Render a Movemental-branded PDF from an HTML source.")
    parser.add_argument("html", help="path to the input HTML file")
    parser.add_argument("--output", "-o", help="output PDF path (default: alongside input, same stem)")
    parser.add_argument("--keep-intermediates", action="store_true", help="keep _cover.pdf and _body.pdf for debugging")
    parser.add_argument("--no-stage", action="store_true", help="do not copy the skill's bundled logo/fonts next to the HTML (use when the HTML references ../assets/... directly)")
    args = parser.parse_args()

    html_path = pathlib.Path(args.html)
    if not html_path.exists():
        sys.exit(f"error: {html_path} not found")

    output_path = pathlib.Path(args.output) if args.output else html_path.with_suffix(".pdf")
    result = render(html_path, output_path, keep_intermediates=args.keep_intermediates, stage=not args.no_stage)

    from pypdf import PdfReader
    pages = len(PdfReader(str(result)).pages)
    print(f"Rendered: {result} · {result.stat().st_size:,} bytes · {pages} pages")


if __name__ == "__main__":
    main()
