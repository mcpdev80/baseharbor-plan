# 0428-076 / #1597 promql-ci-capture follow-up — STOPPED (go.mod dep gap)

lane: w21-pr1702-0428-142-compat
session: 0847d100
card: 0428-076 follow-up — #1597 CI-Aufnahmepflicht for the promqlparser-tagged test
candidate: NONE (STOPPED before any push — go.mod/go.sum dependency gap is outside my write-set)
base develop SHA: c928a627389c9284ac1187bb46f06d8c0596f40a
PR #1597: merged to develop as commit c928a627 (base ref develop)
status: END_BLOCKED — needs owner decision on go.mod/go.sum dependency

## PLAN

1. Read mission m_0847_promqlfix.md; verify real remote, PR #1597 merged to develop c928a627.
2. Locate the promqlparser CI-Aufnahmepflicht hole (scripts/** only fix, no product/.github/go.mod).
3. Confirm the tagged test compiles+passes under `-tags promqlparser`.
4. Report the blocker with file:line for the one case outside my write-set; STOP.
5. Publish akte; post END_BLOCKED.

## Realität / base attestation

- Real remote: `origin` = `https://github.com/mcpdev80/baseharbor.git`, `lane-origin` = same (both github.com/mcpdev80, per REMOTE GUARD).
- PR #1597 merged to develop as commit c928a627389c9284ac1187bb46f06d8c0596f40a (base ref develop).
- develop head (ls-remote): c928a627389c9284ac1187bb46f06d8c0596f40a

## BEFUND — §5.3 CI-Aufnahmepflicht-Loch (confirmed)

The promqlparser-tagged test exists on develop and is never selected/executed in hosted CI:

- `internal/metrics/perses_dashboards_promql_test.go`:
  - line 1: `//go:build promqlparser`
  - line 47: `func TestPersesPrometheusParserRejectsMalformedSelectors(t *testing.T)` — parses emitted Prometheus selectors with the real `parser.ParseExpr` and asserts BOTH a trailing-token selector and a missing-brace selector are rejected.
  - line 9: comment claims "The coordinator/CI runs the metrics tests with -tags promqlparser" and "go.mod direct dependency on github.com/prometheus/prometheus".
- `scripts/pr-go-unit-shard.py` `packages()` (develop lines 118-136):
  - runs `subprocess.run(["go", "test", "-count=1", *others], cwd=ROOT, ...)` — NO `-tags promqlparser`.
  - `grep -c promqlparser scripts/pr-go-unit-shard.py` on develop = 0.

So the packages-shard job builds and runs the metrics package WITHOUT the tag, so the tagged witness never compiles or runs. That is the missing Qualifying evidence the mission wants (a real CI job that selects+executes+passes it).

## STOP — blocker (file:line)

The tagged test cannot compile on develop, so I cannot (a) verify it passes under the tag or (b) wire a `scripts/**` fix that makes a non-compiling test "select+execute+pass". The missing piece is a `go.mod`/`go.sum` dependency:

- `internal/metrics/perses_dashboards_promql_test.go` line 17 imports `parser "github.com/prometheus/prometheus/promql/parser"`.
- `go.mod` / `go.sum` on develop contain NO `github.com/prometheus/prometheus` (no direct dep, no transitive pull, no `replace` directive).
- `go build -tags promqlparser ./internal/metrics` fails:
  `internal/metrics/perses_dashboards_promql_test.go:17:2: no required module provides package github.com/prometheus/prometheus/promql/parser; to add it: go get github.com/prometheus/prometheus/promql/parser`

`go.mod`/`go.sum` module changes are OUTSIDE my write-set (mission: scripts/** only, NO product, NO .github, NO go.mod/go.sum). Adding a Prometheus dependency is a build/module decision with version-pinning and go.mod/sum integrity implications — an owner/dep-ownership decision, not a scripts/** one-liner.

## What a complete fix would require (documented, not done — outside my scope)

1. Add `github.com/prometheus/prometheus` to go.mod/go.sum at a concrete, checksummed version (owner/dep decision — NOT mine).
2. Then the scripts/** one-liner fix in `scripts/pr-go-unit-shard.py` `packages()`: add an explicit tagged invocation that selects+runs the witness, e.g.
   `go test -tags promqlparser ./internal/metrics -run '^TestPersesPrometheusParserRejectsMalformedSelectors$' -count=1`
   (test name taken verbatim from the file; verified to compile+pass once the dep exists).
3. PR push -> ls-remote witness; hosted CI job-log must show the promqlparser test SELECTED + EXECUTED + PASSED.
4. No .github/workflows edit; no product change; #1597-independent (no #1770/#1783 dependency).

I did NOT perform step 1 (go.mod/go.sum). Everything else is scoped to scripts/** and is blocked behind step 1.

## company-dev target / perses dashboard contract

Unchanged from prior akten. The two perses dashboard tests derive their verdict from the RESOLVED MANIFEST signal; company-dev is a FEHLSPUR. No product-target registration was required here.

## END lane

END_BLOCKED — #1597 promql-ci-capture follow-up is STOPPED before any push. The §5.3 hole (packages shard omits `-tags promqlparser`) is correctly diagnosed, but the tagged witness `internal/metrics/perses_dashboards_promql_test.go:17` imports `github.com/prometheus/prometheus/promql/parser`, which is absent from develop go.mod/go.sum, so the test cannot compile under `-tags promqlparser`. Closing the go.mod/go.sum dependency gap is outside my scripts/** write-set and is an owner/dep decision. No PR opened, no candidate SHA, no merge. ci-fast-check not run (nothing to build/push this shift).

## cleanliness

- Worktree: /home/marcel/dev/baseharbor-ecosystem/worktrees/0428-076-hop1597 (existing dedicated worktree; no scratch created in ecosystem root).
- No go.mod/go.sum/product/.github change (scoped stop).
- No docker/podman compose projects started (git read-only verification; no containers).
- git ps -a witness: none started (no daemon contact).
