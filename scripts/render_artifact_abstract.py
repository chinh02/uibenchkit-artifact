#!/usr/bin/env python3
"""Render the ASE artifact abstract Markdown as a compact two-page PDF."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


URL_RE = re.compile(r"https?://[^\s<]+")


def inline_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`(.+?)`", r'<font name="Courier">\1</font>', escaped)
    return URL_RE.sub(lambda match: f'<link href="{match.group(0)}">{match.group(0)}</link>', escaped)


def footer(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(18 * mm, 10 * mm, "UIBenchKit ASE 2026 Artifact")
    canvas.drawRightString(192 * mm, 10 * mm, f"Page {document.page}")
    canvas.restoreState()


def render(source: Path, destination: Path) -> None:
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        alignment=TA_CENTER,
        spaceAfter=5,
        textColor=colors.HexColor("#111111"),
    )
    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=10.2,
        leading=12.5,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True,
        textColor=colors.HexColor("#17365D"),
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.1,
        leading=11.6,
        spaceAfter=4,
        textColor=colors.HexColor("#222222"),
    )

    story = []
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph_lines:
            story.append(Paragraph(inline_markup(" ".join(paragraph_lines)), body))
            paragraph_lines.clear()

    first_heading = True
    for raw_line in source.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            continue
        if line.startswith("# "):
            flush_paragraph()
            text = line[2:]
            if first_heading:
                story.append(Paragraph(inline_markup(text), title))
                story.append(Spacer(1, 1.5 * mm))
                first_heading = False
            else:
                story.append(Paragraph(inline_markup(text), heading))
        else:
            paragraph_lines.append(line)
    flush_paragraph()

    destination.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(destination),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=17 * mm,
        title="UIBenchKit ASE 2026 Artifact Abstract",
        author="UIBenchKit Team",
        subject="ASE 2026 artifact evaluation",
    )
    document.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "ARTIFACT-ABSTRACT.md"
    output_path = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else root / "output" / "pdf" / "UIBenchKit-ASE2026-Artifact-Abstract.pdf"
    )
    render(source_path, output_path)
