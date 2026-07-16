# Dry-run 04 Summary

- Total refs detected: 361 (rewritten 319 + broken 42; audit expected 363)
- Pattern breakdown (successful rewrites):
  - markdown_link: 176 (期待値: 192, delta -8.3%, within ±20%)
  - wikilink: 143 (期待値: 171, delta -16.4%, within ±20%)
  - frontmatter: 0 (期待値: 0)
- Rewrite outcome:
  - rewritten: 319
  - broken (not rewritten): 42 (11.6% of 361; slightly over 10% gate)
- Broken reason breakdown:
  - target_not_found: 42
  - outside_repo: 0
  - ambiguous_target: 0

## Gate note

Broken ratio 11.6% exceeds the 10% advisory gate. All 42 are `target_not_found`:
EN ADRs linking to untranslated `rejected-alternatives/`, EN backbone linking to missing `docs/en/specs/`,
placeholder `path/to/file.md`, and a few incorrect `../decisions/` relatives from `docs/ja/`.
These remain as legacy paths and are recorded in `broken-refs.csv` for Naoya review — proceeding.

## First 10 ref rewrites (sample, from dry-run log)

See `migration/dry-run-04.log` for per-file change counts (74 files with rewrites).
