Ingest raw material into the Bloom vault.

**Before doing anything**, read `AGENTS.md` at the vault root for the full rules of engagement. The summary below is a prompt, not the source of truth.

### What to ingest

1. Check `inbox/` for anything unprocessed. Files can be:
   - Raw `.md` clippings from Obsidian Web Clipper
   - PDFs — extract text
   - Plain URLs in a `.md` file — fetch them
   - Pasted text — treat as an article

2. If `$ARGUMENTS` contains a URL or path, ingest that specifically instead of scanning the inbox.

### YouTube URL handling

If `$ARGUMENTS` is a YouTube URL (contains `youtube.com/watch` or `youtu.be/`):

1. **Fetch and write to inbox** — run:
   ```bash
   uvx --from youtube-transcript-api python3 scripts/bloom-youtube.py "$ARGUMENTS"
   ```
   This script extracts the video ID, gets the title, fetches the transcript, and writes the raw transcript text directly to `inbox/<Video Title>.md`. It prints the output file path to stdout.

2. If the script exits with an error (transcript unavailable, no captions), fall back to the generic URL extraction flow below.

3. **Process as normal** — continue from step "Normalise into a source note"

### URL Extraction (non-YouTube)

If `$ARGUMENTS` is a URL (starts with `http://` or `https://`) and is NOT a YouTube URL:

1. **Extract and write to inbox** — run:
   ```bash
   uvx --with trafilatura python3 scripts/bloom-fetch.py --inbox "$ARGUMENTS"
   ```
   This script fetches the URL, extracts content with trafilatura, and writes the raw extracted content directly to `inbox/<Title>.md`. It prints the output file path to stdout.

2. **Process as normal** — continue from step "Normalise into a source note"

**Fallback:** If the script exits with an error or returns empty content, fall back to the `webfetch` tool once. If `webfetch` also fails or returns empty, do not retry — ask the user to manually add a transcript, text dump, or link to `inbox/` for processing.

### For each item

1. **Normalise into a source note** at `sources/<Title>.md`. Title is Title Case of the source.
2. **Fill front-matter** per CLAUDE.md:
   - `Type: #type/source`
   - `Area:` — use your best judgment (e.g. `#area/craft/<subarea>` or another top-level area from the taxonomy)
   - `Keyword:` — **read the Keywords section of `wiki/_meta/index.md` first**. Reuse existing keywords. If adding a new one, register it there with a one-line definition.
   - `Date created: [[YYYY-MM-DD]]` — today
   - `Source:` — URL or canonical reference
3. **Analyze the content** — read through the extracted content and identify distinct topics/sections
4. **Write detailed topic-by-topic notes**:
    - **Overview**: 1-2 paragraphs summarizing what this source covers
    - **IMPORTANT**: In Notes sections, state the ideas directly — not "the speaker argues X" but "X". The Overview establishes who said it; the Notes treat the topic on its own terms. This applies to Connections sections too.
    - **Topics**: Create a `### Topic Name` section for each key topic with:
      - Detailed explanations of concepts
      - Examples (code snippets, formulas, real-world applications)
      - Important nuances and details
      - Any counterpoints or debates in the field
    - **Key Takeaways**: 3-5 actionable insights or summary points
    - **Connections**: How this relates to existing knowledge in the vault — cross-reference relevant wiki concepts and companion vault notes
5. **Consider a diagram** — if the source contains visual content worth recreating (architecture diagrams, process flows, data models, etc.) or describes a system/process where a visual summary would add clarity, add a mermaid diagram under `## Diagram` at the end of the source note. Default: only when helpful and needed.
6. **Create a people page** if the source has an author and no page exists in `wiki/` yet. Keep it thin — a connector node, not an essay. See CLAUDE.md for the three-tier rule.
7. **Cross-reference the companion vault** (if one is configured in CLAUDE.md): scan for notes on the same topic. If any match, mention them in the Connections section using `[[VaultName/Path/Title]]` style links. Never write into the companion vault.
8. **Clear the inbox**: move the original to `residuals/` once the source note is written.

### Logging

Append to `wiki/_meta/log.md`:

```
## [YYYY-MM-DD] ingest | <one-line descriptor>
- Sources: [[Title]] — one-line descriptor
- Noticed: anything surprising — candidate themes, unusual keywords, contradictions with existing notes
```

Also update the relevant sections of `wiki/_meta/index.md`:
- Add the new source to the Sources catalog
- Increment keyword counts
- If a recurring theme appeared across 2+ sources, add it to Candidates for the compile loop to promote

### Hard rules

- Never write into the companion vault (if configured). Read only.
- Don't create concept articles in this command — that's the compile loop's job. Just get the source notes in clean.
- If the inbox is empty and no argument is given, say so and stop. Don't invent work.

### Arguments

`$ARGUMENTS` — optional. A URL, file path, or keyword. If present, ingest that specific thing. If empty, scan the inbox.
