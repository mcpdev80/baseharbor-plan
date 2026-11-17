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
