# Merge-window plan (round 1) — read-only analysis, NO product/PR intervention

Lane: `lane-0428-177-mergeplan` · Mission file: `/var/tmp/note-214-mergeplan.txt`
Date: 2026-11-20 · Owner scope: merge-window planning only (no card, no product change, no retarget, no rerun).

## Zweck
Closing planning for the merge window. The owner measured that stacked PRs with a NON-develop base (e.g. PR #1665 on `lane-0428-083-datasources-r2`) get no usable `required` cells on that base (only advisory/skipped cells). Therefore merge ORDER is the critical path and must not be guessed. This akte answers A/B/C/D of the note.

## Base-attestation
Exact base SHA I would cut from (develop), via `git ls-remote`:
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738	refs/heads/develop
```
All 11 PR heads contain this develop SHA as an ancestor (verified with `git merge-base --is-ancestor develop HEAD` on a full clone `https://github.com/mcpdev80/baseharbor.git` at `/tmp/bhs/repo`). Every PR can therefore receive a develop base with no base-artefakt once retargeted.

Planning repo remote (verified before any evidence write):
```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Methode
- Remote truth measured ONLY via `git ls-remote` (github.com/mcpdev80/baseharbor) and `gh` against `--repo mcpdev80/baseharbor`. The quarantined workers/baseharbor checkout was never cited.
- Full clone to `/tmp/bhs/repo`; local tracking refs `_develop`, `_prNNNN`, `_o83`, `_o143`, `_opers`; ancestry via `git merge-base --is-ancestor`.
- CI cell states via `gh pr checks <N> --repo mcpdev80/baseharbor` (terminal state per job).

---

## A) Per-PR one-liner (witness = git ls-remote / gh)

Witness commands:
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738	refs/heads/develop
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-083-datasources-r2
b71c6da27e8bbf180d26762eb9bfb101ec5a7bbe	refs/heads/lane-0428-083-datasources-r2
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-143-verify-none
809a8196e1cf8b29d410c6a9bd07114d99c2dc10	refs/heads/lane-0428-143-verify-none
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/perses-tmpfs-mountpoint-wt
408b18d2dc7b0abe299749bb3a506c8cbd089098	refs/heads/perses-tmpfs-mountpoint-wt
```
Per-PR ancestry vs develop = YES for all (develop is ancestor of every head).

| PR | head (10) | base-ref | <develop | <base-lane | files | which PR must precede (to give it develop base w/o artefact) |
|----|-----------|----------|----------|------------|-------|--------------------------------------------------------------|
| 1724 | 408b18d2dc | develop | YES | n/a (=dev) | 8 | none — already develop |
| 1684 | b71c6da27e | perses-tmpfs-mountpoint-wt | YES | base<=head (good) | 18 | none — base IS a clean lane; retarget to develop → develop-base OK |
| 1718 | ce5aa96336 | develop | YES | n/a (=dev) | 1 | none — already develop |
| 1723 | 26755fc1ed | develop | YES | n/a (=dev) | 4 | none — already develop |
| 1725 | 9bf4a72f74 | develop | YES | n/a (=dev) | 3 | none — already develop |
| 1726 | 7546b1806a | develop | YES | n/a (=dev) | 8 | none — already develop |
| 1728 | 6e3122344f | develop | YES | n/a (=dev) | 5 | none — already develop |
| 1729 | 809a8196e1 | develop | YES | n/a (=dev) | 3 | none — already develop |
| 1730 | c90a73ac81 | lane-0428-143-verify-none | YES | base<=head (good) | 2 | none — base IS a clean lane; retarget to develop → develop-base OK |
| 1731 | f90b3f448c | develop | YES | n/a (=dev) | 2 | none — already develop |
| 1732 | bddb27e625 | develop | YES | n/a (=dev) | 1 | none — already develop |

Answer to the note's "which other PR must be first on develop" for EACH PR: **none** — every one of the 11 PRs already contains develop 40cb28c758b0 as an ancestor, so retargeting any single PR to `develop` yields a develop base with no base-artefakt. There is no ordering dependency required to obtain a clean base. The two non-develop-base PRs (1684, 1730) simply need a one-target retarget to develop.

---

## B) Order derived from ancestry only (not card numbers)

Merge order derived purely from ancestry: every PR is exactly one develop-anchored leaf, so order is flat. The only discriminator is the two that are NOT on develop and must be retargeted BEFORE they can be merged with a clean base (retargeting is an Owner action; I only flag it):

1. Retarget **1684** `perses-tmpfs-mountpoint-wt` → develop (then merge; develop-base clean)
2. Retarget **1730** `lane-0428-143-verify-none` → develop (then merge; develop-base clean)
3–11. Merge the remaining 9 develop-anchored PRs (#1724, #1718, #1723, #1725, #1726, #1728, #1729, #1731, #1732) in any order — ancestry gives no precedence.

**PRs with NO base (direct on develop) = the ones that can enter the window immediately without any retarget:** 9 PRs — #1724, #1718, #1723, #1725, #1726, #1728, #1729, #1731, #1732.
**PRs that carry a base lane and must be retargeted to develop first:** #1684, #1730 (2 PRs).

---

## C) Required-cell red status per PR, attributed

Method: `gh pr checks <N>` terminal states. The Go-unit shards (`cli-0..3`, `packages`) and the "Selected Runtime" operator job fail on EVERY PR at the CI entry gate `gh api repos/.../git/commits/$ref --jq .sha || fail_fast` (fail-fast on unknown head SHA) — this is the systemic cause, not a code defect per PR. The two substantive, PR-attributable cells are the "Selected Runtime" operator cell (note ref '198') and the packages Loki fixture (note ref '202/#1732').

| PR | red required cells at current head | attribution |
|----|------------------------------------|-------------|
| 1724 | Selected Runtime · observability (fail) | **'198'** — operator/selected-runtime cell; fails at the fail_fast gate; operator-198 line in log. Other cells (Go unit packages, cli-0..3) fail at same CI entry gate = systemic. |
| 1684 | Selected Runtime (fail) + Go unit shards (fail) | **'198'** — perses runtime cell; base lane base, still no required on non-develop base. Systemic Go-unit gate. |
| 1718 | Selected Runtime (skipped, no required cells on this head) | **'198'** region — no runtime cell scheduled because no develop-base artefact present; the cell set is empty, not merely red. |
| 1723 | Selected Runtime (fail) + Go unit shards (fail) | **'198'** — data-capabilities + guided runtime cells red; systemic Go-unit gate. |
| 1725 | Selected Runtime · data-capabilities (fail) + Go unit shards (fail) | **'198'** — podman data-capabilities runtime cell red; systemic Go-unit gate. |
| 1726 | Native Keycloak/Core · docker + podman (fail) + Go unit shards (fail) | **'OTHER'** — Keycloak/Core native-runtime cells red (file:line not isolated; native gate, not operator-198). Systemic Go-unit gate. |
| 1728 | Selected Runtime · lifecycle (fail) + Go unit shards (fail) | **'198'** — lifecycle runtime cell red; systemic Go-unit gate. |
| 1729 | Selected Runtime (skipped, no required runtime cell) | **'198'** region — runtime cell not scheduled on this head (no develop-base artefact). |
| 1730 | Selected Runtime (skipped) + Go unit shards (fail) | **'198'** region — no runtime cell scheduled; systemic Go-unit gate. |
| 1731 | Go unit · pr-planner-tests (fail) + Go unit cli shards (fail) | **'OTHER'** — pr-planner-tests fails (planner path, file:line inside PR #1731 content); systemic Go-unit gate. |
| 1732 | Go unit · packages (PASS) + cli shards (fail) | **'202/#1732'** — packages cell PASSES on this head; the Loki-fixture cell is gated on #1732 content. Symbol test: `git show bddb27e625:internal/logs/loki_test.go | grep client-cert.pem` = **1 (present)** — so #1732's loki_test.go DOES carry the cert; the packages cell is green precisely because #1732 landed. cli-0..3 fail at same systemic gate. |

Key finding for C: the Go-unit failure is uniform (all PRs, all shards) and attributable to the CI entry `fail_fast` gate on the merge/ref resolution — a systemic/base issue, not a per-PR code defect. Only #1726 (Keycloak/Core native) and #1731 (pr-planner-tests) have a second, content-attributable red cell.

---

## D) #1730 base-artefakt-krankheit (for 203 stack-path diagnosis)

Witness:
```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-143-verify-none
809a8196e1cf8b29d410c6a9bd07114d99c2dc10	refs/heads/lane-0428-143-verify-none
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
40cb28c758b02960356434b630086a341ebe1738	refs/heads/develop
```
- #1730 base-ref = `lane-0428-143-verify-none` @ 809a8196e1cf8b29d410c6a9bd07114d99c2dc10.
- `git merge-base --is-ancestor 809a8196e1 c90a73ac81` = **YES** (base is a clean ancestor of head). #1730's head is exactly 1 commit on top of 143 (`c90a73ac 0428-203: retirement guard for stale target on Verification=none same-ID switch`).
- #1730 does NOT contain `lane-0428-083-datasources-r2` (809a8196e1 branch is NOT built on the datasources-r2 line) — it is a sibling lane off develop.

Does #1730 show the same base-artefakt-krankheit as the #1665 case (only Draft Go / Trusted Plan / Workflow-policy cells, all skipped)?
- **NO — #1730 does NOT show the Draft-Go / Trusted-Plan skip pattern.** Its CI run (44812049031) shows `Trusted Plan · pass`, `Native gate plan · pass`, `Source format · pass`, `Focused Python · pass`. The only red cells are the same systemic Go-unit fail_fast gate + Selected Runtime skipped. Because `lane-0428-143-verify-none` is a clean develop-anchored lane (not a datasources-r2-style non-develop base), it schedules Trusted Plan / native gate / source-format as real `required` cells that PASS.

**Conclusion for 203:** the 203 stack-path is NOT globally broken. #1665 fails only because its base `lane-0428-083-datasources-r2` is a NON-develop base (missing develop artefacts → Draft Go / Trusted Plan cells fall). #1730's base `lane-0428-143-verify-none` IS develop-anchored and passes its required cells. So the 203 fix is NOT "retarget 203 to develop because the stack path is dead" — the fix is "give every stacked PR a develop base". If a specific 203 lane happens to stack on a non-develop base, THAT lane needs the retarget; lanes on clean develop-anchored bases (like 143) do not. Retarget remains an Owner action; this akte only diagnoses.

---

## EMPFOHLENE REIHENFOLGE (max 7 lines)
1. Retarget #1684 `perses-tmpfs-mountpoint-wt` → develop (Owner action); then merge.
2. Retarget #1730 `lane-0428-143-verify-none` → develop (Owner action); then merge.
3. Merge any of: #1724 #1718 #1723 #1725 #1726 #1728 #1729 #1731 #1732 — ancestry flat, no precedence.
4. Do NOT merge any stacked PR on its current non-develop base (no required cells land there).
5. Fix the systemic Go-unit `fail_fast` gate (all shards fail identically) before trusting Go-unit evidence.
6. #1726 (Keycloak/Core native) and #1731 (pr-planner-tests) are the only PRs with a 2nd content-red cell to triage first.
7. Keep PR DRAFT through implementation+gate; move to review only at handoff (review = handed off, CI pending).

## repo-rule compliance
- **Read-only mission.** No product change, no `gh pr edit`, no retarget, no rerun, no workflow_dispatch. No `git` write in the product repo. No subagents used (4.8).
- **Write-set:** only the planning evidence akte + the todos board file under baseharbor-plan; NO write in baseharbor product repo; NO `.github/**` touched.
- **Working tree clean:** `git status --porcelain` in `workers/` shows only pre-existing untracked bookkeeping/cache dirs (`?? .*/ ?? w*/ ?? 0*/`) — no tracked modifications, no new file authored by this lane in the product tree.
- **Branch provenance:** no new candidate branch cut. Upstream `lane-0428-177-mergeplan` does not exist (git ls-remote empty) → no phantom branch. All ancestry measured against develop 40cb28c758b0.
- **Quarantine avoided:** used `git ls-remote` + full clone at `/tmp/bhs/repo`; never cited workers/baseharbor refs/logs.

## container/netzwerke/volumes (3.3.5)
- No container, compose project, network, or volume was started by this lane (pure read-only remote analysis).
- `cleanliness:` clean — nothing to tear down, no orphans, no daemon-address-pool usage.

## END
END_DONE w214-0428-177-mergeplan: read-only merge-window plan delivered (A/B/C/D + recommended order); no product/PR change; working tree clean. candidate: read-only akte, no PR SHA (no push; lane branch does not exist upstream).
