# round-3 — 0428-075 define Perses prov seam

Lane: worker (flash) — correction round r3 on existing candidate
Date: 2026-11-14
Card: t-20261114-r28-perses-contract-seam (0428-075), release v0.4.28
Task: read mission-075-r3.md; fix CODEX-REVIEW R2 REJECT on PR #1575 (tests only)
PR: #1575 (DRAFT, base develop 0e9ccb582), https://github.com/mcpdev80/baseharbor/pull/1575
Branch: lane-0428-075-perses-seam (existing; kept working here, no second branch)
MERGE-FROST: no merge, PR stays DRAFT.

## SOURCE OF TRUTH

- akte: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r28-welle1-2026-11-14/vm-bughunt/act-1575-review-r2.md (plan main d49f7b73)
- task: /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/tasks/t-20261114-r28-perses-contract-seam.md

## PLAN

1. Read akte act-1575-review-r2.md; confirm scope: only cmd/baha/app_perses_cli_test.go changes.
2. Remote truth witnesses: ls-remote refs/pull/1575/head, branch head, develop base.
3. Worktree at exact remote head dc670bfd; fast-forward from stale local head.
4. (a) Rewrite faux CLI tests to execute the genuine baha command path via runWithIO over tmp roots, parsing the status output (precedent 175-r8).
5. (b) Replace the no-op filepath.Abs test with a real command execution.
6. (c) Add the unknown-owner fail-closed case through the CLI.
7. Verify locally: gofmt, go vet, go build, targeted test runs (x3 deterministic), full cmd/baha package + touched internal packages.
8. Commit + push to lane-0428-075-perses-seam; ls-remote + own-commits witnesses.
9. Write round-3.md evidence in baseharbor-plan, push to origin/main BEFORE END.
10. Watch hosted CI run on exact r3 head to terminal; record run-id + per-test PASS names.
11. Final: cleanliness, END line, post END to inbox 594fd2f5.

## Planning repo verification (wrong-zone guard)

Exact command and output before the first evidence commit:

`git rev-parse --show-toplevel`
`/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`

## Base attestation and branch provenance

Cut from the existing candidate head (the r2 reviewed head), which is on the named branch:

`git ls-remote origin refs/pull/1575/head refs/heads/lane-0428-075-perses-seam refs/heads/develop`
`0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop`
`dc670bfd4d32baf29afde0e4b021bfdb63f4e0be	refs/heads/lane-0428-075-perses-seam`
`dc670bfd4d32baf29afde0e4b021bfdb63f4e0be	refs/pull/1575/head`

Base SHA of this round: dc670bfd4d32baf29afde0e4b021bfdb63f4e0be (the exact r2 candidate and
current PR head; develop 0e9ccb582 is an ancestor of it, proven in the r2 akte via merge-base
exit 0). Ancestry witness for the r3 commit: `git merge-base --is-ancestor dc670bfd HEAD`
(r3 commit is a direct child of dc670bfd on the same branch).

