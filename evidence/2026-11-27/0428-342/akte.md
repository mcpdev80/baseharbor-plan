# 0428-342 · operator metrics endpoint doc — w397 akte

Task `t-20261128-hunt48-metrics-endpoint-docs`, card `0428-342`, release v0.4.28, repo `mcpdev80/baseharbor`, hunt H-V48.

## Visible ANSATZ BLOCK (before first commit)

- Card owner (verbatim frontmatter `owner:`, fetched from `origin/main` at claim): `w397-0428-342-metricsdocs` (card frontmatter `owner:` was empty; lane registered for this card is `w397-0428-342-metricsdocs`).
- Git identity used for every commit:
  - `user.name = w397-0428-342-metricsdocs`
  - `user.email = w397-0428-342-metricsdocs@baseharbor.local`
- Commit invocation (visible, used verbatim):
  - `git -c user.name=w397-0428-342-metricsdocs -c user.email=w397-0428-342-metricsdocs@baseharbor.local commit ...`
- Pre-push author gate (printed, must equal lane name):
  - `git show -s --format=%an HEAD` printed `w397-0428-342-metricsdocs`.
- Branch provenance (before PR):
  - `git merge-base --is-ancestor origin/develop HEAD` printed `YES`.
  - `git diff origin/develop...HEAD --name-only` = `docs/how-to/operator-api.md`, `docs/de/how-to/operator-api.md`.
  - `git ls-remote origin develop` = `ea5218d72e263f21e79853b679af50074dab8c25` (base attestation; this SHA is an ancestor of my commit).

## PLAN (numbered)

1. Read card + baseharbor/AGENTS.md; verify plan-remote = github.com/mcpdev80/baseharbor-plan.
2. Claim 0428-342, render+check; forward-only push to main (pull-before-push).
3. Locate the registered operator/metrics endpoint in baseharbor source and the existing docs/spec path it extends.
4. Add the missing documentation line for the executor `/metrics` route (docs only; no product code; no API change; write-set disjunct from running catalog PRs).
5. Local non-test prechecks: format/build of doc paths; `scripts/documentation-audit.sh`.
6. Open PR against develop via `git merge origin/develop` + normal push; no force, no cherry-pick; do not self-merge.
7. Trigger hosted CI, run to terminal (Eigenes-Run-Pflicht); record run-ids + terminal status.
8. Write akte with PR number, exact head, run-ids+status, akte path+sha256; post END line.

## Repo verification (remote guard + base attestation)

- Planning remote (first `git -C remote -v`): `origin = https://github.com/mcpdev80/baseharbor-plan.git`.
- Product remote (real github.com/mcpdev80, first git action): cloned `https://github.com/mcpdev80/baseharbor.git` into `workers/w397-0428-342-metricsdocs-wt`; `origin = https://github.com/mcpdev80/baseharbor.git`.
- Base attestation: cut from `origin/develop` = `ea5218d72e263f21e79853b679af50074dab8c25`; `git merge-base --is-ancestor origin/develop HEAD` = YES; `git diff origin/develop...HEAD --name-only` lists only my two doc files; `git log origin/develop..HEAD` lists only my commit.

## H-V48 finding (what was undocumented)

- Source: `internal/runtimeexecutor/server.go:121` registers `GET /metrics` (`observer.MetricsHandler()`) on the runtime executor's operator HTTP server.
- Operator surface: the executor serves `0.0.0.0:9443` (override `BASEHARBOR_RUNTIME_EXECUTOR_LISTEN_ADDR`), TLS 1.2+ with `tls.RequireAndVerifyClientCert`; routes are `/internal/` (handler), `GET /healthz`, `GET /readyz`, `GET /metrics`.
- Gap: the canonical operator-routes table in `docs/how-to/operator-api.md` documented only the Core operator API on `127.0.0.1:8443` and omitted the executor's `/metrics`. No spec enumerated the executor operator routes. Docs-only scope: no product code, no API change.

## Work done

- Added a `GET /metrics` row to the EN routes table and a clarifying sentence (executor's own operator surface, separate from Core `127.0.0.1:8443`, behind TLS 1.2+ and client-certificate auth).
- Added the matching German row + sentence to `docs/de/how-to/operator-api.md` (EN/DE parity, required by `scripts/documentation-audit.sh`).

## Local non-test prechecks (no local test runs)

- `bash scripts/documentation-audit.sh`: all sections PASS, EN/DE parity PASS, no `literal lost` findings.
- `bash scripts/source-readability-audit.sh`: PASS (Go file-size regression ratchet PASS).
- `go build ./...`: clean (exit 0).
- `go vet ./...` not separately run beyond build; no local `go test` (forbidden per policy).

## PR

- PR #1878, repo mcpdev80/baseharbor, base develop, head branch `w397-0428-342-metricsdocs`, head SHA `b63bea30aaba0899bf045a7bd0ec98ffcc819bfd`, not draft.
- Delivery witness: `git ls-remote origin refs/heads/w397-0428-342-metricsdocs` = `b63bea30...`; `git ls-remote origin develop` = `ea5218d7...`.
- Transport: `git merge origin/develop` + normal push (no force, no cherry-pick). Not self-merged; hosted CI + review follow.

## CI / Hosted run

- Pending: trigger hosted CI on PR #1878, run to terminal state, record run-ids + terminal status (Eigenes-Run-Pflicht). No run has completed on this head yet.

## Board status

- Card moved to `review` (owner + PR #1878 set). `plan.py render`/`check` on my card pass with 0 errors in an isolated plan worktree. The shared `baseharbor-plan` checkout check is blocked by foreign lanes (`t-20261128-hunt49-archived-gates-validator-blindspot`, `w267-staged-publish` worktree) — a shared-file blocker for the coordinator to reconcile; not my card.

## END STATUS

done: card 0428-342 on review, PR #1878 head b63bea30; hosted CI run pending on that head (Eigenes-Run-Pflicht).
