# w385-0428-078-pr1855step — Naechster Schritt fuer PR #1855 (disjoint pre-work Folgeauftrag)

LANE w385-0428-078-pr1650pre. KARTE 0428-078. REPO baseharbor. MISSION 2026-11-27.
ART: NAechster konkreter Schritt, wieder read-only + Akte als DATEI im eigenen Arbeitsbaum.
PLAN-REPO FREEZE (2026-11-27T07:34:31Z, Coordinator-Hinweis): KEIN push nach baseharbor-plan, KEIN PR, KEIN plan.py claim/render.

## Git identity (visible ansatz block)

- Card frontmatter owner (verbatim): `(lane w385-0428-078-pr1650pre)` — full owner value `w385-0428-078-pr1650pre`.
- Git user.name / user.email: `w385-0428-078-pr1650pre` / `w385-0428-078-pr1650pre@baseharbor.local`.
- Commit invocation: `git -c user.name=w385-0428-078-pr1650pre -c user.email=w385-0428-078-pr1650pre@baseharbor.local ...`.
- Pre-push gate line: `git show -s --format=%an HEAD` must equal `w385-0428-078-pr1650pre` exactly.
- No commit was created in this lane (mission is read-only findings + akte as FILE in own worktree; no product PR opened).

## Planning-repo remote attestation (FIRST git action)

- `git -C baseharbor-plan remote -v`: `baseharbor https://github.com/mcpdev80/baseharbor.git (fetch)` (product, blobless) and `origin https://github.com/mcpdev80/baseharbor-plan.git` (planning repo). Confirmed planning repo is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY.
- Write freeze active: evidence delivered as FILE in own worktree, NOT pushed to baseharbor-plan.

## Base attestation

- #1855 remote branch `w279-0428-078-pr1650-reissue`: `d18e4b367940ad5ee36862dbda1eea2d7a605db0` (`git ls-remote baseharbor refs/heads/w279-0428-078-pr1650-reissue`).
- develop base head: `ea5218d72e263f21e79853b679af50074dab8c25` (`git ls-remote baseharbor refs/heads/develop`).

---

## (a) PR #1855 witnesses (gh pr view, mcpdev80/baseharbor)

- headRefName `w279-0428-078-pr1650-reissue`, headRefOid `d18e4b367940ad5ee36862dbda1eea2d7a605db0`, baseRefName `develop`, state `OPEN`, mergeable `MERGEABLE`.
- Files changed by #1855 vs develop (32 files), incl. product + test + contracts + docs + `scripts/pr-gate-coverage.json`:
  `cmd/baha/app_identity_dashboard_status_test.go`, `cmd/baha/app_perses_cli_test.go`, `cmd/baha/app_status_result.go`, `internal/identityprovider/keycloak_realization.go`, `internal/identityprovider/keycloak_signal_attribution_test.go`, `internal/metrics/identity_dashboard_witness.go`, `internal/metrics/identity_dashboard_witness_test.go`, `internal/metrics/perses_dashboards.go`, `internal/metrics/testdata/perses-dashboards/keycloak-identity.json`, `internal/runtime/project_names.go`, `scripts/pr-gate-coverage.json`, plus pagination/contracts/docs.

---

## (b) Ancestry vs develop

