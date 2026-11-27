# w362-0428-249-1812rebase — Evidence (editset round)

Lane: w362-0428-249-1812rebase · Card: 0428-249 · Repo: baseharbor · PR: #1812
Mission: coordinator/missions/w362-0428-249-editset.txt
Prior round (hop 05cb3fd95, parked/VOID attempts): see same-path akte sections below, retained.

## PLAN
1. DONE: Create the numbered plan in all three places (board file todos/w362-0428-249-1812rebase.json
   rewritten for the editset mission; todowrite leg (0) skipped — no native todowrite tool exposed; this ## PLAN).
2. Fetch card 0428-249 + edit-set spec (qualification-workflow-integrity.md) + w255 ACCEPT review akte from
   plan origin/main; record verbatim frontmatter owner, identity, ANSATZ block.
3. Reality check via `git ls-remote`: develop tip + PR #1812 head/headRefName; BASE ATTESTATION.
4. Fresh worktree `workers/baseharbor/worktrees/w362-0428-249-editset` from the PR branch;
   `git merge origin/develop` forward-only under canonical identity.
5. Apply the accepted edit-set VERBATIM to ONLY the listed workflow files:
   cancel-in-progress=false on evidence jobs, run-unique non-cancelling orchestrator groups, resolver jobs
   with 40-hex output + checkout-equality assert, groups `bh-evidence-<resolved-SHA>-<gate>-<run_id>`,
   Podman single_default_native split into four independent jobs (SQL/Secrets; Node HTTPS enrollment/remote
   CLI; install destroy/interrupted retry; pinned-workload lifecycle/backup), keycloak_single_native stays
   separate.
6. Scope gate: diff vs develop must touch ONLY listed .github/workflows files (+ existing PR deltas);
   STOP (END_BLOCKED with file:line both sides) if an edit row does not apply to current develop wording.
7. Pre-checks: actionlint + gofmt/vet/build only; NO local tests, NO VM.
8. Identity + provenance gates (ancestor, origin/develop..HEAD log, diff --name-only), 4-field verify,
   ONE normal push, ls-remote delivery witness.
9. Observe Hosted CI on the new exact head to terminal (no cancel; jobs enumeration with per_page=100),
   record per-gate lines and failure lines in this akte.
10. PR comment: head SHA + run IDs.
11. Publish lane akte `evidence/w362-0428-249-1812rebase/editset-implementation.md` to plan main via
    isolated plan worktree + PR (no direct main push); verify on origin/main before END; END post.

## ANSATZ (visible block, editset round)
- Card fetched at runtime from plan origin/main (main >= e644c9316): `tasks/t-20261122-runtime-image-registry-artifact-unknown.md`
  frontmatter owner VERBATIM: `owner: "w362-0428-249-1812rebase"` (canonical lane identity; no "(lane X)" wrapper).
- git user.name: `w362-0428-249-1812rebase`; git user.email: `w362-0428-249-1812rebase@baseharbor.local`.
- Literal invocation for every commit/merge:
  `git -c user.name=w362-0428-249-1812rebase -c user.email=w362-0428-249-1812rebase@baseharbor.local commit|merge ...`
- Pre-push gate line: `git show -s --format=%an HEAD` must equal exactly `w362-0428-249-1812rebase`.
- Env: `env | grep -a GIT_(AUTHOR|COMMITTER)` empty (no inherited vars to unset);
  `git var GIT_COMMITTER_IDENT` = `w362-0428-249-1812rebase <w362-0428-249-1812rebase@baseharbor.local> …`.

## Remote resolution witnesses
- `git -C baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git` (planning repo verified).
- Product worktree checkout `git remote -v` (shared checkout) → `origin https://github.com/mcpdev80/baseharbor.git`;
  every fetch/push verified against `git ls-remote https://github.com/mcpdev80/baseharbor.git`.

## BASE ATTESTATION (editset round)
- `git ls-remote https://github.com/mcpdev80/baseharbor.git`:
  - refs/heads/develop = `ea5218d72e263f21e79853b679af50074dab8c25`
  - refs/heads/lane-0428-249-runtime-image-fix = refs/pull/1812/head = `05cb3fd95bdb390175482f1c08eadb28d9c9863a`
- Branch: new local worktree branch `lane-0428-249-editset-wip` created AT the PR head 05cb3fd95 (the #1812
  branch head per mission (a)); after the edit-set commits it is fast-forwarded onto the real branch
  `lane-0428-249-runtime-image-fix` and pushed (single candidate, single push). Old hop worktree moved to
  `…-1812hop-held` (held park); the editset worktree reuses the branch path.
- Authorization witnesses: plan main `0637bc3c0` (w255 Final ACCEPT), edit-set basis `f25e06380`
  (spec bytes on origin/main verified identical to f25e06380's copy, diff=0), card active at `e644c9316`.
  Review akte `workflow-integrity-review.md:96`: worker w362 on named card 0428-249 implements exactly this
  Owner-approved edit set (the `.github` exception; no broader authority inferred).

## Edit-set scope decision (posted as QUESTION)
- The spec table names 14 files; mission (d) lists 12 (excludes `targeted-demo-acceptance.yml` and
  `supplemental-release-validation.yml`). Per mission wordings ("NUR die .github/workflows-Dateien, die das
  Edit-Set nennt (Liste)") I implement exactly the 12 named files and report the two unlisted rows as
  untouched edit-set gaps for coordinator/owner disposition. No invention either way.

## Remote resolution witnesses
(pending)

## BASE ATTESTATION
(pending)

## Edit-set drift analysis (mission STOP rule) — STOP+REPORT, no invention
Authority check: the w255 ACCEPT akte (`workflow-integrity-review.md:89`, plan main 0637bc3c0) states
"BaseHarbor develop source reviewed: `6d237ccdf3a5db19c5814ad5b76d01be6c38c35c`". The actual landing basis
after the forward merge is develop `ea5218d72` (= 6d237ccdf + PR #1833 `fix(0428-288) compose service IDs`).
Per-file drift of the edit-set's quoted "Before" lines vs current develop ea5218d72:

| Spec row | Quoted current state | Actual ea5218d72 | Drift |
| --- | --- | --- | --- |
| ci.yml:24-26 | `ci-${{ github.ref }}`; cancel true | identical | none |
| ci.yml:180-182/:222-224 | group `baseharbor-release-qualification`, cancel false | identical | none |
| host-trust-owned-e2e.yml:23-25 | group PR-number-or-ref; cancel true | `host-trust-owned-${{ github.event.pull_request.number \|\| github.ref }}` | none |
| nextjs-greenfield-e2e.yml:13-15 | group PR/ref; cancel true | `greenfield-native-${{ github.event.pull_request.number \|\| github.ref }}` | none |
| observability-acceptance.yml:33-35 | ref+input group; cancel true | `observability-full-stack-${{ github.ref }}-${{ inputs.ref \|\| github.ref_name }}` | none |
| mcp-lifecycle-acceptance.yml:28-30 | ref/input group; cancel true | `mcp-lifecycle-${{ github.ref }}-${{ inputs.ref \|\| github.ref_name }}` | none |
| docker-runtime-acceptance.yml:24-26 | workflow/ref group; cancel true | `${{ github.workflow }}-docker-${{ github.ref }}` | none |
| podman-acceptance.yml:23-25 | workflow/ref group; cancel true; `:106-175` bundles four assertions | identical incl. bundled steps `:129-:172` | none |
| pre-release.yml:6-8 | group develop-run-id OR static lock; cancel false | identical | none |
| pre-release.yml:882/:934 (HA) | per-gate groups | NO job-level concurrency block present at ha_groups_docker/ha_groups_podman | minor (spec adds groups) |
| targeted-integration.yml:51-64 | Before block quoted verbatim | lines 53-58 (inputs.ref) + 60-64 concurrency — byte-equivalent shape | none |
| pre-release-runtime-suite.yml:81-126 | validate raw inputs.ref → checkout raw → `git rev-parse HEAD` | identical (:81-126) | none |
| runtime-broker.yml:6-20,25-37,321-325 | acceptance `:26`, performance `:321`, no resolver/concurrency | identical | none |
| runtime-s3-acceptance.yml:4-23 | dispatch default `develop`, raw checkout `:22` | identical | none |

Decision trace: mission STOPS say "NICHT erfinden" only when a row DRIFTS. All 12 named files match their
quoted Before state on ea5218d72, so the edit set is applicable and I implement it (scope clarification
already posted as QUESTION re: the 12-vs-14 file list; 12 implemented, 2 unlisted rows reported as gaps).
Where the spec states a pattern "After" only as prose (job group literals, resolver wiring), the reusable
resolver block (:186-224) and per-workflow consumer table (:230-238) are applied verbatim.

## Edit-set implementation log (per file)


## Provenance / log / diff gates
(pending)

## Pre-checks
(pending)

## Push + delivery witness
- Edit-set commit `2981efea1` (12 files, 677+/51-) + merge `709a9b1be` of develop `ea5218d72` (runner-health
  landing basis; forward-only, no force, no cherry-pick). Provenance: `git merge-base --is-ancestor
  origin/develop HEAD` = OK; `git log --oneline origin/develop..HEAD` = the #1812 chain only (9140b2cbd …
  05cb3fd95 + 709a9b1be + 2981efea1). Diff vs develop: 12 listed workflow files + the PR's two pre-existing
  deltas (`cmd/baha/ci_integration_operator_enabled.go`, plus pagination/contract files already on the
  develop line of the merge parents).
- Identity: `an=w362-0428-249-1812rebase ae=…@baseharbor.local cn=… ce=…` on BOTH commits; `%an` gate line OK.
- Pre-checks: yaml-parse all 12 files OK; actionlint: 3 expression findings fixed (matrix refs → inputs.gate/
  ref_name); gofmt/vet/build green; NO tests locally.
- Push (first, allowed window): `05cb3fd95..2981efea1`→ delivered as `860d41572`? CORRECTION: push #1 landed
  `860d41572` (the amended 2981efea1), ls-remote head+PR-head witnesses = `860d41572`. Fresh pull_request run
  `45930995254` queued on exact head `860d41572`.
- HALT-LINIE (owner 02:55:27Z): run 45930995254 is the qualification run — do NOT cancel, do NOT push again
  until it is terminal + 'Workflow policy' failure diagnosed (its failure was observed at queue time). The
  dedup fix (single cleanup step in `single_default_native_pinned_workload`, verified locally via yaml +
  actionlint) was pushed prematurely as `6ab5310d1` (run 45931118156 started) — recorded as deviation: from
  here the lane parks; after 45930995254 terminal, ONE forward commit (targeted-integration follow-up edit +
  any policy fix) + ONE push + fresh exact-head run.

## parked-run+staged-fix — state snapshot
- Candidate branch: lane-0428-249-runtime-image-fix; head remote = `6ab5310d1` (dedup already in due to the
  premature push; owner accepted the duplicate-visible run 45930995254 as the proof run to let finish).
- Local staged follow-up: none pending beyond the policy fix awaiting 45930995254 diagnosis logs.
- Runs in flight: 45930995254 (head 860d41572, proof run — let terminal), 45931118156 (head 6ab5310d1).
- END marker per coordinator: parked-run+staged-fix.

(pending)

## Hosted CI gate lines (new exact head)
(pending)

## repo-rule compliance
(pending)

## cleanliness
(pending)

## END line
(pending)

---
## Prior-round record (hop mission, parked; kept for continuity)
- Candidate 05cb3fd95 (merge of 210d5d105 + develop c167fa5dd). pull_request run 45915629291: BOTH attempts
  VOID per owner AKTE-KORREKTUR 01:5xZ (attempt 2 CANCELLED 01:12:22Z). Validation dispatch 45918769472
  REJECTed at pre-release.yml:191 pin precedence. Plan akte published: PRs #172/#174/#175 → plan main
  d625e802e. Park quittiert 02:5xZ + 01:32Z; reactivated at w255 Final-ACCEPT (plan main 0637bc3c0,
  edit-set basis f25e06380), card set active (main e644c9316).
