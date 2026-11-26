# w281-0428-181-1819rebuild — Read-Only Clean-Rebuild Write-Set Recipe for PR #1819

## ROLE / SCOPE
Coordinator-authored read-only planning artifact. Card 0428-181, canonical lane
w54-0428-181-export, chain slot 3 (`#1842 -> #1812 -> #1819 -> #1820`).
Goal: produce the executable RE-PUBLICATION recipe that a future reissue lane will
run, WITHOUT mutating anything. HARD LIMIT = READ ONLY.

## VISIBLE ANSATZ BLOCK (must precede first commit)
- owner (verbatim from origin/main at runtime): see below (`python3 scripts/plan.py show 0428-181`)
- git user.name: w54-0428-181-export
- git user.email: w54-0428-181-export@baseharbor.local
- per-commit invocation (for EVERY commit AND merge in the reissue):
  `git -c user.name=w54-0428-181-export -c user.email=w54-0428-181-export@baseharbor.local commit ...`
- pre-push gate: `git show -s --format=%an`  (must print `w54-0428-181-export`)

## ZERO-MUTATION PROOF (this lane w281)
- No `git commit`, no `git push`, no `git merge`, no `git rebase`, no `git checkout -b` with mutation.
- No tests run on host (no unittest/pytest/go test/ci-fast-check.sh).
- No `.github`, no card files, no plan-main direct write.
- Only read-only git commands: `git ls-remote`, `git diff --name-status`, `git log --oneline`,
  `git show --name-only`, `git cat-file -e`, `git merge-base --is-ancestor`.

## CLEANLINESS
- No containers/compose started. `docker ps -a`: N/A (none started by this lane).
- No scratch under ecosystem root: clone at `/tmp/wt1819` (outside ecosystem root).

---

## (1) REMOTE WITNESSES (all via `git ls-remote https://github.com/mcpdev80/baseharbor.git`)
- develop tip (origin/main of product): `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee` refs/heads/develop
- #1819 head: `b3c5055ad2566b639c2b0d4f4c2848b045221ebf` refs/pull/1819/head — OPEN, base=develop
  title: "0428-181 wire Perses identity dashboard into export path"
  updated 2026-11-25T20:56:51Z
- #1812: branch `0428-1812-env` absent from remote; PR #1812 already MERGED into develop (its content is
  on develop — do NOT re-apply). Its head `0922888af` is NOT on remote (merged-away).
- #1842: remote tip of lane carrying it = `8b8f0eb2d77c778e77b72d241152df7db31c1b6a`
  (refs/heads/w250-1842-fix). #1842 must land on develop BEFORE the 14-gate fires (see §5).
- #1820: `54446a73439341a85a6e47597a9ed0e9955f23e8` (refs/heads/w219-0428-271-0428-286-1820hop-evidence)
  — re-publishable ONLY after #1819 merges.
- #1818: branch absent from remote (merged-away / off-chain); not a dependency of the reissue.

## (2) EXACT WRITE-SET (from `git diff --name-status origin/develop...b3c5055a`)
```
M  .github/workflows/pre-release-runtime-suite.yml
M  internal/application/runtime_postgres.go
A  internal/metrics/perses_dashboard_provision.go
A  internal/metrics/perses_dashboard_provision_test.go
```

### Classification
- (a) CARD-SCOPED CONTENT — re-apply ONLY (0428-181):
  - `internal/metrics/perses_dashboard_provision.go` (A) — author 17381017 fix(0428-181) RC1/RC2
  - `internal/metrics/perses_dashboard_provision_test.go` (A) — author 17381017 (3 regression tests)
  - `internal/application/runtime_postgres.go` (M) — author 9f84f47a "0428-181 wire Perses..."
    Additions: call site `ensurePersesDashboardRuntime(...)` (EnsureRuntime, ~+16 lines @@@141)
    + seam `RegisterPersesDashboardProvisioner` / `persesDashboardProvisioner` /
    `PersesDashboardRuntimeRoot` / `ensurePersesDashboardRuntime` (+~100 lines @@378/449).