Own-commits log over base develop (must show only this chain's commits):

`git log --format='%H %an <%ae> %s' origin/develop..HEAD`
(see END witnesses section below for the pasted post-push output)

## What r2 rejected and what r3 changed

R2 verdict: REJECT — documentation/seam part PASSED, only the tests carry nothing:

- Blocking 1: cmd/baha/app_perses_cli_test.go:22-47 called recordAppliedDeployment /
  application.ApplicationManagementUISurfaces / capability.PersesManagementSurfaceNow
  directly; no Cobra/baha command was executed.
- Blocking 2: :71-76 TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer was a no-op
  (filepath.Abs + unused context).
- Blocking 3: no unknown-owner scenario existed.

r3 changes (only cmd/baha/app_perses_cli_test.go; no feature, doc or .github changes):

- Every cell now executes the genuine production CLI entry `runWithIO` (global option
  parsing, context plumbing, command dispatch, effectiveTarget, resolver, JSON render) in
  both public forms `status --json` (repository-aware root command) and `app status --json`,
  over isolated temporary roots; assertions parse the CLI's own management_ui/checks output
  (persesStatusReport), not helper return values. Precedent 175-r8 applied in the
  go-test-internal variant the r2 recipe wording allows for the configuration-only seam
  ("execute the actual public baha status or baha doctor command path using an isolated
  temporary root and injected dependencies"); the repo-external host rule forbids starting
  any container stack on this session host, so no subprocess cell was added and no
  environment gate: all cells run unconditionally in the package.
- (a) TestBahaStatusPersesSurfaceFailsClosedAndUnverified: selected Perses -> the executed
  status command declares the observability surface with auth class unsupported and no
  authentication marker; unselected -> no surface at all (fail-closed); assertPersesSurfaceUnverified
  additionally refuses any management-ui check in ready/verified state.
- TestBahaStatusPersesSurfaceReachableOnlyWithObservabilityManagementUI: the gate cell now
  EXECUTES `status --json` (was: a direct ApplicationManagementUISurfaces call).
- (b) TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer: the no-op is gone; the cell
  executes both public status entry forms end to end over a tmp root and requires the two
  commands to agree byte-for-byte on the surface entry.
- (c) NEW TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI: a protected deploy
  directory whose deployment.json AND retained .owner band are gone has an unknown owner;
  the executed `baha app status --json` (repo face), `baha app status --uuid <id> --json`
  and `baha app show <name>` (external face) all fail closed — no report body, the
  damaged-state conflict surfaces, no trusted identity is attributed — and the tolerant
  display listing proves the underlying registry state is exactly one ownerless damaged
  entry (deployment.Ownerless()).
- TestBahaStatusPersesReportsUnsupportedAuthThroughCLI: the auth-boundary cell moved from a
  direct helper call onto the parsed CLI output (renamed from
  TestPersesSurfaceReportsUnsupportedAuthWhenNotConfigured; the old direct-call name is
  gone, the new name is discovered by `go test ./cmd/baha -list .`).
- TestPersesReleaseFailClosedOnUnknownAuthClass kept as the contract-seam guard the executed
  paths validate against.

Reachability stays 'unverified' everywhere; no container is started; no probe is faked.

## SOP witnesses (first END lines, per owner instruction 2026-11-14)

Exact `git ls-remote` of the product remote (final r3 head confirmed):

`git ls-remote origin refs/pull/1575/head refs/heads/lane-0428-075-perses-seam`
`c195a9a2049253accdf57a082e6eb33fc36ec7dd	refs/heads/lane-0428-075-perses-seam`
`c195a9a2049253accdf57a082e6eb33fc36ec7dd	refs/pull/1575/head`

Hosted run on the exact head: 43647090290 — completed/success (owner-run witness
confirmed identical). Shard PASS lines: see the hosted run record below.

Test-name PASS lines, executed locally by this lane on the exact r3 head
`c195a9a2049253accdf57a082e6eb33fc36ec7dd` (`go test ./cmd/baha -run
'TestBahaStatusPerses|TestPersesRelease' -v -count=1`, stable across 3 repeats):

```
--- PASS: TestBahaStatusPersesSurfaceFailsClosedAndUnverified (2.35s)
    --- PASS: TestBahaStatusPersesSurfaceFailsClosedAndUnverified/selected (1.17s)
    --- PASS: TestBahaStatusPersesSurfaceFailsClosedAndUnverified/unselected-fail-closed (1.18s)
--- PASS: TestBahaStatusPersesSurfaceReachableOnlyWithObservabilityManagementUI (0.48s)
--- PASS: TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer (2.38s)
--- PASS: TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI (1.16s)
--- PASS: TestBahaStatusPersesReportsUnsupportedAuthThroughCLI (1.22s)
--- PASS: TestPersesReleaseFailClosedOnUnknownAuthClass (0.00s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	7.605s
```

On the hosted shards the runner prints aggregate PASS lines and fails closed if a
selected test is missing or not passed; the six cells map deterministically onto
cli-0/cli-1/cli-3 under `scripts/pr-go-unit-shard.py` (mapping replayed below).

## CI pickup (no .github changes)

The changed path is cmd/baha; scripts/pr-go-unit-shard.py discovers Test* names with
`go test ./cmd/baha -list .` and distributes them over the cli-0..cli-3 shards of the
"PR · Draft Go" jobs (workflow "CI · Source & Quality", event pull_request). No trigger
rule or workflow file was touched. Replaying the shard selector on this candidate, the
six cells land deterministically and were each executed-and-passed (the shard runner
raises "CLI shard incomplete" on any selected test that is missing or did not pass):

- cli-0: TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer,
  TestBahaStatusPersesSurfaceFailsClosedAndUnverified, TestPersesReleaseFailClosedOnUnknownAuthClass
- cli-1: TestBahaStatusPersesReportsUnsupportedAuthThroughCLI,
  TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI
- cli-3: TestBahaStatusPersesSurfaceReachableOnlyWithObservabilityManagementUI

## Hosted run record (Eigenes-Run-Pflicht, watched to terminal by this lane)

Run: 43647090290, workflow "CI · Source & Quality", event pull_request,
headSha c195a9a2049253accdf57a082e6eb33fc36ec7dd (exact r3 candidate).
status=completed, conclusion=success. Observed by this session from dispatch to the
terminal result. Job results (all executed jobs; everything else skipped under draft
selection; no rerun or workflow_dispatch):

- PR · Draft source and routing: success
- PR · Draft Go · cli-0: success — log line: PASS cli-0: 411 passed / 13 intentionally skipped / 424 discovered; CLI inventory total=1675
- PR · Draft Go · cli-1: success — PASS cli-1: 405 passed / 10 intentionally skipped / 415 discovered; CLI inventory total=1675
- PR · Draft Go · cli-2: success — PASS cli-2: 407 passed / 19 intentionally skipped / 426 discovered; CLI inventory total=1675
- PR · Draft Go · cli-3: success — PASS cli-3: 395 passed / 15 intentionally skipped / 410 discovered; CLI inventory total=1675
- PR · Draft Go · packages: success

(The shard scripts print aggregate PASS lines, not per-test names; the per-cell pass
witness is each shard job's success, since the runner fails closed when a selected test
is missing, skipped-unexpectedly or not passed.)

## Local verification on the exact r3 candidate

- gofmt -l: clean; go vet ./cmd/baha: clean; go build ./...: OK (go1.26.8 per toolchain).
- go test ./cmd/baha -run 'TestBahaStatusPerses|TestPersesRelease' -count=1: PASS, run 4x
  (deterministic; subtests selected/unselected-fail-closed included).
- go test ./internal/capability ./internal/metrics ./internal/application -count=1: ok.
- Full go test ./cmd/baha -count=1 (with this PR's seam code + new tests): see CI run record
  and the local full-suite note in the END witnesses section.

## repo-rule compliance

- One candidate, one branch: worked on lane-0428-075-perses-seam; no second branch.
- Write set: cmd/baha/app_perses_cli_test.go only (plus this planning evidence file).
  No .github/**, no docs, no feature code (all passed r2).
- No subagents, no containers, no compose projects started by this lane (nothing to bring
  down; cleanliness: this session ran no docker/podman commands beyond read-only `docker
  info`/`docker context ls` on the coordinator host and a version probe of a built binary).
- No secrets logged. Evidence lives only in baseharbor-plan.
- Reality witnesses taken via git ls-remote against the product remote; the quarantined
  workers/baseharbor checkout was never cited.

## Local verification on the exact r3 candidate

- gofmt -l: clean; go vet ./cmd/baha: clean; go build ./...: OK (toolchain go1.26.8).
- go test ./cmd/baha -run 'TestBahaStatusPerses|TestPersesRelease' -count=1: PASS, run 4x
  deterministically (subtests selected/unselected-fail-closed included).
- go test ./internal/capability ./internal/metrics ./internal/application -count=1: ok.
- Full-suite context: this host (the coordinator/codeman machine) runs several lanes'
  `go test ./cmd/baha` package passes at once; a local full-package run under that load
  hit the 10-minute Go-test alarm in unrelated runtime cells
  (TestAppEditCommandCompleteProviderEditRunsRealLifecycle: "start real isolated Core for
  App Edit: existing native network lacks a protected Core or shared backend owner" — a
  shared-daemon fixture collision, present identically when the base candidate dc670bfd is
  run here; not a change introduced by this lane). The authoritative full-package verdict
  is the hermetic hosted shard runs recorded above, all green on the exact r3 head.

## END witnesses

Exact `git ls-remote` after the push (from the product remote of the worktree):

`git ls-remote origin refs/pull/1575/head refs/heads/lane-0428-075-perses-seam refs/heads/develop`
`0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop`
`c195a9a2049253accdf57a082e6eb33fc36ec7dd	refs/heads/lane-0428-075-perses-seam`
`c195a9a2049253accdf57a082e6eb33fc36ec7dd	refs/pull/1575/head`

Own-commits log base..HEAD (`git log --format='%H %an <%ae> %s' origin/develop..HEAD`):

`c195a9a2049253accdf57a082e6eb33fc36ec7dd lane-0428-075-perses-seam <lane-0428-075-perses-seam@baseharbor.dev> test(0428-075): execute the genuine baha status path for the Perses seam + unknown-owner fail-closed (r3)`
`dc670bfd4d32baf29afde0e4b021bfdb63f4e0be mcpdev80 <dev@pfingstgraef.eu> fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability`
`61f76fa18897d4a0709c09c27ae67e1ded8dba20 lane-0428-075-perses-seam <lane-0428-075-perses-seam@baseharbor.dev> feat(0428-075): define optional Perses provider seam (fail-closed)`

All three commits belong to this card's chain on the named branch (r1, r2, r3); no foreign
commit is carried on top. `git merge-base --is-ancestor dc670bfd4 HEAD` exits 0.

Pre-push remote witness of the planning repo (exact command and output):

`git ls-remote origin main`
`6bb7a3b457796a16b06b112ae3997e00fa83a4b4	refs/heads/main`

Post-push witness: main moved to c44acb61042be4e941ff1c697319624e2a7dbf3e (this file +
the card's evidence links).

Candidate SHA under review: c195a9a2049253accdf57a082e6eb33fc36ec7dd
Hosted run: 43647090290 (terminal, success; per-test PASS witness: the shard
aggregate lines above + the runner's fail-closed per-test completeness check).

Cleanliness: this lane started no containers, compose projects, networks or volumes and
left no state directories (all Go tmp roots are under /tmp and removed by the test
runner); docker was used read-only for an ambient `docker info` check. No .github/**
change; no subagent.

END mission-075-r3.md DONE — candidate c195a9a2049253accdf57a082e6eb33fc36ec7dd on
refs/pull/1575/head, run 43647090290 success.
