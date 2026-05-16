# Bloom - An Agent-Run Obsidian Vault

This is an autonomous knowledge vault maintained by Codex. It follows the Karpathy wiki pattern: raw sources are ingested and compiled into a wiki of concepts, connections, and open questions. This file is the single source of truth for how Codex operates inside it.

---

## Companion vault (optional)

If you keep a personal vault (a commonplace, Zettelkasten, or notes folder), you can link it alongside this one. The contract:

- **Your vault** — read-only for Codex. Never write, edit, move, or delete anything there. Cross-link into it with `[[YourVault/Path/Note Title]]` style references when a Bloom note is informed by your writing.
- **Bloom** — Codex writes, maintains, reorganises. You read, query, and occasionally correct.

One-way read, cross-linkable. That's the contract. If you don't have a companion vault, Bloom works fine standalone.

---

## Directory structure

Three layers, following the Karpathy wiki pattern:

| Directory | Purpose | Who writes |
|---|---|---|
| `inbox/` | Staging for unprocessed drops (PDFs, URLs, screenshots, pasted text) | You drop, Codex moves to residuals after ingest |
| `sources/` | Immutable atomic source notes — one per article/paper/transcript | Codex on ingest; minor edits only after creation |
| `wiki/` | LLM-maintained pages: concepts, queries, sessions, people, index, log, health | Codex maintains |
| `residuals/` | Processed inbox items kept as originals; never edited by Codex | Codex moves here after ingest |

Special files in `wiki/_meta/`:
- **`index.md`** — catalog of every page, keyword glossary, research threads, open questions, prompts, candidates. Codex reads this first when answering a query. Updated on every operation.
- **`log.md`** — append-only chronological record. Each entry: `## [YYYY-MM-DD] operation | Title`. Never rewritten, only appended.
- **`health.md`** — lint dashboard. Overwritten each `/bloom-lint` run.

---

## File naming

- **Source notes**: Title Case — `The Rosetta Stone of Design Engineering.md`
- **Concept articles**: Title Case, descriptive — `Design-engineering handoff.md`
- **People**: `FirstName LastName.md` with hyphens only inside compound names. If surname unknown, `FirstName.md` and note the uncertainty.
- **Queries**: `YYYY-MM-DD-slug.md`
- No emoji, no unicode hacks, no date prefixes in titles (dates go in front-matter)

---

## Front-matter

Plain key-value lines, not YAML. Blank line then `---` then body.

Note from @jameesy: This is very personal to the way I like to use Obsidian, and the way that I use tags across vaults. You can change to a different style here to suit however you are currently working.

**Source notes (`sources/`):**
```
Type: #type/source
Area: #area/craft/ai
Keyword: #keyword/knowledge-management #keyword/llms
Date created: [[2026-04-14]]
Source: https://example.com/article

---

## Overview

2–4 paragraphs. Not a summary — a reconstruction. Who wrote this, in what context, and why it matters. What is the central argument or purpose? What assumptions does it rest on? What does it leave unresolved? Write this as if the reader will never see the original.

## Notes

One section per major topic in the source. Each section is a self-contained set of detailed notes — not bullets lifted from the text, but your own restatement of the ideas with enough depth to replace reading the original.

Notes should treat the topic directly. The Overview establishes the source context (who, what medium); the Notes section speaks about the ideas themselves. Avoid framing like "the speaker argues", "the video shows", "the author writes", or "the article says" — state the content on its own terms. The same rule applies to Connections sections: say "both advocate cause-and-effect reasoning" not "mirrors the video's insistence".

For each topic, cover as many of the following as the source warrants:
- What the concept is and how the author defines or frames it
- The reasoning or evidence behind it (mechanism, argument, data, example)
- Edge cases, caveats, or tensions the author acknowledges
- Concrete examples, analogies, or case studies from the source
- Any formulas, frameworks, or step-by-step processes described
- How this topic connects to or complicates adjacent ideas in the source

Aim for density over completeness. One rich paragraph beats five thin bullets. Preserve the author's distinctions — don't collapse nuance for the sake of brevity.

### Topic Name

[Detailed notes here]

### Another Topic

[Detailed notes here]

## Key Takeaways

3–5 sharp, claim-shaped sentences. Each one should be something a reader could disagree with. Not "the author discusses X" — "X implies Y."

## Connections

How this source speaks to existing notes in the vault. Name specific concept pages, source notes, or (if using a companion vault) your own writing that this source confirms, complicates, or extends. Flag genuine tensions — don't smooth them over.

## Diagram

If the source contains visual content (architecture diagrams, process flows, data models, etc.) or describes a system/process where a visual summary would add clarity, add a mermaid diagram here.

```mermaid
```

If no diagram is needed, omit this section entirely. Default: only when helpful and needed.
```

