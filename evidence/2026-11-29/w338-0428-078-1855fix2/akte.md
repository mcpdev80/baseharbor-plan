# w338-0428-078-1855fix2 — PR #1855 correction round 3 (re-laned from w327 per NO-RESPONSE rotation)

Card: 0428-078 (t-20261114-r28-perses-dashboard-identity), PR mcpdev80/baseharbor#1855,
branch `w279-0428-078-pr1650-reissue` (verified via `gh pr view 1855 --json headRefName`).
Correction round on w267 CHANGES review comment 7196719214 against head
879655f07f5fb28aba4e37ce33fdb2a8e0cce046 (run 45845829221 SUCCESS, not acceptance).

## PLAN

1. Resolve remotes (github.com/mcpdev80 only) and verify the real baseharbor-plan path.
2. Fetch the w267 review comment 7196719214 in full; enumerate every named item.
3. Verify exact PR head branch + SHA; record base attestation.
4. Claim card 0428-078 onto plan main with note 're-laned from w327 per NO-RESPONSE rotation' (done: plan PR #145, squash commit 3d31d1a4a).
5. Fresh clone of the PR branch at workers/w338-0428-078-1855fix2-wt; cleanliness ps witnesses.
6. Triage/reproduce each review item; implement fixes in ONE ordinary commit under the canonical lane identity.
7. Non-test pre-checks only (gofmt/vet/build); ensure every new/changed test has a real CI route in the same PR.
8. Ancestry, diff --name-only, log-only-own-commits, %an gate; push (no force); ls-remote delivery proof.
9. Watch my own Hosted CI pull_request run on the exact new head to terminal.
10. Publish this akte to plan origin/main (branch + plan PR + admin squash), then END post.

## Visible Ansatz block (owner-required, before first commit)

Card frontmatter owner VERBATIM, fetched from origin/main at claim time
(tasks/t-20261114-r28-perses-dashboard-identity.md after my claim commit 3d31d1a4a):

    owner: w338-0428-078-1855fix2 (e1f6c79e-8ce1-4d2d-b55f-7e3a2658c23d) — re-laned from w327 per NO-RESPONSE rotation

Canonical lane identity string inside '(lane X)': not present (no `(lane X)` wrapper); the
full owner value is therefore admitted as `w338-0428-078-1855fix2` — the card's canonical
session name, matching my registered session name exactly (codeman agent list witness:
name w338-0428-078-1855fix2, id e1f6c79e-8ce1-4d2d-b55f-7e3a2658c23d).

Identity I will use in every worktree (cleared of any template residue, repo-local):

    git var GIT_AUTHOR_IDENT    -> w338-0428-078-1855fix2 <w338-0428-078-1855fix2@baseharbor.local> ...
    git var GIT_COMMITTER_IDENT -> w338-0428-078-1855fix2 <w338-0428-078-1855fix2@baseharbor.local> ...
    git config --show-origin --get user.name  -> file:.git/config  w338-0428-078-1855fix2
    git config --show-origin --get user.email -> file:.git/config  w338-0428-078-1855fix2@baseharbor.local

Literal commit invocation (product clone AND plan worktree):

    git -c user.name=w338-0428-078-1855fix2 -c user.email=w338-0428-078-1855fix2@baseharbor.local commit ...

Pre-push gate lines (before EVERY push):

    git show -s --format=%an HEAD      (must print exactly: w338-0428-078-1855fix2)
    git log --format='%h an=%an cn=%cn' -1

## Remote resolution (FIRST git action, per remote-guard rule)

Planning repo verification:

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
    baseharbor	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
    baseharbor	https://github.com/mcpdev80/baseharbor.git (push)
    origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
    upstream2	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    upstream2	https://github.com/mcpdev80/baseharbor-plan.git (push)

Shared product checkout /home/marcel/dev/baseharbor-ecosystem/baseharbor was NOT used for
transport; I worked in a fresh clone whose only remote is
https://github.com/mcpdev80/baseharbor.git (origin). No local-path remote was involved.

## Base attestation (branch provenance)

- PR #1855 head branch (gh pr view --json headRefName,headRefOid): `w279-0428-078-pr1650-reissue`
  @ 879655f07f5fb28aba4e37ce33fdb2a8e0cce046.
- Base branch live head, measured: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  -> 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 refs/heads/develop
- I did NOT cut a new branch: I checked out the existing PR head branch (fresh clone,
  --branch w279-0428-078-pr1650-reissue) at exactly 879655f07f5fb28aba4e37ce33fdb2a8e0cce046 and
  commit forward (one ordinary commit; mission forbids branch switches/base merges).
- Ancestor proof of the base against the head I built on:
  `git merge-base --is-ancestor origin/develop HEAD` -> OK (develop 5a37ddbd is an ancestor of
  879655f0, re-measured after the fetch in my clone).

## Review triage (w267 CHANGES 7196719214, all named items)

Item 1 — production record shape never carries the runtime:// attribution the witness now requires.
  Reproduced exactly: internal/identityprovider/keycloak_realization.go registers
  ProviderSignalRuntime.Target as the literal "keycloak:9000"; RegisterProviderSignals copies
  runtimeSignal.Target verbatim into SignalSource.Target (internal/observability/
  provider_registration.go:77-79). ParseRuntimeTarget rejects any value without the runtime://
  prefix (internal/observability/registry.go:176-187), while the witness REQUIRED a successful
  parse (identity_dashboard_witness.go:328-331 at 879655f0) — so the guard failed closed on ALL
  actual production records, including ordinary Target names.
  Fix: the producer now registers through the registry's own canonical grammar
  observability.RuntimeTarget(files.Project, "keycloak@<target>:9000") (keycloakSignalTargetRoot
  + keycloakSignalAttributedService), where the attribution token is the state-root DIRECTORY
  name = the exact validated Target name (injective; deployment.TargetStateRoot keys the
  directory on it). The witness's ID expectation changed from the CALLER manifest name to the
  PRODUCTION project grammar (shared: runtime.TargetInstallationProject(target) =
  SharedProjectName(target-core) — the identityprovider keycloakStateIdentity grammar;
  application: ApplicationProjectName(target, <app>-identity, env)), and the shared-placement
  listing now reads the registry directly (observability.ListAll) because the central List()
  environment filter would otherwise drop every shared production record for non-"prod"
  consumers (installation pins environment "prod", keycloak_files.go:134). The application-
  placement path KEEPS the production List() seam (environment isolation of 0428-121 unchanged).

Item 2 — the dotted collision test used a record shape production does not emit.
  Reproduced exactly: the helper manufactured RuntimeTarget(keycloakRecordTargetAttribution(...))
  (identity_dashboard_witness_test.go:41,55-61 at 879655f0) with the synthetic raw-name project
  bh-<root name>-core-shared; production computes the shared project through
  SharedProjectName(namespace + "-core") (keycloak_files.go:426-430) whose projectToken maps
  dots to hyphens (internal/runtime/project_names.go:41-48), so production COLLAPSES a.b and
  a-b to one project, while keycloakInstallationProject fabricated distinct raw-name strings
  (identity_dashboard_witness.go:362-381). The collision test passed only with the test-created
  attribution.
  Fix: every witness test seed now registers THROUGH THE PRODUCTION SEAM
  observability.RegisterProviderSignals with the realization's registration struct (ID, Class,
  Scope, SharingBoundary "core", OwnerApplication = caller app name, descriptor, endpoint) — no
  synthetic grammar remains (keycloakRecordTargetAttribution / keycloakInstallationProject are
  deleted; the new runtime twin is runtime.TargetInstallationProject). The injective separation
  was MOVED OUT of the lossy project position into the service position's state-root token, so
  the dotted pair is now proven exactly as production writes it: one shared project
  (bh-a-b-core-shared for BOTH names — asserted as the premise), distinct attributions
  (keycloak@a.b:9000 vs keycloak@a-b:9000).

