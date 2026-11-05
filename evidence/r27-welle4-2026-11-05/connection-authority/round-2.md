# WORKER EVIDENCE — w172-boundary-r2 (r27 connection-authority, ROUND 2)

## Task / mission

Worker lane `w172-boundary-r2` (Coord f49a3303), card `t-20261105-r27-connection-authority-boundary` (Runde 2).
Branch/PR (THE candidate): `work/r27-connection-authority` — PR #1386.
AKTE: `baseharbor-plan/evidence/r27-welle4-2026-11-05/connection-authority/review-1386a.md`.

Round-1 (Round 1) PR #1386 was REJECTED by CODEX-REVIEW: the resolver in `internal/coreinstallation/authority.go`
called `serviceaccess.EnsureLocalIssuer` at line 352, which generates and persists a new base CA when
`service-access/issuer/issuer.pem` is absent. That is **authority creation during resolution**, despite the
resolver's read-only/derive-only contract. A missing or incomplete authority therefore did NOT fail closed —
selection could silently fabricate a new trust root.

Resolution recipe (strictly READ-ONLY): observe the existing issuer via `CheckLocalIssuer`; missing or
incomplete issuer state returns a named fail-closed error and must NOT create the directory or CA. Keep
explicit issuer materialization in its authorized lifecycle phase. Only the two card-reserved files may touch.

## ##PLAN (Worker steps — all done)

- Step 1: Read mission + AKTE; confirm `work/r27-connection-authority` (PR #1386, head b730243cbe1) is THE candidate; attest develop SHA is ancestor of candidate HEAD. DONE
- Step 2: Create worktree under /tmp/opencode/w172-boundary-r2-wt; verify develop is ancestor before cutting branch. DONE
- Step 3: Commit — make authority.go resolver read-only: replace EnsureLocalIssuer with observeLocalIssuer (CheckLocalIssuer observe-only + LocalIssuer on demand). DONE
- Step 4: Commit — extend w168_boundary_probe_test.go: absent-directory + empty-issuer-file probes assert error and no issuer.pem; keep existing unverified/foreign/valid checks. DONE
- Step 5: Local checks: go build ./...; go test ./internal/coreinstallation ./cmd/baha (targeted); go vet; gofmt -l. DONE
- Step 6: Push branch; ls-remote==head verbatim; commit log = ONLY my commit on top of candidate. DONE
- Step 7: PR ready (not draft) + watch PR Selected Checks terminal — all SUCCESS. DONE
- Step 8: Evidence round-2.md + ##PLAN ticked + END line; post END_DONE to f49a3303. DONE

## Base / branch attestation (BEFORE branch cut)

- develop (base ref): `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7`
- candidate HEAD (before my commit): `b730243cbe100387db5ce89611028a3487a89894`
- `git merge-base --is-ancestor 24c7d0492f... HEAD` => YES (develop is ancestor of candidate HEAD and of my commit)
- `git merge-base --is-ancestor b730243c... HEAD` => YES (candidate HEAD is ancestor of my commit)
- Provenance: my commit `aa62518c` sits directly on `b730243c` sits on `24c7d0492f`. No foreign candidate carried.
- ls-remote (verbatim): `aa62518c6a65c207db5a0b49e37d03ca470c7b26  refs/heads/work/r27-connection-authority`
- name-only diff vs candidate head `b730243c`: `internal/coreinstallation/authority.go` + `internal/coreinstallation/w168_boundary_probe_test.go` (exactly the two card-reserved files).

## Worktree

- Location: `/tmp/opencode/w172-boundary-r2-wt/repo` (outside the ecosystem root, per fixed workspace layout). NOTE: an earlier `/tmp` hygiene sweep removed the first worktree after my first commit; the worktree was recreated fresh from the same candidate head `b730243c` and the change re-applied and re-committed (`aa62518c`), so no work was lost and no foreign content was introduced.

## The fix (read-only, fail-closed)

`internal/coreinstallation/authority.go` — `ResolverForTargetSelection` previously called
`serviceaccess.EnsureLocalIssuer(issuerDir)`, which fabricates+persists a new base CA when `issuer.pem` is
absent. Replaced with a new package helper `observeLocalIssuer`:

- validates the existing issuer with the read-only `serviceaccess.CheckLocalIssuer(dir)` preflight;
- returns a `&serviceaccess.LocalIssuer{Dir: dir}` whose `load()` is deferred to the caller's demand (mirrors
  the accepted production path in `cmd/baha/application_service_issuer.go` `resolveApplicationServiceIssuer`);
- any missing dir, absent `issuer.pem`, partial/unprotected or incomplete issuer state surfaces as an error
  that the caller maps to the named fail-closed `ErrUnverifiableInstallation` BEFORE any issuer material is
  produced — the resolver never creates the directory, `issuer.pem`, or a new CA, and never opens a second
  trust source.

