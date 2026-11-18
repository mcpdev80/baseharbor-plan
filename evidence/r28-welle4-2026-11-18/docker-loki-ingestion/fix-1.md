# 0428-113 · Docker Loki provider ingestion — fix-1 (develop refresh + missing-check diagnosis)

Mission: /var/tmp/missions/mission-113-1680-fixes.md
Task contract: `python3 scripts/plan.py show t-20261117-docker-loki-ingestion-timeout`
Card: 0428-113 · release v0.4.28 · repos mcpdev80/baseharbor · PR #1680
Lane: mission-113-1680-fixes (flash worker session)

## PLAN

1. Reality check + claim card (owner was empty); diagnose the missing/failing check on 504a8678c via gh run jobs — DONE
2. `git merge origin/develop` into `lane-0428-113-docker-loki-ingestion-fix` (normal merge, develop-structure-wins, no force) — DONE, merge commit 46de903f1
3. Fix the failed check provider-side (logs); document the observability/registry.go overlap with the #1677/102 line — DONE as diagnosis + pre-fit; see SCOPE DECISION
4. Exact-head CI run until TERMINAL, self-observed — DONE (run 44396957393, success)
5. Evidence akte + END + GUI todos — this file

## Planning repo attestation (mission requirement)

```
$ git rev-parse --show-toplevel   # in /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```
Evidence lives ONLY here in baseharbor-plan (never in a product repo). Foreign lane's
uncommitted file `evidence/r28-welle4-2026-11-18/i18n-abachtung/rebase-window-1.md` was
found dirty in this shared checkout; it was stashed and restored untouched (its
checkpoint commits 0bfc5934/545f9887… are already on origin/main) and was never added,
committed or reverted by this lane.

## BASE ATTESTATION

