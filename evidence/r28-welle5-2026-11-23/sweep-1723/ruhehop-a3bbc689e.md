# 0428-199 / #1723 — RUHE-HOP onto develop >= fc3eecbf4 (rev-parse am tag massgeblich)

Date: 2026-11-23
Lane/sitz: w076-0428-076-1789rest (mission sitz ffe7611b, hinter der 1793-kette)
Mission: /tmp/opencode/m_ffe_1723cd.md.g
Candidate branch: `lane-0428-199-workloadport` (mission-named, single candidate), worktree
`/tmp/opencode/1723-sweep-wt`.

## PLAN

1. Locate the mission branch and attest remote layout (REMOTE GUARD first).
2. fetch + rev-parse origin/develop; tip must be >= fc3eecbf4 (#1793 merged) — take the higher tip.
3. ONE `git merge --no-ff origin/develop` (no force/rebase/amend); union-style resolution where base consolidated.
4. BELEG before push: katalog byte-identical to develop; changed files == 0428-199 write-set; .github untouched; ancestry + log-line proof; focused local checks.
5. Push + `ls-remote refs/pull/1723/head` witness; PR stays OPEN; KEIN merge by lane.
6. One PR-triggered run watched to terminal; END with head + run-id + gates.

## Remote layout (REMOTE GUARD — first git actions)

`/tmp/opencode/1723-sweep-wt` (existing mission worktree, no second checkout created):

```
lane-origin  https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin  https://github.com/mcpdev80/baseharbor.git (push)
origin       https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
```

Only the github.com/mcpdev80 URL was used for fetch/push. (An unrelated, untracked
`lane-origin -> …/baseharbor.git` mapping existed without a push URL; untouched.)

## Base attestation (rev-parse am tag massgeblich)

- Mission start: `git ls-remote lane-origin refs/heads/develop` →
  `826d498fc1ae9524112d07477a8809798d8272a7` at first fetch; the documented mission tip floor
  fc3eecbf4 (#1793) and the prior hop base b3df96348 are both ancestors of it.
- Mission-named head attested pre-work: `refs/heads/lane-0428-199-workloadport` and
  `refs/pull/1723/head` were BOTH `7ade9ee08` (a hop merge whose second parent is the named
  6de8ebd9e, base 15c65213-stage, three tip-stages old; its old green run 45123039781 = history).
- Base tip moved twice more during this turn (parallel merges): b517b279c, then a3bbc689e (#1763).
  Per mission "hoeheren tipp nehmen" the FINAL hop onto a3bbc689e is the delivered candidate.

## Hop

- Hop 1: `git merge --no-ff --no-edit lane-origin/develop` (b3df96348) → 67e0e3484 (ort, zero conflicts).
- Hop 2 (base had moved to 826d498fc): second `merge --no-ff` → 019074b44 (zero conflicts).
- Pushed 019074b44 + witnessed; PR-run 45143306703 watched to terminal `completed / success`.
- Hop 3 (final, base a3bbc689e at push time): `merge --no-ff` → **37ddf3bdca8a0115f5c57b93740a21c90e13ac62**
  (parents 019074b44 + a3bbc689e), zero conflicts;
  `git merge-base --is-ancestor lane-origin/develop HEAD` → exit 0.

## BELEG (before each push)

- `git diff lane-origin/develop HEAD -- scripts/pr-gate-coverage.json` → **0 lines at every
  candidate** (catalog byte-identical to develop, including final 37ddf3bdc vs a3bbc689e).
- Content delta vs develop (`git diff lane-origin/develop...HEAD --name-only`): exactly the
  0428-199 write-set — `cmd/baha/app_apply.go`, `cmd/baha/app_workload_ports.go`,
  `cmd/baha/runtime.go`, `cmd/baha/workload_port_local_regression_test.go` (221 insertions,
  1 deletion). No other files.
- `.github/**`: 0 files in the diff; no workflow edited or triggered by lane.
- `git log --oneline lane-origin/develop..HEAD` → only this lane's own chain (hop merges + the
  0428-199 hop history 7ade9ee08/6de8ebd9e/59f3470bb/198f9bdad/d7b4f1b3d/…); no foreign candidate.
- Focused local checks (no full local suites): `go build ./...` exit 0; `go vet ./cmd/baha/` exit 0;
  named-form package run `go test ./cmd/baha/ -count=1 -skip
  "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` → `ok 439s`;
  python gate group `scripts.test_ci_check_routes test_pr_required_final test_pr_ci_fallback
  test_pr_gate_plan test_pre_release_runtime_reuse test_pr_diff_base test_targeted_gate_ref` →
  EXIT 0 `OK` (the whole-module `test_pr_gate_plan` run is slow on this memory-pressured host —
  measured 27 s per test, module finished OK in background, exit 0).

## New-test CI reachability (gate rule)

`workload_port_local_regression_test.go` (7 tests) is reachable by real CI without any route
change: the catalog maps all four changed files to `source.gate.atomic.{docker,podman}.data.capabilities`
(runtime.go additionally to `…guided`), and the GitHub workflows execute the full `./cmd/baha`
package on the release-source job (`go test ./cmd/baha`, ci.yml:129) plus the named native
`docker/podman data-capabilities` cells. Run 45143306703 proves it: `PR · Native ·
native/docker/data-capabilities` and `native/podman/data-capabilities` executed and succeeded on
the candidate containing the new test. No `.github` change needed.

## Push + witnesses

- `git push lane-origin HEAD:refs/heads/lane-0428-199-workloadport` → `019074b44..37ddf3bdc`
  (earlier: `7ade9ee08..019074b44`).
- `git ls-remote lane-origin refs/pull/1723/head refs/heads/lane-0428-199-workloadport refs/heads/develop`:

```
a3bbc689e4da70da73a0dcf5370d9a9e2e81d24d  refs/heads/develop
37ddf3bdca8a0115f5c57b93740a21c90e13ac62  refs/heads/lane-0428-199-workloadport
37ddf3bdca8a0115f5c57b93740a21c90e13ac62  refs/pull/1723/head
```

- PR #1723: state OPEN, isDraft=false, base develop. KEIN merge performed by this lane.

## Hosted CI (Eigenes-Run-Pflicht)

- Run on 019074b44 (base 826d498fc): **45143306703**, pull_request, watched to terminal
  `completed / success`. Executed-and-green (16 of 39 jobs correctly skipped, matrix-conditional):
  PR · Trusted Plan, PR Selected Checks, Source format, Runner Interface, Focused Python, Demo Pin,
  cli-gofmt/go-build/go-vet, Go unit cli-0..3 + owner + packages, Selected Runtime
  docker·guided, docker·data-capabilities, podman·data-capabilities, Native
  native/docker/data-capabilities + native/podman/data-capabilities.
- Run on final head 37ddf3bdc (base a3bbc689e): **45147022935**, pull_request, watched to terminal
  `completed / success` — 23 executed-and-green (PR · Trusted Plan, PR Selected Checks, Source
  format, Runner Interface, Focused Python, Demo Pin, go-build/go-vet/cli-gofmt, Go unit
  cli-0..3+owner+packages, Selected Runtime docker·guided + docker/podman·data-capabilities,
  Native native/docker + native/podman·data-capabilities), 16 correctly-skipped matrix jobs.
- develop moved again after that run (a3bbc689e → 304b3ad1d, #1798): initially recorded as no
  write-set touch; the reviewer verdict then demanded base EXACTLY current develop, so the LAST
  HOP followed (next section).

## EIN LETZTER HOP (coord order 2026-11-23 10:0x, reviewer-verdict REQUEST CHANGES)

- Delta check first: `git diff --name-only a3bbc689e..origin/develop` → app_new_wizard_test.go,
  application_provider_preferences.go, scripts/pr-gate-coverage.json — grep for
  app_apply|workload_ports|runtime.go|workload_port_local → **no write-set touch** (no STOP).
- `git fetch lane-origin develop && git rev-parse lane-origin/develop` →
  `304b3ad1d88647377ea647d0d94174bfc9298e14` (== ordered tip); HEAD stood at 37ddf3bdc.
- ONE additive `git merge --no-ff --no-edit lane-origin/develop` →
  **340e66a881e60e20252ef5b284ca95e959732b59** (parents 37ddf3bdc + 304b3ad1d), zero conflicts;
  ancestry exit 0; catalog `git diff lane-origin/develop HEAD -- scripts/pr-gate-coverage.json`
  → 0 lines (BYTE-EQUAL develop); content delta still exactly the 4 write-set files; 0 .github;
  `go build ./...` ok and planner MappingTests group green locally (cheap pre-check only).
- Push `37ddf3bdc..340e66a88`; `git ls-remote lane-origin refs/pull/1723/head
  refs/heads/lane-0428-199-workloadport refs/heads/develop` →
  branch + PR head `340e66a88…`, develop `304b3ad1d…` (PR BASE == current develop, EXACT).
- Run **45153328164** (pull_request, head 340e66a88) watched to terminal: `completed / success`;
  23 executed-and-green jobs (PR · Trusted Plan, PR Selected Checks, Source format, Runner
  Interface, Focused Python, Demo Pin, go-build/go-vet/cli-gofmt, Go unit cli-0..3+owner+packages,
  Selected Runtime docker·guided + docker/podman·data-capabilities, Native data-capabilities),
  16 conditional skips. **TP BASE_SHA witness:** job log line
  `BASE_SHA: 304b3ad1d88647377ea647d0d94174bfc9298e14` — the exact ordered base.

## cleanliness

- git-only hop + read-only CI probes + focused local unit runs; no containers, compose projects,
  networks or volumes started by this lane on this host (test-runner rule honored: named-form
  `go test` with RunsRealLifecycle skipped; zero stray lifecycle containers observed).
- `docker ps -a` on this host: zero containers (header only) before and after; ambient untouched.
- Files created only inside the existing worktree /tmp/opencode/1723-sweep-wt and this
  plan-repo evidence directory.

## STOPP (coord/owner-ordering 2026-11-23 10:5x) — hop ruht, lane idle bis freigabe

- Order: NO further hop on #1723 before #1801 merges (1801 is priority, running on f6ab22b7d with
  2 native jobs active). Sequence after that: 1801 terminal -> review/merge -> THEN one single hop
  onto the post-1801 tip. No push, no run from this side until release.
- State at STOP (as left, nothing rolled back): branch + `refs/pull/1723/head` == **12bf50c4c**
  (hop merge onto f6ab22b7d, delivered and ls-remote-witnessed before the stop arrived); the
  auto pull_request run 45159172695 was `queued` at STOP time — the lane observes NOTHING further
  of it and starts nothing new. PR #1723 OPEN, non-draft, mergeStateStatus BLOCKED (base moved
  after the stop: #1801 pending).
- Earlier delivered chain this shift stands as evidence: 340e66a88 @ 304b3ad1d, run 45153328164
  completed/success with TP log `BASE_SHA: 304b3ad1d…` (section above).

## END

- HEAD: 12bf50c4c8dbeadeb5fa9324fdafa4069e267d8d (lane-0428-199-workloadport; hop work STOPPED per
  owner-ordering — further hop awaits #1801 merge and coordinator release)
- STATUS: BLOCKED (extern: #1801 merge must land first; lane idle, no push/run until release)

## Evidence-on-origin/main verification (second-to-last action)

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main \
    && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep sweep-1723/ruhehop-a3bbc689e
 * branch                main       -> FETCH_HEAD
evidence/r28-welle5-2026-11-23/sweep-1723/ruhehop-a3bbc689e.md
(origin/main tip 38cc2f9ed; evidence push 84178f505..38cc2f9ed)
```

Planning repo remote (verified before first evidence commit):
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` →
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