Required-correction wording — "preserve a collision-free, validated Target identity in the
actual producer-to-registry record (or another production-owned attribution field) without
relying on the normalized project/network": DONE — the canonical runtime Target's service
component is the production-owned attribution field; the normalized project/network are no
longer the separation mechanism (they stay as structural/consistency guards).
"have the dotted collision regression consume the real production registration shape, proving
the foreign Target fails closed and the matching Target remains eligible": DONE —
TestIdentityDashboardWitnessTwoValidDottedTargetsIsolation + the producer-side
TestKeycloakSignalRegistrationDottedCollisionProductionShape.
"Keep the state-root pin, real network check, and existing consent/auth behavior unchanged":
DONE — the TargetStateRoot pin at keycloakMetricSignals entry and the Network-equality guard are
retained verbatim; no consent/auth surface (cmd/baha, serviceaccess, operatorauth) is touched;
this is a read-side attribution check plus one producer registration string.

## Mechanism (decision + justification)

Producer (internal/identityprovider/keycloak_realization.go) + witness
(internal/metrics/identity_dashboard_witness.go):
- Registration Target: observability.RuntimeTarget(r.files.Project,
  "keycloak@<base(r.dataDir)>:9000"). dataDir is resolved.TargetStateRoot at every production
  call site (cmd/baha/app_identity.go:64/:236); keycloakSignalTargetRoot fail-closes when the
  directory name is not a validated Target name.
- The service position is grammar-legal: ParseRuntimeTarget rejects services containing "/",
  so the token is the directory NAME (path-free, URI-safe), validated by
  deployment.ValidateTargetName on both sides.
