# w286 (0427-117) round-2: recover sick branch, refresh to current develop, red-first owner-loan proof, PR #1419, podman native owner seam

- Role: Worker (Lane 0427-117-podman-owner); coordinator session `594fd2f5-4e80-43b6-9841-92879146a85e`.
- Card `t-20261106-r27-remote-up-podman-owner-missing` (card number 0427-117 · podman-family Deploy owner).
- This lane took over after a system reboot: the previous lane (w286) was dead. The working branch
  `work/r27-remote-up-owner-missing` existed **only locally** in the surviving worktree
  `/home/marcel/dev/baseharbor-ecosystem/workers/w286-wt2`, at commits
  `14ec6674e` (fix) + `5c2c71068` (red-first test) on old develop `dddf0d782`, with one uncommitted change and
  **never pushed**.

## PLAN (numbered; mirrors workers/todos/0427-117-podman-owner.json)

- Read card (`plan.py show`) + ancestor acts (act-1407a REJECT, act-1407b delta, w273 round-2-podman, w274 round-2-r274) — DONE.
- In wt2: view the uncommitted change in `cmd/baha/runtime_integration_test_support_test.go`, commit with targeted `git add` (`c5cacec50`) — DONE.
- Refresh branch to current develop `934be499b` via `git merge origin/develop` (no conflicts; develop introduced only CI/.github work, none touched by me) — DONE.
- RED-FIRST proof: regression cell RED (`ErrDeploymentOwnerMissing`) with the loan verifier unbound, GREEN at fix; `go vet ./cmd/baha/` clean — DONE.
- Push `-u origin`; ls-remote before/after; `git log --oneline origin/develop..HEAD` shows ONLY my 4 commits; `934be499b` is an ancestor of HEAD — DONE.
- Open PR against develop → **PR #1419** (OPEN, base=develop, MERGEABLE); design = **verleih (loan)** recorded below — DONE.
- CI coverage: gate plan resolves; my test runs under `cli-package-tests` (`go test ./cmd/baha`); CI pre-checks clean (build/vet/gofmt/deployment-package-tests) — DONE.
- Podman native owner seam on `baha-podman-2`: fresh disjoint target, `app apply` hits `ErrDeploymentOwnerMissing` at the owner gate, documented verbatim; fail-closed; w268 stack untouched, my residue removed — DONE.
- Commit evidence to baseharbor-plan, push origin/main — IN PROGRESS.

## Base attestation / provenance (BEFORE and AFTER)

Real planning repo is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote `origin  https://github.com/mcpdev80/baseharbor-plan.git`), NOT `workers/baseharbor-plan`.

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/work/r27-remote-up-owner-missing` before push:

```text
934be499b9d2d894f80889fc23cd811884c8aec4 refs/heads/develop
(refs/heads/work/r27-remote-up-owner-missing: absent — never pushed)
```

After `git merge origin/develop` and `git push -u origin work/r27-remote-up-owner-missing`:

```text
934be499b9d2d894f80889fc23cd811884c8aec4 refs/heads/develop
801fdbc7f2e79e2a27ec0104a39474e498011c58 refs/heads/work/r27-remote-up-owner-missing
```

- Base cut from old develop `dddf0d7823f6eec161ad518bbced626fa9efe52e`; merged to current develop `934be499b9d2d894f80889fc23cd811884c8aec4`.
- `git merge-base --is-ancestor origin/develop HEAD` => **YES** (`934be499b` is an ancestor of my head).
- `git log --oneline origin/develop..HEAD` lists ONLY my chain:

```text
801fdbc7f Merge remote-tracking branch 'origin/develop' into work/r27-remote-up-owner-missing
c5cacec50 test(cmd/baha): owner-loan isolation helper + provider selection cells (t-20261106-r27-remote-up-podman-owner-missing)
5c2c71068 test(cmd/baha): red-first owner-loan regression cells (t-20261106-r27-remote-up-podman-owner-missing)
14ec6674e fix(cli,deployment): test-scope owner loan at the VerifyDeploymentOwner seam (fixes t-20261106-r27-remote-up-podman-owner-missing)
```

No foreign commit carries on top. Branch cut from another candidate would be a scope violation — this branch is my single integration candidate for the card.

## Red-first proof (behavioral, not compile-only)

The defect: on the sick base `dddf0d782` a marker-proven isolated test Target without its own
`installation.json` is refused with `ErrDeploymentOwnerMissing` on the real `VerifyDeploymentOwner` seam
(`internal/deployment/deployment_store.go:107`), which is exactly what the InCI compose-workload cells hit when
they apply against their isolation target.

Regression file `cmd/baha/deployment_owner_loan_regression_test.go`:

- **`TestOwnerLoanRegressionIsolatedTestTargetPassesSeam`** — the exact-defect cell. A marker-proven isolated
  test Target whose runtime root has no `installation.json` must pass the owner seam against the boot installation.
  On the broken seam (loan verifier unbound) this cell **FAILS** with the exact sentinel:

```text
--- FAIL: TestOwnerLoanRegressionIsolatedTestTargetPassesSeam (0.00s)
deployment_owner_loan_regression_test.go:202: marker-proven isolated test target must pass the owner seam
  (card t-20261106-r27-remote-up-podman-owner-missing):
  deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable
