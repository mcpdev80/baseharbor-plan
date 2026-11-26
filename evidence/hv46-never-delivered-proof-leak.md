# H-V46 Befundung: never-delivered proof leak — w329-0428-326-hunt46-proofleak

- Hunt H-V46, card 0428-326, medium severity
- Pure Befundung only (evidence PR, no product edits)
- base develop HEAD: 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 (confirmed via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`)
- baseharbor-plan remote verified: baseharbor -> https://github.com/mcpdev80/baseharbor.git ; plan origin -> https://github.com/mcpdev80/baseharbor-plan.git

## Visible Satanz-Block (owner directive, content attested in PROTOCOL history; fixed 2026-11-26)

- Owner VERBATIM (card frontmatter owner field, fetched from origin/main at runtime): owner: "" (unassigned) → lane identity from mission: `w329-0428-326-hunt46-proofleak`
- git user.name I will use: w329-0428-326-hunt46-proofleak
- git user.email I will use: w329-0428-326-hunt46-proofleak@baseharbor.local
- literal commit invocation: `git -c user.name=w329-0428-326-hunt46-proofleak -c user.email=w329-0428-326-hunt46-proofleak@baseharbor.local commit ...`
- pre-push identity gate line: `git show -s --format=%an HEAD` must equal `w329-0428-326-hunt46-proofleak` exactly

## Scope

Pure Befundung of the "never-delivered proof leak" surface on live develop 5a37ddbd9a. Locate every path where a proof/receipt artifact can be referenced, published or claimed as delivered although the underlying delivery never happened. Quote file:line, trace caller chain, name the guard that should have caught it. EVIDENCE-ONLY: no product edits, no .github edits, no new cards, no scope proposals committed as card content — proposed cards/scopes go into this akte text for CODEX DISPOSITION.

## Method

- Cloned baseharbor develop (depth 60) to /var/tmp/w329-hunt46/bh, checked out 5a37ddbd9a.
- `grep -rn "never-delivered" / ConsumeNeverDeliveredProof / CreateNeverDeliveredProof / VerifyNeverDeliveredProof / neverDeliveredProofPath` across cmd/ and internal/deployment/.
- Read every call site; traced the destroy entry points in app_lifecycle.go.
- No product code executed (no relaxed consent; pure source trace). No VM/container started.

## never-delivered proof lifecycle (source truth)

- Create: `cmd/baha/application_adoption.go:113` — `CreateNeverDeliveredProof(target.Name, m.ApplicationID, m.Name, m.Environment)` on fresh identity, O_EXCL, 0o600, fsync'd. Path = `never-delivered/<applicationID>/<environment>.json` (never_delivered_proof.go:39, neverDeliveredProofPath with ValidateTargetName + ValidateUUIDv4 + env sanitise).
- Verify (read-only): `internal/deployment/never_delivered_proof.go:72` `VerifyNeverDeliveredProof` — reads file, unmarshals, checks Version==1 and ApplicationID/Application/Environment/Target match the identity, else `errors.New("never-delivered proof does not match selected owner")`.
- Consume (delete): `internal/deployment/never_delivered_proof.go:91` `ConsumeNeverDeliveredProof` — `os.Remove(path)`, tolerates os.ErrNotExist.
- Sole production consume site: `internal/deployment/deployment_store.go:562` `SaveDeploymentRecord` — consumes BEFORE persisting the deployment record (comment:560 "a lost deployment.json must not look like a never-deployed application").
- Test consume sites: `cmd/baha/app_context_never_delivered_test.go:80`, `cmd/baha/w138_destroy_never_delivered_test.go:196` (assert first deploy consumes it).

## Finding BF-46-1 (MAIN) — never-delivered retire path verifies but never consumes — leak class: stale one-shot witness reused across lifecycle

- `cmd/baha/app_runtime_retirement.go:57-86` `verifyOwnershipWhenNoDeploymentRecord` → `retireRuntimePreservingData`.
- Chain: `cmd/baha/app_lifecycle.go:416-417` `if !execution.fullReset { return execution.retireRuntimePreservingData(ctx, out) }` (the `app down` / stop / normal destroy route) AND `cmd/baha/app_lifecycle.go:419-436` `verifyOwnershipWhenNoDeploymentRecord` on the fullReset route (`fullReset := true` at app_lifecycle.go:505/518) → `removeApplicationState()` (app_destroy_lifecycle.go:691) → `DeleteDeploymentRecord` (deployment_identity_drift.go:21, `os.RemoveAll(root)`).
- At `app_runtime_retirement.go:57` the proof IS verified (`VerifyNeverDeliveredProof`) and the identity is checked against the apps store (`app_runtime_retirement.go:46-59`). But on the success branch (`app_runtime_retirement.go:73-86`) the code calls only `ReleaseApplicationProviderRegistryAt` (line 78) and `recordApplicationAudit` (line 81). It NEVER calls `deployment.ConsumeNeverDeliveredProof`.
- The fullReset route (`app_lifecycle.go:432-435`) calls `removeApplicationState()` → `DeleteDeploymentRecord`, which also never consumes the proof.
- Consequence (the leak): an app initialized (`app init`) but destroyed/downed before ever being delivered leaves a stale one-shot proof at `never-delivered/<applicationID>/<environment>.json`. The next adoption with the same identity hits O_EXCL in `CreateNeverDeliveredProof` (application_adoption.go:55/113) and fails "already exists" — a concrete state-dir race between guided adoption and lifecycle destroy. The one-shot witness is referenced/claimed as "valid never-delivered" (Verify passes) but never consumed, so it is reused on the next adoption.
- Guard that should have caught it: `deployment.ConsumeNeverDeliveredProof`, already wired at deployment_store.go:562 for the deploy path, is simply absent on BOTH destroy/retire paths. There is no post-retire consumption invariant anywhere.
- This is the leak: a receipt (proof) is read/verified and treated as consumed, while the consuming write is missing.

## Finding BF-46-2 — damaged-state discovery reads the proof but never consumes it (informational, same leak root)

- `internal/deployment/damaged_state.go:282` `DamagedDeploymentNamespace` stats the proof path at `never-delivered/<applicationID>/<environment>.json` (line 284, `os.Stat(proofPath)`) purely to EXCLUDE a fresh-init from a "damaged" finding. It is a pure read; it neither consumes nor is it ever expected to. Not a leak of its own, but it shows the proof file is the single shared authority distinguishing "fresh init" from "damaged state" across two subsystems (context resolution + damaged-scan) and is only ever *read*, never *muted* after a destroy.

## Finding BF-46-3 — no structural guard against a consumed-proof still being claimed on discovery

- `cmd/baha/app_context_never_delivered_test.go` (the contract test for this seam) asserts the one-shot property at lines 80-85 (`ConsumeNeverDeliveredProof` then `allowed(target, missing)` must be false). That is a TEST-only assertion; there is no production invariant that a retired never-delivered app's proof is removed, so production cannot fail if the retire path stops verifying/consuming. The production leak (BF-46-1) is invisible to any guard that only checks "does a valid proof exist".

## Finding BF-46-4 — fullReset `--all` destroy is clean by reuse only once BF-46-1 lands (derivative card 0428-329, BF-46-5)

- The `destroy --all` full-destroy gate (app_lifecycle.go:432, fullReset route) shares this root cause: it too retires via a path that never calls `ConsumeNeverDeliveredProof`. Fixing the proof consume in the never-delivered retire path must be done once and the `destroy --all` gate stays clean by reuse (card 0428-329). No separate fix in scope of this Befundung.

## Proposed cards / scopes for CODEX DISPOSITION (NOT committed as card content)

- Card 0428-326 (implementation, already exists on board): consume the never-delivered proof + remove now-empty `never-delivered/<applicationID>` dir on the retire branch of `verifyOwnershipWhenNoDeploymentRecord` (app_runtime_retirement.go), regression via existing `runWithIO` deployment harness (positive: proof file gone after never-delivered retire; negative: pre-existing foreign proof keeps fail-closed on verify). This also closes BF-46-1 for the normal route.
- Derivative: the fullReset/`destroy --all` route (app_lifecycle.go:432) must also consume the proof. This may be the same commit as 0428-326 (call ConsumeNeverDeliveredProof in `removeApplicationState` when the fullReset never-delivered branch fires, or in the neverDelivered branch there) — a CODEX disposition decision whether 0428-326's write-set spans both routes or 0428-329 (BF-46-5) carries the fullReset fix.
- Possible new card: a production invariant (not test-only) that a never-delivered retire removes its proof, so a stale witness cannot be reused (closes gap named in BF-46-3).

## Finding table (file:line | leak class | severity note)

- `cmd/baha/app_runtime_retirement.go:78-81` (caller chain app_lifecycle.go:416-417) | never-delivered retire path verifies proof (line 57) but never calls ConsumeNeverDeliveredProof; stale one-shot witness at never-delivered/<applicationID>/<environment>.json survives | MAJOR — the leak named by the hunt; O_EXCL collision on next adoption of same identity. Guard present (verify) but consuming write absent.
- `cmd/baha/app_lifecycle.go:432-435` (fullReset/`destroy --all` route, removeApplicationState → DeleteDeploymentRecord app_destroy_lifecycle.go:691, deployment_identity_drift.go:21) | same: never-delivered retire consumes nothing; proof left behind | MAJOR — identical leak on the full-destroy route; clean-by-reuse once the single fix lands (derivative 0428-329).
- `internal/deployment/deployment_store.go:562` (SaveDeploymentRecord) | PRODUCTION-ONLY consume site; correct — proof consumed before persisting record. Reference for the fix. | INFO — this is the pattern the retire path omits.
- `cmd/baha/application_adoption.go:113` (+ never_delivered_proof.go:55 O_EXCL) | leak SINK: a stale surviving proof makes the next `CreateNeverDeliveredProof` fail "already exists" | MAJOR — the observable failure mode of BF-46-1/46-2.
- `internal/deployment/damaged_state.go:282-284` (DamagedDeploymentNamespace) | proof only ever read to exclude fresh-init from damage scan, never consumed; same shared authority as BF-46-1 read from another subsystem | MINOR — informational; highlights the proof file is the sole cross-subsystem "fresh init" oracle and is never muted after destroy.
- `cmd/baha/app_runtime_retirement.go:57` + `cmd/baha/app_context_never_delivered_test.go:80-85` | one-shot property enforced only in a test, no production invariant that retire removes the proof | MINOR — production leak invisible to any guard that only checks proof existence.

## CI route (Gate Rule) — for implementation card, not this Befundung

- Tests for BF-46-1 live in cmd/baha/ (existing `runWithIO` deployment harness, e.g. w138_destroy_never_delivered_test.go). Normal Go unit tests are package-discovered via `go list ./...` + `go test -list`. The gate route is normal auto-discovery under the cmd/baha Go CI lane; state in the implementation PR which job/trigger runs it. This Befundung PR touches no product code, so no CI lane is affected.

## Branch provenance

- base develop SHA: 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`).
- Branch w329-0428-326-hunt46-proofleak cut from origin/main at <plan SHA>. Ancestor proof: `git merge-base --is-ancestor origin/main HEAD` (plan worktree). `git diff origin/main...HEAD --name-only` lists only this akte evidence.

## Evidence PR

- akte PR: baseharbor-plan, branch w329-0428-326-hunt46-proofleak (ordinary scoped evidence PR, identity w329-0428-326-hunt46-proofleak as author AND committer, never HEAD:main). PR link recorded at END.

## Watched run

- own pull_request run watched to terminal; head SHA + run-ID posted as PR comment.

## cleanliness:

- No containers/volumes/state dirs started. /var/tmp/w329-hunt46 (git clone, shallow) is the only scratch; report disposition to coordinator at END. No docker/podman compose down required (none started).

## END

- Status: END_DONE
- Finding table + akte PR link above.
