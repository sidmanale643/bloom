#!/usr/bin/env python3
"""
bloom-graph.py - Generate a connection graph of the entire Bloom vault.

Usage:
    python scripts/bloom-graph.py

Output:
    wiki/_meta/graph.md - Mermaid diagram + structured analysis

Parses plain key-value frontmatter and ## Connections sections from all
wiki/ and sources/ .md files. Builds nodes and edges from:
  - Related:   (concept -> concept)
  - Sources:   (concept -> source)
  - Connections (source -> source/concept/query)
  - Keyword overlap (implicit edges between nodes sharing keywords)
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
VAULT_ROOT = Path(__file__).parent.parent.resolve()
WIKI_DIR = VAULT_ROOT / "wiki"
SOURCES_DIR = VAULT_ROOT / "sources"
OUTPUT_PATH = WIKI_DIR / "_meta" / "graph.md"
LOG_PATH = WIKI_DIR / "_meta" / "log.md"

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Node:
    slug: str
    title: str
    node_type: str  # concept, source, query, person, meta
    area: str
    keywords: List[str] = field(default_factory=list)

@dataclass
class Edge:
    source: str
    target: str
    relation: str  # related, sources, connects, keyword
    label: str = ""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(title: str) -> str:
    """Create a mermaid-safe ID from a note title."""
    s = title.strip()
    # Remove file extension if present
    if s.endswith(".md"):
        s = s[:-3]
    # Replace spaces and special chars with underscores, keep alphanumerics
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "_", s)
    # Ensure valid mermaid ID (must start with letter or underscore)
    s = s.strip("_")
    if s and s[0].isdigit():
        s = "_" + s
    return s or "node"


def extract_wikilinks(text: str) -> List[str]:
    """Extract [[Title]] links, stripping optional path prefixes."""
    links = []
    for match in re.finditer(r"\[\[([^\]]+)\]\]", text):
        raw = match.group(1)
        # Strip path prefix like VaultName/Path/Note Title
        if "/" in raw:
            raw = raw.split("/")[-1]
        links.append(raw.strip())
    return links


def parse_frontmatter(content: str) -> Dict[str, str]:
    """Parse plain key-value frontmatter (not YAML). Stops at first '---'."""
    lines = content.splitlines()
    fm: Dict[str, str] = {}
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            break
        if ":" in stripped and not stripped.startswith("#"):
            # Split only on first colon
            key, val = stripped.split(":", 1)
            fm[key.strip().lower()] = val.strip()
    return fm


def parse_connections_section(content: str) -> List[Tuple[str, str]]:
    """
    Parse ## Connections section in source notes.
    Returns list of (linked_title, description_or_empty).
    """
    lines = content.splitlines()
    in_connections = False
    results: List[Tuple[str, str]] = []
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("## connections"):
            in_connections = True
            continue
        if in_connections:
            # Stop at next h2 or empty section end
            if stripped.startswith("## ") and not stripped.lower().startswith("## connections"):
                break
            if stripped == "":
                continue
            # Match bullet with wikilink: - [[Title]] — description
            m = re.match(r"[-*]\s+\[\[([^\]]+)\]\]\s*(?:[—\-–]\s*(.*))?", stripped)
            if m:
                title = m.group(1).strip()
                desc = (m.group(2) or "").strip()
                # Strip path prefix
                if "/" in title:
                    title = title.split("/")[-1]
                results.append((title, desc))
            else:
                # Fallback: just grab any wikilinks in the line
                for link in extract_wikilinks(stripped):
                    results.append((link, ""))
    return results


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def scan_directory(directory: Path, node_type: str) -> Dict[str, Node]:
    """Scan a directory for .md files and build Node objects from frontmatter."""
    nodes: Dict[str, Node] = {}
    if not directory.exists():
        return nodes
    for filepath in directory.rglob("*.md"):
        if filepath.name.startswith("."):
            continue
        # Skip _meta directory for node creation (meta files are not part of the graph)
        if "_meta" in str(filepath.relative_to(VAULT_ROOT)):
            continue
        content = filepath.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)

        title = filepath.stem  # filename without .md
        # Use 'Type' frontmatter to override inferred type
        detected_type = fm.get("type", "")
        if detected_type.startswith("#type/"):
            detected_type = detected_type.replace("#type/", "")
        node_type_final = detected_type or node_type

        area = fm.get("area", "")
        if area.startswith("#area/"):
            area = area.replace("#area/", "")

        # Parse keywords
        kw_raw = fm.get("keyword", "")
        keywords = [k.replace("#keyword/", "") for k in kw_raw.split() if k.startswith("#keyword/")]

        slug = slugify(title)
        node = Node(
            slug=slug,
            title=title,
            node_type=node_type_final,
            area=area,
            keywords=keywords,
        )
        nodes[title] = node
    return nodes


def build_graph(wiki_nodes: Dict[str, Node], source_nodes: Dict[str, Node]) -> Tuple[Dict[str, Node], List[Edge]]:
    """
    Build the complete graph by scanning all files for edges.
    Returns (all_nodes, edges).
    """
    all_nodes = {**wiki_nodes, **source_nodes}
    edges: List[Edge] = []
    edge_set: Set[Tuple[str, str, str]] = set()  # dedup

    def add_edge(source_title: str, target_title: str, relation: str, label: str = ""):
        s = slugify(source_title)
        t = slugify(target_title)
        key = (s, t, relation)
        if key not in edge_set and s != t:
            edge_set.add(key)
            edges.append(Edge(source=s, target=t, relation=relation, label=label))

    # 1. Parse frontmatter edges from wiki files (Related, Sources)
    for title, node in wiki_nodes.items():
        filepath = WIKI_DIR / (title + ".md")
        if not filepath.exists():
            continue
        content = filepath.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)

        # Related: links
        related_raw = fm.get("related", "")
        for link in extract_wikilinks(related_raw):
            if link in all_nodes:
                add_edge(title, link, "related")

        # Sources: links
        sources_raw = fm.get("sources", "")
        for link in extract_wikilinks(sources_raw):
            if link in all_nodes:
                add_edge(title, link, "sources")

    # 2. Parse Connections sections from source files
    for title, node in source_nodes.items():
        filepath = SOURCES_DIR / (title + ".md")
        if not filepath.exists():
            continue
        content = filepath.read_text(encoding="utf-8")
        for linked_title, desc in parse_connections_section(content):
            if linked_title in all_nodes:
                add_edge(title, linked_title, "connects", desc[:30] if desc else "")

    # 3. Parse Connections sections from wiki files (some concepts might have them too)
    for title, node in wiki_nodes.items():
        filepath = WIKI_DIR / (title + ".md")
        if not filepath.exists():
            continue
        content = filepath.read_text(encoding="utf-8")
        for linked_title, desc in parse_connections_section(content):
            if linked_title in all_nodes:
                add_edge(title, linked_title, "connects", desc[:30] if desc else "")

    # 4. Keyword overlap edges (implicit connections)
    keyword_to_nodes: Dict[str, List[str]] = defaultdict(list)
    for title, node in all_nodes.items():
        for kw in node.keywords:
            keyword_to_nodes[kw].append(title)

    for kw, titles in keyword_to_nodes.items():
        if len(titles) < 2:
            continue
        # Add edges between all pairs sharing this keyword
        for i in range(len(titles)):
            for j in range(i + 1, len(titles)):
                t1, t2 = titles[i], titles[j]
                # Only add if not already connected by explicit edge
                s1, s2 = slugify(t1), slugify(t2)
                if (s1, s2, "related") not in edge_set and (s2, s1, "related") not in edge_set and \
                   (s1, s2, "sources") not in edge_set and (s2, s1, "sources") not in edge_set and \
                   (s1, s2, "connects") not in edge_set and (s2, s1, "connects") not in edge_set:
                    add_edge(t1, t2, "keyword", kw)

    return all_nodes, edges


# ---------------------------------------------------------------------------
# Mermaid generation
# ---------------------------------------------------------------------------

def generate_mermaid(nodes: Dict[str, Node], edges: List[Edge]) -> str:
    """Generate a mermaid flowchart TD string."""
    lines: List[str] = ["graph TD"]

    # Node definitions with styling
    type_shapes = {
        "concept": ("([", "])"),
        "source": ("[", "]"),
        "person": ("((", "))"),
        "query": ("{", "}"),
        "meta": ("[/", "/]"),
    }

    for title, node in nodes.items():
        open_shape, close_shape = type_shapes.get(node.node_type, ("[", "]"))
        label = node.title.replace('"', '#quot;')
        lines.append(f"    {node.slug}{open_shape}\"{label}\"{close_shape}")

    # Class definitions for coloring
    lines.append("")
    lines.append("    classDef concept fill:#e1f5fe,stroke:#01579b,stroke-width:2px")
    lines.append("    classDef source fill:#f3e5f5,stroke:#4a148c,stroke-width:1px")
    lines.append("    classDef person fill:#e8f5e9,stroke:#1b5e20,stroke-width:1px")
    lines.append("    classDef query fill:#fff3e0,stroke:#e65100,stroke-width:1px")
    lines.append("    classDef meta fill:#eceff1,stroke:#263238,stroke-width:1px")
    lines.append("")

    # Assign classes
    class_groups: Dict[str, List[str]] = defaultdict(list)
    for title, node in nodes.items():
        class_groups[node.node_type].append(node.slug)
    for ntype, slugs in class_groups.items():
        lines.append(f"    class {','.join(slugs)} {ntype}")
    lines.append("")

    # Edges
    for edge in edges:
        label = edge.label.replace('"', '#quot;') if edge.label else edge.relation
        if edge.relation == "related":
            lines.append(f"    {edge.source} -->|\"{label}\"| {edge.target}")
        elif edge.relation == "sources":
            lines.append(f"    {edge.source} -.->|\"{label}\"| {edge.target}")
        elif edge.relation == "connects":
            lines.append(f"    {edge.source} -->|\"connects\"| {edge.target}")
        elif edge.relation == "keyword":
            lines.append(f"    {edge.source} ==>|\"{label}\"| {edge.target}")
        else:
            lines.append(f"    {edge.source} -->|\"{label}\"| {edge.target}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Analysis sections
# ---------------------------------------------------------------------------

def generate_analysis(nodes: Dict[str, Node], edges: List[Edge]) -> str:
    """Generate markdown analysis sections."""
    lines: List[str] = []

    # Stats
    lines.append("## Stats")
    lines.append("")
    lines.append(f"- **Nodes**: {len(nodes)}")
    lines.append(f"- **Edges**: {len(edges)}")

    # Count by type
    type_counts: Dict[str, int] = defaultdict(int)
    for n in nodes.values():
        type_counts[n.node_type] += 1
    lines.append(f"- **By type**: " + ", ".join(f"{k}: {v}" for k, v in sorted(type_counts.items())))

    # Avg connections
    degree: Dict[str, int] = defaultdict(int)
    for e in edges:
        degree[e.source] += 1
        degree[e.target] += 1
    avg_degree = sum(degree.values()) / len(nodes) if nodes else 0
    lines.append(f"- **Avg connections per node**: {avg_degree:.1f}")
    lines.append("")

    # Orphans (nodes with 0 or 1 connection)
    lines.append("## Orphans")
    lines.append("")
    lines.append("Nodes with fewer than 2 connections (concepts should link to at least 2 existing concepts).")
    lines.append("")
    orphans = [(title, node) for title, node in nodes.items() if degree[node.slug] < 2]
    if orphans:
        for title, node in sorted(orphans, key=lambda x: x[1].node_type):
            lines.append(f"- [[{title}]] ({node.node_type}) — {degree[node.slug]} connection(s)")
    else:
        lines.append("No orphans found.")
    lines.append("")

    # Keyword clusters
    lines.append("## Keyword Clusters")
    lines.append("")
    lines.append("Groups of nodes sharing keywords.")
    lines.append("")
    keyword_to_nodes: Dict[str, List[str]] = defaultdict(list)
    for title, node in nodes.items():
        for kw in node.keywords:
            keyword_to_nodes[kw].append(title)

    for kw, titles in sorted(keyword_to_nodes.items(), key=lambda x: -len(x[1])):
        if len(titles) >= 2:
            lines.append(f"- **{kw}**: " + ", ".join(f"[[{t}]]" for t in titles))
    lines.append("")

    # Dense connections (most connected nodes)
    lines.append("## Hubs")
    lines.append("")
    lines.append("Nodes with the highest degree (most connected).")
    lines.append("")
    sorted_nodes = sorted(nodes.items(), key=lambda x: degree[x[1].slug], reverse=True)
    for title, node in sorted_nodes[:10]:
        if degree[node.slug] > 0:
            lines.append(f"- [[{title}]] — {degree[node.slug]} connections")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("[bloom-graph] Scanning vault...")

    wiki_nodes = scan_directory(WIKI_DIR, "meta")
    source_nodes = scan_directory(SOURCES_DIR, "source")

    print(f"[bloom-graph] Found {len(wiki_nodes)} wiki nodes, {len(source_nodes)} source nodes")

    all_nodes, edges = build_graph(wiki_nodes, source_nodes)
    print(f"[bloom-graph] Built graph: {len(all_nodes)} nodes, {len(edges)} edges")

    mermaid = generate_mermaid(all_nodes, edges)
    analysis = generate_analysis(all_nodes, edges)

    # Write output
    today = "2026-05-04"  # In a real script, use datetime.today().isoformat()
    # Actually let's use real date
    import datetime
    today = datetime.date.today().isoformat()

    output_content = f"""Type: #type/meta
Area: #area/meta
Keyword:
Date created: [[{today}]]

---

Vault connection graph. Regenerated by `/bloom-graph`. Do not edit manually.

```mermaid
{mermaid}
```

{analysis}
"""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(output_content, encoding="utf-8")
    print(f"[bloom-graph] Written to {OUTPUT_PATH}")

    # Append to log
    log_entry = f"\n## [{today}] graph | Bloom vault connection graph\n\nGenerated graph with {len(all_nodes)} nodes and {len(edges)} edges. See [[graph]].\n"
    if LOG_PATH.exists():
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(log_entry)
    print(f"[bloom-graph] Appended to {LOG_PATH}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
