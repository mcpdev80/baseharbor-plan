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

## CI pickup (no .github changes)

The changed path is cmd/baha; scripts/pr-go-unit-shard.py discovers Test* names with
`go test ./cmd/baha -list .` and distributes them over the cli-0..cli-3 shards of the
"PR · Draft Go" jobs (workflow "CI · Source & Quality", event pull_request). The six test
names in the file all appear in `go test ./cmd/baha -list .` output; no trigger rule or
workflow file was touched.

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

## END witnesses

(candidate SHA + ls-remote + hosted run: pasted below as they are observed)

END line: see final section.
