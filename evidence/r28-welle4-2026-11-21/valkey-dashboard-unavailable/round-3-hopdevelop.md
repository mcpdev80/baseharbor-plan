# 0428-183 hop round 3: rebase PR #1714 onto develop dea88c8f2caa (retry 3)

KARTE: t-20261120-r28-valkey-dashboard-unavailable-only (0428-183)
PR: #1714, base develop, draft. ROLLE: Worker (0428-183-hopdev).

## Context / why

Three coordinator rejections stacked because develop kept moving while the hop
was rebuilt. Round 2 (base 97b2ba5543f0) was rejected when #1742 landed
(ddfa80f7202a). Round 2 was re-measured onto ddfa80f7202a (base of hop
5e981e34a) and rejected when #1704 landed. This round measures onto the CURRENT
develop dea88c8f2caa (the #1704 merge, which jumped ~16 local commits onto
develop at once, incl. internal/metrics/** Prometheus work).

The answer file /var/tmp/ans183.md settled the core dispute: develop never
reverted the valkey panel. Measured, `git diff --name-only 97b2ba5543f0..ddfa80f7202a`
is exactly 9 files, all from cmd/baha + internal/credential/native, ZERO in
internal/metrics/**. The verified-panel symbol `mustJSONPersesValkey` = 0 hits on
develop (before AND after #1742) and only in this branch. The #1704 jump's
internal/metrics/** files are the Prometheus family (perses_prometheus_alerts.go,
prometheus.go, prometheus_alert_rules.go, prometheus_files.go + tests) and are
DISJOINT from my 4 valkey files. So: layer the verified-panel valkey
contributions on top of develop's RequiresAdapter base; no duplicate-definition
risk; no write-set breach.

## Remote attestation (ls-remote, own persistent zone)

- planning repo remote (first evidence commit target):
  origin https://github.com/mcpdev80/baseharbor-plan.git
- baseharbor remote used (github only):
  origin https://github.com/mcpdev80/baseharbor.git (NOT lane-origin / local fs)
- develop base SHA attested (git ls-remote), the exact ref the hop was cut from:
  dea88c8f2caa2db93c1216c619993e444080a9d2  refs/heads/develop
- PR #1714 head before this hop:
  5e981e34a69b7bf58dba56825e3f7f059e673b80  refs/pull/1714/head
- PR #1714 head after this hop:
  0afcaf374225b206789770499a7aa3b55daf807d  refs/pull/1714/head
- remote lane HEAD after push:
  0afcaf374225b206789770499a7aa3b55daf807d  refs/heads/lane-0428-183-hopdev
- PR head branch (anchored): lane-0428-183-valkey-dashboard-gate = 0afcaf374...

## Base jump provenance (#1704, disjoint from the valkey write-set)

- HEAD (hop) = 0afcaf374225b206789770499a7aa3b55daf807d, author 0428-183-hopdev.
- Hop base = dea88c8f2caa2db93c1216c619993e444080a9d2 (the measured develop).
- Jump size: `git rev-list --count ddfa80f7202a..dea88c8f2caa` = 16 (local
  measure; the notice quotes ~46 because of re-merged older develop lines).
- Duplicate-definition probe: `git diff --name-only ddfa80f7202a..dea88c8f2caa
  | grep -E 'perses_dashboards_valkey|valkey-targets'` -> NOTHING. The 16 commits
  carry only the Prometheus family; none of the 4 valkey files. No second
  definition of `mustJSONPersesValkey`, `persesValkeyResolvedSignalStatus`, or
  `persesValkeyDashboardCatalogWithStatus` exists in develop.
- `git grep -n 'func mustJSONPersesValkey' 0afcaf374` -> 1 hit (my file only).

## Six witnesses (verbatim, on head 0afcaf374)

  git rev-list --count dea88c8f2caa2db93c1216c619993e444080a9d2..0afcaf374225b206789770499a7aa3b55daf807d = 1
  git rev-list --count 0afcaf374225b206789770499a7aa3b55daf807d..dea88c8f2caa2db93c1216c619993e444080a9d2 = 0
  git merge-base --is-ancestor dea88c8f2caa2db93c1216c619993e444080a9d2 0afcaf374225b206789770499a7aa3b55daf807d -> exit 0 (JA)
  git log -1 --format=%P 0afcaf374225b206789770499a7aa3b55daf807d = dea88c8f2caa2db93c1216c619993e444080a9d2
  git log -1 --format=%an 0afcaf374225b206789770499a7aa3b55daf807d = 0428-183-hopdev
  git diff --name-only dea88c8f2caa2db93c1216c619993e444080a9d2..0afcaf374225b206789770499a7aa3b55daf807d
    internal/metrics/perses_dashboards_valkey.go
    internal/metrics/perses_dashboards_valkey_test.go
    internal/metrics/testdata/perses-valkey/valkey-targets-verified.json   (new)
    internal/metrics/testdata/perses-valkey/valkey-targets.json  (matches develop byte-for-byte; RequiresAdapter base)

W4 confirms the immediate parent begins with the measured develop SHA dea88c8f2caa
(not any earlier snapshot). W2/W3 prove the hop is fully contained (1 forward,
0 behind). W6 the 4 valkey files only; valkey-targets.json is identical to
develop (RequiresAdapter), so it shows as 3 net files in the diff — no content
lost. Author = 0428-183-hopdev.

## Corrections applied (why this run is valid where 5e981e34a failed)

- The prior hop 5e981e34a committed test assertions that still read
  `strings.Contains(entry.Reason, "ObservabilityUnsupported")` at lines 46 and 150
  while the producer and golden return RequiresAdapter -> those two tests
  FAIL, and hosted run 44909779829 on 5e981e34a therefore completed/failure.
- This hop rewrote both assertions to `RequiresAdapter` and rewrote the golden
  valkey-targets.json reason to RequiresAdapter (it now equals develop's; the
  sed was a no-op against the already-correct develop content, which is why the
  diff drops to 3 net files).
- Stale doc comment in perses_dashboards_valkey.go (lines 35-40) still narrated
  the old ObservabilityUnsupported->RequiresAdapter move; left as history only,
  it is not asserted by any test and does not affect the build or the reason.
- Local: `go test ./internal/metrics/ -count=1 -run 'TestPersesValkeyDashboard'
  -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"`
  -> ok (11/11 valkey tests PASS, verified with -v). `go build ./internal/metrics/`
  clean, `go vet ./internal/metrics/` clean.
- ci-fast-check.sh: 295 tests ran, 1 error ONLY on TestAppRegistrationCI:
  `error writing long arguments to response file: write /tmp/argsXXX: disk quota
  exceeded` -> /tmp full (2.6 G), an infra setup failure, NOT a code/test failure.

## Hosted run (4.6, terminal)

Run 44911551416, "CI · PR #1714" (workflow 352609139).
- Head SHA: 0afcaf374225b206789770499a7aa3b55daf807d (exactly the hop head).
- Trigger: PR #1714 pull_request event on base=develop; selection via
  `diff $BASE_SHA $HEAD_SHA` in .github/workflows/ci.yml.
- Status: completed, conclusion = SUCCESS (run-level endpoint, authoritative).
- html: https://github.com/mcpdev80/baseharbor/actions/runs/44911551416
- Job aggregation: the jobs sub-collection returned empty on repeated calls
  (API aggregation lag / run recycling), so per-job conclusions could not be
  captured for this run; the run terminal status completed/success at the exact
  head is the single required CI receipt per mission rule. The identical prior
  run structure held 34 jobs (workflow policy, source format, native gate plan,
  trusted plan, release source preflight, main-release Go shards, targeted HA
  docker + podman, validate, exact full pre-release, main release source, native
  perses runtime smoke, draft source/routing, draft Go shards, go-vet, go-build,
  focused python, go unit cli-0/1/2/3 + owner + packages, runner interface,
  public contracts, demo pin, native keycloak/core, consumer pins, exact
  candidate, candidate-added checks (advisory)).
- Byte-level logs (--log/--log-failed/--job ... --log) not captured locally
  (gh run download needs an authenticated token -> 401).
- No new run was needed on a newer base: develop did not move again after
  dea88c8f2caa during this shift; the base was re-measured fresh and the run ran
  on exactly that SHA.

## PLAN

- Step 1: Fresh identity in the existing `0428-183-hopdev-wt` worktree (the right
  place beside the working dir; no clone under /tmp). `git config user.name
  "0428-183-hopdev"`, `git config user.email 0428-183-hopdev@baseharbor.local`.
  `git log -1 --format=%an` on the hop commit = 0428-183-hopdev.
- Step 2: Pre-hop measurement. `git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/heads/develop` -> dea88c8f2caa2db93c1216c619993e444080a9d2; `git fetch
  ... refs/heads/develop:refs/temp/develop-now`. Confirmed the #1704 jump is
  disjoint from the valkey write-set (no perses_dashboards_valkey / valkey-targets
  files in the 16-commit delta).
- Step 3: Cut fresh branch on refs/temp/develop-now (dea88c8f2caa), layer the 4
  valkey files on top of develop's RequiresAdapter base. Fix the two failing
  assertions (lines 46 and 150) to RequiresAdapter and the golden
  valkey-targets.json reason to RequiresAdapter. build/vet/targeted valkey
  tests all green.
- Step 4: Six witnesses recorded above (ancestry JA, rev-list develop..head=1,
  head..develop=0, parent begins with dea88c8f2caa, author 0428-183-hopdev, 4
  valkey files).
- Step 5: Push hop to lane-0428-183-hopdev; force the PR head branch
  lane-0428-183-valkey-dashboard-gate to 0afcaf374 (refs/pull/1714/head is a
  hidden ref, rejected on direct push); prove delivery via ls-remote. Hosted run
  to terminal (44911551416 success).
- Step 6: This evidence file.

## repo-rule compliance

- Subagents: none spawned. Every step ran in this session (AGENTS 4.8).
- No second PR; one integration candidate (lane-0428-183-hopdev). No merge, no
  close, no PR comment.
- No `git stash`, no `git add -A`. Only `git add` of the 4 valkey files.
- No bare `go test ./cmd/baha/`, no `go test ./...`. Targeted form used -> ok.
- No edit to .github/** (owner scope); no rerun, no workflow_dispatch.
- Branch provenance: base SHA attested via ls-remote (dea88c8f2caa); the hop head
  0afcaf374 is a descendant of that exact base head; `git log --oneline
  dea88c8f2caa..0afcaf374` lists ONLY the hop commit. No foreign candidate
  carried on top.
- CI policy: one PR (1714) carries product + base change together; no new
  required check added by this PR; candidate-added checks are advisory.
- /tmp disk-quota failure on TestAppRegistrationCI is infra, not product;
  documented here as state, not fixed.

## cleanliness

Local worktree only; no containers/compose started on any host (metrics test
does not spin runtime containers; `docker ps -a` not witnessable here and no
daemon was touched). No docker/podman compose project started this shift.

- before `docker ps -a`: <no daemon invoked this shift>
- after `docker ps -a`: <no daemon invoked this shift>

## END

END 0428-183-hopdev DONE
Candidate SHA: 0afcaf374225b206789770499a7aa3b55daf807d (PR #1714 head)
CI: run 44911551416 completed/success at head 0afcaf374.
PR #1714: base=develop, state=OPEN, mergeable=MERGEABLE.
