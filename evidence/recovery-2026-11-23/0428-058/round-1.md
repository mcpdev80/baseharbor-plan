# 0428-058 — Audit secret and env actions (round 1)

- Bounding task: `t-20261114-r28-cli2-audit-events` (0428-058), release v0.4.28, repo `mcpdev80/baseharbor`.
- Slice of umbrella `t-20261114-r28-cli-command-semantics`; NOT a second independent product.
- Evidence lives in `baseharbor-plan` ONLY (real repo). No `.evidence/` directory in the product repo.

## Repo rule compliance

- Real planning repo verified: `baseharbor-plan` remote is `https://github.com/mcpdev80/baseharbor-plan.git` (confirmed before first evidence commit).
- Product checkout used: fresh clone at `/tmp/opencode/w058-0428-058-cli2-audit-events-src`, remote `origin = https://github.com/mcpdev80/baseharbor.git`. The quarantined stale-ref checkout under `workers/baseharbor` was NOT cited as evidence (per REALITY WITNESSES directive).
- Write-set respected: did NOT touch `cmd/baha/local_workload_authority.go` (0428-243) or `internal/capability/perses_selection.go` (0428-186). No `.github/**` edits (Owner scope).

## PLAN

- Numbered work steps in the live board file `workers/todos/w058-0428-058-cli2-audit-events.json`.
- Validate current `develop` and the owner-approved contract before coding.
- Audit which secret/env operations already write audit events and which do not.
- Add auditable outcomes for secret set/delete/list and env edit/delete: who/what/where/result, no values, human vs runtime actor, authorization result, exact resource context.
- Follow the existing `connection-reveal` / `recordEnvDestroyAudit` pattern in `cmd/baha`.
- Add focused unit tests; keep them CI-reachable in this same PR.
- One candidate branch `lane-0428-058-cli2-audit-events`, one PR (DRAFT until impl + gate complete).

## Base attestation

- Real `origin/develop` head (via `git ls-remote https://github.com/mcpdev80/baseharbor.git develop`):
  - `dc8626e9c52be07a8ea5b87b468c5991b7540c4f`
- Branch cut from that exact head; `git log --oneline origin/develop..HEAD` lists only my own commits (verified clean at creation).
- Dependent cards `t-20261114-r28-cli2-env-delete`, `-env-policy`, `-env-registry`, `-identity-secrets` merged into `develop` (confirmed by HEAD listing; 0428-061 source-pull is the latest develop commit).

## Scope finding (contract conformance)

- `internal/evidence` already implements the storage contract: `Append(root, AuditEvent)` with 0700 dir / 0600 file, retention bound (`MaxAuditEvents = 1000`, `maxAuditBytes = 8MiB`), integrity via `Seal`.
- Existing audit-write patterns (models to follow):
  - `recordEnvDestroyAudit` (`cmd/baha/env_destroy.go:335`) writes `env.destroy` → `success`/`denial`.
  - `recordConnectionRevealAudit` (`cmd/baha/app_access.go:368`) writes `connection-reveal` → `allow`, populating `Actor` fields from `AuthorizationDecisionFromContext` / `PrincipalFromContext`.
- GAP discovered: `secret.set`, `secret.delete`, `secret.list` in `cmd/baha/secret_operations.go` currently write NO audit events. `authorizeApplicationOperation` gates them (operation id `secret.set`/`secret.delete`/`secret.list`) but nothing is appended to the audit log.
- `authorizeHumanReveal` gates the human-only `--reveal` seam on `secret.reveal`; the connection-reveal precedent shows how to attribute a verified principal.

## Scope decision / contract drift check

- No contract drift: command-map maps `baha app secret` → `baha app data secrets`, `baha app env` → `baha app data env`; owner brief (brief.md line 11) requires audit on all access paths for `app data secrets`, "never values; no personal attribution without person identity."
- Audit-storage semantics (who/what/where/result, no values, retention integrity only with proof, trusted-local is not a person) are unambiguous from the existing `internal/evidence` model + card acceptance. No STOP/QUESTION raised.

## Results

- (To be completed after implementation.)

## NEXT

- Implement secret audit hooks in `secret_operations.go`.
- Implement env edit/delete audit hooks where the env mutation path exists.
- Add unit tests + ensure CI reachability.
- Push candidate, verify delivery, collect CI run, commit evidence, END.
