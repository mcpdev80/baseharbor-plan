# Bug-Hunt: I18N RESTSCAN

- Mission: `hunt-i18n-scan` — pure findings, no edits, no commits to product. German fallback/label text remaining in product output at `develop@bcae1e8c`.
- Context: cards 093 (Achtung->warning dual-match) + 099 (demo consumer rename) in window; 0428-099 was itself a bug-hunt find.
- Scope: cross-cutting scan for ALL remaining German fallback/label text in product output (CLI strings, compose labels, dashboard titles, README sections with operator-lead value).
- grep-matrix: `['Achtung','Warnung','Fehler:','Hinweis:']` over `cmd/ internal/ deploy* demos/ docs*`.
- Output: prioritize findings by user impact; `file:line`; consumer-visible vs docs-only classification.
- STOP at real card work.

## PLAN

- Read mission, attest remote develop@bcae1e8c, set up evidence dir. DONE.
- Run grep-matrix across cmd/ internal/ deploy* demos/ docs* at base SHA. DONE.
- Categorize each find: consumer-visible vs docs-only; rank by user impact. DONE.
- Write prioritized befund-*.md evidence files. DONE (befund-1.md, befund-2.md).
- Commit evidence to planning repo origin/main; confirm present. DONE (commit a56a320e, verified on origin/main).
- Post END_DONE; clean up any containers/compose. DONE (no containers started).

## BASE ATTESTATION

- Remote `origin develop`: `git ls-remote origin develop` -> `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`. Confirmed.
- Base SHA for scan: `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`.
- Read-only findings hunt; no branch cut, no commit to the product repo. No candidate commit exists, so the ancestor-of-first-commit check does not apply.
- Repo: `origin` = `https://github.com/mcpdev80/baseharbor.git`; product root `/home/marcel/dev/baseharbor-ecosystem/baseharbor`.
- Evidence repo: planning repo `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (origin/main), NOT `workers/baseharbor-plan` (quarantined checkout).

## EVIDENCE ON origin/main (before END)

`git ls-tree origin/main --name-only -r -- evidence/r28-welle3-2026-11-16/hunt-i18n-scan/` after `git fetch origin main`:

```
evidence/r28-welle3-2026-11-16/hunt-i18n-scan/befund-1.md
evidence/r28-welle3-2026-11-16/hunt-i18n-scan/befund-2.md
evidence/r28-welle3-2026-11-16/hunt-i18n-scan/mission-hunt-i18n-scan.md
```

Committed locally in `a56a320e`; present on `origin/main`. Path confirmed.

## FINDINGS

This is a read-only bug-hunt. Two findings, prioritized by user impact:

**FINDING 1 (HIGH — consumer-visible, 12 occurrences):** German fallback/label strings rendered directly to end users on destructive, consent-gated CLI paths. `Achtung:` (German "Warning/Caution") is hardcoded in Go string literals via `fmt.Fprintln`/`fmt.Fprintf` with no i18n layer:
- `cmd/baha/control_plane_stop_impact.go:180`
- `cmd/baha/node_disconnect_client.go:158`
- `cmd/baha/target_definition_change.go:33`
- `cmd/baha/application_stop_impact.go:189`
- `cmd/baha/runtime_destroy_impact.go:178,180`
- `cmd/baha/provider_change_confirmation.go:42,82,84,104`
- `cmd/baha/application_restore_authorization.go:158`
- `cmd/baha/provider_external_removal.go:36`

These appear on stop / destroy / restore / provider-change / disconnect / Core-stop flows. A German-speaking operator reads `Achtung:` as an intended safety warning; an English-speaking operator sees an untranslated German word embedded in an English sentence — genuine i18n regression degrading a safety-critical lead token. The `Achtung` value is also a language-neutral model const in `contracts/provider-impact/v1/impact.schema.json:33,1051` and `scope.schema.json:30` (data, not a renderable label). Untouched by cards 093/099; descends from v0.4.25 capability-contract work (#905).

**FINDING 2 (LOW — docs-only / data, no user impact):** Remaining `Warnung`/`Fehler`/`Hinweis:` occurrences are confined to `docs/de/releases/*.md` (intentional German docs) and `mkdocs.de.yml:102,120` (German doc nav labels), plus test-fixture/model-const JSON. No product-output regression.

---

## END STATUS

END_DONE posted to coordinator d4212c96-16b8-4fe3-a6ef-587d20c0e0d0. No product edits, no branch cut, no commits to product repo. No containers/compose started this shift (cleanliness: none; ambient-core `bh-local-shared-*` stacks are foreign and left untouched).