No `.github/**` touched. Explicit issuer materialization stays in its authorized lifecycle phase.

## Tests (w168_boundary_probe_test.go)

- Existing checks retained: unverified-installation, foreign-target, unreadable-root, valid-target. The valid-target
  tests now materialize a genuine base CA on the authorized lifecycle path (`EnsureLocalIssuer`) so the observe-only
  resolver reads back an existing issuer and the test also asserts the resolver did not rewrite the existing issuer dir.
- New absent-directory probe `TestResolverFailsClosedOnAbsentIssuerDir`: no issuer dir => `ErrUnverifiableInstallation`,
  and no dir created by the observe-only resolver.
- New empty-issuer-file probe `TestResolverFailsClosedOnEmptyIssuerFile`: dir present but no `issuer.pem` =>
  `ErrUnverifiableInstallation`, and no `issuer.pem` fabricated.

Local results: `go build ./...` rc=0; `go test ./internal/coreinstallation/` ok; `go test ./cmd/baha/`
(targeted) rc=0; `go vet ./internal/coreinstallation/` rc=0; `gofmt -l` clean.

Full `cmd/baha` suite: one failure in `TestW138DestroyWithoutYesPreservesNeverDeliveredProof` with
`getwd: no such file or directory`. This is a PRE-EXISTING ENVIRONMENTAL FLAKE, NOT caused by this change:
- the test file `cmd/baha/w138_destroy_never_delivered_test.go` is NOT in my diff;
- it passes in isolation (`-run TestW138DestroyWithoutYesPreservesNeverDeliveredProof`, rc=0) on this branch;
- it passes on the pristine candidate base `b730243c` (rc=0).
The `getwd` error is the known race where Go's parallel test runner reaps a test's `t.TempDir()` while a later
`os.Getwd()` call resolves against the now-deleted directory. The hosted `PR · Validation · cli-guided-tests`
gate (which runs the same suite on a stable shared runner) passed SUCCESS — authoritative.

## Hosted CI — PR Selected Checks (terminal, documented)

PR #1386 state: OPEN, ready (not draft), base `develop`, head `aa62518c6a65c207db5a0b49e37d03ca470c7b26`.
No rerun / workflow_dispatch issued (Owner: .github is Owner-owned). CI triggered by my push.

```
Workflow policy                              COMPLETED  SUCCESS
Release Source Preflight                     COMPLETED  SKIPPED
Targeted HA · docker                         COMPLETED  SKIPPED
Targeted HA · podman                         COMPLETED  SKIPPED
validate                                     COMPLETED  SKIPPED
PR · Source format                           COMPLETED  SUCCESS
PR · Trusted Plan                            COMPLETED  SUCCESS
PR · Runner Interface                        COMPLETED  SKIPPED
PR · Consumer Pins                           COMPLETED  SKIPPED
PR · Demo Pen                                COMPLETED  SKIPPED
PR · Exact Candidate                         COMPLETED  SKIPPED
PR · Focused Python                          COMPLETED  SUCCESS
PR · Validation · authority-package-tests    COMPLETED  SUCCESS
PR · Validation · cli-build                  COMPLETED  SUCCESS
PR · Validation · cli-guided-tests           COMPLETED  SUCCESS
PR · Validation · cli-vet                    COMPLETED  SUCCESS
PR · Validation · source-contracts           COMPLETED  SUCCESS
PR · Public Contracts                        COMPLETED  SKIPPED
PR · Selected Runtime                        COMPLETED  SKIPPED
PR Selected Checks                           COMPLETED  SUCCESS
```

`PR Selected Checks` = SUCCESS. All focused validation gates for the authority-package fix pass; docker/podman/
Release Preflight correctly SKIPPED (non-blocking, not run as shared-runners-only gates that do not apply here).

## GOAL ACHIEVED

Round-2 rejection resolved: the resolver is now strictly read-only. A missing or incomplete management-connection
authority (absent issuer dir, absent `issuer.pem`, partial/unprotected/incomplete issuer) fails closed with the
named `ErrUnverifiableInstallation` and fabricates NO new trust root during selection. The red line holds:
selection DERIVES the existing verified-authority identity, it never DECIDES or creates it.

## END

END_DONE w172-boundary-r2: head=aa62518c6a65c207db5a0b49e37d03ca470c7b26 lesend=<kein EnsureLocalIssuer, observeLocalIssuer via CheckLocalIssuer, 4 green probes> fehlgeburt_mutante=<kein generiertes Material bei fehlender/fremder Autoritaet> lauf=41988118382 PR Selected Checks=SUCCESS | Round-1 REJECT resolved: resolver now strictly read-only, fail-closed on missing/incomplete issuer, no CA fabrication.
