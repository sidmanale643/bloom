#!/usr/bin/env python3
"""
web_fetch.py - Scrape text and articles from the web.

Usage:
    python scripts/web_fetch.py

Output:
    wiki/_meta/graph.md - Mermaid diagram + structured analysis

Parses plain key-value frontmatter and ## Connections sections from all
wiki/ and sources/ .md files. Builds nodes and edges from:
  - Related:   (concept -> concept)
  - Sources:   (concept -> source)
  - Connections (source -> source/concept/query)
  - Keyword overlap (implicit edges between nodes sharing keywords)
"""