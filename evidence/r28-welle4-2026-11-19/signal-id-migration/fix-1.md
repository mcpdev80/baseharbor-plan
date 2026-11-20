# 0428-168 keycloak signal ID migration gap

## PLAN

- Step 1: Reality check — git ls-remote develop 6b8188df (now moved to 83b19dce), read merge b7cbc00f (PR #1707), before/after ID formula: literal `keycloak-metrics` → `keycloak:` + project.
- Step 2: Reproduce the leiche FIRST — TestLegacyKeycloakMetricsSourceIsCorpseProvesTheBug witnesses the corpse (source dropped by RegisterProviderSignals when a sibling project registers its new scoping ID).
- Step 3: Migration — ReconcileLegacySignals (idempotent, no-mutation, state-lock via mutate), wired into registerKeycloakSignals.
- Step 4: Regression — corpse witness (buggy), rebook fix, idempotent + foreign-provider untouched, end-to-end integration test for 3 distinct Keycloak projects.
- Step 5: CI shard wiring (packages, draft Go shard) + hopf-merge onto moved develop + PR run to terminal.
- Step 6: Commit evidence to baseharbor-plan origin/main, END_DONE with run-id.

## Repo-rule compliance

- Scope: product code + tests only. No .github/** change (Owner scope); no CI-file edit needed — my tests run under CI shard `packages` on the develop base (pr_draft_go_shards).
- No merge by me. No write to internal/logs/realization.go or internal/telemetry/realization.go (card 0428-167). No subagents (§4.8). No VM/container/network/volume.
- Working clones isolated under /tmp (bh-168-clean, w-168-168-pr, bh-plan-168); stray test-eigen runtime dirs removed before push. Evidence only in baseharbor-plan, never in a product repo.
- Branch provenance: base develop 83b19dce24e2 (ancestor of first commit 983152b9), branch lane-0428-168-signal-id-migration. PR #1709.
- CI: run 44660104342, conclusion SUCCESS, on exact candidate SHA 983152b976. Required jobs executed (not skipped): Go unit packages, go-vet, identity-provider-package-tests, go-build, cli-0/1/2/3, owner, validation.
- CI-audit: ci-fast-check.sh PASS, source-readability-audit.sh PASS (registry.go 766 lines, migration.go separate), gofmt clean, go vet clean, full test suite for affected packages PASS.

## Evidence witnesses

ls-remote develop (task start):
6b8188df26a1e263750379a8c5e8255ee4ef740c	refs/heads/develop

Merge b7cbc00f (PR #1707) — before/after ID formula:
- before: `ID: "keycloak-metrics"`
- after: `ID: registrationID` where `registrationID := "keycloak:" + r.files.Project`

Corpse witness (buggy code): `ListMetrics` under app-a returns 0 Keycloak sources after a sibling Keycloak project registers its scoping ID; the legacy `keycloak-metrics` source of record is gone from List and unremovable by its own ID.

## Cleanliness:

(none — no containers, networks, volumes or state directories created; stray test-eigen runtime dirs under internal/application/* removed before push)

---

## Task status: DONE

Branch: lane-0428-168-signal-id-migration | PR #1709 | base develop 83b19dce
Run 44660104342 = SUCCESS on 983152b976 (Go unit packages + go-vet + validation)
