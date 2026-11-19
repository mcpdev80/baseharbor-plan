# 0428-121 / PR #1691 — Environment-Filter Hyphen Bug Fix (Correction Round r4)

- Mission: /var/tmp/missions/mission-121-envfix-round4.md (121-envfix-round4)
- Mission Nachtrag (r4 round-2): /var/tmp (comment 7004115394, four points restated)
- Card: 0428-121 · PR #1691
- Candidate head worked on: d1fcfdf6b8376a30f5100c8c30f5f3491427cf9e on refs/heads/lane-0428-efilter
- Base on develop: da76c5cf9c963207038d5599bd130b89ecb1e8a4 (monotone hop, ahead 2 / behind 0)

## PLAN

- Establish ground truth: fresh baha checkout at /var/tmp, confirm baseSHAs via ls-remote
- Locate exact bug site: projectTokenFromID + SourceEnvironment callers, token-count assumption
- Resolve ambiguity with Owner (QUESTION): anchor on OwnerApplication instead of parsing env from name
- Implement fix on isolation worktree under /var/tmp (no ProviderPlacement/Security.go/.github scope)
- Write regression tests on the real seam (four mandated cases a/b/c/d + anchor table)
- gofmt -l . empty, go build ./..., go vet ./..., monotonic hop on develop
- Push to refs/heads/lane-0428-efilter with ancestor witness; drive CI to terminal SUCCESS
- Write evidence, push to origin/main, clean host, report terminal run, post END

## GROUND TRUTH

- ls-remote origin main (baseharbor-plan): c468e219eb4998a3cf552ef3013b08b8296d52f3
- ls-remote origin develop: da76c5cf9c963207038d5599bd130b89ecb1e8a4
- ls-remote origin lane-0428-efilter: d1fcfdf6b8376a30f5100c8c30f5f3491427cf9e
- merge-base d1fcfdf6b ... develop == da76c5cf9c963207038d5599bd130b89ecb1e8a4 (monotone hop, no foreign commit)
- base SHA attested (commit cut from): d1fcfdf6b8376a30f5100c8c30f5f3491427cf9e
- git merge-base --is-ancestor d1fcfdf6b <new> : to be recorded in evidence after commit

## ROOT CAUSE (file:line)

`internal/observability/environment.go`, function `trailingProjectEnvironment`, the pre-fix
fixed-token-count rule (develop lines 100-118): the operator grammar
`ApplicationProjectName(namespace, application, environment)` (internal/runtime/project_names.go:31)
is `bh-<target>-<app>-<env>` and the runtime grammar is `baseharbor-<app>-<env>`. Both
`Name` and `Environment` are validated by `validateSlug` (internal/application/manifest_validation.go:442/33),
which allows hyphens. The old code did `strings.Split(value, "-")` and required exactly
3 (operator) / 2-or-3 (runtime) tokens, so a hyphenated application name such as
`my-app` produced four tokens (`bh-prod-my-app-dev`) and `SourceEnvironment` returned
`ok=false`; `SourceMatchesEnvironment` then dropped the source silently.

The decisive ambiguity (resolved with the Owner, not guessed): the failing shape
`bh-<ns>-<app>-<env>` is structurally identical to a legacy unresolvable name
(`baseharbor-prod-west`, app `prod-west`, no env). Both `Name` and `Environment` are
free-form slugs, so no token-count or "last token" rule can separate "hyphenated app
name" from "legacy name". The system already knows the owning application
(`SignalSource.OwnerApplication`, registry.go field `owner_application`), so the
environment is the segment that FOLLOWS the known application anchor in the project
name, not a count of hyphens.

## DECISION

Anchor rule (no new field, no `ProviderPlacement.Environment`, no env allowlist, no
signature change): for an app-scoped source the environment membership is given iff the
project name contains the known `OwnerApplication` exactly once as `-<app>-`; the
environment is the segment following that anchor (case-normalised, leading/trailing
hyphens stripped). Fail closed when there is no anchor, an empty remainder, or more than
one anchor. This is the canonical generator pattern (internal/runtime/project_names.go:31
`ApplicationProjectName`) applied via the already-known `OwnerApplication` — the only
source of truth the system has. `SourceEnvironment` calls `projectTokenFromID`
(environment.go:74) which calls `trailingProjectEnvironment` (environment.go:88); the
metrics ID grammar (`application:metrics:<app>:<env>:<source>`) keeps its existing
explicit segment resolver (`applicationMetricsSourceEnvironment`), which is unambiguous.

