# act-1588-review-r1.md — PR #1588 CODEX-REVIEW (frost, no merge)

ROLE: CODEX-REVIEW (no merge). Shift r28-welle1, 2026-11-15. Card 0427-186 (Target policy presets).

## PLAN

1. Fix PR #1588 head via `git ls-remote` (base develop 0e9ccb582), confirm run 43735861483 success (NOT the run-43707049604 era head).
2. Card 0427-186 acceptance points: presets CLI/wizard consistent; verified source provenance at Core ingress (forged refuse); operator edit existing policy without auth-bypass.
3. Evaluate the deferred point: does #1588 carry the operator-edit operation, or is it a REJECT+recipe?
4. Draft-PR frost check: if open (non-draft) record draft-set as protocol detail, not a substantive reject.
5. Write APPROVE/REJECT, validate, publish evidence on origin/main, verify remote, post END.

## Candidate and provenance

PR #1588 OPEN/DRAFT (frost), branch `lane/0427-186-target-policy-presets`, base develop `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, exact head `9534edd49c205adabe858516e1400640ad6ec2cb`. Product `git ls-remote`:

```text
9534edd49c205adabe858516e1400640ad6ec2cb	refs/pull/1588/head
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
```

Base `0e9ccb582` is an ancestor of the reviewed head (`git merge-base --is-ancestor` succeeded). Base-to-head log contains only the candidate's own commit.

## Card 0427-186 acceptance (4 points)

1. Presets editable in wizard and CLI with consistent persisted Target rules — **present**: `--deployment-preset development|test|staging|production|custom|none` + CLI resolution (`cmd/baha/target_deployment_policy_edit.go`) and wizard editing.
2. Core evaluates verified source identity/branch/dirty provenance at ingress, refuses forged evidence — **present**: `internal/deployment/immutable_provenance.go` (`ImmutableProvenance`, `FromVerifiedCandidate`, `toAdmissionEvidence`) + tests `TestFromVerifiedCandidateRejectsUnverifiedAndUnbound`, `TestAdmissionEvidenceForRemoteApplyFailsClosedWithoutRecord`. Core-owned, never from client metadata; nil/partial → fail closed.
3. Operator can edit an existing Target policy without bypassing authorization — **deferred future-scope** (see below).
4. Exact-head targeted CI, security negatives, e2e acceptance documented — **present** (CI below; target-policy-edit_b_test.go).

## The deferred point (card says so; coordinator OPTION-1 note)

Card integration-status 2026-11-09 and owner-closure 2026-11-13 explicitly state:
- "Core-authoritative provenance verification and remote editing of existing policies remain **future scope**; they are explicitly **not** claimed as implemented."
- "unverified Core provenance and remote target policy editing must not be claimed complete until 0.4.28 acceptance."

Point 3 is therefore the deferred item, NOT an unmet acceptance that triggers REJECT. #1588 carries point 2 (immutable provenance) as the 0.4.28 slice; point 3 (remote operator edit) stays out of this diff.

## Point 3 status in #1588 — operator edit still refused at remote

Confirmed: the remote operator-edit operation is **not** implemented in #1588.
- `cmd/baha/target_deployment_policy_edit.go`: remote Target edit returns `ErrorUnsupported` (`access.Provider != "local"`) — "Editing a remote Target policy requires the owning Core operator mutation endpoint."
- #1588 adds **zero** files implementing a remote existing-target policy-mutation endpoint, and no new machine-contract registry entry (diff is 7 files, all listed below).
- The diff documents the deferral: `cmd/baha/machine_coverage.go` and `docs/reference/cli-machine-coverage.md` update the `baha target policy set` description to "remote operator policy mutation for existing Targets is future scope (see card 0427-186)."

Verdict: **not a REJECT**. The card itself declares point 3 out of scope for this slice; the coordinator's OPTION-1 (full acceptance) applies to the card's remaining work, which #1588 does not attempt. #1588 delivers and CI-tests point 2 correctly.

## Diff (7 files, docs + provenance slice only)

```text
cmd/baha/app_remote_lifecycle.go                    +18  (build Core-owned admission evidence up-front)
cmd/baha/deployment_record.go                       +30  (admissionEvidenceForApplyingMutation)
cmd/baha/machine_coverage.go                        +2   (docs: remote mutation = future scope)
cmd/baha/target_deployment_policy_edit_b_test.go    +88  (remote edit refused; local preserves Core binding)
docs/reference/cli-machine-coverage.md              +2   (mirror of machine_coverage)
internal/deployment/immutable_provenance.go         +152 (ImmutableProvenance + tests)
internal/deployment/immutable_provenance_test.go    +85
```

No reserved files (`cmd/baha/commands.go`, machine registry, `.github/**`, release notes untouched).

## CI witness

Exact-headed `pull_request` run 43735861483, head `9534edd4` (cli-0..3 + packages):

```json
{"conclusion":"success","databaseId":43735861483,"event":"pull_request","headSha":"9534edd49c205adabe858516e1400640ad6ec2cb","status":"completed","workflowName":"CI · Source & Quality"}
```

Job-level: all `PR · Draft Go · cli-0..3` and `PR · Draft Go · packages` = success; remaining jobs skipped (draft PR — frost). The new tests pass:
```
--- PASS: TestRemoteTargetPolicyEditRefusesLocalSubstitution (0.00s)
--- PASS: TestLocalTargetPolicyEditPreservesCoreBinding (0.01s)
```
No rerun or workflow_dispatch initiated.

## Draft-PR protocol note

#1588 is OPEN/DRAFT (`gh pr view 1588 --isDraft=true`). Per frost this is a protocol detail, not a substantive reject.

## Verdict

APPROVE #1588 at `9534edd49c205adabe858516e1400640ad6ec2cb`. Delivers card 0427-186 point 2 (Core-verified immutable source provenance, forged/refuse fail-closed) with CI-green tests; presets CLI/wizard present (point 1). Point 3 (remote operator edit) is the card's explicitly deferred future-scope and is correctly NOT in this diff — the remote-edit path still refuses with `ErrorUnsupported` and the diff documents the deferral. This is not a REJECT: the card declares point 3 out of scope for the slice. No product code, workflow, CI, container or VM changed. PR #1588 NOT merged (frost honoured).

## repo-rule compliance

Evidence in the actual planning repository (verified before commit). Product remote state from a fresh clone and `git ls-remote`; the quarantined workers checkout was not used. No product code, `.github/**` files, CI, containers or VMs changed. No merge. No markdown checkbox lines.

## END mission-1588-r1 DONE — APPROVE #1588 at 9534edd49c205adabe858516e1400640ad6ec2cb (point 3 = card-deferred future-scope, not a REJECT)

## Planning validation

`python3 scripts/plan.py render && python3 scripts/plan.py check` completed successfully. `git diff --check` passed. No Markdown checkbox lines.

Planning origin/main witness before push (`git ls-remote origin refs/heads/main`):

```text
65ff0c7c74e15bb40cc2bc28f4f9b7b13e5ce0e7	refs/heads/main
```