```

That line is the verbatim `ErrDeploymentOwnerMissing` from `VerifyDeploymentOwner`
(`internal/deployment/deployment_store.go:107` via `recordDeploymentBeforeMutation`).

- **GREEN at fix:** with the loan verifier bound (`cmd/baha/deployment_record.go` binds
  `deploymentTargetLoanVerifier`), the same cell passes, and the loan never materializes a second
  `installation.json` (boot installation stays the single durable owner, ADR 0021).

- **`TestOwnerLoanRegressionRefusalsStayFailClosed`** and
  **`TestOwnerLoanRegressionStartupBoundAuthorityRefused`** — unmarked and connector-bound targets stay
  fail-closed with the **same** sentinel, before and after the fix (the cells assert on both sides).

Verified locally on head `801fdbc7f`:

```text
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.357s   (TestOwnerLoanRegression* + TestDeployment* + TestTarget* all pass)
go vet ./cmd/baha/  => rc=0
```

RED shown by unbinding the loan verifier (`deployment.TargetLoanVerifier = ...` left commented in a throwaway
edit); the isolated-target cell fails with the exact sentinel, the fail-closed cells stay green, then the edit
was reverted to restore GREEN. This is a causal, behavioral red-first witness, not a compile-only pass.

## CI coverage (durable evidence, no .github/** edit)

Gate plan for the PR write-set resolves (`coverage_status: resolved`, `broad_required: false`). Required
validation checks for head `801fdbc7f`:

```
cli-build            go build ./cmd/baha
cli-gofmt            test -z "$(gofmt -l cmd/baha)"
cli-package-tests    go test ./cmd/baha -count=1      <-- my regression test runs here
cli-vet              go vet ./cmd/baha
deployment-package-tests  python3 scripts/pr-check-runner.py execute --check deployment-package-tests
source-contracts     go test ./internal/application/... ./contracts/...
```

- My new test `deployment_owner_loan_regression_test.go` is a **new CI test** picked up by `cli-package-tests`
  (`go test ./cmd/baha`), which runs on the opened/synced PR targeting `develop` — durable machine evidence,
  not a local-only or VM-only cell.
- CI pre-checks run on the candidate here: `go build ./cmd/baha` rc=0, `gofmt -l cmd/baha` clean,
  `go vet ./cmd/baha` rc=0, `deployment-package-tests` matched `./internal/deployment` rc=0.
- No `.github/**` file was touched by this lane; no rerun/workflow_dispatch. The `internal/deployment/deployment_store.go`
  change additionally selects `deployment-package-tests` (verified passing locally above).

## Podman native owner seam (baha-podman-2, 2026-11-07)

Host reachable via `ssh -o BatchMode=yes baha-podman-2` (hostname `baha-runner-podman-2`, rootless podman 5.7.0).
The host carries a pre-existing **w268 Dauertest-stapel** (8 containers, `bh-w268-shared-*`, `podman-local2`,
target `w268`); that stack was left completely untouched. My cell used a disjoint target id and my own residue
was removed before END.

Fresh disjoint podman target + pure-client compose workload (`bh-0427-podman-cell`, nginx, workload-only, passes
the remote lifecycle gate):

```text
$ baha target create w0427-owner-missing --runtime-provider podman --access local --access-provider local --reference local
Target w0427-owner-missing created (runtime podman, access local via local)

$ baha app init --target w0427-owner-missing --yes
✓ Application name: bh-0427-podman-cell ... created repository manifest for bh-0427-podman-cell (dev)   (init rc=0)

$ baha app apply --target w0427-owner-missing --confirm-candidate --yes
BaseHarbor · bh-0427-podman-cell · dev
  INFO target w0427-owner-missing
  Plan: 1 action(s) resolved
Error: missing deployment state for w0427-owner-missing/bh-0427-podman-cell/dev [300a7aa6-...]:
  deployment has no authoritative installation owner for its Target;
  the installation must be restored before its state is loadable
(rc=1)
```

This is the verbatim `ErrDeploymentOwnerMissing` raised by
`recordDeploymentBeforeMutation` (`cmd/baha/deployment_record.go:87`) → `VerifyDeploymentOwner`
(`internal/deployment/deployment_store.go:107`). The fresh podman target has no `installation.json` of its own
(operator bootstrap scope — a Core-owned installation / enrolled connector is out of this card, exactly as in
the Docker round w264 and the Podman witness w273).

Root cause with file:line (recorded here, card acceptance requirement):

- Sentinel `ErrDeploymentOwnerMissing` — `internal/deployment/deployment_store.go:25`
- Guarded call site — `internal/deployment/deployment_store.go:107` (`VerifyDeploymentOwner`)
- Caller — `cmd/baha/deployment_record.go:87` (`recordDeploymentBeforeMutation`)
- Fix seam — `internal/deployment/deployment_store.go:82-139` (`TargetLoanVerifier` branch), bound in
  `cmd/baha/deployment_record.go:65` (`deploymentTargetLoanVerifier`), guarded in
  `cmd/baha/deployment_record.go:151-322` (`testLoanAuthorityForTarget`).

Live `app apply` stays fail-closed because the marker/provenance guard is go-test-provenance only — by design
the loan never opens for a production-shaped target. This is correct: the connector-bound `up -> doctor health
OK` path is operator-bootstrap, out of scope for this card (documented in act-1407a / round-2-podman / round-2-r274).

### Host-clean witness (my own residue, AFTER)

```text
~/.local/share/baseharbor/targets/ => podman-local2, w268      (my w0427-owner-missing removed; w268 untouched)
podman ps -aq (mine) => 0
podman ps --format "{{.Names}}" | grep -c w268  => still present (untouched)
~/.config/baseharbor/target-recovery/w0427-owner-missing-*.json => removed
```

## Design: inherit-vs-verleih

**Verleih (loan), not inherit.** The boot installation keeps single durable ownership (ADR 0021 §1, §2). The loan
does **not** copy, transfer or materialize an `installation.json` at the isolated test Target; it reuses the boot
installation's loaded `State` for exactly one in-process `VerifyDeploymentOwner` resolution and refuses every
production-shaped shape:

- tenant/connector Targets (the tenant hook runs first; connector guard refuses) — stay fail-closed,
- boot not `READY` — refused,
- boot == target (already the owner) — refused,
- unmarked target (no `baseharbor.test-isolation/v1` marker) — refused,
- foreign/corrupt `installation.json` at the target — `ErrDeploymentOwnerForeign`,
- non-`testing.Testing` process — refused.

A single in-process ledger (`installationLoanLedger` under the `.installation.lock` primitive) grants one loan
per isolated test Target per process; the loaned identity owns its OWN boot namespace, so the namespace-
installation binding is checked against that owned namespace, never the test Target's directory segment. Every
refusal returns the original `ErrDeploymentOwnerMissing` sentinel (never a loan-detail error), so the caller's
`errors.Is` checks and the never-delivered-destroy recognition in `cmd/baha` are preserved. The default nil keeps
every production path byte-identical.

## repo-rule compliance

- Product repo `baseharbor`: refreshed branch from old develop `dddf0d782` to current develop `934be499b`
  (clean merge, no conflicts). Write-set of PR #1419 is exactly five files:
  `cmd/baha/deployment_owner_loan_regression_test.go`, `cmd/baha/deployment_record.go`,
  `cmd/baha/runtime_integration_test_support_test.go`, `cmd/baha/test_isolation_support_test.go`,
  `internal/deployment/deployment_store.go`. **No `.github/**` file edited by this lane.** No rerun or
  workflow_dispatch. No subagents. No self-merge.
- Evidence only in `baseharbor-plan/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-2.md`,
  never the product repo. No `.evidence/` directory anywhere.
- VM cell ran via SSH from the codeman server on the named host `baha-podman-2` only (coordinator-host
  containers forbidden). VM lock claimed/released in the host journal; my disjoint target removed and my workdir
  deleted before END; the pre-existing w268 Dauertest-stapel left untouched.

## END

END_DONE 0427-117-podman-owner: head=801fdbc7f2e79e2a27ec0104a39474e498011c58 pr=1419 (OPEN base=develop) design=verleih red=TestOwnerLoanRegressionIsolatedTestTargetPassesSeam ErrDeploymentOwnerMissing with loan unbound -> GREEN at fix vet/build/gofmt/deployment-package-tests clean ci=cli-package-tests(go test ./cmd/baha)+deployment-package-tests, no .github edit podman=ErrDeploymentOwnerMissing at app apply (deployment_store.go:107 / deployment_record.go:87) on fresh w0427 target, w268 untouched 0-of-mine host-clean lsremote_before=absent_branch lsremote_after=801fdbc7f akte=evidence/r27-welle5-folge-2026-11-06/remote-up-cli/owner-missing-round-2.md