**Wiki pages — concepts (`wiki/`):**
```
Type: #type/concept
Area: #area/craft/ai
Keyword: #keyword/knowledge-management
Date created: [[2026-04-14]]
Sources: [[Source One]], [[Source Two]]
Related: [[Concept A]], [[Concept B]]

---
```
Body: `What it is` > `Why it matters` > `Key points` > `Evidence across sources` > `Open questions` > `Prompts`.

**Voice for concepts.** The Bloom gives you a *foundation* for your own writing — not a finished essay. Favour sharp one-liners, evidence citations, and open questions over flowing prose. Key points should be pithy — one line each, claim-shaped. When in doubt, write less.

**Prompts.** Essay-shaped prompts where the concept intersects your existing notes or thinking. Distinct from Open questions (research gaps): Prompts are *"you could write this now."* One or two sentences each, pointed and specific. Empty is fine.

**Wiki pages — queries:**
```
Type: #type/query
Area: #area/craft/management
Keyword: #keyword/leadership
Date created: [[2026-04-14]]
Question: the question asked

---
```

**Wiki pages — people:**
```
Type: #type/person
Area: #area/craft/ai
Keyword: #keyword/llms
Date created: [[2026-04-14]]

---

One-line identifier. Topic description.

**Sources in Bloom**
- [[Source Title]]

**Concepts they inform**
- [[Concept Title]]
```

---

## Tag taxonomy

Hierarchical sub-areas under Craft. Customise the top-level areas to match your life.

**`#area/`** — examples: Self, Craft, Work, Health, Finances, Meta (use whatever top-level areas fit your life)
**`#area/craft/`** — design, engineering, management, ai, product, writing

**`#type/`** — each note gets exactly one:
- `source` — an ingested external source (in `sources/`)
- `concept` — a synthesised wiki page built from 2+ sources
- `query` — a research report answering a question
- `person` — an entity page for a thinker/author
- `session` — a narrative reconstruction of a Codex conversation
- `meta` — vault infrastructure (index, log, health)

**`#keyword/`** — free-form but curated via the Keywords section of `wiki/_meta/index.md`. Before creating a new keyword:
1. Check `wiki/_meta/index.md`
2. If a near-match exists, reuse it
3. If genuinely new, add it to the Keywords section with a one-line definition

---

## People — when to create a page

Three tiers:

| Tier | Trigger | Action |
|---|---|---|
| Author | Person authored a source in `sources/` | Always create a page in `wiki/` on ingest |
| Subject | Source is substantively about a person | Create page with a richer profile |
| Passing reference | Mentioned in passing | Use `[[Name]]` wikilink without creating a file. Create only on the **second** independent citation |

People pages stay thin — connector nodes, not essays.

---

## Citation & linking

- **Every claim in a concept must be traceable.** `Sources:` front-matter lists the source notes the claim rests on.
- **Backlink rule**: every new concept links at least 2 existing concepts in `Related:`, or notes why it's an island (flagged in `wiki/_meta/health.md` Orphans section).
- **Cross-vault links** (if using a companion vault) use `[[VaultName/Path/Note Title]]` form.
- **Never break a link.** If renaming, update all backlinks.

---

## Diagrams

Bloom uses mermaid for diagrams. Diagrams are visual supplements — they should be drawn when helpful and needed, not by default.

### When to generate

Generate a diagram when a concept, source, or query involves:
- System architectures or component relationships
- Data flows or state transitions
- Hierarchical structures or taxonomies
- Processes with distinct steps or decision points
- Comparisons or trade-off matrices
- Visual content in a source article worth recreating (e.g., architecture diagrams, process flows)

