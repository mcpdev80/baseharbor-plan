# mission-093-1663-fixes — rebase-window-2 (base freshness + failing-check fixes, PR #1663)

Card: t-20261115-bughunt-d28-i18n-achtung (0428-093), PR #1663, branch
`lane-0428-093-i18n-abachtung`. Continues `rebase-window-1.md` (same folder).
Candidate under repair: `b6055fd47` with 5 failing checks in run 44025048848.

## Planning-repo verification (wrong-zone check)

    $ pwd && git rev-parse --show-toplevel
    /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan   (real planning repo, NOT workers/baseharbor-plan)

Remote truth witnesses (ls-remote only; workers/baseharbor never cited):

    907f16713cbf38693d30c9dadaad7fe299759219  refs/heads/develop
    b6055fd47a160b47f55c9f2c50317a014d313091  refs/heads/lane-0428-093-i18n-abachtung  (at mission start)

Claim: card state `review`, owner `coord` (existing claim untouched; this lane
acts on coord's dispatch, no claim churn).

## PLAN

1. Reality sync + claim check (ls-remote, PR state, prior act) — DONE
2. Diagnose the 5 failed checks of run 44025048848 against rebase-window-1 — DONE
3. `git merge origin/develop` (normal, no force, no rebase) — DONE (candidate 4ef41a31)
4. Targeted fixes only inside the write-set; develop-side bugs → STOP + finding — DONE (no fixable delta; develop-side cause repaired by merged #1679, carried via base merge; docs-surface scoping finding recorded in AC1a)
5. Push, observe exact-head run to TERMINAL — DONE (run 44396406150 completed/success, own poll loop to terminal)
6. This act committed and pushed to origin/main — DONE (see push witness below)
7. Cleanliness sweep + END post — last action

## Diagnosis of the 5 failing checks (run 44025048848 on b6055fd47)

Failed jobs: docker app-gate, docker coreless-lifecycle aggregate, podman
app-gate, podman coreless-lifecycle aggregate, `PR Selected Checks` (aggregate).
All five trace to ONE root cause documented in rebase-window-1: at
`cmd/baha/application_otlp_handoff_runtime_test.go:120` the shared-identity
union reports `Action:add` for `opentelemetry-collector/shared` during apply,
and verify then fails on `native OTLP trace source prometheus:... has no
runtime probe adapter` (`cmd/baha/app_traces.go` `nativeTraceSourceProbe`,
default branch). Rebase-window-1 proved this reproduces IDENTICALLY on neutral
develop@bcae1e8c without any branch content — a develop-side bug inherited by
the branch, NOT the i18n candidate. The podman-side `stale-impact-consent`
line was triaged as a possible Flake, not in scope.

## Base refresh and develop-side fix already merged

- Merged in: `origin/develop` @ `907f16713cbf38693d30c9dadaad7fe299759219`
  (current remote develop). One merge commit `4ef41a31f250b7824b57b874895790cc4435712a`,
  ort strategy, zero conflicts (merge-tree conflict count: 0). No rebase, no force.
- This develop head contains PR #1679 (`0ec4706b`, card 0428-108 "traceprobe"):
  the exact fix for the line-120 wound — `internal/observability/registry.go`
  keys mutations on provider, and `nativeTraceSourceProbe` (app_traces.go:171)
  now routes `ProviderOTelCollector` / `ProviderExternalOTLP` to the receiver
  export probe instead of the "no runtime probe adapter" default. The failure
  rebase-window-1 diagnosed was develop-side, and develop-side has since
  REPAIRED it; this lane carries that repair via the base merge.
- Write-set check: `git diff b6055fd4..HEAD` touches 49 files — ALL are the
  develop fold-in (0428-081 Perses/Valkey, 0428-100, 0428-108, 0428-109 docs).
  The only branch-content file in the diff region is
  `application_otlp_handoff_runtime_test.go`, which develop itself changed
  (#1657 empty-target, #1679) and which this lane did NOT edit.
  No targeted fix was possible or needed inside the write-set: per mission
  rule (3) a develop-side bug not curable here means STOP + finding — but the
  finding ("develop-side, owned by 0428-108") resolved by merge into develop
  before this window, so the base refresh alone is the complete remedy.

## Ancestries and own-commits proof

- `git merge-base --is-ancestor 907f1671 HEAD` → true (base attestation).
- `git merge-base --is-ancestor b6055fd4 HEAD` → true (candidate continuity).
- `git log --oneline origin/develop..HEAD` → exactly 4 commits, all lane-owned:
  `55550400` (the approved i18n content), `acb69658`, `b6055fd4`, `4ef41a31`
  (the three base merges). No foreign commit is carried on top.

## Local verification (on candidate 4ef41a31)

- `go build ./...` → PASS. `go vet ./cmd/baha ./internal/observability` → PASS.
  `gofmt -l cmd internal` → clean.
- `go test ./internal/observability/` → ok.
- `go test ./cmd/baha/ -run 'Achtung|Warning|Contract|Marker'` → ok
  (0428-093 regression `TestProviderImpactConsequenceHintIsEnglishOutputAndContractMarker` passes).
- The decisive proof is the hosted native docker+podman gate on the exact head
  (Eigenes-run-pflicht below); no local container was started on the
  coordinator host (AGENTS: tests only on the named SSH hosts).

## Push witness

    $ git push origin lane-0428-093-i18n-abachtung
       b6055fd4..4ef41a31  (fast-forward, no force)

    $ git ls-remote origin refs/heads/develop refs/heads/lane-0428-093-i18n-abachtung
    907f16713cbf38693d30c9dadaad7fe299759219  refs/heads/develop
    4ef41a31f250b7824b57b874895790cc4435712a  refs/heads/lane-0428-093-i18n-abachtung

## CI run (Eigenes-run-pflicht)

Run `44396406150` (`CI · Source & Quality`, event=pull_request) started on exact
head 4ef41a31f at 2026-11-18T20:57:21Z. Terminal outcome, observed by this
session's own poll loop (watcher) until terminal:

    run_id=44396406150 status=completed conclusion=success sha=4ef41a31f250b7824b57b874895790cc4435712a
    https://github.com/mcpdev80/baseharbor/actions/runs/44396406150

All five previously failing checks are now green on the exact head:

    PR · Selected Core-less · docker / ... · coreless-lifecycle            success
    PR · Selected Core-less · docker / ... · coreless-lifecycle · application  success
    PR · Selected Core-less · podman / ... · coreless-lifecycle            success
    PR · Selected Core-less · podman / ... · coreless-lifecycle · application  success
    PR Selected Checks                                                      success

No failure or cancelled jobs in the run (jobs[] failure filter → empty). The
55550400-era go-build/vet/gofmt/unit/documentation checks were SUCCESS as well.
This confirms the rebase-window-1 diagnosis end-to-end: the branch inherited
develop-side red, develop-side #1679 (0428-108) repaired the cause, and the
base merge to 907f1671 made the candidate green without any content change.

## Test binding / CI mapping

No new test was added by this lane; the existing 0428-093 regression test runs
in `release_source_preflight` (`go test ./cmd/baha`) and the Go-unit cli shards.
The inherited native OTLP handoff gate is executed by the
`PR · Selected Core-less · {docker,podman} / PR selected · integration/* coreless-lifecycle · application`
jobs, triggered by the pull_request path selection. That selection logic lives
in `.github/**` (Owner scope) — untouched here.

## VM smoke state

Before dispatching anything: `ssh baha-docker` → `docker ps -a -q | wc -l` = 0;
`ssh baha-podman` → no `bh-*`/baseharbor containers. Both hosts clean; no
compose project was started or left by this lane. Hosted CI runs on
GitHub-managed runners.

## Acceptance criteria (card fields empty — enumerated by this act)

- AC1: The Germanism `Achtung` no longer appears in English CLI output or the
  JSON contract: all 15 non-test sites changed — 9 user-facing prompt strings
  `Achtung:` → `Warning:` and the contract marker VALUE `Attention` field
  literal `Achtung` → `Warning` across the 3 composition setters, the
  normative JSON schema const (scope + impact) and goldens/testdata.
  Verified by `git diff origin/develop...HEAD`: only the literal string value
  changes; marker KEY names (`Attention`, `attention`) and every
  presence-based check (`!= ""`) are untouched — diff lines confirm the
  consent LOGIC is unchanged (label text and marker value only).
- AC1a (surface demarcation, corrector note 2026-11-18): the intended fix is
  the CODE / i18n-catalog surface (Go prompt strings, contract marker value,
  normative schema const, goldens); docs prose keeps the unified **Achtung**
  label (card 0428-107, already-compliant) and card 0428-106 concerns only
  the consent paths.
  FINDING (reality check on this candidate, not assumed): content commit
  55550400 ALSO renamed **Achtung** → **Warning** at 13 English doc-prose
  sites — `docs/cli/applications.md`, `docs/cli/targets.md`,
  `docs/how-to/external-providers.md`, `docs/how-to/machine-operations.md`,
  `docs/reference/backup-and-restore.md`, `docs/releases/v0.4.25.md`,
  `docs/releases/v0.4.25.preparation.md`, `docs/spec/capability-first-v0425.md`,
  `docs/spec/runtime-explorer-v1.md`, `docs/internal/v0.4.25-provider-mutation-coverage.md`
  and 3 `docs/internal/*.json` checkpoint files (per-file +Warning counts
  above, measured via `git diff origin/develop...HEAD -- docs/`). Under the
  demarcation these are OUT of the 093 surface (the EN docs carry a localized
  label choice, while DE docs intentionally keep **Achtung**).
  This window did NOT revert them unilaterally, because a doc revert is a
  content change to an already batch20-APPROVED candidate and must go through
  the review/abnahme decision; it is reported here as the scoping finding.
  Side evidence: `scripts/documentation-audit.sh` has no untranslated-germanism
  rule for `docs/**` (grep: no `Achtung`/`germanism` hits), so a revert would
  not redden any CI gate. Awaiting coordinator/abnahme ruling: either keep
  the docs sites (current green candidate 4ef41a31) or a follow-up revert
  commit on this same branch before merge.
- AC2: German docs (`docs/de/**`) remain German; English docs/contracts align
  to the renamed marker value.
- AC3: Regression test `TestProviderImpactConsequenceHintIsEnglishOutputAndContractMarker`
  (cmd/baha) covers one user-output case and one JSON-contract case.
- AC4: exact-head CI run 44396406150 TERMINAL SUCCESS on all required checks
  (result appended below; the previously red docker+podman
  `coreless-lifecycle · application` gates plus their aggregates and
  `PR Selected Checks` are the gate list that must be green).

## Required-check binding (card field empty — this act fixes the mapping)

- No new test was introduced by this card; the AC3 regression is
  auto-discovered normal Go test in package `cmd/baha`, executed by the
  existing CI jobs `PR · Go unit · cli-*` shards and `release_source_preflight`
  (`go test ./cmd/baha`), both on the `pull_request` trigger. No
  `REQUIRED_CLIENT_TESTS`/`pr-gate-plan.py` change is needed (test binding:
  normal/auto-discovered).
- The inherited native gates for the merge-base correctness are
  `PR · Selected Core-less · {docker,podman} / PR selected ·
  integration/{docker,podman}/coreless-lifecycle · application` (GitHub-hosted
  runners), same pull_request trigger. Their selection logic is in
  `.github/**` (Owner scope) — untouched by this lane.

## Handoff (card field empty — current state)

- Branch: `lane-0428-093-i18n-abachtung` @ `4ef41a31f250b7824b57b874895790cc4435712a`
  (base-fresh: develop@`907f1671` is an ancestor; own commits: i18n content
  `55550400` + three base-merge commits only). PR #1663 OPEN, mergeable=MERGEABLE.
- Content APPROVED earlier (batch20); this window only refreshed the base and
  re-qualified. The 5 prior FAIL checks (run 44025048848) had a develop-side
  cause (line-120 OTLP probe) which develop itself repaired via PR #1679
  (0428-108); the base merge carries that repair. No write-set fix was due.
- Gate to watch to acceptance: exact-head run 44396406150 terminal
  completed/success (observed, see CI-run block above). Open scoping ruling
  for the abnahme session: AC1a docs-prose finding (13 sites — keep vs
  revert-forward on this branch). This lane performs NO merge
  (abnahme-session merges after green terminal).

## END

END_DONE mission-093-1663-fixes.md: candidate 4ef41a31f (develop@907f1671
folded in, zero conflicts), run 44396406150 completed/success on exact head,
all 5 prior FAIL checks green; docs-prose scoping finding in AC1a for abnahme.

## repo-rule compliance

- No `.github/**` change; no PR merge; no rebase; no force-push; no subagent
  (§4.8); scratch under /var/tmp only; no container on the coordinator host;
  one candidate branch (`lane-0428-093-i18n-abachtung`), no second branch.
- Remote truth measured only via `git ls-remote` / `gh` against GitHub.
