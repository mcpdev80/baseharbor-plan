# Bug-Hunt H-V27: Env/Org/Registry Lifecycle Desk (Slice H-V27)

**Lane:** `w62-0428-276-huntenvdesk`
**Type:** Read-only Befundung, NO product/plan/CI changes, NO commits/pushes/PRs
**develop-Anchor:** `3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd` (v0.4.28, only CLOSED/merged)
**Scope:** merged `#1809`/`0428-058` env/org + registry surface. Read-only. No fix.

## Repo-rule compliance

This is a read-only bug-hunt mission. No product code, no planning, no CI edits.
All findings documented in this evidence file only. No evidence written into any
product repo (no `.evidence/` directory, no main-branch writes). No subagents,
no Codex, no merge, no hosted runs. Containers/volumes/networks only on named
SSH hosts (none started here — pure read-only source inspection on the anchor
worktree).

## Reality witnesses (pre-work)

```
# baseharbor-plan remote (evidence repo)
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
git ls-remote origin main -> 470e7f6f3b9ff786e3fcb36a8db958b1ade232fe refs/heads/main

# baseharbor product remote (real github.com URL)
origin	https://github.com/mcpdev80/baseharbor.git
lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
upstream	https://github.com/mcpdev80/baseharbor.git

# develop anchor attestation
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
-> 3ebfb90daaf472a1f98a7fe648589bd3e15fb1cd refs/heads/develop
# anchor is ancestor of worktree HEAD: OK (git merge-base --is-ancestor 3ebfb90d HEAD)
```

Evidence path `evidence/r28-welle6-2026-11-24/bughunt-hv27-env-org-registry/round-1.md`
was ABSENT from `origin/main` before writing (created this shift).

## PLAN

- Establish reality witnesses (remote HEAD, base attestation, evidence path)
- Section A: env reveal-success-after-read + secret runtime-actor/allow (#1809 A/B)
- Section B: env_destroy trusted-local/allow + --confirm-delete-data consent (#1809 C)
- Section C: app/target/node association in environment.json (env path)
- Section D: registry-access / local-registry round trip
- Cross-check against H-V25 (status/observability) and H-V26 (candidate/consent/runtime-gate)
- Write read-only finding list to evidence round-1.md
- Record cleanliness, post END_DONE, report to coordinator

## Methodology notes

- No hosted runs triggered (no PR). No VM containers started (pure read-only source inspection).
- Findings carry file:line, reproducible path, expected vs. actual, severity, reference card/PR.
- Duplicates to `0428-189..194`, H-V25 F1-F9, H-V26 F1-F5 are NOT re-reported.
- Avoid H-V25 (status/observability) and H-V26 (candidate/consent/runtime-gate) hot-spots; probe OTHER spots with 'wie 0428-1xx' note.

## Findings

Scope: read-only Befundung of the merged #1809 / 0428-058 env/org + registry
surface on develop anchor 3ebfb90d. No product weakness confirmed as a
blocker. Two precision/audit findings below are non-blocker; the rest of the
surface is correct. Duplicates to 0428-189..194 / H-V25 / H-V26 are NOT
re-reported.

### F1 (non-blocker, audit precision) — env destroy `OwnerVerified` marker is nominal

- Where: `internal/deployment/environment_destroy_scope.go`, Z. 183-185:
  `CollectEnvironmentDestroyScope` sets `OwnerVerified: true` on every scoped
  `EnvironmentDestroyDeployment`.
- Expected: the destroy path re-verifies each scoped deployment's one-installation
  owner before deleting (the `applyEnvironmentDestroyScope` guard at
  `cmd/baha/env_destroy.go`, Z. 264 checks `!dep.OwnerVerified`).
- Actual: owner verification happens once inside `ListDeployments` ->
  `listDeploymentRecords` (`internal/deployment/deployment_list.go`, Z. 110
  `verifyDeploymentOwnerAtSeam`), which returns records only when every owner
  verified or fails closed. `CollectEnvironmentDestroyScope` never calls
  `VerifyDeploymentOwner` per-deployment; the `OwnerVerified: true` field is
  always true and reflects only the `ListDeployments` pass, not a per-deployment
  re-check. The guard in `applyEnvironmentDestroyScope` therefore always passes.
- Severity: Low. No bypass: an ownerless/malformed deployment still fails the
  shared `ListDeployments` read before the scope is built, so the fail-closed
  behavior is intact; only the per-deployment owner marker is cosmetic.
- Ref: card 0428-055 (`t-20261114-r28-cli2-env-delete`).

### F2 (non-blocker, audit-precision nuance) — reveal failure records `AuthorizationResult=allow`

- Where: `cmd/baha/environment_operations.go`, Z. 39-44: a failed
  `inspectApplicationEnvironment` (e.g. `os.Stat(files.ApplicationEnv)` missing
  at Z.39) calls `recordRevealFailed`, which reads the stored
  `AuthorizationDecision` and sets `AuthorizationResult=allow` (the human reveal
  was authorized) while `Outcome=failed`.
- Expected: an audit event that carries both a consistent authorization-result
  and outcome.
- Actual: the event records `outcome=failed` (the material fact is correct) but
  `AuthorizationResult=allow` because the human-operator + secret.reveal decision
  was already granted upstream (`authorizeHumanReveal`, `cmd/baha/secret_operations.go`,
  Z.111-130). The `outcome` field correctly signals the failure; only the
  authorization-result sub-field is arguably inconsistent with a failed release.
- Severity: Low. Non-blocker; the reveal success path is recorded only after a
  genuine successful read (`cmd/baha/environment_operations.go`, Z.52-55) and
  the H-V14 secret-reveal-paths evidence already validated the reveal seams.
- Ref: H-V14 / 0428-171.

### Sections B, C, D: correct (no finding)

- Section A (`env --reveal`): `RequireHumanOperator` fails closed on missing /
  unverified operator identity (`internal/operatorauth/authorization.go`, Z.330-356);
  success is recorded only after a successful read (`environment_operations.go`,
  Z.52-55); the audit precedence correctly records denied decisions as `deny`
  (`secret_audit_test.go`, Z.206-247). Correct.
- Section B (`env destroy`): abandoned runs retain the environment identity for
  retry (`cmd/baha/env_destroy.go`, Z.175-178); scoped-vs-global classification
  is by `application_id`, not name (`environment_destroy_scope.go`, Z.176-205);
  shared/global deployments preserved; `--confirm-delete-data` requires
  `--delete-data` (`env_destroy.go`, Z.426-428). Correct.
- Section C (app/target/node association): membership key is the `(kind, id)`
  tuple; collision is fail-closed (`ErrAssociationAlreadyExists`), migration is
  idempotent (`RegisterEnvironmentAssociation`, `internal/deployment/environment_association.go`,
  Z.193-239); path traversal rejected by slug guard + binding-check
  (`TestDeregisterEnvironmentAssociationRejectsEnvironmentPathTraversal`). Correct.
- Section D (registry-access / local-registry): the OCI org-config path is
  opt-in only and fails closed with distinct hard-rejection identities
  (`internal/orgconfig/source_oci.go`, `isHardRegistryRejection` Z.90-97;
  `classifyOrgRegistryError` Z.105-121); public-default endpoints rejected;
  unverifiable (no sha256 digest) resolution never covered by a mutable
  fallback (`resolveOCI`, `internal/orgconfig/source.go`, Z.185-239). Correct.

## Cleanliness

No containers/volumes/networks started on any host. Pure read-only source inspection
on anchor worktree `workers/w62-0428-276-huntenvdesk-wt`.

## Handoff

END_DONE with finding count. Coordinator cards per §3.3.5.
