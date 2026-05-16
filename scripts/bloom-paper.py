#!/usr/bin/env python3
"""Fetch a research paper with trafilatura and write a cleaned packet to inbox/.

Usage:
    uvx --with trafilatura python3 scripts/bloom-paper.py <arxiv_url_or_id>

The script prefers arXiv HTML over PDF extraction, then uses trafilatura to
extract Markdown and removes obvious low-value sections before Bloom ingest.
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


trafilatura = None

ARXIV_ID_RE = re.compile(r"(?P<id>(?:[a-z-]+/\d{7})|(?:\d{4}\.\d{4,5}))(?:v\d+)?", re.I)
NOISE_HEADING_RE = re.compile(
    r"^(references|bibliography|acknowledg(e)?ments?|funding|"
    r"author contributions?|conflicts? of interest|competing interests?|"
    r"ethics statement|data availability statement|license|about this paper|"
    r"appendix(?:\s+[a-z0-9].*)?)$",
    re.I,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
INLINE_CITATION_RE = re.compile(r"\s*\[(?:\d+(?:\s*,\s*\d+)*|\d+\s*[-–]\s*\d+)\]")
LICENSE_LINE_RE = re.compile(r"^provided proper attribution is provided\b", re.I)
PROMPT_TEMPLATE_MARKER_RE = re.compile(
    r"^(#\s*CONTEXT:|\[!htbpPrompt Template|Prompt Template for\b)",
    re.I,
)


def sanitize_title(title):
    title = re.sub(r"\s+", " ", title or "").strip()
    title = re.sub(r"[/:]", " - ", title)
    title = re.sub(r"[\\?*\"<>|]", "", title)
    return title[:180].strip(" .") or "Untitled Paper"


def compact_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def extract_arxiv_id(value):
    match = ARXIV_ID_RE.search(value)
    return match.group("id") if match else None


def candidate_urls(value):
    arxiv_id = extract_arxiv_id(value)
    if arxiv_id:
        return [
            f"https://arxiv.org/html/{arxiv_id}",
            f"https://ar5iv.labs.arxiv.org/html/{arxiv_id}",
        ]

    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"}:
        return [value]

    return []


def load_trafilatura():
    global trafilatura
    if trafilatura is None:
        import trafilatura as trafilatura_module

        trafilatura = trafilatura_module
    return trafilatura


def extract_metadata(downloaded):
    tf = load_trafilatura()
    metadata = tf.extract(
        downloaded,
        output_format="json",
        with_metadata=True,
        include_links=False,
        include_images=False,
        include_formatting=False,
    )
    if not metadata:
        return {}
    try:
        data = json.loads(metadata)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def fetch_extract_first(urls):
    tf = load_trafilatura()
    errors = []

    for url in urls:
        downloaded = tf.fetch_url(url)
        if not downloaded:
            errors.append(f"{url}: empty download")
            continue

        markdown = tf.extract(
            downloaded,
            output_format="markdown",
            with_metadata=False,
            include_links=True,
            include_images=True,
            include_formatting=True,
            favor_precision=True,
        )
        if not markdown or len(markdown.strip()) < 2000:
            errors.append(f"{url}: extracted body too short")
            continue

        metadata = extract_metadata(downloaded)
        return url, markdown, metadata

    raise RuntimeError("Could not extract paper HTML with trafilatura:\n" + "\n".join(errors))


def normalize_heading_text(text):
    text = compact_text(text).rstrip(":")
    text = re.sub(r"^\d+(\.\d+)*\s*", "", text)
    return text


def strip_noise_sections(markdown):
    kept = []
    dropping = False
    drop_level = 0

    for line in markdown.splitlines():
        match = HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            heading = normalize_heading_text(match.group(2))

            if dropping and level <= drop_level:
                dropping = False

            if NOISE_HEADING_RE.match(heading):
                dropping = True
                drop_level = level
                continue

        if not dropping:
            kept.append(line)

    return "\n".join(kept)


def strip_citation_noise(markdown):
    lines = []
    for line in markdown.splitlines():
        if LICENSE_LINE_RE.match(line.strip()):
            continue
        line = re.sub(r"\s*\[[^\]\n]*(?:\([^)\n]*#bib\.bib[^)\n]*\)[^\]\n]*)+\]", "", line)
        line = re.sub(r"\s*\([^()\n]*(?:\([^()\n]*#bib\.bib[^()\n]*\)[^()\n]*)+\)", "", line)
        line = re.sub(r"\s*\([^()\n]*#bib\.bib[^()\n]*\)", "", line)
        line = re.sub(r"\[\s*(?:\(#bib\.[^)]+\)\s*,?\s*)+\]", "", line)
        line = re.sub(r"\[[^\]]*\]\(#bib\.[^)]+\)", "", line)
        line = re.sub(r"\s*(?:,?\s*\(#bib\.[^)]+\)\]?)+", "", line)
        line = INLINE_CITATION_RE.sub("", line)
        line = re.sub(r"\[\s*\]", "", line)
        line = re.sub(r"(?<!\))\]", "", line)
        line = re.sub(r"\s*,\s*,+", ",", line)
        line = re.sub(r"\s+,", ",", line)
        line = re.sub(r"\s+([,.;:])", r"\1", line)
        lines.append(line.rstrip())
    return "\n".join(lines)


def strip_prompt_template_tail(markdown):
    kept = []
    for line in markdown.splitlines():
        if PROMPT_TEMPLATE_MARKER_RE.match(line.strip()):
            break
        kept.append(line)
    return "\n".join(kept)


def collapse_blank_lines(markdown):
    lines = []
    previous_blank = False
    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        blank = not line
        if blank and previous_blank:
            continue
        lines.append(line)
        previous_blank = blank
    return "\n".join(lines).strip() + "\n"


def clean_markdown(markdown):
    markdown = strip_noise_sections(markdown)
    markdown = strip_citation_noise(markdown)
    markdown = strip_prompt_template_tail(markdown)
    return collapse_blank_lines(markdown)


def metadata_list(value):
    if isinstance(value, list):
        return ", ".join(compact_text(str(item)) for item in value if compact_text(str(item)))
    return compact_text(str(value)) if value else ""


def metadata_date(value, arxiv_id):
    date = compact_text(value)
    if not date:
        return ""

    if arxiv_id and re.match(r"^\d{4}\.\d{4,5}$", arxiv_id):
        yy = int(arxiv_id[:2])
        year = 2000 + yy if yy < 90 else 1900 + yy
        month = arxiv_id[2:4]
        if not date.startswith(f"{year}-{month}"):
            return ""

    return date


def title_from_metadata(metadata, arxiv_id):
    for key in ["title", "pagetitle", "sitename"]:
        value = compact_text(metadata.get(key))
        if value:
            value = re.sub(r"^(Title:\s*)", "", value, flags=re.I)
            return value
    return f"arXiv {arxiv_id}" if arxiv_id else "Untitled Paper"


def build_packet(url, markdown, metadata, original_input):
    arxiv_id = extract_arxiv_id(original_input) or extract_arxiv_id(url)
    title = title_from_metadata(metadata, arxiv_id)
    authors = metadata_list(metadata.get("author") or metadata.get("authors"))
    date = metadata_date(metadata.get("date"), arxiv_id)
    body = clean_markdown(markdown)

    if len(body) < 2000:
        raise RuntimeError("Cleaned paper body is too short; refusing partial packet")

    lines = [f"# {title}", ""]
    if authors:
        lines.extend([f"Authors: {authors}", ""])
    if date:
        lines.extend([f"Date: {date}", ""])
    if arxiv_id:
        lines.extend(
            [
                f"arXiv ID: {arxiv_id}",
                f"Canonical: https://arxiv.org/abs/{arxiv_id}",
                f"HTML: https://arxiv.org/html/{arxiv_id}",
                f"PDF: https://arxiv.org/pdf/{arxiv_id}",
                "",
            ]
        )
    lines.extend([f"Extracted from: {url}", "", "---", "", body])

    return title, collapse_blank_lines("\n".join(lines))


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: uvx --with trafilatura python3 scripts/bloom-paper.py <arxiv_url_or_id>",
            file=sys.stderr,
        )
        sys.exit(1)

    original_input = sys.argv[1]
    urls = candidate_urls(original_input)
    if not urls:
        print(f"Error: could not recognize arXiv ID or HTML URL: {original_input}", file=sys.stderr)
        sys.exit(1)

    try:
        url, markdown, metadata = fetch_extract_first(urls)
        title, packet = build_packet(url, markdown, metadata, original_input)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    vault_root = Path(__file__).resolve().parent.parent
    inbox_dir = vault_root / "inbox"
    inbox_dir.mkdir(exist_ok=True)

    filepath = inbox_dir / f"{sanitize_title(title)}.md"
    filepath.write_text(packet, encoding="utf-8")

    print(str(filepath))


if __name__ == "__main__":
    main()
