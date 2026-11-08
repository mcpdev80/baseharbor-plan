# 0427-136 app init Owner-Naht regression FIX — round-1

**Task:** t-20261108-bughunt-0427-appinit-owner-seam (karte 0427-136)
**Owner:** lane-w136-appinit
**Lane:** w136-appinit
**Branch:** (to be cut from develop before first edit; base SHA recorded below)
**Host runtime:** Docker 29.8.1 (rootful) on this coordinator host

## PLAN

- Fetch develop (07ae6c3e9), verify remote truth via ls-remote; claim ownership.
- Reproduce Ist-Repro auf eigenem Worktree: `target create --reference local` + `app init --quick` bricht mit ErrDeploymentOwnerMissing in der recordDeploymentBeforeMutation-Naht.
- Root-Cause: #1347 (42bfcb1c) machte VerifyDeploymentOwner in recordDeploymentBeforeMutation Pflicht; ein frischer --reference local Target hat vor dem ersten Core-bootstrap KEINE installation.json, also schlaegt die One-Installation-Owner-Pruefung zu. In v0.4.25 (bad37ce6) gab es diese Pruefung nicht, deshalb lief der native Acceptance-Pfad durch.
- Fix AM SEAM: fuer reference-local Targets ohne existierendes Core einen genuinen owner (Core installation.json) etablieren BEVOR die Pflichtpruefung laeuft — analog zum bestehenden runtime-up/app-up-Pfad, der Core via installCore bootstrap. KEIN revert/remove der owner-pruefung (#1347 bleibt fuer pfade die owner wirklich brauchen intakt).
- Regression: native bootstrap-pfad als CI-erfasster test in der validierungs-/native-gruppe anbinden (test->check->trigger benennen; routing-fehlt => own-block file:line, keine .github-Aenderung).
- PR gegen develop, drift-merge; runtime_destroy_all.go (#1453) NICHT anfassen; terminal + ls-remote + cleanliness.
- Beleg, dass native acceptanz-pfad (round-3 repro-kette) mit meinem head durchkommt (lokaler lauf als vorbote).

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`, PR #1453.
- Develop head (base for this lane): `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (`git ls-remote ... refs/heads/develop`).
- PR #1453 head: `7557a0b1d088ee8bcb0df2a82a230b5c17f51530`.
- v0.4.25 release head: `bad37ce6` (passes).
- #1347 commit: `42bfcb1c` (makes VerifyDeploymentOwner mandatory inside recordDeploymentBeforeMutation).
- Planning repo used: `/tmp/opencode/0427-136-seam-plan-wt` (origin = baseharbor-plan.git); baseharbor-plan under workers/ is bookkeeping, never committed to.
- Base SHA for this lane (ancestor of first commit): `<to-record before branch cut>`.

## Reproduction (Ist-Zustand, develop 07ae6c3e9)

Build + exact reproduce on own host with isolated state dir:

```
$ git clone https://github.com/mcpdev80/baseharbor.git /tmp/opencode/0427-136-seam-wt
$ cd /tmp/opencode/0427-136-seam-wt && git checkout origin/develop
$ go build -o /tmp/baha-136 ./cmd/baha
$ BASEHARBOR_STATE_DIR=/tmp/baha-136-repro/state BASEHARBOR_TARGET="" /tmp/baha-136 target create installation-retry-native --provider docker --access installation-retry-native --reference local --default
Target installation-retry-native created (runtime docker, access installation-retry-native via local)
$ printf 'version: 1\napp:\n  name: installation-retry\n  environment: dev\nservices:\n  sql: true\n  identity: true\n' > baseharbor.yaml
$ printf 'services:\n  web:\n    image: alpine:3.24\n' > compose.yaml
$ /tmp/baha-136 app init --quick --json
{"contract_version":"v1","error":{"code":"internal_error","message":"missing deployment state for installation-retry-native/installation-retry/dev [...]": "deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable"}}
```

Identical failure on the exact native-acceptance test (BASEHARBOR_INSTALLATION_DESTROY_ACCEPTANCE=1 BASEHARBOR_TEST_RUNTIME=docker):

```
=== RUN   TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry
    installation_destroy_native_test.go:43: missing deployment state for installation-retry-native/installation-retry/dev [759aedbd-...]: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable
--- FAIL: TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry (0.01s)
FAIL
```

## Root-cause (file:line)

- `VerifyDeploymentOwner` is the one-installation-owner seam (internal/deployment/deployment_store.go:93), enforced at `verifyDeploymentOwnerAtSeam` (deployment_store.go:33) and called on the write path from `cmd/baha/deployment_record.go:414` inside `recordDeploymentBeforeMutation` (the `app init` / `app apply` candidate choke point).
- #1347 (42bfcb1c) introduced that call. Before #1347 (v0.4.25) `recordDeploymentBeforeMutation` never verified the owner, so a fresh `--reference local` target with no Core passed.
- A `--reference local` target has NO Core installation (`targets/<target>/runtime/installation.json` absent) until `runtime up` / `app up` bootstrap it via `installCore` (cmd/baha/core_installation.go:41). The native-acceptance test and the plain `app init --quick` flow never run `runtime up` first, so the seam fails closed on a missing owner that simply does not exist yet.
- The loan seam (`TargetLoanVerifier` / `productionLoanAuthorityForTarget`, deployment_record.go:233) only grants for a Local target whose boot Target has a DIFFERENT genuine Core — not applicable to a single fresh local target with no boot Core. So the loan cannot rescue this path either.

## Repo-rule compliance

- Evidence + reproduction only. No product file, test, or workflow modified yet. No workflow edited or dispatched.
- No Markdown checkbox task lines in this file.

## Scope decision (pending Owner)

The fix must establish a genuine Core owner for a fresh `--reference local` target at the init/apply seam before the one-installation-owner check. This is consistent with #1347 (a genuine installation owns the deployment), not a weakening of it. Confirm this content-semantics choice, or redirect.

END_BLOCKED 0427-136: reproduction complete (develop 07ae6c3e9, fails identically at app init --quick seam and native-acceptance test:43 with ErrDeploymentOwnerMissing; v0.4.25 passes). Root cause file:line documented. Awaiting Owner scope decision on content-semantics of the seam fix (establish genuine Core owner for reference-local at init/apply seam, consistent with #1347).
