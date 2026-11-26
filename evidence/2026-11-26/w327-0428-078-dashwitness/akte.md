# w327-0428-078-dashwitness — PR #1855 Target-isolation correction (round 2)

Card: t-20261019-r27-0428-078 (identity dashboard witness), PR mcpdev80/baseharbor#1855.
Mission: fix the residual Target-isolation defect w267 reported in the CHANGES review
(comment 7194027071) on head 77bd785cb404c502443a78a56b9edb1d2b8eb4e2, push one ordinary
commit as the lane identity, watch the exact-head pull_request run, comment on the PR,
publish this evidence.

## Finding reproduced

w267 CHANGES 7194027071, blocker 2: the round-1 binding compared the registry record's
`Network` against the network derived from the resolved Target. That mapping is NOT
injective for valid Target names: `deployment.ValidateTargetName` admits periods
(internal/deployment/target.go), while `application.IdentityProviderNetworkNameForPlacement`
maps dots to hyphens (internal/application/identity_network.go:40). The two valid Targets
`a.b` and `a-b` therefore share one consumer-network token, so a signal registered by one
Target could still satisfy the other Target's witness. Reproduced in the new regression:
the plain-grammar networks for `a.b` and `a-b` are asserted equal in
`TestIdentityDashboardWitnessTwoValidDottedTargetsIsolation`.

## Mechanism (decision + justification)

Binding now runs through the observability registry's OWN canonical attribution grammar,
`runtime://<project>/<service>` (`observability.ParseRuntimeTarget` — the same grammar the
environment resolver keys on, internal/observability/environment.go). In
`keycloakMetricSignals` a registry record counts as evidence only when ALL of:

1. `ID` equals the production project grammar `keycloak:<manifest name>` (0428-1707
   scoping; pinned by `TestIdentityDashboardWitnessNonEmptyRegistrationIDIsTargetScoped`).
2. The descriptor shape matches (endpoint service `keycloak:9000`, protocol, path, mode,
   verification) — kept from round 0, all original assertions retained.