- merge-base(#1855 head, develop) = `c167fa5dd323ae0746385caa2bdb8364ec7ad03f`.
- `git rev-list --count d18e4b36..ea5218d7` (commits of head not on develop) = 6.
- `git rev-list --count ea5218d7..d18e4b36` (develop commits NOT reachable from head, i.e. missing) = 18.
- `git merge-base --is-ancestor ea5218d7 d18e4b36` = **false** => develop is NOT an ancestor of the current head.
- HOP IS NEEDED: the current head `d18e4b36` is 18 develop-commits behind `ea5218d7`. A forward-merge `git merge origin/develop` is required before #1855 can qualify cleanly on a current develop base. The head's own log shows prior absorb-merges (`absorb(0428-078): forward-merge origin/develop ...`) but they predate the latest 18 develop commits.
- The 6 candidate-specific commits are the reissue core (43326cf57 reissue, 7d805dc6b content correction, 123666c82 gate binding, 572d64891 catalog-row removal) plus the Keycloak attribution commits (d5545573a, 879655f07, 18ccd8ea8, f13d37d4c, 77bd785cb) and the trailing new-merge.

---

## (c) Gate posture (gh pr checks 1855 + gh run list on exact head)

Single GitHub Actions run on the exact head: **run 45911769054**, event `pull_request`, head_sha `d18e4b367940ad5ee36862dbda1eea2d7a605db0` (confirmed EXACT-HEAD MATCH via run API). All three failing jobs belong to this ONE run_id.

FAILURES (all in run 45911769054, exact head d18e4b36):

1. Job `PR · Go unit · packages` (job 140221639232) — failure.
   - Failing test: `TestKeycloakSignalRegistrationTargetProductionAttribution`
     (`internal/identityprovider/keycloak_signal_attribution_test.go:74`).
   - Exact failing log line: `keycloak_signal_attribution_test.go:74: attribution root = "docker-dev", want the producer's state root "/tmp/TestKeycloakSignalRegistrationTargetProductionAttribution3197917589/001/targets/docker-dev"`
   - Package result line: `FAIL github.com/mcpdev80/baseharbor/internal/identityprovider 9.797s`
2. Job `PR · Validation · identity-provider-package-tests` (job 140221639553) — failure (same test, same package `internal/identityprovider`, run 45911769054).
3. Job `PR Selected Checks` (job 140228648981) — failure. Run-level gate `Require complete selected Go shard coverage`: `UNIT_SCOPE: full`, `UNIT_RESULT: failure` => "REJECT: Go test selection missing or invalid".

PASSING (run 45911769054, same exact head) — key ones: `Trusted Plan` pass, `Source format` pass, `Go vet` pass, `go-build` pass, `Focused Python` pass, `Candidate-added checks (advisory)` pass, `Demo Pin` pass, `Exact Candidate` pass, `Selected Runtime (atomic/docker/identity, docker, identity)` pass (5m38s), `Selected Runtime (atomic/docker/data-capabilities)` pass, podman data-capabilities/observability pass, `Go unit · cli-0..3` pass, `Go unit · owner` pass, `Selected Runtime (atomic/podman/identity)` pass.

ERROR-CLASS CLASSIFICATION (per the three classes):

- **(i) Catalog rows / #136 (trusted-plan):** NOT the cause. `Trusted Plan` passes on run 45911769054; the Keycloak attribution commit `d5545573a` binds `internal/runtime/project_names.go` and `keycloak_realization.go` to the data-capabilities gate. No catalog row defect visible.
- **(ii) Pin / #183 (Demo Pin):** NOT the cause. `Demo Pin` passes on run 45911769054. No demo-pin defect.
- **(iii) Echter Produktfehler (real product/behavior defect):** THIS is the cause. `TestKeycloakSignalRegistrationTargetProductionAttribution` fails because the production Keycloak signal registration attributes the metrics record to the bare endpoint `"docker-dev"` instead of the producer's canonical `runtime://` Target state root. The candidate's `keycloak_realization.go` (attribution commit) does not yet bind the producer-side attribution to the resolved Target state root — a genuine behavior bug in the candidate, not a catalog/pin/infra issue.

---

## (d) Rechenweg der Reihenfolge (qualification math)

Prerequisite for #1855 to qualify FIRST (ahead of #1650, #1818):

1. **Hop needed.** Absorb the 18 missing develop commits: `git merge origin/develop` on the #1855 branch (transport + qualification merge). The head is 18 commits behind develop; current-base ancestry is otherwise unproven.
2. **Fix the real defect.** `TestKeycloakSignalRegistrationTargetProductionAttribution` fails → the Keycloak attribution must bind to the producer's resolved Target state root (fix `internal/identityprovider/keycloak_realization.go` + re-run the golden/regression). The failing test is the candidate's own new test (file added by #1855, 136 insertions), so the fix lives in THIS PR's product write-set — no Owner-scope change required.
3. **Wire the gate.** Per the gate rule the new/changed tests must be reachable by a real CI check in this same PR: the data-capabilities native gate already covers `internal/identityprovider/*` (run 45911769054 `Selected Runtime (atomic/docker/identity)` + podman data-capabilities pass). Confirm `keycloak_signal_attribution_test.go` is picked by that group; if the group selection needs a change under `.github/**`, report file:line to the Coordinator (Owner scope) — do NOT edit.
4. **Two distinct run-IDs on the EXACT head.** A qualified run is a distinct run_id on `d18e4b367940ad5ee36862dbda1eea2d7a605db0` with the required jobs actually executed (SKIPPED/queued is NOT a pass). One run is not enough; a second is obtained by close+reopen (authorized exact-head trigger): `gh pr close --comment 'second exact-head hosted run trigger (coordinator-authorized)' && gh pr reopen` → new run_id on the same head. A rerun raises run_attempt on the SAME id and is VOID as pair evidence.
5. **Order 1855 -> 1650 -> 1818.** #1855 is the superset (byte-identical Perses core to #1650 + Keycloak). Once #1855 qualifies on current develop with a full green required set + a second exact-head run_id, #1650 shares the identical core (qualify once via #1855, or close #1650 superseded-after-#1855 per the two-run pair rule — this lane does not close it). #1818 is the divergent hop branch (no develop ancestor) → hop onto develop first, lowest priority.

---

## (e) Akte (4-Feld w385-0428-078-pr1650pre)

- 4-Feld lane: w385-0428-078-pr1650pre.
- Delivery: PLAN-REPO FREEZE active — akte delivered as FILE in own worktree, NOT pushed to baseharbor-plan (Coordinator stages under coordinator/evidence-staging/).
- Absolute path: `/home/marcel/dev/baseharbor-ecosystem/workers/worktrees/w385-0428-078-pr1650pre/evidence/w385-0428-078-pr1855step/akte.md`
- sha256: (recorded by sha256sum at write time).

## Cleanliness

- Read-only lane: no docker/podman containers started. `docker ps -a` witness: no w385 containers (no compose project to bring down).
- Product worktree `workers/worktrees/w385-0428-078-pr1650pre` detached at `37c4d847`, clean.

## END

`END_DONE w385-0428-078-pr1855step: #1855 witness OPEN on develop @ d18e4b36; hop NEEDED (head 18 develop-commits behind ea5218d7, merge-base c167fa5dd); gate run 45911769054 exact-head: 3 failures ALL in one run (Go unit packages job 140221639232 + Validation identity-provider job 140221639553 + PR Selected Checks job 140228648981) caused by REAL product defect TestKeycloakSignalRegistrationTargetProductionAttribution keycloak_signal_attribution_test.go:74 "attribution root = docker-dev" want producer state root (NOT catalog/#136, NOT demo-pin/#183); Trusted Plan/format/vet/go-build/runtime-identity+data-capabilities all PASS; qualification order 1855->1650->1818 requires (1) absorb 18 develop commits via merge origin/develop, (2) fix producer-side Keycloak attribution to resolved Target root in THIS PR write-set, (3) confirm data-capabilities gate picks up the new test, (4) two distinct run-IDs on d18e4b36 via close+reopen; akte delivered as FILE in own worktree (plan freeze)`
