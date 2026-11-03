# Fix round r2 — state-owner seam, identity binding, tenant bypass, test hardening

Lane: s2-stateowner-r2 · Role: Worker · Coord: f49a3303
Basis: PR #1347 head cdfc75bf (branch work/r27-state-owner, base develop)
Evidence contract: plain bullets, no checkboxes.

## PLAN

1. SEAM-WIRKLICHKEIT: route LoadDeploymentRecord + listing + SaveDeploymentRecord through VerifyDeploymentOwner at the loader path (production seam), not test-only helper; tests drive real Load/Save/list path (positive, foreign owner, missing state, corrupt file).
2. IDENTITÄTS-BINDUNG: bind deployment to installation.ID (not only target pathname). Look up ID in existing installation-authorities (compare internal/installauthority/coreinstallation develop templates). Tests: same-target two-installation, copied-state, binding-change. STOP clause if durable ID binding requires an accepted protocol that is missing -> END_BLOCKED with exact stop location.
3. TENANT-BYPASS: remove VerifyDeploymentOwner:50-53 tenant early-return OR replace with a genuine authorized owner path for tenant targets; both server and local paths tested.
4. TEST-HAERTTE: TestDeploymentOwnerRejectsForeignInstallationDir creates a real symlink at a nonexistent path; setup failure => t.Fatal; fixture-remove errors not swallowed.
5. ANSENDE-PFLICHT: merge origin/develop; diff grep -E '^(\.github|scripts/)' empty; content parity to 15fe7762/cdfc75bf files; tests TMPDIR=/tmp go build ./... + go test ./internal/deployment ./cmd/baha; push FF; ls-remote.

## repo-rule compliance

- Write-set bounded by task card: internal/deployment/deployment_store.go, cmd/baha/app_context.go, cmd/baha/deployment_record.go, matching state-owner tests (task-karten line 52).
- No edits to another slice's files; no installauthority/coreproduction files; no CI files.
- STOP rule: two failed identical fixes => END_BLOCKED; no merge.

## END line

END DONE s2-stateowner-r2: <candidate SHA>
