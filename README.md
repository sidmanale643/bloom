![Bloom](docs/image.png)

# Bloom

A living knowledge vault managed by Claude. You gather raw material; Claude shapes it into a wiki of interconnected concepts, unresolved questions, and emergent themes.

Inspired by [Andrej Karpathy's LLM wiki pattern](https://x.com/karpathy/status/2039805659525644595): feed in unprocessed documents, and an LLM progressively distils them into concept articles with dense backlinks, turning the wiki into fertile ground for research and discovery.

## Quick start

1. **Clone this repo** and open it in [Obsidian](https://obsidian.md) as a vault
2. **Install Claude Code** — [claude.ai/code](https://claude.ai/code) (or whichever agent you prefer)
3. **Drop something into `inbox/`** — a URL, a web clipping (via [Obsidian Web Clipper](https://obsidian.md/clipper)), a PDF, or plain text
4. **Run `/bloom-ingest`** — Claude turns everything in the inbox into detailed, topic-by-topic source notes and moves the originals to `residuals/`
5. **Run `/bloom-compile`** — Claude hunts for themes that surface in two or more sources and assembles concept articles
6. **Run `/bloom-ask`** followed by a question — Claude investigates across the vault and drafts a report

That's the loop. Drop, ingest, compile. The vault compounds on its own.

## How it works

### Three layers

| Directory | Purpose | Who writes |
|---|---|---|
| `inbox/` | Staging for unprocessed drops (URLs, clippings, PDFs, pasted text) | You |
| `sources/` | Detailed source notes — one per article/paper/transcript. Broken down topic-by-topic with overview, key takeaways, and connections | Claude |
| `wiki/` | Concept articles, people pages, query reports, index, log, and health | Claude |
| `residuals/` | Processed inbox items kept as originals; never edited | Claude |

### The contract

You decide what enters. Claude owns everything downstream. That boundary is deliberate — your judgement filters what deserves attention, while Claude handles the synthesis that would exhaust a human at scale.

### The 2-source rule

A single source is never enough for a concept. Themes are parked as **candidates** in `wiki/_meta/index.md` until another source independently corroborates them. This stops the wiki from bloating with half-baked ideas.

### What compounds

- **Sources** stack up as the raw substrate
- **Concepts** harden where patterns repeat
- **Queries** (`/bloom-ask`) generate research reports filed back into the wiki — every question enriches the whole
- **Sessions** (`/save`) capture working conversations as narrative wiki pages
- **Graphs** (`/bloom-graph`) visualise the entire vault as a connection network
- **Research threads** surface once three or more concepts cluster around the same keywords

## The six commands

| Command | What it does |
|---|---|
| `/bloom-ingest` | Turn inbox items into source notes, then move originals to `residuals/`. Auto-fetches YouTube transcripts and extracts web content from URLs |
| `/bloom-compile` | Forge or expand concept articles from un-compiled sources |
| `/bloom-ask` | Probe the vault with a question and write up the findings |
| `/bloom-lint` | Audit the vault: statistics, orphans, keyword drift |
| `/bloom-graph` | Generate a mermaid connection graph of the entire vault |
| `/save` | Capture the current Claude conversation as a narrative wiki page |

## Features

### Smart ingest
- **YouTube URLs** — transcripts fetched automatically via `youtube-transcript-api`
- **ArXiv papers** — HTML pages are fetched into filtered reading packets that preserve equations, figures, tables, methods, and results while stripping bibliography noise
- **Non-YouTube URLs** — content extracted via trafilatura (`scripts/bloom-fetch.py`)
- Falls back to `webfetch` if extraction fails

### Companion vault (optional)
Link a personal vault (commonplace, Zettelkasten, or notes folder) as read-only. Claude cross-references your notes during compilation but never modifies them. See `AGENTS.md` for setup.

### Connection graph
`/bloom-graph` runs `python3 scripts/bloom-graph.py` and writes a mermaid diagram to `wiki/_meta/graph.md` with nodes styled by type, edges from backlinks and keyword overlap, orphans, hubs, and keyword clusters.

### Mermaid diagrams
Inline ` ```mermaid ``` ` blocks inside any note. Notes with diagrams are tracked in `wiki/_meta/index.md`. No Excalidraw dependency.

### People pages
Three-tier system: always create on ingest for authors, create richer profiles for subjects, use wikilinks for passing references until the second independent citation.

### Front-matter
Plain key-value lines (not YAML). One `#type/` per note. Types: `source`, `concept`, `query`, `person`, `session`, `meta`.

## What's included

Sample notes so you can see the structure in action:

- `sources/HTTP Protocol for Backend Engineers.md` — a full source note on HTTP statelessness, methods, headers, and security
- `wiki/2026-05-04-what-is-http.md` — a query report answering "what is HTTP", referencing the source above
- `residuals/http.md` — the raw transcript that was ingested to produce the source note

Remove these and wipe `wiki/_meta/index.md` once you have the hang of it, or leave them as seeds.

## Schema

Every operational rule lives in `AGENTS.md`. That file is the canonical spec. Read it to understand the system, or edit it to bend the rules. `CLAUDE.md` contains the skill trigger bindings and per-session instructions.

## Customisation

- **Areas**: Tweak the `#area/` taxonomy in `AGENTS.md` to reflect your own domains
- **Keywords**: Curated in `wiki/_meta/index.md` — expand as your reading deepens
- **Voice**: Concepts are rough scaffolding for your prose, not finished pieces. Adjust the voice guidance in `AGENTS.md` for a different register

---

Built with [Claude Code](https://claude.ai/code) and [Obsidian](https://obsidian.md).
