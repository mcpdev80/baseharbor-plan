# Bug-Hunt: I18N RESTSCAN

- Mission: `hunt-i18n-scan` — pure findings, no edits, no commits to product. German fallback/label text remaining in product output at `develop@bcae1e8c`.
- Context: cards 093 (Achtung->warning dual-match) + 099 (demo consumer rename) in window; 0428-099 was itself a bug-hunt find.
- Scope: cross-cutting scan for ALL remaining German fallback/label text in product output (CLI strings, compose labels, dashboard titles, README sections with operator-lead value).
- grep-matrix: `['Achtung','Warnung','Fehler:','Hinweis:']` over `cmd/ internal/ deploy* demos/ docs*`.
- Output: prioritize findings by user impact; `file:line`; consumer-visible vs docs-only classification.
- STOP at real card work.

## PLAN

- [x] Read mission, attest remote develop@bcae1e8c, set up evidence dir
- [ ] Run grep-matrix across cmd/ internal/ deploy* demos/ docs* at base SHA
- [ ] Categorize each find: consumer-visible vs docs-only; rank by user impact
- [ ] Write prioritized befund-*.md evidence files
- [ ] Commit evidence to planning repo origin/main; confirm present
- [ ] Post END_DONE; clean up any containers/compose

## BASE ATTESTATION

- Remote `origin develop`: `git ls-remote origin develop` -> `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`
- Base SHA for scan: `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`
- This is a read-only findings hunt; no branch cut, no commit to the product repo. No candidate commit exists, so the ancestor-of-first-commit check does not apply.
- Repo: `origin` = `https://github.com/mcpdev80/baseharbor.git`; product root `/home/marcel/dev/baseharbor-ecosystem/baseharbor`.
