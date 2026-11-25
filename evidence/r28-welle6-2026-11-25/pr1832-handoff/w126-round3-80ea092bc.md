# PR #1832 — Round 3 (review fixes 1–4) exact-head CI witness: 80ea092bc

Date: 2026-11-25

## Review handoff (previous round)

Reviewer (author==reviewer account) COMMENTED PR #1832 with four same-file fixes:
1. Carry the detected endpoint tuple (service/source, internal port, HTTP path) instead of hardcoding `/metrics`.
2. AMBIGUOUS detection → fail closed / ask, no silent default.
3. Tests assert EXACT paths: Quarkus `/q/metrics`, Spring `/actuator/prometheus`, conventional `/metrics`.
4. Module-service attribution EXACT with path boundaries (fix `api` matching `api-old`).

## Candidate: 80ea092bc (exact head, develop f7540e591 integrated)

Built from metrics review fixes committed as `ef7e58eb8` on develop `9d7e22902`, then a gofmt
fix, then `git merge origin/develop` (base moved to `f7540e591`, PR #1837) + normal push.

Files changed vs develop (clean same-file scope, no `.github/**`, no `scripts/**` product code):
- `internal/repositoryinspect/capability_detectors.go` — `metricsPathPattern`, `metricsEndpointFromText`
  (captures exact path), `metricsPathClass` (quarkus/spring/conventional/other); detector scans
  `.properties` so Quarkus/Spring Boot config yields the proven `/q/metrics` / `/actuator/prometheus`
  path instead of a bare `/metrics` substring.
- `cmd/baha/app_init_wizard.go` — `appProjectDetection` gains `MetricsPath string`.
- `cmd/baha/app_init_detection.go` — detection loop captures `d.MetricsPath` via `metricsProvenPath`
  helper; `detectedMetricsTarget` returns the full tuple `(source, service, port, path string, ok bool)`;
  `metricsModuleAttributableToWorkload` uses path boundaries (exact head match, not `strings.HasPrefix`),
  so `api` no longer leaks onto `api-old`.
- `cmd/baha/app_init_selection.go` — `addGuidedObservability` threads the exact path into
  `WithMetricsSource`.
- `cmd/baha/app_init_prompts.go` — `promptMetricsTarget` takes the detected path.
- `cmd/baha/app_init_wizard_test.go` — 3 exact-path regression tests (Quarkus `/q/metrics`,
  Spring `/actuator/prometheus`, conventional `/metrics`) plus `api` vs `api-old` boundary test.

Local precheck (before push): `gofmt -l` clean, `go build ./...` pass, `go vet ./cmd/baha/` pass,
all `TestQuickInit` + metrics tests pass.

## Hosted CI witness — run 45523287558 (exact head 80ea092bc86ad1c0cc9df93a893bfb7397a72f28)

Run-level GitHub API lags (reports `in_progress`); all **30 jobs terminal, 0 failure**:
**20 success / 10 skipped** (skipped = release/release-gate matrix, not affected by this change).

Key green gates:
- `PR · Native gate plan` — **success** (jobid `138905251902`), atomic docker/podman gates
- `PR · Source format`, `PR · Validation · inspect-gofmt` — success
- `PR · Validation · go-vet`, `PR · Validation · go-build` — success
- `PR · Trusted Plan`, `PR · Exact Candidate`, `PR · Runner Interface` — success
- `PR · Go unit · cli-0..3`, `PR · Go unit · owner`, `PR · Go unit · packages` — success

Two exact-head run IDs as evidence: `45523287558` (Native gate plan orchestrates the docker + podman
native data-capabilities runs on this exact head; single workflow run, both gates green).

Stale-run hygiene: own runs `45521348017` (@ef7e58eb, format-failed) and `45522283304`
(@4d7abb5f, base-bad) cancelled via `gh run cancel`; not rerun for counting. Base-bad head `67a1eb3a`
run `45522275641` already completed/superseded.

## Push + merge witnesses (ls-remote / git)

```
git ls-remote lane-origin refs/heads/lane-0428-290-metrics-discovery
80ea092bc86ad1c0cc9df93a893bfb7397a72f28  (refs/heads/lane-0428-290-metrics-discovery)
git ls-remote origin develop
f7540e591...  (develop tip, PR #1837 atomic gates)
```
merge-base witnesses: `git merge-base --is-ancestor f7540e591 HEAD` = YES (develop integrated);
`git merge-base --is-ancestor 67a1eb3a1 HEAD` = YES (metrics code preserved through merge).

PR #1832 head = `80ea092bc`, state open.

## Repo-rule compliance
- Same-file scope as card: only `cmd/baha` and `internal/repositoryinspect` product files.
- No `.github/**` change; no `ci.yml` change; no auth/consent change.
- Catalog rows already landed on develop via PR #1837; this round adds no new source rows.
- Tests run via Hosted CI (no new local-only test); local build/vet/gofmt were pre-push prechecks only.

## Next: Codex review + merge
Hand exact head `80ea092bc` to Codex (CODEX-REVIEW) for an independent SHA-precise review vs card
`t-20261116-r28-bug-metrics-discovery`; CODEX-MERGE only on full green exact-head evidence.
Not merged by worker (author==reviewer account — GitHub only accepts COMMENT events).
