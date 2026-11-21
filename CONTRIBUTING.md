# Contributing

Contributions are welcome: corrections, new sources, new vendors, new host templates, scripts and test cases.

## Rules for the knowledge base
1. **Every technical claim needs a source** (URL to the vendor page, datasheet, application note, standard or book) and a tag:
   - `FATO`: verified in the source you read.
   - `INFERÊNCIA`: your own deduction or common practice without a primary source.
2. **Never invent numbers.** If you could not find it, write "não encontrado" / "not found".
3. **Vendor data changes.** Put the consultation date next to capabilities, prices and tax rules.
4. **Do not commit third-party PDFs.** Add the document and its official link to `docs/pdf-catalog.md` instead.
5. Host-specific content (a board that plugs into a particular device) goes to `skill/cupraxis/references/hosts/` and must be tagged, e.g. `[FLIPPER]`.

## Changing the skill
- Keep `SKILL.md` under ~500 lines; push detail into `references/`.
- Add or update a test case in `skill/cupraxis/evals/<case>/` (prompt, `case.yaml`, one grader per assertion).
- Run the evals with and without the skill before and after the change (`claude plugin eval .` from the skill folder, or the skill-creator loop) and report the pass rates in the PR.

## Scripts
- Read-only by default; anything that edits a board must support a dry run and must be documented with a backup step.
- Scripts that use `pcbnew` run with KiCad's own Python.