Consequence that resolves every mandated case without guessing:
- `bh-prod-my-app-dev` + app `my-app` → anchor `-my-app-` → env `dev` (case d)
- `bh-local-demo-prod-west` + app `demo` → env `prod-west` ≠ `west` → west caller sees nothing (case a, fail-closed)
- `bh-local-demo-prod-west` + app `demo-prod` → env `west` → west caller sees it (a')
- reserved-token project `bh-local-prometheus` + app `demo` → no anchor → fail closed (case b)
- legacy bare ID `demo-metrics` → no anchor → fail closed (case c)

## REGRESSION CASES (all in envfilter_route2_test.go)

- (d) TestRoute2HyphenatedApplicationProvider — generated namespaced provider for a
  hyphenated app `my-app` in env `dev`: visible to the `dev` caller (ListLogs),
  invisible to the `prod` caller. Real seam through List/ListLogs.
- (a) TestRoute2AnchorRuleTable row `{"demo", "bh-local-demo-prod-west", "prod-west"}` —
  env resolves to `prod-west`, so a `west` caller stays fail-closed.
- (a') same table row `{"demo-prod", "bh-local-demo-prod-west", "west"}` — env `west`.
- (b) table row `{"demo", "bh-local-prometheus", ""}` — reserved-token project, fail closed.
- (c) table row `{"demo", "demo-metrics", ""}` — legacy bare ID, no anchor, fail closed.
- (e) table row `{"demo", "bh-demo-local-demo-dev", ""}` — two anchors, fail closed.
- (d) table rows `{"my-app", "bh-prod-my-app-dev", "dev"}` and
  `{"my-app", "baseharbor-my-app-dev", "dev"}` — hyphenated app, both grammars.
- Existing (d-equivalent) TestRoute2ProviderEnvMatch (bh-local-demo-prod) stays green.

Each table row logs the file:line that decides it: environment.go
`trailingProjectEnvironment` (anchor via `strings.Index(value, "-<app>-")`, remainder as
env; `strings.Count` guard for the double-anchor case).

## CI EVIDENCE

- Run: `44495408370`, conclusion **success** (terminal), head_sha `f28b97a53870bb3f5cb5c90618dea977df3f1c2b`, branch `lane-0428-efilter`.
- Required PR jobs all SUCCESS: `PR · Source format`, `PR · Validation · go-build`, `PR · Validation · go-vet`, `PR · Exact Candidate`, `PR · Runner Interface`, `PR · Demo Pin`, `PR · Focused Python`, `PR · Validation · identity-provider-package-tests`, `PR · Go unit · {cli-0,cli-1,cli-2,cli-3,packages,owner}`, `PR · Native gate plan`, `PR · Trusted Plan`, `PR · Workflow policy`, docker runtime gates `PR · Selected Runtime ... observability` + `identity`.
- Trigger: standard push-triggered CI on the branch push (no rerun/workflow_dispatch by this lane).
- Local pre-checks (before push): `gofmt -l .` empty; `go build ./...` exit 0; `go vet ./...` clean; `go test ./internal/observability/ ./internal/metrics/ ./internal/logs/ ./internal/application/` all ok; `bash scripts/source-readability-audit.sh` all three checks PASS.

## BRANCH PROVENANCE

- Base attested (cut from): d1fcfdf6b8376a30f5100c8c30f5f3491427cf9e (lane-0428-efitter head / monotone on develop da76c5cf9)
- My commit: f28b97a53870bb3f5cb5c90618dea977df3f1c2b (single commit, 2 files, +152/−24)
- `git merge-base --is-ancestor d1fcfdf6b ... f28b97a5` → YES (monotone hop, no foreign commit)
- Push: `d1fcfdf6..f28b97a5 HEAD -> lane-0428-efilter` (remote head before push d1fcfdf6b, after push f28b97a5)

## HOST HYGIENE

- before docker ps -a: ambient bh-local-shared-* containers (openbao/postgres), none mine
- before podman ps -a: podman not installed on this host
- after docker ps -a: unchanged — this lane ran pure Go unit tests, no containers/compose
- after podman ps -a: n/a (not installed)
- cleanliness: clean. Zero containers created. /var/tmp/baha-r4 worktree removed after commit. Ambient bh-local-shared-* and core-* images left untouched.

## HANDOFF

- END_DONE mission-121-envfix-round4.md: hyphenated env-filter candidate fixed via
  OwnerApplication anchor; terminal CI run reported to Owner.
