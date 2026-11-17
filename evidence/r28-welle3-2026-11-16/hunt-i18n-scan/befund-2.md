# Befund 2 — German fallback terms in docs and contract JSON (docs-only)

- Type: docs-only reference / data-model const (not rendered as end-user label)
- SHA base: `bcae1e8c1261c9e44db03fe285a5d090c532dfcd`
- Repo: `https://github.com/mcpdev80/baseharbor.git`

## Finding
Remaining German terms `Warnung`, `Fehler`, `Hinweis:` and `Fehler:` outside the CLI surface are confined to:
- `docs/de/releases/v0.4.9.md:26` — German release note (intentional German docs)
- `docs/de/releases/v0.4.15.1.md:31` — German release note (intentional German docs)
- `docs/de/releases/v0.4.25.preparation.md:560` — German release note (intentional German docs)
- `mkdocs.de.yml:102,120` — German doc nav labels (intentional German docs site config)

These are the German documentation site's own language; not a product-output fallback regression.

## Model const (data, not label)
- `contracts/provider-impact/v1/scope.schema.json:30` and `impact.schema.json:33,1051` — `attention: { const: "Achtung" }`. Language-neutral protocol value, part of the published capability contract; the German word is the chosen semantic token, not a renderable user label.
- `internal/application/testdata/v0425-provider-impact-consent.json:7` — test fixture mirroring the model const.

## User impact
NONE as consumer-facing regression. Docs-only / data-model. Low priority; retained here for completeness of the cross-cutting scan.