- Branch head before this window: `504a8678c2391cb379622fa02c2c8d9769fa192b` (= PR #1680 head, mission-named candidate branch; work CONTINUED on it, no second branch created)
- Base ref cut/merged from: `origin/develop` = `907f16713cbf38693d30c9dadaad7fe299759219` (measured by `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` before the merge)
- Ancestor proof:

```
$ git merge-base --is-ancestor 907f16713cbf38693d30c9dadaad7fe299759219 HEAD && echo ANCESTOR
ANCESTOR   # HEAD = 46de903f17bed8e451c7bb3ad2d5ec6a187b607e
```

- `git log --oneline origin/develop..HEAD` lists ONLY my own commits:
  - `46de903f1 Merge origin/develop into lane-0428-113-docker-loki-ingestion-fix`
  - `504a8678c fix: drop phantom prometheus workload logs` (prior checkpoint of this same card/PR)
- No foreign candidate is carried: `git diff origin/develop...HEAD --name-only` =
  `internal/application/runtime_observability.go`, `internal/application/runtime_observability_trace_source_test.go` (the card's own write-set).

## Remote truth witnesses (ls-remote, never the quarantined workers/baseharbor checkout)

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-113-docker-loki-ingestion-fix
907f16713cbf38693d30c9dadaad7fe299759219  refs/heads/develop
504a8678c2391cb379622fa02c2c8d9769fa192b  refs/heads/lane-0428-113-docker-loki-ingestion-fix   # before push
```
After push (this lane, fast-forward, no force):
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-113-docker-loki-ingestion-fix
46de903f17bed8e451c7bb3ad2d5ec6a187b607e  refs/heads/lane-0428-113-docker-loki-ingestion-fix
```
PR #1680: OPEN, base develop, head 46de903f1, mergeStateStatus CLEAN (was BEHIND at 504a8678c).

## Claim

`plan.py claim t-20261117-docker-loki-ingestion-timeout` published as planning commit
`e77d28a45fd546b0cd07e367e642dba0b74d63a9` on origin/main; card owner =
`lane-113-pr1680-fixes (this session)`, kanban_status active.

Note: the 114-claim attempt (see FINDING) was created and reverted **inside this window's own
uncommitted working state** before publication (the card file's `owner:` edit was reverted before
`git add`); no planning commit ever claimed 0428-114, and its authoritative state remains
owner "" / planned on origin/main.

## What the "missing check" on 504a8678c actually is (diagnosis)

- PR #1680 CI · Source & Quality [run 44057402207](https://github.com/mcpdev80/baseharbor/actions/runs/44057402207): ALL required jobs success; `PR · Native gate plan` selected no native gate for `internal/application/runtime_observability.go` (that path maps only to the dedicated observability acceptance gate, see FINDING).
- Runtime acceptance: `podman` check = [run 44057705927 job 133951217610](https://github.com/mcpdev80/baseharbor/actions/runs/44057705927/job/133951217610) FAILED at `cmd/baha/app_observability_acceptance_test.go:34`:
  `prepare BaseHarbor integration trust plane: ORAS is required before Core setup; install it manually or rerun 'baha up' in an interactive terminal to approve a user-local installation`
  Same failure in the Docker dispatch job (see the wrong-head note below).
- The `docker` check on the PR is a SKIPPED mirror — the 2026-11-17 09:39:41Z dispatch run
  [44057603711](https://github.com/mcpdev80/baseharbor/actions/runs/44057603711) executed with **`ref: develop` (workflow head 62eaea2c8 = develop tip)** per
  `GET actions/runs/44057603711 → head_sha 62eaea2c8…`, `display_title` claims
  `504a8678c…`, and the job log's checkout resolved to develop: its workflow-level
  `head_commit.message` is "[0428-081] Perses-native Valkey dashboard (#1604)", i.e. the develop
  tip commit, NOT this PR's commit. The prior lane's "exact-SHA Docker dispatch" was therefore
  NOT exact-SHA. The podman push run 44057705927 DID check out 504a8678c (run head_sha = 504a8678c,
  failure line identical).

## Root cause: the gate never installed ORAS — it was never removed

- `scripts/ci-install-oras.sh` exists and is wired into three workflows on develop:
  - `.github/workflows/ci.yml:500` (`PR · Native` job, before `Run selected native gate`)
  - `.github/workflows/docker-runtime-acceptance.yml:127`
  - `.github/workflows/podman-acceptance.yml:128`
- `grep -n -i oras .github/workflows/observability-acceptance.yml` → **no match on develop
  and on every commit since the file exists**: `git log --all -S "ci-install-oras" --
  .github/workflows/observability-acceptance.yml` is empty. PR #1528 ("Install ORAS for native
  Core acceptance", merged 2026-11-13 as ff9e8b2da) added the step to
  docker-runtime-acceptance.yml + podman-acceptance.yml + the script — observability-acceptance.yml
  was NEVER in its write-set. So there is no "restoration": the dedicated
  `Acceptance · Observability Full Stack` gate (the only route that executes
  `TestObservabilityFullStackAcceptanceInCI`) never had a verified ORAS bootstrap.
- The same ORAS gate gap also explains the PR #1680 podman failure; it is an
  acceptance-environment (gate workflow) issue, not product behavior. Product side is proven
  unaffected: the fail-closed consent message in `cmd/baha/oras_setup.go:43` is required behavior
  and is pinned by `cmd/baha/oras_setup_test.go:29` (`TestEnsureORASForCoreUpRequiresExplicitInteractiveConsent`,
  "noninteractive" case must fail without installing) and `:74` (`TestRuntimeUpRequiresORASBeforeCoreBootstrap`).
  Changing that path would weaken the consent boundary — out of scope and explicitly not done.

## FINDING for the Owner (`.github/**` is Owner scope — not edited by this lane)

Needed change (exactly the PR #1528 pattern, mirrored into the observability gate):

1. `.github/workflows/observability-acceptance.yml` — add to BOTH jobs (docker and podman):
   after `- name: Prepare verified rootless runtime` (lines 56 and 126 on current develop) insert
   `- name: Install verified ORAS for Core bootstrap` / `run: bash scripts/ci-install-oras.sh`,
   before `Run focused full-stack observability acceptance` (lines 74 and 182).
2. Routing: `scripts/pr-gate-coverage.json` — add a mapping entry so
   `internal/application/runtime_observability*.go` selects
   `source.gate.atomic.docker.observability` and `source.gate.atomic.podman.observability`
   (precedent: the catalog already maps `cmd/baha/app_observability_acceptance_test.go` to both,
   and PR #1664 mapped `cmd/baha/oras_setup.go` the same way). Today a PR touching
   `internal/application/runtime_observability.go` runs NO native gate — the 0428-113 failure was
   only visible because a manually dispatched run happened to check out develop.
3. Re-execute: exact-SHA Docker dispatch must pass `ref=<full commit SHA>` explicitly; the
   prior dispatch used `ref: develop` default (see diagnosis). Workflow dispatch defaults
   (`.github/workflows/observability-acceptance.yml` `inputs.ref default: develop`) are the
   footgun; the dispatcher should always pin the SHA.

This lane starts no rerun and no workflow_dispatch (mission GRENZEN: KEIN .github, no rerun/dispatch).

## SCOPE DECISION — observability/registry.go write conflict with #1677/102 (mission item 3)

- Mission warned `observability/registry.go` is touched in parallel by the #1677/102 line.
- This lane kept its change provider-side (logs) in `internal/application/runtime_observability.go`
  ONLY and touched ZERO lines of `internal/observability/registry.go` (PR #1680 write-set witness
  above).
- Measured overlap on real heads (fetch `refs/pull/1677/head` = 36bb90196 into a disposable probe
  in /tmp, applied with `git apply --3way`): both PRs are textual-merge CLEAN, but a combined build
  breaks: #1677 changes `observability.List` from 5 to 6 bool args (adds the application-class arg,
  `internal/observability/registry.go`), and my checkpoint's added test block calls the 5-arg form at
  `internal/application/runtime_observability_trace_source_test.go` (the re-enable block added in 504a8678c).
- Decision: do NOT pre-adapt to #1677's in-flight API (it can still change and the merge order is not
  mine to fix). #1680 stands on its own against develop and is green. Whoever integrates #1677 with
  #1680 (Luna/CI owner, merge order 1680-first per the card note "keep #1677 open until #1680 is
  accepted") adds the third `false` argument to those call sites — a one-line mechanical fix;
  it is documented here so it is not a surprise.

## Checks executed on the merged candidate 46de903f17bed8e451c7bb3ad2d5ec6a187b607e

- `go build ./...` → clean
- `go vet ./...` → clean
- `gofmt -l internal cmd` → empty; `git diff --check` → clean
- `go test ./internal/application ./internal/observability ./internal/metrics -count=1` → all ok
- `go test ./internal/application -run TestLegacyPrometheusTraceSignalIsReclaimedWithoutMetricsPolicy -v` → PASS (regression named by the card's Test binding)
- CI · Source & Quality on the exact head: run [44396957393](https://github.com/mcpdev80/baseharbor/actions/runs/44396957393), triggered by this lane's PR push, self-observed to TERMINAL: **completed success** (Workflow policy, Native gate plan, Trusted Plan, Source format, Focused Python, all Go unit shards, go-vet, go-build, PR Selected Checks = success; native/HA/release jobs correctly skipped; `PR · Native gate plan` selected no runtime gate — the catalog gap in the FINDING).
- Docker + Podman runtime acceptance: NOT executed (blocked by the ORAS gate gap; this lane may not edit `.github/**` nor dispatch). No claim of green runtime evidence — the card stays open on that requirement.

## repo-rule compliance

- Write-set: only the card's own two files (unchanged content this window; the window adds the develop merge commit). No `.github/**`, no security.go, no registry.go edits. No CI files touched.
- One candidate per chain: continued on the mission-named branch `lane-0428-113-docker-loki-ingestion-fix`; no second branch; push was a normal fast-forward merge commit (no force).
- No merge, no PR creation/closing actions beyond pushing to the existing PR head.
- No subagents (§4.8). All git/gh/test commands executed in this session.
- No containers/compose started on this coordinator host (docker not even present here; runtime tests belong to hosted gates/SSH test hosts).
- Remote truth measured only via `git ls-remote` / GitHub API; the quarantined `workers/baseharbor` checkout was never cited.

## CLEANLINESS

- No docker/podman compose projects started by this lane (witness: work happened in existing worktree `/home/marcel/dev/baseharbor-ecosystem/work/0428-113-wt`; probes were `git clone`/`git apply` only under /tmp).
- Probe worktrees (`/tmp/probe1677`, `/tmp/oras-probe`) removed before END; ps-witness below.

## END

END_BLOCKED mission-113-1680-fixes.md: candidate 46de903f1 on PR #1680 (develop merged, PR CI green on exact head, registry.go/#1677 overlap documented); required Docker+Podman Loki runtime acceptance blocked by missing ORAS step in observability-acceptance.yml (.github Owner scope, finding filed; card 0428-114) — runtime evidence cannot be produced by this lane.