- (b) TEST-ONLY / CI-ROUTING COMPANION (re-apply with the card):
  - `.github/workflows/pre-release-runtime-suite.yml` (M) — the two `docker/podman load` blocks
    (lines ~350 and ~391). This is the CI route that lets the reissue's runtime gate run on old lanes;
    it is Owner-scope (.github/**). Reissue lane MUST NOT edit it directly — report as a :2048 finding
    with file:line if the load-block is missing on the target base.
- (c) FOREIGN-CARRIED CONTENT — belongs to ANOTHER card, MUST NOT ride along:
  - `.github/workflows/pre-release-runtime-suite.yml` reload-line `9140b2cb "ci: reload candidate image
    before runtime publish"` (lane **w249 runtime-image-fix**) — the two `image inspect … docker/podman
    load` blocks. NOT 0428-181.
  - `scripts/release-requirements.json` net diff = `3859d466 "release-requirements: add v0.4.28 to 14
    docker/podman light gate rows"` MINUS `10129196 "Drop scripts/release-requirements.json from #1812"`
    (lane **w198 / PR #1746 trace, v0.4.28 gate work**). This file is NOT in the 0428-181 write-set at all
    (it is not touched by 9f84f47a/17381017) — do not touch it.

### Ancestry proof (required before any reissue branch)
- `git merge-base --is-ancestor origin/develop b3c5055a` => **NO** (the candidate was hop-mutated).
- `git log --oneline origin/develop..b3c5055a` lists ONLY: 9f84f47a, 17381017 (0428-181) PLUS
  9140b2cb, 64d3dc0e, 2ea41620, 3859d466, 10129196, eafd5e6d, 394559ec, a3ee25f6, b3c5055a (foreign).
  → A single foreign commit in this list is a scope violation if carried into the reissue. This is the
  concrete proof of WHY the clean reissue is required.

## (3) BUILD RECIPE (commands, not prose — for the future reissue lane)
Base ref to cut from (attest SHA first):
```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
# -> ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee   (write this into the akte; prove it is an ancestor)
```
Reissue branch (cut from develop tip, NOT from the hop-mutated 1819 head):
```
git clone --no-checkout https://github.com/mcpdev80/baseharbor.git wt1819-reissue && cd wt1819-reissue
git fetch origin develop
git checkout -b lane-0428-181-pr1819-reissue origin/develop
git checkout b3c5055ad2566b639c2b0d4f4c2848b045221ebf -- \
    internal/metrics/perses_dashboard_provision.go \
    internal/metrics/perses_dashboard_provision_test.go \
    internal/application/runtime_postgres.go
# per-file conflict handling if develop moved:
#   git diff --cached --name-only            # what landed from the checkout
#   git checkout HEAD -- <path>               # or: re-derive the file from 17381017 (RC2) and re-stage
#   STOP + STATE with file:line if a path cannot resolve to the reviewed blob
```
Identity for EVERY commit and merge (never bare `git commit`):
```
git -c user.name=w54-0428-181-export -c user.email=w54-0428-181-export@baseharbor.local \
    commit -m "0428-181 reissue: clean single-lane republish of reviewed Perses export wiring"
```
Payload guard (must be non-empty AND exactly the (a)/(b) list — NO foreign path):
```
git diff develop...HEAD --name-status
# EXPECTED:
# A  internal/metrics/perses_dashboard_provision.go
# A  internal/metrics/perses_dashboard_provision_test.go
# M  internal/application/runtime_postgres.go
#   (plus the .github load-block ONLY if the reissue lane is authorised/patched for it)
```
Ancestry proof (fail before push):
```
git merge-base --is-ancestor origin/develop HEAD
git log --oneline origin/develop..HEAD    # must list ONLY 9f84f47a/17381017-derived commits
git show -s --format=%an                   # pre-push gate -> w54-0428-181-export
```

## (4) DEPENDENCY PROOF — what must already be on develop for the reissued head to build & qualify
- **Seam-C `persesDashboardProvisionForLifecycle`** (the `fn` passed to the registration seam from the
  metrics `init()` at `perses_dashboard_provision.go:309`): the mission's claim "exists only in the #1819
  candidate at file:84" is **partly wrong** — the symbol is at `perses_dashboard_provision.go:309`, not
  :84 (line 84 is a `RuntimeFiles{}` struct literal). Regardless, the truth holds: **this reissue IS what
  puts the provisioner + its consumer onto develop.** On `origin/develop` the symbol `persesDashboardProvisionForLifecycle`
  does not exist (grep of the develop blob is empty). So the reissue is self-sufficient for build-ability;
  it carries both sides of the seam.
- **Catalog rows from #1822**: already MERGED on develop — `persesDashboardCatalog()` (`perses_dashboards.go:487`)
  defines exactly-once the four keys `prometheus-targets`, `loki-logs`, `tempo-traces`,
  `postgresql-targets`, `mongodb-targets` (`:487-529`), resolved via `persesDashboardCatalogWithResolved`
  (`:531`). No #1819 commit touches these rows → exactly-once holds; the reissue must NOT re-add them.
- Build also needs the existing `capability.FilterEligibleDashboards` and `perses_dashboards.go`
  (`persesDashboardForBackend :590`, `manifestPersesSelected :425`, `PersesDashboardAvailability :688`) —
  all present on develop.

## (5) GATE PREVIEW — which native gates EXECUTE for the clean reissue write-set (current tip ac7c970)
Source: `scripts/pr-gate-plan.py` (present on develop).
- `internal/application/runtime_postgres.go` → covered by `CODE_CHECKS` `go test ./internal/application/...
  ./contracts/...` (`:71`) and the broad CONSERVATIVE `go-unit-tests` `go test ./... -count=1` (`:1745`).
  Metrics files → same unit gate (`go test ./...`). The 3 new tests (`perses_dashboard_provision_test.go`)
  are package-discovered by `go list ./...` / `go test -list`; NO per-test registration list required
  (AGENTS doctrine: ordinary Go unit tests are auto-discovered).
- `internal/metrics/perses_dashboard_provision.go` + `_test.go` → unit gate `go test ./... -count=1` (`:1745`).
- `.github/workflows/pre-release-runtime-suite.yml` (the `.github/**` Owner-scope path) → triggers the
  **Atomic Acceptance Gate** (`pre-release-runtime-suite.yml:1 name:`) + the runtime-light/heavy matrix
  (`scripts/release-requirements.json` rows `110-317`: atomic/docker/{guided,lifecycle,policy,connectivity,
  reconciliation,failure,full-destroy,data-capabilities,observability,identity,security}).
- **14-gate fire (w276):** fire-ready is **conditional on #1842 landing on develop first**. #1842 remote tip
  currently `8b8f0eb2d77c778e77b72d241152df7db31c1b6a` (w250-1842-fix) — must be merged before the reissue's
  docker/podman gates qualify. Until then the runtime gates are expected **SKIPPED / not-fired** (documented
  as STATE, not as a pass or a failure of the reissue content).
- Expected SKIPPED on the reissue: any heavy runtime gate gated behind #1842, and release-matrix rows that
  bind only after merge. Report skipped as STATE, never as a pass.
- #1820 (#1818) may be re-published ONLY after #1819 merges — chain order enforced by depends_on.

## (6) ONE-LINE ANSWER
The #1819 reissue is **strictly a RE-PUBLICATION of already-reviewed content** (commits 9f84f47a + 17381017)
moved onto a clean develop base, stripped of foreign commits (w249 `9140b2cb` reload-line, w198/1746
`3859d466`+`10129196` release-requirements) — NO new product work is required; the seam-C `persesDashboardProvisionForLifecycle`
is carried by the reissue itself and #1822 catalog rows are already on develop.

## PLAN PR
- Reissue recipe published on MY OWN plan branch via a plan PR (NOT merged by me; merge is Owner/Codex).

## END_DONE
Lane w281-0428-181-1819rebuild: read-only recipe authored; zero mutation; witnesses + write-set + dependency +
gate-preview + verdict captured above.
