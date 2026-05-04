Compile source notes in the Bloom vault into concept articles.

**Before doing anything**, read `AGENTS.md` at the vault root for the full rules of engagement.

### Scope

Scan `sources/` for source notes that haven't been fully compiled. A source is "un-compiled" if its title doesn't appear in any concept article's `Sources:` field across `wiki/`.

If `$ARGUMENTS` names a specific source note, concept, or theme, focus the compile run on that. Otherwise work through un-compiled sources oldest first.

### For each un-compiled source

1. **Read the source note** in full, including Claude's notes at the bottom.
2. **Scan existing concept articles** in `wiki/` for topical overlap. If a companion vault is configured, also check it for related first-person notes.
3. **Decide**: extend an existing concept, or spin out a new one.
    - **Extend** when the source adds a new example, counter-example, or nuance to an existing concept. Add the source to the `Sources:` line. Add a paragraph or bullet under **Evidence across sources** that cites the new source.
    - **Spin out** when a distinct idea recurs across 2+ sources that doesn't fit existing concepts. A new concept article needs:
      - Clear one-sentence answer to "What it is"
      - One short paragraph on "Why it matters"
      - Key points — sharp one-liners, claim-shaped (one per line)
      - Evidence across sources — cite each source
      - Open questions — real research gaps
      - Prompts — essay-shaped prompts where the concept intersects existing notes (empty is fine)
      - At least 2 `Related:` links to existing concepts. If zero exist, note why it's an island in the body (and expect the lint to flag it).
4. **Consider a diagram** — if the concept describes architecture, systems, data flows, processes, or relationships where a visual summary would add clarity, generate an Excalidraw diagram. Save as `wiki/<Concept Title>.excalidraw`. Embed under `## Diagram` at the end of the concept body. Register it in `wiki/_meta/index.md`. Default: only when helpful and needed.
5. **If uncertain**: log the theme as a candidate in the Candidates section of `wiki/_meta/index.md` with a one-line rationale. Don't create speculative concepts from a single source — wait for cross-source signal.

### Cross-vault synthesis

If a companion vault is configured in CLAUDE.md, check it for notes on the same topic. If a relevant note exists:
- Cite it in the concept's `Sources:` as `[[VaultName/Path/Note Title]]`
- Attribute in the body: *"In a note on X, the author argues…"*
- Never copy verbatim — paraphrase.

### Maintenance passes

After compiling:

1. **Update the Research Threads section of `wiki/_meta/index.md`** — if a new thread has formed (a cluster of ≥3 concept articles sharing keywords), add a section for it with links. If a thread gained new articles, update its list.
2. **Append to the Prompts section of `wiki/_meta/index.md`** — roll any new essay prompts from the compiled concept articles into the vault-wide aggregate.
3. **Keywords** — register any new keywords used during compile in the Keywords section of `wiki/_meta/index.md`, and increment counts.
4. **Update `wiki/_meta/log.md`** — append today's entry under `## [YYYY-MM-DD] compile | <summary>`, listing new concepts and extended ones.

### Output

End with a short summary printed to the user:
- Sources compiled (count + titles)
- New concepts created (titles + one-line each)
- Existing concepts extended (titles)
- Candidates flagged (titles + reason)

### Hard rules

- Never write into the companion vault (if configured).
- Never create a concept article from a single source. Default is to wait for 2+ sources.
- Always update backlinks when renaming or restructuring. Never leave broken links.
- If you delete or substantially rewrite an existing concept, note it in the log under a **Restructured** bullet.

### Arguments

`$ARGUMENTS` — optional. A specific source note title, concept name, or theme to focus the compile run on. If empty, compile all un-compiled sources.
