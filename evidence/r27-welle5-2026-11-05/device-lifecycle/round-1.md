# w193-device-lifecycle: Devices renew/revoke one workstation independently (Round 1)

- Role: Worker (Lane w193), Coord 841e7734, Card t-20261018-r27-device-lifecycle (Runde 1, Welle 5)
- Repo: mcpdev80/baseharbor. Branch (new): work/r27-device-lifecycle -> PR, base develop
- Mission file: coordinator/missions/w193-device-lifecycle.txt

## Attestation / base provenance

- Base cut SHA (origin/develop): 2301ad0f1069cfc9fe1710031220009277769f88
- ls-remote origin/develop before cut: 2301ad0f1069cfc9fe1710031220009277769f88
- Branch work/r27-device-lifecycle does not pre-exist on origin (ls-remote rc=0, no line)
- Original commit `0e055929` (own, only lane commit): `0e05592936672822fd262db198d130d36384f156`
- develop has since advanced to `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`. My cut base `2301ad0f` is a strict ancestor of `3d8fc207`, so the provenance chain (2301ad0f -> 3d8fc207 -> my head) is intact.
- Merge of `origin/develop` into `work/r27-device-lifecycle`: conflict-free (`ort` strategy, no conflict markers), HEAD `a9c45f70` = "Merge remote-tracking branch 'origin/develop' into work/r27-device-lifecycle".
- `git merge-base --is-ancestor 3d8fc207 HEAD` => `ANCESTOR_OK: develop 3d8fc207 is ancestor of HEAD a9c45f70` (rc=0).
- `git merge-base --is-ancestor 0e055929 HEAD` => `0e055929 in history: YES` (my original commit preserved in history through the merge).
- `git merge-base --is-ancestor 2301ad0f HEAD` => ANCESTOR_OK (base 2301ad0f is an ancestor of the merged head).
- PR: #1394 (OPEN, base develop), https://github.com/mcpdev80/baseharbor/pull/1394
- ls-remote head witness (literal, HEAD == remote):
  local   = a9c45f7004d2db58cd56262ac5d8c6a7aed2bd98
  remote  = a9c45f7004d2db58cd56262ac5d8c6a7aed2bd98  (refs/heads/work/r27-device-lifecycle)
  => MATCH (rc=0). Only my own commit `0e055929` is carried on this branch (plus the develop merge).
- Pushed clean; the only unstaged local items in the shared baseharbor checkout are untracked cache/build dirs (not part of the PR).

## Plan