- Witness attribution: parse runtime:// grammar → service must match keycloak@<name>:9000 →
  <name> must validate AND equal the witnessed root's directory name (= targetName, already
  pinned by the state-root pin) → project must be a production installation project of THAT
  target (shared grammar exact, or application grammar's target token position) → else fail
  closed. Pre-correction plain "keycloak:9000" records and stamped-legacy
  runtime://<project>/keycloak (port stripped, migration.go) resolve NO attribution and fail
  closed; the registry's own 0428-168 migration re-books legacy records under the canonical
  ID grammar, and the witness's ID/project axes accept the production grammars only.
- Network guard KEPT: source.Network == the producer's consumer network for the witnessed
  Target (unchanged). The attribution name and the network's raw target segment are written by
  the SAME producer from the SAME resolved Target, so real production records satisfy both
  axes; a fabricated root+network pair fails closed (HOLD 7192567805 semantics preserved).
- Registration-ID expectation KEPT PRODUCTION-correct: shared placement =
  "keycloak:" + runtime.TargetInstallationProject(targetName); application placement =
  "keycloak:" + runtime.ApplicationProjectName(targetName, <app>-identity, env) — the exact
  grammars keycloakStateIdentity writes (files.Project feeds both ID and Target, so they can
  never disagree).
Why not the alternatives:
- A new SignalSource/ProviderSignalRuntime registry field: shared observability schema used by
  every provider and persisted format; the registry's OWN canonical runtime:// grammar is the
  production-owned attribution field the review named — smaller and consistent with every
  existing provider registration (logs/application sources).
- Keeping the separation in the project position (raw directory names inside the project):
  NOT what production writes (item 2 exactly); rejected.
- Deriving attribution from the consumer network: the network maps dots to hyphens too
  (identity_network.go:40) — lossy, rejected by the review.
- Injective-at-any-cost that ignores the production project would reject ordinary production
  records (item 1); this design accepts exactly what production writes and fails closed on
  everything else.

## Test binding (AGENTS: test -> check -> trigger -> execution)

- All new/changed tests are ordinary Go package tests in internal/metrics,
  internal/identityprovider and internal/runtime: package-discovered through
  `go list ./...` + `go test` by the baseharbor PR CI go-unit jobs and executed by the PR's
  Selected Runtime docker/podman · observability/data-capabilities gates. scripts/pr-gate-
  coverage.json already binds these packages (already in the PR's diff set); no .github/**
  change exists in the PR's file set (measured: `gh pr view 1855 --json files` lists 11 files,
  none under .github/). Trigger: pull_request on #1855 head.
- Witness regressions: TestIdentityDashboardWitness* (production-seam seeds; no synthetic
  attribution helper remains — keycloakRecordTargetAttribution/keycloakInstallationProject
  deleted).
- Producer regressions: TestKeycloakSignalRegistrationTargetProductionAttribution (the record
  the real registerKeycloakSignals -> RegisterProviderSignals path writes carries the canonical
  runtime:// attribution naming its own state root) and
  TestKeycloakSignalRegistrationDottedCollisionProductionShape (a.b vs a-b: one installation
  project, one network — asserted premise — distinct attributions through the production seam).

## cleanliness

Host: this session's coordinator host ran NO container work (docker/podman tests are Hosted-CI
jobs; no VM smoke is named in this mission).
`docker ps -a` line count before: 0 (measured `docker ps -a --format ... | wc -l`, pid 626183).
After: recorded below at END.

## Candidate transport (identity-gated, forward-only, no force)

Commit 1 (correction): d5545573adbb01829b52dd565b6e3a8cd8920695
  git show -s --format='%h an=%an cn=%cn' HEAD -> d5545573 an=w338-0428-078-1855fix2 cn=w338-0428-078-1855fix2
Commit 2 (gate catalog for the same PR's new source — mission RULES authorize the
catalog entry as the check route; the trusted-planner error message itself names this
exact fix): fe940dc311192e81ea6fd3580d02f313dfe4e849
  git show -s --format='%h an=%an cn=%cn' HEAD -> fe940dc3 an=w338-0428-078-1855fix2 cn=w338-0428-078-1855fix2
git var GIT_AUTHOR_IDENT / GIT_COMMITTER_IDENT (product clone, before commits):
  w338-0428-078-1855fix2 <w338-0428-078-1855fix2@baseharbor.local> 1795713767 +0100 (both)
  git config --show-origin --get user.name  -> file:.git/config w338-0428-078-1855fix2
  git config --show-origin --get user.email -> file:.git/config w338-0428-078-1855fix2@baseharbor.local

Ancestry: git merge-base --is-ancestor origin/develop HEAD -> OK (develop 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74,
fetched via https://github.com/mcpdev80/baseharbor.git).
git log --oneline origin/develop..HEAD -> the branch's own card commits (43326cf5..879655f0 from prior rounds of
this same PR chain) plus d5545573 and fe940dc3; the prior-round commits are the PR's own carried history (base
879655f0 was the PR head at mission start), no foreign candidate is on top.
git diff origin/develop...HEAD --name-only -> 11 files: cmd/baha/app_identity_dashboard_status_test.go,
cmd/baha/app_perses_cli_test.go, cmd/baha/app_status_result.go, internal/identityprovider/keycloak_realization.go,
internal/identityprovider/keycloak_signal_attribution_test.go, internal/metrics/identity_dashboard_witness.go,
internal/metrics/identity_dashboard_witness_test.go, internal/metrics/perses_dashboards.go,
internal/metrics/testdata/perses-dashboards/keycloak-identity.json, internal/runtime/project_names.go,
scripts/pr-gate-coverage.json.

Delivery witness: git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/w279-0428-078-pr1650-reissue
  fe940dc311192e81ea6fd3580d02f313dfe4e849 refs/heads/w279-0428-078-pr1650-reissue

## Hosted CI (self-run duty)

- Run 45867807943 (pull_request, exact head d5545573): terminal. PR · Trusted Plan FAILED —
  "ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared
  runtime gate owner: internal/runtime/project_names.go (id source.internal_runtime_project_names_go):
  add this source with its surfaces to scripts/pr-gate-coverage.json, e.g. {...docker.data.capabilities,
  podman.data.capabilities...}"; PR Selected Checks failed downstream ("UNIT_SCOPE:" empty ->
  "REJECT: Go test selection missing or invalid"). All other executed jobs passed. This is a
  gate-catalog route gap this PR must close itself (GATE RULE), not a product defect.
- Fix commit fe940dc3 (catalog row with the exact pair the planner message prescribes, mirroring
  the witness components' surfaces). New run on fe940dc3: 45868143276 — terminal (see the
  gate-catalog route section: base-catalog admission, not a product defect).

## Gate-catalog route (trusted-plan admission) — coordinator finding

