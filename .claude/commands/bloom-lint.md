Health-check the Bloom vault.

**Before doing anything**, read `AGENTS.md` at the vault root for the full rules of engagement.

### What this does

Scan every file in `sources/` and `wiki/` (including `wiki/_meta/`). Validate structure, cross-references, and consistency. Overwrite `wiki/_meta/health.md` with the results. This is the vault's immune system — it catches drift before it compounds.

### Checks to run

#### 1. Stats

Count and report:
- Source notes in `sources/`
- Concept articles in `wiki/` (Type: #type/concept)
- Query reports in `wiki/` (Type: #type/query)
- People pages in `wiki/` (Type: #type/person)
- Diagrams (notes with `## Diagram` sections)
- Total keywords registered in the Keywords section of `wiki/_meta/index.md`
- Total wikilinks across the vault (rough gauge of connectivity)

#### 2. Front-matter validation

Every `.md` file in `sources/` and `wiki/` (except `_meta/`) must have:
- `Type:` — one of `#type/source`, `#type/concept`, `#type/query`, `#type/person`
- `Area:` — starts with `#area/`
- `Keyword:` — at least one `#keyword/...` tag (empty is a warning, not an error)
- `Date created:` — in `[[YYYY-MM-DD]]` format

Additional required fields by type:
- **source**: `Source:` (URL or reference)
- **concept**: `Sources:` (at least one `[[...]]` link), `Related:` (at least one `[[...]]` link — fewer than 2 is flagged in Orphans)
- **query**: `Question:`
- **person**: body must contain `**Sources in Bloom**` and `**Concepts they inform**` sections

Report any file missing required fields.

#### 3. Orphans

**Concept articles under the 2-Related rule**
- Concepts with fewer than 2 entries in `Related:`. List each with its current Related count and Sources count for context.

**Uncited source notes**
- Source notes in `sources/` whose title does not appear in any concept's `Sources:` field. These are ingested but never compiled.

**Unreferenced people**
- People pages where both **Sources in Bloom** and **Concepts they inform** sections are empty or contain only `_(none...)_` markers.

#### Diagrams

- **Orphaned `## Diagram` sections** — mermaid code blocks in notes not listed in `wiki/_meta/index.md`
- **Broken diagram references** — entries in `wiki/_meta/index.md` pointing to notes without `## Diagram` sections

#### 4. Broken links

Scan all wikilinks (`[[...]]`) in `sources/` and `wiki/`. Flag any that point to a file that doesn't exist in the vault. Exclude `[[VaultName/...]]` links that reference a companion vault (those live outside the repo — don't validate them, just skip). Exclude `[[YYYY-MM-DD]]` date links.

#### 5. Index staleness

Cross-check `wiki/_meta/index.md` against reality:
- Files in `sources/` or `wiki/` not listed in the appropriate section of `index.md`
- Entries in `index.md` that reference files which no longer exist
- Keyword count mismatches: recount how many files use each keyword vs the count listed in `index.md`

#### 6. Candidates needing attention

Read the Candidates section of `wiki/_meta/index.md`. Surface:
- **Close to promote**: candidates explicitly marked as close, or where you can verify that a second source has landed since the candidate was logged
- **Stale**: candidates that have been sitting since the vault's earliest logs without progress
- **Ready to fold**: candidates marked as likely-a-section-not-a-concept, still sitting as open candidates

Don't duplicate the full candidates list — just flag the ones that need action.

#### 7. Keyword drift

- **Suspected duplicates**: keywords in the Keywords section of `index.md` that are near-synonyms or overlap semantically (e.g. `focus` / `attention`). Use judgment — flag pairs that a human should decide on, don't flag obvious distinctions.
- **Unregistered keywords**: `#keyword/...` tags used in file front-matter but not listed in the Keywords section of `index.md`.
- **Phantom keywords**: keywords listed in `index.md` but never used in any file's front-matter.

### Writing the report

Overwrite `wiki/_meta/health.md` entirely. Preserve the existing front-matter block:

```
Type: #type/meta
Area: #area/craft/meta
Keyword:
Date created: [[YYYY-MM-DD]]

---

Single lint dashboard. Overwritten by each `/bloom-lint` run. Do not edit manually — edits get clobbered.
```

Then write each section. Keep the report scannable:
- Use bullet lists, not prose
- Lead each finding with the file name as a `[[wikilink]]`
- If a section has zero findings, write `- _(clean)_` — don't skip the section header

End the Stats section with `- **Last lint run:** YYYY-MM-DD` using today's date.

### Logging

Append to `wiki/_meta/log.md`:

```
## [YYYY-MM-DD] lint | Health check
- Sources: N, Concepts: N, Queries: N, People: N
- Orphans: N, Broken links: N, Index issues: N
- Keyword drift flags: N
```

### Final summary to print

After writing `health.md` and appending to `log.md`, print a short summary:
- Vault size (sources / concepts / queries / people)
- Issues found (orphans, broken links, index staleness, keyword drift) — count per category
- Candidates needing attention (count + titles)
- If the vault is clean, say so

### Hard rules

- Never write into the companion vault (if configured).
- Never modify any file except `wiki/_meta/health.md` and `wiki/_meta/log.md`.
- Don't fix issues — only report them. Fixes are the job of other commands or the user.
- Don't invent problems. If a check passes, report it as clean.
- If `$ARGUMENTS` is `--dry-run`, print the summary but don't write `health.md` or `log.md`.

### Arguments

`$ARGUMENTS` — optional. `--dry-run` to preview without writing. Otherwise ignored.
