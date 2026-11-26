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