Run 45868143276 (exact head fe940dc3) FAILED "PR · Trusted Plan" with the SAME uncataloged-
source message, although scripts/pr-gate-coverage.json gained the exact row at fe940dc3. Root
cause measured from the run log: the Trusted Plan job's checkout ends at
"HEAD is now at 5a37ddbd feat(0428-352): trusted catalog row so runtime-suite candidates select
Docker/Podman gates (#1859)" — the planner and catalog are read from the TRUSTED BASE tip
(checkout ref: 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74, "Resolve exact immutable PR inputs using
trusted base policy"). Base 5a37ddbd has NO row for internal/runtime/project_names.go (measured:
`git show origin/develop:scripts/pr-gate-coverage.json` -> no project_names row), so the
admission is unsatisfiable from the candidate side for ANY PR touching this file — the same
standing blocker w288 documented for this chain (evidence/w288/0428-078/1855-catalog-baseline-
block-2026-11-26.md; w267-rehearsed run 45848260001 showed the identical failure shape).
Per the mission's STOPS rule (catalog BASE rows = question, never silent scope work) I froze the
candidate chain here: the candidate commits d5545573 + fe940dc3 are pushed and delivered; the
PR-internal catalog row stays (it binds future bases and is harmless now). Required base action
(coordinator): merge my candidate rows into develop's scripts/pr-gate-coverage.json (or apply the
planner's prescribed example row) so Trusted Plan admission passes, then a new exact-head run
qualifies. The candidate-added advisory job on this run also confirmed the row is valid when
read from the candidate side.

Candidate-chain note (mission RULES: exactly one ordinary commit per correction cycle): the
first push (d5545573) was verified as the exact-head run's subject; the single follow-up commit
fe940dc3 was required by the GATE RULE (this same PR must carry the catalog route for its new
source) and discovered by watching MY OWN run per §4.6 — it carries no product content. Both
commits are forward-only on the named branch under the canonical lane identity; the branch
history is unchanged otherwise (no force, no rebase, no cherry-pick, no base merges).

## Commits / runs / handoff

## Final publication witnesses

Evidence delivery (this section is part of the akte's own publication chain): plan PR #148
merged to main at 6a6232abad90215456759ccfdd6e84a056b5e151 after ancestry proof to current
origin/main and green hosted 'Plan · validate' (run 45868914812).
Before this follow-up: `git -C baseharbor-plan ls-tree -r --name-only origin/main | grep
w338-0428-078-1855fix2` -> evidence/2026-11-29/w338-0428-078-1855fix2/akte.md (main @ 6a6232aba).

Candidate final head: fe940dc311192e81ea6fd3580d02f313dfe4e849 (branch
w279-0428-078-pr1650-reissue, ls-remote-verified above).
Own exact-head runs watched to terminal: 45867807943 (d5545573) and 45868143276 (fe940dc3);
both failed ONLY the base-catalog Trusted Plan admission (finding section); PR · Native gate
plan, unit shards and every executed product gate that ran were green; no .github/** or ci.yml
change exists in the PR's file set (measured via gh pr view --json files).

## Item -> fix -> test table (mission END)

| Review item (w267 CHANGES 7196719214) | Fix | Test |
| --- | --- | --- |
| 1. Producer wrote literal "keycloak:9000"; witness-required runtime:// parse fails closed on ALL real production records | keycloak_realization.go registers RuntimeTarget(files.Project, "keycloak@<state-root name>:9000") via keycloakSignalTargetRoot/keycloakSignalAttributedService; witness expects the production ID grammars (runtime.TargetInstallationProject / ApplicationProjectName) and reads the registry directly on the shared placement (List() env filter would drop shared records for non-prod consumers) | TestKeycloakSignalRegistrationTargetProductionAttribution (producer seam); TestIdentityDashboardWitnessPositiveMatchesConcreteTarget through the production RegisterProviderSignals seam |
| 2. Dotted collision test used a synthetic raw-name project production never emits | Attribution moved OUT of the lossy project position into the injective state-root token; synthetic helpers deleted; every seed registers through the production seam | TestIdentityDashboardWitnessTwoValidDottedTargetsIsolation (real shape); TestKeycloakSignalRegistrationDottedCollisionProductionShape (one project+network, distinct attribution); TestIdentityDashboardWitnessRootAttributionResolvers (grammar matrix incl. cross-grammar fail-closed) |
| Required: collision-free validated Target identity in the actual record; state-root pin/network check/consent-auth unchanged | Canonical runtime:// grammar + ValidateTargetName on both sides; pins kept verbatim; no consent/auth surface touched | TestIdentityDashboardWitnessTwoValidTargetsIsolation; TestIdentityDashboardWitnessForeignTargetFailsClosed; TestIdentityDashboardWitnessRequiresTargetStateRoot; TestIdentityDashboardWitnessExternalPlacementFailsClosed |
| New source internal/runtime/project_names.go uncataloged (Trusted Plan base-policy admission) | Candidate catalog row added in fe940dc3; BASE rows are STOP territory per mission -> coordinator finding (file:line: scripts/pr-gate-coverage.json components; base 5a37ddbd lacks the row) | Advisory/plan routes report it; qualification needs the base row (coordinator action), then one clean exact-head run |

## cleanliness

`docker ps -a` (this session's host, pid 626183 zone): before = 0 containers, after = 0
containers. No compose project started; no VM smoke named in this mission; worktrees under
workers/ only; no /var/tmp usage; no .github/** touched.

END_BLOCKED w338-0428-078-1855fix2: corrections pushed (candidate fe940dc3), review items
1+2 fixed through the production attribution grammar with tests; exact-head qualification is
BLOCKED by the trusted-BASE catalog missing the internal/runtime/project_names.go row
(Trusted Plan admission; coordinator action per mission STOPS) — evidence on plan main.


# Correction round 3 (mission w338-0428-078-1855fix3, 2026-11-26)

w267 delivered a pattern ruling as comment 7199844002 on PR #1855 after my round-2 END_BLOCKED.
Key quote (mission): 'The project_names.go row must be delivered through a separate catalog-only
PR under the 0428-359/#136 baseline family, not embedded in #1855.' Review body adds: the row
must carry `runtime_specific: true` (Docker+Podman data.capabilities) and the round-2 embedded
row is not admissible in the product PR; the forward merge of the develop-owned row into #1855
happens AFTER the family row lands (mission fix3 restricts me to: remove embedded row forward-
only + create the family catalog PR + watch runs; NO merges, freeze holds).

## PLAN (round 3)

1. Plan in all three places (board file, this list; coordinator todowrite leg skipped: no native tool);
   verify identity pin sources via git var + config --show-origin (config.worktree pin; bare git config untouched).
2. Fetch w267 ruling comment 7199844002 verbatim; verify PR head fe940dc3 + develop tip via gh/ls-remote.
3. Round-3 akte section with visible Ansatz block written in the plan worktree (this section).
4. Forward-only commit on the #1855 branch removing ONLY the embedded project_names.go catalog row.
5. Pre-push gates; push (no force); ls-remote delivery proof.
6. Family catalog PR off origin/develop tip carrying ONLY the row (runtime_specific: true per ruling);
   Ready, not draft; NO merge.
7. Watch Hosted runs to terminal on BOTH exact heads; record full-40 SHAs + run IDs.
8. Publish akte via branch + plan PR + hosted validate + admin squash (own evidence PR, clarifier).
9. Cleanliness + END line + codeman post.

## Visible Ansatz block (round 3)

Card frontmatter owner VERBATIM (fetched at runtime from origin/main @ 9986e8146,
tasks/t-20261114-r28-perses-dashboard-identity.md):

    owner: w338-0428-078-1855fix2 (e1f6c79e-8ce1-4d2d-b55f-7e3a2658c23d) — re-laned from w327 per NO-RESPONSE rotation

No '(lane X)' wrapper present -> canonical identity string = w338-0428-078-1855fix2 (exact
session registration; codeman agent list witness from round 1: id
e1f6c79e-8ce1-4d2d-b55f-7e3a2658c23d).

Identity pin state (mission: config.worktree pin, bare git config FORBIDDEN):
- product clone workers/w338-0428-078-1855fix2-wt: repo-local .git/config carries the lane pin
  (set in round 1 before the first commit); git var author+committer verified before EVERY commit.
- plan worktree workers/w338-0428-078-1855fix2-plan: config source verified this round as
  file:.../baseharbor-plan/.git/worktrees/w338-0428-078-1855fix2-plan/config.worktree (coordinator
  15:2xZ pin), git var -> w338-0428-078-1855fix2 <w338-0428-078-1855fix2@baseharbor.local>.

Literal commit invocation (both repos):
    git -c user.name=w338-0428-078-1855fix2 -c user.email=w338-0428-078-1855fix2@baseharbor.local commit ...

Pre-push gate lines (before EVERY push):
    git show -s --format=%an HEAD   (must print exactly: w338-0428-078-1855fix2)
    git log --format='%h an=%an cn=%cn' -1

## Reality witnesses (round 3)

- gh pr view 1855 --json headRefOid,state,isDraft -> head fe940dc311192e81ea6fd3580d02f313dfe4e849,
  state OPEN, draft false.
- git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
  refs/heads/w279-0428-078-pr1650-reissue -> develop 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74,
  branch fe940dc311192e81ea6fd3580d02f313dfe4e849.
- git remote -v (product clone, FIRST git action): origin =
  https://github.com/mcpdev80/baseharbor.git (fetch+push) only; no local-path remote.
- Planning repo (git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v):
  origin = https://github.com/mcpdev80/baseharbor-plan.git (verified round 1, re-verified now).
- w267 ruling: comment 7199844002 (2026-11-26T17:55:07Z), fetched full-text via gh api.
- Family reference PR #1865 pattern: catalog-only single-row PR against develop (review body
  confirms it does NOT include project_names.go; the #1864/#1855 rows extend the 0428-359 family).

## Round-3 delivery (rounds executed inside this session; product repo = fresh clone under workers/, plan edits only in the isolated worktree per the shared-checkout rule)

Step 1 — embedded row removed forward-only from the #1855 candidate:
  commit 70c005e8bc48b6186da1095a183905a42ee6c493 ("ci: drop the embedded project_names.go
  catalog row from the candidate"), parent fe940dc311192e81ea6fd3580d02f313dfe4e849 (NOT
  rewritten); git diff --name-only fe940dc3..HEAD = scripts/pr-gate-coverage.json only; the
  scripts catalog at HEAD equals the 879655f0 state byte-for-byte (diff rc 0, empty); the
  0428-078 product/test payload untouched.
  Identity gate before commit: git var GIT_AUTHOR_IDENT / GIT_COMMITTER_IDENT -> both
  w338-0428-078-1855fix2 <w338-0428-078-1855fix2@baseharbor.local> (file:.git/config pin);
  after commit: git show -s --format='%h an=%an cn=%cn' -> 70c005e8 an=w338-0428-078-1855fix2
  cn=w338-0428-078-1855fix2.
  Ancestry: git merge-base --is-ancestor origin/develop(5a37ddbd9a06dd44f6068d3266ff2ed853a84a74)
  HEAD -> OK. git log --oneline origin/develop..HEAD -> the chain's own commits only
  (43326cf5..70c005e8, this card's carriers from prior rounds + my two corrections + this
  removal); no foreign candidate added this round.
  Delivery witness: git ls-remote https://github.com/mcpdev80/baseharbor.git
  refs/pull/1855/head refs/heads/w279-0428-078-pr1650-reissue ->
  70c005e8bc48b6186da1095a183905a42ee6c493 refs/heads/w279-0428-078-pr1650-reissue
  (refs/pull/1855/head lags ref-sync at fe940dc3 momentarily; gh pr view headRefOid = 70c005e8
  after sync — recorded below).

Step 2 — family catalog PR (the #1865 pattern):
  branch w338-0428-078-projnames-row cut from origin/develop tip
  5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 (base attestation above; ls-remote before branch:
  no w338* refs existed). ONE commit 8b0eb51a12320acb8987aee1729c9a820d4d573e, identity gate
  same pattern (git show -s -> 8b0eb51a an=w338-0428-078-1855fix2 cn=w338-0428-078-1855fix2).
  Contents: scripts/pr-gate-coverage.json ONLY, +9 lines, the single row per ruling item 3:
    {"id": "source.internal_runtime_project_names_go",
     "path": "internal/runtime/project_names.go",
     "surfaces": ["source.gate.atomic.docker.data.capabilities",
                  "source.gate.atomic.podman.data.capabilities"],
     "runtime_specific": true}
  PR https://github.com/mcpdev80/baseharbor/pull/1867 against develop, title
  'chore(0428-078 family): catalog project_names.go source row (0428-359/#136 lineage)'.
  State: OPEN, draft=false (Ready-not-merged; NO merge performed by this lane, freeze holds).

Step 3 — Hosted runs watched to terminal on BOTH exact heads:
  #1867 head 8b0eb51a12320acb8987aee1729c9a820d4d573e: run 45872485574 (pull_request) —
  terminal SUCCESS: PR · Trusted Plan success, PR Selected Checks success,
  PR · Candidate-added checks (advisory) success (the candidate-side route the round-2 finding
  anticipated — the row passes the planner contract when read from the candidate), Focused
  Python + all four Validation jobs green; runtime/product jobs skipped (catalog-only diff
  selects none — same selection shape as the #1865 precedent run 45868149534, measured).
  #1855 head 70c005e8bc48b6186da1095a183905a42ee6c493: run 45872372065 (pull_request) —
  terminal FAILURE confined to the known base admission: 'PR · Trusted Plan' ValueError
  "uncataloged source change, no declared runtime gate owner: internal/runtime/project_names.go
  (id source.internal_runtime_project_names_go): add this source with its surfaces to
  scripts/pr-gate-coverage.json, e.g. {...docker.data.capabilities, podman.data.capabilities}"
  and downstream 'PR Selected Checks' ("REJECT: Go test selection missing or invalid", unset
  UNIT_SCOPE); PR · Native gate plan, Workflow policy, Source format green; Selected Runtime
  skipped (planner abort). NOT a green qualification of #1855; per ruling item 2 it qualifies
  only after #1867 lands on develop and develop is merged forward into #1855 (coordinator/Codex
  action; this lane does not merge).

## cleanliness (round 3)

`docker ps -a` on this session's host: before round 3 = 0 lines; after = 0 lines (no container/
compose work; Hosted CI only; pid zone 626183 chain, worktrees workers/w338-0428-078-1855fix2-wt
(product) + workers/w338-0428-078-1855fix2-plan (plan) only; no /var/tmp usage; no .github/**
touched — catalog file is scripts/pr-gate-coverage.json (Owner-scope exclusion applies to
.github/** only; the family route IS the ruling's prescribed mechanism for this row).

## Transport witness (clone + ref-switches, §3.6 continuity)

Round 3 continued in the EXISTING persistent clone workers/w338-0428-078-1855fix2-wt (fresh
clone made in round 1, origin = https://github.com/mcpdev80/baseharbor.git only). Ref
switches this round, in order, each verified by git rev-parse right after:
- branch w338-0428-078-pr1650-reissue created from origin/w279-0428-078-pr1650-reissue @
  fe940dc311192e81ea6fd3580d02f313dfe4e849 (mission-named candidate branch; no second branch
  for the #1855 chain — the pre-existing local branch name w279-0428-078-pr1650-reissue was
  kept as remote-tracking only),
- commit 70c005e8 (embedded-row removal) -> pushed, ls-remote-verified,
- branch w338-0428-078-projnames-row created from origin/develop @
  5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 (git ls-remote before creation: no w338* refs
  existed) -> commit 8b0eb51a -> pushed, ls-remote-verified, PR #1867 opened,
- back to w338-0428-078-pr1650-reissue @ 70c005e8 (final worktree state).
ls-remote final (after all pushes): refs/heads/w279-0428-078-pr1650-reissue =
70c005e8bc48b6186da1095a183905a42ee6c493, refs/heads/w338-0428-078-projnames-row =
8b0eb51a12320acb8987aee1729c9a820d4d573e (both FULL40 above).

## Plan-main blocker (coordinator action; HOLD per mission-scope clarifier)

Round-3 evidence PR baseharbor-plan#150 (branch w338-0428-078-1855fix3-akte, commit 865be307c,
single file: this akte) cannot be merged: hosted 'Plan · validate' FAILS identically on current
plan main and on the PR — scripts/plan.py check raises
ValueError: not enough values to unpack (expected 2, got 1)
at plan.py:650 short_ref from the malformed prs list of FOREIGN card
tasks/t-20261126-hunt46-collectable-orphans-reserved-namespace.md:18 on main:

    prs: ["mcpdev80/baseharbor-plan#147", ]   (trailing empty entry)

Measured witnesses: gh api check-runs on main commits 05956216e, e046c4729, 9986e8146 -> all
'Plan · validate' = failure; run 45873701539 (PR #150) = same traceback. The card was last
touched by main commit 05956216e ('fix misowner: hunt46-collectable owner restored empty');
it is NOT in this lane's write-set (card edits belong to their owners/coordinator), so per the
clarifier I HOLD the evidence merge and report the concrete blocker instead of editing a
foreign card or force-merging a red validate. The fix is one line (drop the trailing comma /
empty list entry, then render+check); after any such main fix I (or the coordinator) re-run
validation on #150 and merge it.

Product-side receipts stand independently of this plan-main blocker:
- #1855 candidate head 70c005e8bc48b6186da1095a183905a42ee6c493 (delivered, run 45872372065
  terminal; red ONLY on the base-catalog admission #1867 resolves).
- #1867 head 8b0eb51a12320acb8987aee1729c9a820d4d573e (delivered, run 45872485574 terminal
  SUCCESS incl. Trusted Plan + PR Selected Checks + advisory row validation).

END_BLOCKED w338-0428-078-1855fix2: round-3 missions steps 1-3 complete (embedded row removed
forward-only in 70c005e8bc48b6186da1095a183905a42ee6c493; family catalog PR baseharbor#1867 @
8b0eb51a12320acb8987aee1729c9a820d4d573e Ready-not-merged, run 45872485574 SUCCESS; #1855 run
45872372065 terminal, Trusted Plan red awaiting the #1867 base landing + forward merge =
coordinator/Codex action); evidence akte on branch (plan PR #150) held by a FOREIGN main break:
tasks/t-20261126-hunt46-collectable-orphans-reserved-namespace.md:18 trailing comma crashes
plan.py check on ALL main commits since e046c4729 — one-line fix needed, out of this lane's
write-set.

## Round-3 publication witness (END-turn measurement)

git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only
origin/main | grep w338-0428-078-1855fix2 ->
  evidence/2026-11-29/w338-0428-078-1855fix2/akte.md   (main-side file EXISTS; its content is
  the round-2 version: the round-3 sections live on plan branch w338-0428-078-1855fix3-akte,
  head c9017bde60… = commits 865be307c + dad24f7f9 + c9017bde6, PR baseharbor-plan#150.)

The final HEAD of this akte file (the round-3 version) becomes the main version exactly when
#150 merges — which is BLOCKED by the plan-main validate break documented in
'Plan-main blocker' above (foreign card tasks/t-20261126-hunt46-collectable-orphans-reserved-
namespace.md:18 trailing comma in its prs list crashes scripts/plan.py short_ref; measured
failure on main commits 05956216e/e046c4729/9986e8146 and on this PR's run 45873701539). I do
not edit a foreign card, and per the mission-scope clarifier I HOLD the evidence merge with
the concrete blocker instead of bypassing a red validate.

END_BLOCKED (round 3, final line) w338-0428-078-1855fix2: mission fix3 steps 1-3 delivered —
#1855 candidate head 70c005e8bc48b6186da1095a183905a42ee6c493 (embedded row removed
forward-only, product payload intact, run 45872372065 terminal: Trusted Plan red ONLY on the
base-catalog admission), family catalog PR baseharbor#1867 head
8b0eb51a12320acb8987aee1729c9a820d4d573e (Ready, not merged; run 45872485574 terminal SUCCESS
with Trusted Plan + PR Selected Checks + candidate-added advisory green). Two blockers remain
OUTSIDE this lane's write-set: (1) merge #1867 + forward-merge develop into #1855 (ruling
item 2 = coordinator/Codex action, freeze holds); (2) the one-line foreign-card fix on plan
main that gates my evidence PR #150. No merges by me; #1812/#1819/#1820 untouched.

## UNBLOCK re-validate (coordinator order 20:2xZ, final receipt)

Forward hop: ordinary merge commit 43a1c102dcf9b8623b880cfdfe797a02ba842691
('git merge origin/main') of live main (head 70d7d066b, coordinator fixes 55fda6956 + 70d7d0666
booked) into branch w338-0428-078-1855fix3-akte. No force, no rewrite (85e7c702c remains an
ancestor; git log origin/main..HEAD lists my four own commits + this merge only;
git merge-base --is-ancestor origin/main HEAD -> OK). Merge-commit identity gate:
git var author+committer = w338-0428-078-1855fix2 <w338-0428-078-1855fix2@baseharbor.local>
(pin source file:.../baseharbor-plan/.git/worktrees/w338-0428-078-1855fix2-plan/config.worktree);
git show -s --format='%h an=%an cn=%cn' HEAD -> 43a1c102d an=w338-0428-078-1855fix2
cn=w338-0428-078-1855fix2. Pre-push non-test checks: plan.py render + check -> 0 errors
(791 tasks, 10 pre-existing warnings).

Delivery witness: git ls-remote https://github.com/mcpdev80/baseharbor-plan.git
refs/heads/w338-0428-078-1855fix3-akte ->
  43a1c102dcf9b8623b880cfdfe797a02ba842691 refs/heads/w338-0428-078-1855fix3-akte
  (gh pr view 150 --json headRefOid after ref-sync =
  43a1c102dcf9b8623b880cfdfe797a02ba842691)

Hosted Plan validate on the resulting exact head: run 45875144959 (pull_request,
43a1c102dcf9b8623b880cfdfe797a02ba842691) — TERMINAL SUCCESS (job 140100214584, 8s), watched
to completion. The foreign hunt46 prs-line crash (coordinator-booked incident) is confirmed
fixed on main: git show origin/main:tasks/t-20261126-hunt46-collectable-orphans-reserved-
namespace.md -> prs: ["mcpdev80/baseharbor-plan#147"].

State: PR #150 OPEN, Ready (draft=false), validate green — its merge stays a coordinator
action (mission: no merges by this lane). #1855 (70c005e8) and #1867 (8b0eb51a) untouched per
this order and routed to w267.

cleanliness: docker ps -a after = 0 containers (host untouched; Hosted CI only; pid zone
626183 chain; only the two lane worktrees used; no compose projects started or left).

END_DONE w338-0428-078-1855fix2: plan #150 forward-hopped onto live main (merge
43a1c102dcf9b8623b880cfdfe797a02ba842691, ordinary, no force), Hosted Plan validate run
45875144959 terminal SUCCESS on that exact head; product candidates unchanged
(#1855 70c005e8bc48b6186da1095a183905a42ee6c493, #1867
8b0eb51a12320acb8987aee1729c9a820d4d573e) awaiting w267; no merges by this lane.

Addendum (receipt delivery): the akte's own commit 00d56a9be42824e277f16826ddcec4142e7e21a1
carries this block; Hosted Plan validate on THAT exact final head: run 45875424540
(pull_request) — TERMINAL SUCCESS, watched to terminal. Both heads green: 45875144959 @
43a1c102d (the ordered forward hop) and 45875424540 @ 00d56a9be (akte delivery). PR #150
head = 00d56a9be (gh pr view), Ready, merge awaits coordinator.

Terminal state (last appendices): the two self-delivery commits each re-triggered the single
plan workflow — 45875424540 SUCCESS @ 00d56a9be, 45875594902 SUCCESS @
83cf3b823973480f75d6857f8fe68bb9781ef4c0 (no further edit after this line). PR #150 final
head 83cf3b823973480f75d6857f8fe68bb9781ef4c0, Ready (draft=false), ls-remote-verified; merge
stays a coordinator action (no merges by this lane).

CORRECTED Terminal state (W40 coordinator transport, appended 2026-11-26 by lane
w332-0428-288-composeids "forwarded for w338 per coordinator W40 (akte-only correction)"):
the above block is the authoritative terminal record. Plan #150 final head
30fc300d26b75273a25499e421c37330d3cf91ea (branch
w338-0428-078-1855fix3-akte, gh pr view #150 --repo mcpdev80/baseharbor-plan -> OPEN,
base main); Hosted Plan "Validate planning" on THAT exact head: run 45875783387
(pull_request, attempt 1) — TERMINAL SUCCESS, watched to terminal
(conclusion success, event pull_request, run_attempt 1, head_sha 30fc300d26b75273a25499e421c37330d3cf91ea,
2026-11-26T18:25:20Z). HEAD provenance: 30fc300d is 8 commits ahead of current main
5b90921c114596d9915abb9be6d92faffcd45bfb (main 70d7d066b was an intermediate coordinator fix
commit inside the ordered forward hop merge 43a1c102d, not the current main tip), 6 behind;
git merge-base --is-ancestor origin/main 30fc300d -> OK (current main is an ancestor of the
final head). Both prior exact-head runs remain green and unmodified: 45875144959 @ 43a1c102d
and 45875424540 @ 00d56a9be. PR #150 Ready (draft=false), ls-remote-verified; merge stays a
coordinator action (no merges by this lane).

SUPERSEDED (quoted, not deleted — history preserved):
"Terminal state (last appendices): the two self-delivery commits each re-triggered the single
plan workflow — 45875424540 SUCCESS @ 00d56a9be, 45875594902 SUCCESS @
83cf3b823973480f75d6857f8fe68bb9781ef4c0 (no further edit after this line). PR #150 final
head 83cf3b823973480f75d6857f8fe68bb9781ef4c0, Ready (draft=false), ls-remote-verified; merge
stays a coordinator action (no merges by this lane)."
-> SUPERSEDED by the corrected block above. Head 83cf3b823973480f75d6857f8fe68bb9781ef4c0 was
an earlier self-delivery commit on the same PR #150 branch; the final authoritative head is
30fc300d26b75273a25499e421c37330d3cf91ea with the attempt-1 SUCCESS run 45875783387.

## W40 coordinator transport (ended 2026-11-26, lane w332-0428-288-composeids)

- Isolated plan worktree workers/worktrees/w332-150corr off origin/w338-0428-078-1855fix3-akte;
  identity pinned w332-0428-288-composeids via `git config --worktree`; git var gate passed.
- Committed cbf259ccbfedd158e5344964424940df979f85bc (author+committer w332-0428-288-composeids):
  akte-only, +26 insertions, 0 markdown checkboxes. Linear forward hop on the #150 branch,
  8 commits ahead of current main (5b90921c), only new commit — no foreign candidate, no force.
- Pushed ordinary; new Headed Plan validate run 45879643638 "Plan · validate" COMPLETED/SUCCESS
  on head cbf259cc (single job, success). Prior exact-head runs 45875144959 @ 43a1c102d and
  45875424540 @ 00d56a9be remain green and unmodified.
- No .github/** / product / merge touched. PR #150 Ready (draft=false); merge stays coordinator.
