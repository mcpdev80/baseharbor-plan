# 0428-284 — Serial Execution Runbook (read-only plan/runbook)

**Mission:** `coordinator/missions/w99-0428-284-serial-runbook.txt`
**Shift:** r28-welle6-2026-11-25
**Scope:** READ-ONLY. Plan/runbook only. NO edits/PR/merge/rebase/CI-trigger on #1812/#1819/#1820/#1818; NO touching #1826/consent/demo. NO subagents (§4.8). Contact no other session.
**Outcome:** END_DONE. Delivered the ordered, copy-pasteable runbook. Created nothing, edited nothing.

## PLAN

- [x] Read mission file + coordinator-runtime.toml; run basics-check + events-check --ack
- [x] Witness remote state via `git ls-remote` + `gh api`: develop f14fb87c8, demo c23bd9ac, PR heads
- [x] Verify #1823 deny-override present on develop (guard); verify #1820 branch contaminated 28803d11
- [x] Write this evidence file only — no product/plan edits, no branch, no PR, no CI trigger
- [x] Post END_DONE to coordinator lane

## Remote witnesses (measured, read-only)

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/main`:
```
f14fb87c8f5afd91168e4f174d620c9f00e6341e	refs/heads/develop
c000c5db2560c471fe84842136e03d6e54d96779	refs/heads/main
```

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/<n>/head`:
```
PR 1812: 47590207518ce9501f1b1bbb115d72d64a206d14	refs/pull/1812/head
PR 1819: 17381017be986f0eccb25662ad742ad759296346	refs/pull/1819/head
PR 1820: 28803d11027197e7734fb3ec94bef9b34e224b0d	refs/pull/1820/head
PR 1818: 20fc1cb7d49602dc7f8aa0004a7562a81311d78c	refs/pull/1818/head
```

demo: `git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/heads/develop` = `c23bd9ac58919302ffad3a43f43afb1a34bfbc96`

## Current PR state (gh pr view, read-only)

All four PRs: `state=OPEN`, `baseRefName=develop`, `mergeStateStatus=BEHIND`, `mergedAt=null`.

- #1812 `lane-0428-249-runtime-image-fix` — fix(ci): re-load missing runtime image before ORAS publish. Changed 1 file (+20/-0): `.github/workflows/pre-release-runtime-suite.yml`. Base SHA `46d3dccc1` (the commit BEFORE #1823).
- #1819 `w54-0428-181-export` — 0428-181 wire Perses identity dashboard into export path.
- #1820 `fix/broker-build-identity` — fix(0428-271): prove exact runtime broker commit in readiness probe. Head = `28803d11` (the contaminated head per w89).
- #1818 `lane-0428-078-cf-fix` — fix(0428-078): consume real Perses probe for identity dashboard eligibility. Head = `20fc1cb7` (the VOID'd per w99).

## CI witnesses (PR Selected Checks, exact-head)

- #1812: `PR Selected Checks` SUCCESS @ run 45397265257 (2026-11-24T12:51:06Z). All required gates SUCCESS; docker/podman Targeted HA + Go unit + Native SKIPPED (path-based, not run for this single-file CI fix).
- #1819: `PR Selected Checks` SUCCESS @ run 45380314808 (2026-11-24T11:24:04Z). Go unit (cli-0..3, packages, owner) SUCCESS; docker · data-capabilities SUCCESS; required gates SUCCESS.
- #1820: last run 45382404741 — `PR · Selected Runtime / Executed docker · data-capabilities` CANCELLED; `PR Selected Checks` absent. #1820 needs a fresh re-run after the fresh-cut head is fixed.
- #1818: last run 45316544436 — `PR Selected Checks` SUCCESS @ 03:25:13Z; all runtime docker/podman gates SUCCESS. Head `20fc1cb7` is the VOID'd candidate per w99 — needs reset to `8e2c50c1`.

## develop recent commits (f14fb87c8 is HEAD)

```
f14fb87c8 fix(0428-277): fail-closed AuthorizationResult for failed reveal (#1823)
46d3dccc1 fix(0428-249): build baha-ci-operator-testonly artifact with its build tag (#1825)
2b9a2c6d1 fix(0428-276): make env-destroy OwnerVerified a genuine per-deployment owner re-check (#1824)
05ef48536 fix(0428-270): remove dead trusted-local fail-open arm from authorizeMachineOperation (#1821)
90086a1f9 # feat(0428-269): batch baseline — pr-gate-coverage six rows + pre-release baha-ci-operator-testonly (#1822)
3ebfb90da 0428-250: source=local config-organization predicate + wrong-gate negatives (base develop 840c4a6b) (#1815)
cd2fcda7e 0428-152: alert-verifier caller wiring — one honest consumer for the Perses alert evaluator (#1816)
840c4a6b6 0428-058: audit secret and env actions (#1809)
```

## Guard verification: #1823 deny-override on develop (f14fb87c8)

#1823 added `cmd/baha/secret_operations.go` + `cmd/baha/secret_audit_test.go`. Post-rebase of #1812/#1819 onto develop must PRESERVE these deny-override assertions (the branches' base is pre-#1823, so a merge/rebase keeps develop's #1823 content — verify it is content-reversing-NEGATIVE, i.e. #1823 lines remain present):

`secret_operations.go` @ f14fb87c8, relevant lines:
- L58: `if decision.Allowed {` then L61: `event.AuthorizationResult = "deny"`
- L81: `event.AuthorizationResult = "deny"` (failure with no decision)
- L171, L186, L217/L224: recordRevealFailed passes "deny" (fail-closed override 0428-277)