3. `Network` equals the Target's installation consumer network
   (`keycloakTargetConsumerNetwork`, `runtime.SharedResourceProjectName("<target>-core")`
   through the producer's network grammar) — the real-network guard from round 1, kept in
   force.
4. NEW (the collision-class fix): the record's `Target` carries a canonical
   `runtime://<project>/<service>` attribution whose project equals
   `keycloakInstallationProject(witnessedRoot)` = `bh-<root directory name>-core-shared`
   and whose service equals the signal's realization endpoint. The token is the Target's
   STATE-ROOT DIRECTORY name, which `deployment.TargetStateRoot` keys on the exact
   validated name — directory-unique, hence INJECTIVE even for `a.b` vs `a-b`, whose
   normalized tokens collide. The shapes follow the producer's installation project
   grammar (internal/identityprovider keycloakStateIdentity ->
   runtime.SharedProjectName("<target>-core")), with the raw directory name retained in
   the token position instead of the lossy `projectToken` normalization.

A record without canonical attribution, or attributed to a foreign root's project, is
rejected (fail-closed, the conservative direction). The matching Target's attributed
signal stays eligible — asserted positively in both two-Target regressions.

Why not the alternatives:
- Making the NETWORK itself injective fails: every network-grammar output normalizes dots
  to hyphens (identity_network.go:40), and witness-side-only grammar changes would not
  match what the producer writes into the record (round-1 rejection).
- Changing the registry schema (a new per-source root attribute) or the Keycloak producer
  is outside this card's write-set (internal/metrics only) — documented as the paired
  producer-side follow-up; until it lands, real shared-placement records must carry the
  canonical attributed form for availability, which fails closed, never forgeable.
- Binding on the registration ID: the production ID is project-scoped and identical for
  every Target (the HOLD defect itself) — cannot bind.

## Write-set compliance

Only `internal/metrics/identity_dashboard_witness.go` and
`internal/metrics/identity_dashboard_witness_test.go` changed (git diff --name-only over
the correction commits). No `.github/**`, no ci.yml, no cmd/baha, no consent/auth files.
`BASEHARBOR_PR_DEMO_SOURCE_SHA` untouched (verified against the CI run env below).

## Tests -> CI routing

New/changed tests are ordinary Go unit tests in `internal/metrics`, auto-discovered by
`go list ./...` / `go test -list` and executed by the existing pull_request CI unit gate
(no new check file, no catalog change needed; test names:
`TestIdentityDashboardWitnessTwoValidDottedTargetsIsolation`,
`TestIdentityDashboardWitnessRootAttributionResolvers` plus the retained six). Trigger:
pull_request on develop for PR #1855. Execution result: recorded in the PR comment and
the exact-head run watched to terminal (run id + 4 Selected Runtime job results below).

## Prechecks (non-qualifying, per owner ruling single-exact-head-run)

- `gofmt -l internal/metrics/` clean; `go vet ./internal/metrics/... ./cmd/baha/` OK;
  `go build ./...` OK; `go test -list` OK.
- Local `go test ./internal/metrics -run TestIdentityDashboard` (isolated
  BASEHARBOR_STATE_DIR): 8 PASS — NON-QUALIFYING; qualification is the hosted run.

## Commits (ordinary, lane identity author+committer, no force, no rebase)

- Base absorbed: none needed — `git merge-base --is-ancestor origin/develop HEAD` OK
  (develop 5a37ddbd9a06dd44f6068d3266ff2ed853a84a74 already an ancestor).
- f13d37d4ca54a58a7c179b56dfe92ab6b407b397 — witness attribution via the Target's root
  directory (fix + regressions).
- 18ccd8ea80d462a71964fd95a1d0dab31e6a713f — dead-code cleanup of superseded helpers
  (same write-set, no behavior change).
- 879655f07f5fb28aba4e37ce33fdb2a8e0cce046 — attribution comments aligned with the final
  grammar (comments only, no behavior change). FINAL CANDIDATE HEAD.
- `git show -s --format=%an` on all three: `w327-0428-078-dashwitness`.

## CI (hosted, exact head)

- Pushed to `w279-0428-078-pr1650-reissue`; `git ls-remote` witnesses: refs/heads and
  refs/pull/1855/head = 879655f07f5fb28aba4e37ce33fdb2a8e0cce046.
- Own pull_request run on exact head 879655f07f5fb28aba4e37ce33fdb2a8e0cce046:
  **45845829221 — completed, conclusion SUCCESS** (watched to terminal). The 4 Selected
  Runtime jobs all SUCCESS: docker·observability, podman·observability,
  podman·data-capabilities, docker·data-capabilities. PR Selected Checks posted
  (.github#5). Superseded intermediate-head runs (NOT qualification): 45843285141
  (f13d37d4 — every completed job green, cancelled after the two data-capabilities
  runtime jobs had passed, to free runners for the final head), 45843907729 (18ccd8ea,
  auto-cancelled by the branch concurrency group when 879655f0 was pushed).
- `BASEHARBOR_PR_DEMO_SOURCE_SHA` untouched: no file in the delta (8635ba07..HEAD touches
  only internal/metrics/identity_dashboard_witness*.go) can set it; the PR · Demo Pin job
  consumed the trusted repository variable pin (demo_sha 98e4d549…, workflow-internal
  default, not an override) and completed SUCCESS.

## cleanliness

No containers, networks, volumes or state directories were created by this lane on this
host (unit tests use `t.TempDir()`/isolated BASEHARBOR_STATE_DIR only).
`docker ps -a` before: (empty) — after: (empty).

## END

END_DONE w327-0428-078-dashwitness: #1855 round-2 Target-attribution fix on final head
879655f07f5fb28aba4e37ce33fdb2a8e0cce046, exact-head run 45845829221 SUCCESS.
