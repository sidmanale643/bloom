#!/usr/bin/env python3
"""Fetch and extract web article content using trafilatura.

Usage:
    uvx --with trafilatura python3 scripts/bloom-fetch.py <url>
    uvx --with trafilatura python3 scripts/bloom-fetch.py --inbox <url>

Default: output to stdout.
With --inbox: write to inbox/<Title>.md and print the path to stdout.
"""

import re
import sys
from pathlib import Path

import trafilatura


def sanitize_title(title):
    return re.sub(r"[/.]", "-", title).strip()


def main():
    args = sys.argv[1:]
    write_to_inbox = False

    if "--inbox" in args:
        write_to_inbox = True
        args.remove("--inbox")

    if not args:
        print(
            "Usage: uvx --with trafilatura python3 scripts/bloom-fetch.py [--inbox] <url>",
            file=sys.stderr,
        )
        sys.exit(1)

    url = args[0]

    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        print(f"Error: could not download {url}", file=sys.stderr)
        sys.exit(1)

    result = trafilatura.extract(
        downloaded,
        output_format="markdown",
        with_metadata=True,
        include_links=True,
        include_images=False,
        include_formatting=True,
    )

    if result is None:
        print(f"Error: could not extract content from {url}", file=sys.stderr)
        sys.exit(1)

    if not write_to_inbox:
        print(result)
        return

    metadata = trafilatura.extract(
        downloaded,
        output_format="json",
        with_metadata=True,
        include_links=False,
        include_images=False,
        include_formatting=False,
    )

    import json

    title = "Untitled"
    if metadata:
        try:
            meta = json.loads(metadata)
            title = meta.get("title") or meta.get("sitename") or "Untitled"
        except (json.JSONDecodeError, AttributeError):
            pass

    safe_title = sanitize_title(title)
    vault_root = Path(__file__).resolve().parent.parent
    inbox_dir = vault_root / "inbox"
    inbox_dir.mkdir(exist_ok=True)

    filepath = inbox_dir / f"{safe_title}.md"
    filepath.write_text(result, encoding="utf-8")

    print(str(filepath))


if __name__ == "__main__":
    main()