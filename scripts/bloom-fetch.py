#!/usr/bin/env python3
"""Fetch and extract web article content using trafilatura.

Usage:
    uvx --with trafilatura python3 scripts/bloom-fetch.py <url>

Output to stdout: title + date + source in frontmatter, then body as markdown.
"""

import sys
import trafilatura


def main():
    if len(sys.argv) < 2:
        print("Usage: uvx --with trafilatura python3 scripts/bloom-fetch.py <url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]

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

    print(result)


if __name__ == "__main__":
    main()
