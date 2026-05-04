Answer a research question using the Bloom vault, with read-only access to any companion vault configured in CLAUDE.md.

**Before doing anything**, read `AGENTS.md` at the vault root for the full rules of engagement.

### Scope

`$ARGUMENTS` is the question to answer.

If `$ARGUMENTS` is empty, open `wiki/_meta/index.md` and pick the oldest entry in the **Open Questions** list. If that list is empty too, say so and stop — don't invent a question.

### How to answer

1. **Search in this order** (most distilled first):
   - Concept articles in `wiki/` — these already synthesise across sources. Read every concept whose title, keywords, or `Related:` plausibly touches the question.
   - Source notes in `sources/` — for specific claims, quotes, and evidence.
   - Prior query reports in `wiki/` (Type: #type/query) — queries compound.
   - The companion vault (if configured) — the author's own first-person writing. Read-only.

2. **Cite every claim.** Every factual or interpretive sentence in the answer must trace back to a specific note via `[[Title]]` or `[[VaultName/Path/Title]]` wikilinks. If a claim has no source, either find one or drop it — don't invent evidence.

3. **Paraphrase the companion vault, never copy.** If a companion-vault note informs the answer, attribute it (*"In a note on X, the author argues…"*) and rewrite in your own words.

4. **Hold tensions explicitly.** When sources disagree, name the disagreement rather than collapsing it. Honest signal matters more than a clean answer.

### Output

Write to `wiki/YYYY-MM-DD-<question-slug>.md`. Slug the question — kebab-case, ~6 words max, enough for the filename to be scannable.

Front-matter:

```
Type: #type/query
Area: #area/...
Keyword: #keyword/...
Date created: [[YYYY-MM-DD]]
Question: <the user's exact question>

---
```

Body. **Bias toward terse.** A tight, dense report is more useful than a thorough one.

- **Short answer** — one paragraph, ~4-6 sentences max. The honest answer, not a summary of the search. If the vault can't answer, say so and name what's missing.
- **Evidence** — 5-8 bullets max. Each bullet is one claim, cited to 1–N notes with wikilinks. Collapse related points into one bullet rather than spawning sub-headers.
- **Tensions** — 0-3 bullets. Name real disagreement, not every mild difference. Empty is fine.
- **Open gaps** — 3-5 bullets max. Real questions the vault raised but can't answer. These feed back into `wiki/_meta/index.md` → Open Questions.
- **What this suggests writing** — 3-5 bullets max. Essay-shaped prompts, one sentence each, pointed and specific. Same register as a concept article's Prompts section. Cut any prompt that's lukewarm.
- **Diagram** — if the question involves systems, architectures, flows, or relationships where a visual summary would add clarity, generate an Excalidraw diagram. Save as `wiki/YYYY-MM-DD-<slug>.excalidraw` and embed under `## Diagram`. Default: only when helpful and needed.

### Feedback into the graph (so queries compound)

After writing the report:

1. **Any finding backed by ≥2 sources** that isn't yet a concept article — add it to the Candidates section of `wiki/_meta/index.md` with the query filename as the rationale. This is how `/bloom-ask` feeds the compile loop.
2. **Any Open gap** that isn't already in `wiki/_meta/index.md` → Open Questions — append it there, one line each.
3. **Any essay prompt** worth elevating to the vault-wide aggregate — append to `wiki/_meta/index.md` → Prompts, under a new `### From query: <filename>` subheading.
4. **If the question came from the Open Questions list**, move it from **Open** to **Answered** with a link to the query report.
5. **Update `wiki/_meta/log.md`** under `## [YYYY-MM-DD] query | <slug>` — one-line answer summary.

### Final summary to print

- Question
- One-sentence answer
- Report path
- Candidates flagged (count + titles)
- Open gaps logged (count)

### Hard rules

- Never write into the companion vault (if configured).
- Never invent a citation. If the vault doesn't contain evidence for a claim, leave the claim out.
- Never summarise your search process in the report — the report is the answer, not a diary of the lookup.
- Never collapse a real tension into false consensus. If sources disagree, the report must say so.
- If the report would be thin (fewer than 3 cited claims), stop and return a note saying the vault isn't yet ready to answer this question. Don't pad with speculation.
- Tight over thorough. If a bullet repeats the claim above it, cut one. If a section has nothing pointed to say, leave it empty.

### Arguments

`$ARGUMENTS` — the research question. If empty, pull the oldest Open Question from `wiki/_meta/index.md`.