`secret_audit_test.go` @ f14fb87c8 asserts `event.AuthorizationResult == "deny"` at L195/196, L241/242, L310/311 (loa2/[password,webauthn] deny paths). **Guard = re-run post-rebase and grep that these deny-assertions are still present; a clean merge-tree keeps them, so confirm no content-reversing removal.**

## #1820 contamination witness

PR #1820 head = `28803d11027197e7734fb3ec94bef9b34e224b0d` = the contaminated head. Must be cut FRESH from develop `f14fb87c8` carrying ONLY the 0428-271 regression (`cmd/baha/app_broker_compat_test.go:76-81`), dropping the inverted 0428-276 fold per w89.

---

## The runbook (deliverable)

Strict-serial dependency edges — none may run in parallel:

```
#1812  →(merge→) #1819 →(merge→) #1820
                  │
                  └─(merged) → gates #1818 (also needs owner C)
```

1812→1819→1820 linear; #1818 sits behind #1819's merge AND owner decision C. All four remain DRAFT.

### 0. PREREQUISITE — operator-provisioning fix (0428-283 family)

Owner authorized the single operator-provisioning fix (confirmed by w92 as the #1812 blocker). This must merge to develop first, producing new develop SHA **X**. Every step below waits on X.

```
# after 0428-283 merges to develop:
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
# => new SHA X  (post f14fb87c8)
```

### 1. #1812 requalification (first chain action, after X)

Target branch: `lane-0428-249-runtime-image-fix`. Base is currently `46d3dccc1` (pre-#1823).

Guard (preserve #1823): after rebase, grep confirm `cmd/baha/secret_operations.go` deny-override (L58/L61/L81/L171/L217) + `cmd/baha/secret_audit_test.go` deny assertions (L195/241/310) are present — base is pre-#1823, merge-tree clean but content-reversing, so verify post-rebase.

```
# branch checkout + rebase onto X (owner executes; read-only here)
git fetch origin develop
git switch lane-0428-249-runtime-image-fix
git rebase origin/develop          # base now = X, #1823 deny-assertions stay present
git log --oneline origin/develop..HEAD   # MUST list ONLY this lane's commits
git push --force-with-lease origin lane-0428-249-runtime-image-fix
# witness delivery:
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1812/head
```

Exact CI — v0.4.27 Docker Light (only_gates = 7 atomic/docker ids, tag v0.4.27, demo_ref = demo tip containing operator fix), then Podman family after Docker terminal:

```
gh workflow run pre-release-runtime-suite.yml \
  --ref develop \
  --field only_gates="7 atomic/docker ids" \
  --field tag=v0.4.27 \
  --field demo_ref=<demo tip with operator fix>
# then after Docker terminal: Podman family run
```

Record: the 2 owner-required run IDs (Docker Light + Podman family) + the 14 gate outcomes.

### 2. #1819 (serial pos 2, after #1812 merged)

Rebase `w54-0428-181-export` onto current develop (same #1823-preservation guard; 2 behind), force-push, exact CI. Post-merge it makes the `perses_dashboard_provision` coverage rows (card 0428-278) go live.

```
git fetch origin develop
git switch w54-0428-181-export
git rebase origin/develop          # same #1823 guard
git log --oneline origin/develop..HEAD
git push --force-with-lease origin w54-0428-181-export
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1819/head
```

### 3. #1820 (serial pos 3, after #1819 merged)

CUT FRESH from develop `f14fb87c8` (NOT the contaminated `28803d11`); drop the inverted 0428-276 fold per w89, carrying ONLY the 0428-271 regression (`cmd/baha/app_broker_compat_test.go:76-81`).

```
# provenance: cut from develop base, witness ancestor
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
git log --oneline <develop-sha>..HEAD     # only this lane's commits; base ancestor check
# branch carries only the 0428-271 regression, no 0428-276 fold
```

Open PR, exact CI. Head must NOT be `28803d11` — the fresh-cut replaces it.

### 4. #1818 (gated on #1819-merge + owner C)

Reset `lane-0428-078-cf-fix` to the canonical clean head `8e2c50c1` (VOID `20fc1cb7`). Apply C retarget: persesDashboardProvisionForLifecycle seam at `internal/metrics/perses_dashboard_provision.go` + `TestPersesKeycloakDashboardQueriesSelectRealProviderLabels` at `cmd/baha/perses_dashboards_test.go:766`. Exact head, `--confirm-candidate` only after #1819 merged.

```
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1818/head   # before: 20fc1cb7 (VOID)
# reset to canonical 8e2c50c1, apply C retarget (seam + test), re-run CI
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1818/head   # after: 8e2c50c1-derived
```

### Merge order (enforced)

```
#1812  (first, after prereq X)
  └─ #1819   (after #1812 merged)
       └─ #1820 (after #1819 merged; fresh-cut head)
       └─ #1818 (after #1819 merged + owner C; reset to 8e2c50c1)
```

---

## repo-rule compliance

- Read-only mission. No product files, no `.github/**` (Owner scope), no plan cards, no edits.
- No branch created, no PR opened/updated, no merge/rebase, no workflow_dispatch / CI-trigger.
- No subagents (§4.8). No local product tests (hosted-only §2026-11-23). No VM runs.
- Evidence written only into `baseharbor-plan/evidence/r28-welle6-2026-11-25/serial-execution-runbook/round-1.md`.

## Evidence provenance

Planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (NOT the workers/ bookkeeping checkout). `git -C baseharbor-plan remote -v` confirms the real GitHub remote before any evidence commit.

## cleanliness

- Read-only session. Started no containers, no compose projects, no VM stacks. `docker ps -a` not needed (no stack owned).
- Nothing created; nothing edited.

## Status

END_DONE. Delivered the ordered runbook. No product/plan/PR/CI action taken.