Don't generate diagrams when:
- The content is purely textual or philosophical with no structural elements
- A text explanation is clearer and more concise
- The source contains no visual content to recreate and no process worth visualizing

Default stance: **only when helpful and needed.**

### Where diagrams live

Diagrams are inline mermaid code blocks inside the note they illustrate, placed under a `## Diagram` heading at the end of the body.

### Tracking

Notes containing `## Diagram` sections are listed in `wiki/_meta/index.md` under a **Diagrams** subsection of **Pages**.

---

## Operations

### Ingest (`/bloom-ingest`)

Process anything in `inbox/` — web clippings, PDFs, URLs, pasted text — into detailed source notes in `sources/`.

**YouTube URLs:** When the argument is a YouTube URL (`youtube.com/watch` or `youtu.be/`), use the dedicated script which extracts the video ID, fetches the title and transcript, and writes the raw transcript directly to `inbox/<Video Title>.md`:
```
uvx --from youtube-transcript-api python3 scripts/bloom-youtube.py "<YOUTUBE_URL>"
```
The script writes raw transcript text (no frontmatter, no headers) to `inbox/` and prints the file path. Then process as normal.

**ArXiv research papers:** When the argument is an arXiv URL (`arxiv.org/abs/...`, `arxiv.org/pdf/...`, `arxiv.org/html/...`) or a bare arXiv ID, prefer the HTML paper over PDF extraction. Normalize the input to the arXiv ID, then fetch:
```
https://arxiv.org/html/<ARXIV_ID>
```
If the official HTML page is unavailable or empty, try:
```
https://ar5iv.labs.arxiv.org/html/<ARXIV_ID>
```

Use the paper cleaner to fetch the HTML route and write a clean reading packet to `inbox/`:
```
uvx --with trafilatura python3 scripts/bloom-paper.py "<ARXIV_URL_OR_ID>"
```

The packet must preserve: title, authors, date/version, arXiv ID, canonical abs/html/pdf links, abstract, main claims, contributions, section-by-section argument, important equations in LaTeX with explanations, compact tables as markdown tables, figure numbers/captions/image links where exposed by HTML, algorithms/pseudocode, experimental setup, datasets, metrics, ablations, limitations, and conclusions.

The packet must strip: references/bibliography, citation metadata dumps, page headers/footers, navigation, license blocks, related links, repeated author/institution boilerplate, and appendix material unless it contains core equations, implementation details, proofs, or important extra results. Keep inline citations only when they matter to the argument; never include the full reference list in the inbox packet.

Then process the inbox packet as normal. Do not use PDF extraction for arXiv papers by default. If both HTML routes fail, stop and ask the user for pasted text or explicit approval to attempt a PDF fallback; do not ingest noisy PDF text as a source note.

**Non-YouTube URLs:** Use the fetch script with the `--inbox` flag, which extracts content via trafilatura and writes it directly to `inbox/<Title>.md`:
```
uvx --with trafilatura python3 scripts/bloom-fetch.py --inbox "<URL>"
```
The script writes raw extracted content (no Bloom frontmatter) to `inbox/` and prints the file path. Then process as normal (read > write source note > update index/log > move to residuals).

If the script exits with an error or returns empty content, fall back to the `webfetch` tool **once**. If `webfetch` also fails or returns empty, do not retry — ask the user to manually add a transcript, text dump, or link to `inbox/` for processing.

**The standard for a good source note:** a reader should be able to understand and use the ideas in the source without going back to the original. That means reconstructing arguments, not just cataloguing topics. Favour paragraphs over bullets. Preserve distinctions the author makes — especially ones that are easy to collapse. If the source is technical, include enough of the mechanism that the note is actually useful later.

**Reading strategy for long files:** Use the two-pass approach:

1. **Pass 1 - Structure scan:** First scan the document to identify key topics, terms, and logical sections. Use keyword searching, scan the first/last 10% and middle section. Goal: understand what the document covers before diving deep.

2. **Pass 2 - Deep read:** Based on Pass 1 findings, target specific sections relevant to the source note goals. Skip or skim sections outside scope.

3. **For files with no line breaks:** Use character-based reading (head -c / tail -c) in 2000-char chunks. Summarize each chunk before proceeding.