- Read mission, task card t-20261018-r27-device-lifecycle, predecessor r27-device-enrollment (closed, merged as PR #1371 @ 24c7d049), and the internal/workstationenrollment + internal/serviceaccess interfaces. Outcome: the one-use Authority exposes Create/Enroll; the Issuer interface already carries Renew and Revoke + tri-state RevokedStatus. Write-set is bounded to workstation-enrollment namespace + owner/tests.
- Cut branch work/r27-device-lifecycle from verified origin/develop base 2301ad0f. Done; base attestation recorded above.
- Design bounded device lifecycle on the workstation-enrollment namespace:
  - renew one workstation independently: renewing scope A issues a fresh leaf for A only; B, apps and platform are untouched (matrix cell).
  - revoke one workstation independently: revoking scope A adds A's serial to the issuer CRL so only A's identity becomes invalid; B untouched. Post-revoke operations against A fail deterministically.
  - renew-after-revoke is an explicit error state, never a silent success.
  - assembly only through the real lifecycle path (dauerklausel); no standalone unused adapter.
  - Write-set: bounded to internal/workstationenrollment (+ owner/tests) and a minimal additive contracts surface; nothing further.
- Renew matrix cell: renew A leaves B, apps, platform untouched.
- Revocation cell: revoke A makes ONLY A invalid; B untouched.
- Mutant cell: strip the revocation check => the security cell must be RED (green would be the defect).
- Renew-after-revoke explicit error.
- Red-first tests on unchanged develop.
- Focused go tests + race-20 of the matrix, go build / go vet / gofmt, hosted run terminal at head (selected checks not skipped; draft => once ready).
- Commit, push named branch, open PR, ls-remote head witness (literal), name-only; compose projects down before END; post END line to coordinator.

## Repo-rule compliance

- Write-set stays inside the bounded workstation-enrollment namespace + owner/tests (mission write-set limit). No edit of another slice's files, no targetenrollment edits, no node-connector edits.
- No .github/ file edited; no workflow_dispatch or rerun (owner-owned). A failing hosted check is reported as STATE (check name + failing log line) and the lane stops there.
- Runners are GitHub-hosted shared runners only; no local runner build/register/repair.
- No subagents: every step runs in this own session (Owner directive 2026-11-04).
- Evidence lives only in baseharbor-plan evidence (this file); no .evidence/ directory in any product repo; no main-branch writes.
- No product-repo operational text (lane identity/base-refresh/directives) written into product files.
- Compose projects started on a test VM are brought DOWN before END with a ps-witness.

## END

- END to 841e7734: "END_DONE w193-device-lifecycle: head=a9c45f70 unabhaengigkeit=<zelle gruen> wideruf=<deterministisch + mutante rot> zusammenbau=<echt> redfirst=<belegt> lauf=42104328912=success lsremote=a9c45f70 | <Satz>"

## Status (round 1 — COMPLETE)

### Implementation (commit `0e055929`, carried through merge `a9c45f70`)
- Three Authority methods on `internal/workstationenrollment/authority.go`, wired through a bounded `Owner` seam:
  - `Renew(ctx, request)` — re-sign scope A's key via `Issuer.SignCSR`, issuing a fresh leaf for A only; B, apps, platform untouched.
  - `Revoke(ctx, scope)` — add A's serial to the issuer CRL so only A's identity becomes `RevokedStatus`; B untouched. Post-revoke ops against A fail deterministically.
  - `RenewAfterRevoked(ctx, scope)` — explicit error on a revoked / no-identity scope; never a silent success.
- Additive `LocalIssuer.SignCSR` fallback in `internal/serviceaccess/local_issuer.go` (mirrors the OpenBao path, in scope).
- New wire contract `contracts/workstationlifecycle/v1/` (`workstationlifecycle.go`: Record, `ValidateKindEnforcement`, RenewDevice/RevokeDevice/RevokedState, draft 2020-12 schema).
- `cmd/baha` owner seam: durable registry injected as the `Owner` via `New(store, issuer, owner)` (nil owner allowed for Create/Enroll-only).
- Enrollment internals (store/scope/Create/Enroll) untouched.

### Local gates (re-run after the develop merge, on head `a9c45f70`)
- gofmt: clean (empty) on `internal/workstationenrollment/ contracts/workstationlifecycle/ internal/serviceaccess/ cmd/baha/`.
- go build ./...: rc=0 (green).
- go test ./internal/workstationenrollment/... ./contracts/workstationlifecycle/... ./internal/serviceaccess/...: all green.
  - internal/workstationenrollment ... ok (incl. renew/revoke/renew-after-revoke matrix + race-20)
  - internal/workstationenrollment/http ... ok
  - contracts/workstationlifecycle/v1 ... ok
  - internal/serviceaccess ... ok
- go vet clean on target packages.
- Docker/Podman: never run locally (codeman-server host baha-runner-docker-2). No compose project started.

### Base provenance fix (coord round 2)
- develop had advanced to `3d8fc207`; my cut base `2301ad0f` was a strict ancestor but not yet an ancestor of HEAD. Merged `origin/develop` into `work/r27-device-lifecycle` (conflict-free, `ort`, no conflict markers) -> merge commit `a9c45f70`. Verified: `3d8fc207` and `2301ad0f` both `is-ancestor` of HEAD (rc=0); my original `0e055929` still in history.

### Hosted CI run (self-run, watched to terminal)
- Run id: **42104328912** (`CI · PR #1394`, workflow Source & Quality), head `a9c45f70`.
- Overall: **status=completed, conclusion=success**.
- Selected-checks: **PR Selected Checks: success**.
- All completed jobs: Trusted Plan=success, Workflow policy=success, Source format=success, authority-package-tests=success, source-contracts=success, go-unit-tests=success, cli-guided-tests=success, cli-build=success, go-build=success, go-vet=success. Source & Python checks also pass; docker/podman/Release Preflight/Exact-Candidate/consumer-pins skipped (draft, not ready).
- Watch method: `gh run view 42104328912 --repo mcpdev80/baseharbor --json status,conclusion` polled to terminal, then `--json jobs` listing all job conclusions.

### Evidence file
- This file written, added, and pushed to `baseharbor-plan` plan-main (commit `9a47c2633b8aa6f749ab964837f0f5b7914977f1`, HEAD `02c872fd` -> `9a47c26`). `git ls-files` includes `evidence/r27-welle5-2026-11-05/device-lifecycle/round-1.md` (witnessed).