4. **Structure-first alternative:** If document has clear headings/sections, read those first to understand logical flow before reading content.

Flow: read source fully before writing > identify the major topics and the logic connecting them > write the Overview as a reconstruction of the argument, not a contents list > write each topic section with full explanations, examples, caveats, and formulas where present > write Key Takeaways as falsifiable claims > note Connections to existing vault content > cross-reference companion vault (if any) > update `wiki/_meta/index.md` (Sources section, keyword counts) > append to `wiki/_meta/log.md` > move inbox items to `residuals/`.

A single ingest touches: the new source note, the index, the log, and occasionally a people page.

Won't do: write into your companion vault, create concept articles (that's compile's job), invent work if inbox is empty, compress detailed content into thin bullet lists.

### Compile (`/bloom-compile`)

Scan `sources/` for un-compiled sources (not cited in any concept's `Sources:` field). Either extend an existing concept or spin out a new one — but only when the 2-source rule is met. Otherwise, log the theme to the Candidates section of `wiki/_meta/index.md` and wait.

After each run: update Research Threads, append new Prompts, update keyword counts — all in `wiki/_meta/index.md`. Append to `wiki/_meta/log.md`.

Won't do: write into your companion vault, spin out a concept from a single source, break links.

### Query (`/bloom-ask`)

Research a question across Bloom and companion vault (read-only). Write report to `wiki/YYYY-MM-DD-slug.md`. Every claim cites its source. Good answers get filed as wiki pages — explorations compound.

Findings with 2+ sources feed back to Candidates. Open gaps feed to Open Questions. Essay prompts to Prompts — all in `wiki/_meta/index.md`.

Won't do: write into your companion vault, invent citations, pad thin answers.

### Lint (`/bloom-lint`)

Health-check the whole vault. Overwrite `wiki/_meta/health.md` with: Stats, Orphans, Candidates needing attention, Keyword drift.

### Graph (`/bloom-graph`)

Generate a connection graph of the entire vault. Overwrite `wiki/_meta/graph.md` with a mermaid diagram plus structured analysis.

**What it reads:** All `.md` files in `wiki/` and `sources/` — frontmatter (`Related:`, `Sources:`, `Keyword:`) and `## Connections` sections.

**What it outputs:**
- Mermaid `graph TD` with nodes styled by type (concept, source, person, query, meta)
- Edges from: `Related:` (solid), `Sources:` (dotted), `## Connections` (labeled), keyword overlap (thick)
- **Stats** — node/edge counts, type breakdown, average degree
- **Orphans** — nodes with < 2 connections (violates backlink rule for concepts)
- **Keyword Clusters** — groups of nodes sharing keywords
- **Hubs** — most connected nodes

**Run:** `python3 scripts/bloom-graph.py`

Won't do: modify any notes, create new notes, generate excalidraw files, or visualize companion vault content.

### Save (`/save`)

Capture the current Codex conversation as a narrative wiki page. Only invoked explicitly — no auto-save.

**Trigger:** `/save <Title Case — Descriptive Name>` (e.g. `/save Debugging Redis Connection Pool Leaks`)

**What it produces:** `wiki/<Title>.md` — a narrative prose reconstruction written as if the reader wasn't in the session. Type adapts to content: `#type/concept` by default (most working sessions), `#type/query` for research-heavy sessions, `#type/source` if the session processed an external artifact.

Front-matter follows the same convention as other pages:
```
Type: #type/concept
Area: #area/...
Keyword: #keyword/...
Date created: [[YYYY-MM-DD]]
Sources: (any sources referenced or created)
Related: (links to existing wiki pages)

---
```

Body is a flowing essay: what was done, why, key decisions made, artifacts produced, concepts explored, open questions left behind. Ends with a `## Connections` section linking to related wiki pages and sources.

**Housekeeping:**
- Append entry to `wiki/_meta/log.md`
- Update `wiki/_meta/index.md` (Pages section, keyword counts)

Won't do: write into companion vault, save unless invoked, create sessions from single-variable chitchat.

---

## First Principles Explanation Mode

When the user explicitly asks for a first-principles explanation (e.g. "explain X from first principles", "from the ground up", "from fundamentals", "break X down from first principles", "teach me X", "learn X from scratch", "why does X exist"), Codex switches into this mode. Do not activate on implicit requests unless the user is clearly asking to study or learn a concept, algorithm, tool, pattern, or system.

This is a teaching mode, not an essay mode. Bloom should make the user feel the need for the concept before naming the concept.

### Behavioral rules

1. **Start with the pain before the tool.** Do not begin with a definition. Begin with the concrete problem we face without the concept. Make the failure vivid: wasted work, repeated calls, confusing state, slow lookup, duplicated logic, fragile coordination, etc. Use the domain's real pain, not generic filler.

2. **Boil the pain down to the root cause.** After describing the symptoms, state the root cause plainly: "So the root cause is..." The root cause should be simple enough that a beginner can hold it in their head. Example shapes: "we are recomputing work when the inputs did not change", "we are searching without ordering the data", "we are mixing responsibilities that change for different reasons."

3. **Ask the natural next question.** Use human, curiosity-led questions to move forward: "So how can we solve this?", "What would have to be true for this to be faster?", "When is this value smallest?", "What did people use before this?", "Why did that older method break down?" Ask the question, then answer it. Let each answer create the next question.

4. **Introduce the concept only after the need is obvious.** Once the problem and root cause are clear, name the concept as the solution. Explain how its design directly attacks the root cause. Avoid "X is used for Y" as the main explanation; prefer "We had problem P because of cause C, so X exists to change C in this specific way."

5. **Rebuild causally from the bottom up.** Explain with a chain where each insight follows from the previous one. For algorithms and problem solving, use the pattern: goal > when would the answer be easiest to see? > what structure exposes that? > what operation creates that structure? > what remains to check? For concepts and tools, use: old way > pain in old way > root cause > desired property > new concept > how it fixes the cause.

6. **Emphasize why more than what.** Every major step should answer "why does this exist?", "why does this work?", or "why is this better than the naive approach?" If the explanation only describes behavior, keep digging until the cause is visible.

7. **Use beginner-friendly language.** Assume the user is smart but new. Keep words simple, sentences short, and examples concrete. Use light analogies or fun examples when they clarify the mechanism, but never let the analogy replace the real explanation.

8. **Bridge to pre-existing knowledge.** Connect each layer to what the user likely already understands. First-principles explanations fail when they start from a floor the reader does not share.

9. **Cross-reference vault sources.** If Bloom has source notes or concepts related to the topic, pull from them. Use the vault as knowledge, not as a constraint. Cite specific sources when they inform the explanation.

10. **Teach the learner how to learn it.** When the user asks "as a human, what questions should I ask to learn X?", respond with a question ladder. The ladder should move from purpose, to old approaches, to pain points, to root causes, to the new concept, to tradeoffs, to practice problems.

11. **Suggest recursive questions.** End each explanation with 3–5 follow-up questions that naturally arise from the current layer, encouraging the user to keep digging.

### Output structure

Use these headings conversationally when they help. For short answers, keep the same flow without heavy headings:

- **What problem are we actually solving?** — the pain without the concept
- **What is the root cause?** — the simplest cause underneath the symptoms
- **So how could we fix that?** — the natural question that creates the need for the idea
- **The concept** — introduce the idea and show how it attacks the root cause
- **Why this works** — causal chain, step by step, with each insight leading to the next
- **What people did before / why it was not enough** — when historically or technically useful
- **Beginner mental model** — simple example or analogy, only after the mechanism is clear
- **Questions to learn it deeply** — 3–5 recursive questions or a question ladder

Do not save these explanations to the wiki unless the user explicitly requests it with `/save`.

---

## What NOT to do

- Don't write into the companion vault (if one exists).
- Don't create files outside `sources/`, `wiki/`, `inbox/`, or `residuals/`.
- Don't speculatively create concepts from a single source. Wait for cross-source signal.
- Don't compress nuanced source material into thin bullet lists. A source note should be dense enough to replace the original.
- Don't use emojis.
- Don't add TODO comments. If something's missing, log it in Candidates.
- Don't create helpers, templates, or meta-infrastructure. The schema (this file) + index + log is all the infrastructure the vault needs.
- Don't edit or delete files in `residuals/`. They are kept as immutable originals.
