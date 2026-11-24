# #0428-283 operator-auth fallback applicability (round 1)

- Lane: w100-0428-283-fallback
- Mission: coordinator/missions/w100-0428-283-fallback.txt (READ-ONLY DESK)
- Date: 2026-11-24
- Scope: READ-ONLY Befund. No edits, no PR, no merge, no CI trigger on #1812/#1819/#1820/#1818/#1826/consent. No subagents (§4.8). No other session contacted. No local Go test / unit suite on the coordinator host. No containers / compose projects started.

## Mission

Reconcile a worker CONFLICT precisely, read-only:

- w93: the Light gates need NO operator seeding because a trusted-local fallback at `internal/operatorauth/authorization.go:247` covers them.
- w92 + owner's raw logs: policy's first in-gate failure in CI = `operator authentication needs interactive setup but input is not a terminal` -> the non-interactive path is NOT engaging in the CI Light env.

Question: does the trusted-local / non-interactive CI operator path actually cover (a) the Docker/Podman LIGHT gates and (b) the static/mcp gate, given their differing inputs?

## Remote attestations (ls-remote witnesses)

- develop (baseharbor) origin HEAD: `f14fb87c8f5afd91168e4f174d620c9f00e6341e` (refs/heads/develop) — witness `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`.
- develop (baseharbor-demo) origin HEAD: `c23bd9ac58919302ffad3a43f43afb1a34bfbc96` (refs/heads/develop) — witness `git ls-remote https://github.com/mcpdev80/baseharbor-demo.git refs/heads/develop`.
- baseharbor remote used: `https://github.com/mcpdev80/baseharbor.git` (verified via `git remote -v`; lane-origin/origin both point at github.com/mcpdev80, no filesystem origin).
- baseharbor-demo remote used: `https://github.com/mcpdev80/baseharbor-demo.git`.

## Planning repo remote witness (wrong-zone check)

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The `workers/baseharbor-plan` directory is a directory inside the bookkeeping repo (commits never reach github); it was NOT used as the planning repo.

## 1. The non-interactive / managed-local operator path — EXACT conditions

Two distinct mechanisms can make a machine operation non-interactive in CI:

### 1a. `authorizeMachineOperation` (internal/operatorauth/authorization.go) — the "trusted-local" claim site

The mission points at `authorization.go:247`. **This line is a return-statement closing the claim-membership branch, not a trusted-local fail-open.** The full trust decision is `authorizeMachineOperation` (lines 144-307). The EXACT live outcomes at the current base (develop HEAD `f14fb87c8`) and in this checkout (2 commits ahead) are:

- Line 201-226: if a **tenant-scoped** context is present → require an authenticated principal + tenant permission (fail closed otherwise).
- Line 235-269: if NO tenant scope but `ok` (a verified principal exists) → resolve claim membership; missing membership, unverified principal, failed lookup, or ambiguous membership all **fail closed** (`claim_membership_unresolved`). This is NOT the trusted-local fallback — the comment at 232-234 is explicit: "This fails closed rather than falling through to the trusted-local fallback."
- Line 270-275: **local-runtime grant** (`!ok && grantValid`) → allowed as `local-runtime/<target>`. This is the opaque single-use grant from `local_runtime.go`, only for registered local-workload operations.
- Line 276-283: **explicit comment — no trusted-local fail-open.** "There is no policy source in the decision context that establishes host-local trust, so an unauthenticated request without a valid grant is denied below regardless of the environment name. The environment name is never a trust signal; do not reintroduce an `!ManagedEnvironment(...)` arm here."
- Line 285-295: `!ok` (no principal) → `operator_authentication_required`, `ErrorAuthenticationFailed`, **fail closed** — regardless of environment name.
- Line 297-306: `Allowed = true` only when a verified principal is present.

**Conclusion for 1a: There is NO `!ManagedEnvironment(...)` trusted-local fail-open arm at develop HEAD or in this checkout.** w93's cited line 247 does not contain that fallback. The test `TestAuthorizeMachineOperationNameOnlyPolicyFailsClosed` (authorization_test.go:45, :56-57) pins that "environment name alone unexpectedly enabled trusted-local authorization" must NOT happen; `dev` with no principal fails closed (`operator_authentication_required`). The compatibility helper `ManagedEnvironment` (config.go:89-91) now fails closed and treats EVERY environment name as managed (no name establishes trusted-local); explicit trusted-local must come from a policy source, and no production machine-authorization caller supplies `trustedLocal` (config.go:101-110).

### 1b. `ciIntegrationManagedLocalGateReason` (cmd/baha/ci_integration_operator_enabled.go:96-107) — the CI synthetic-operator gate

This is the only path that lets a **tagged CI binary** (`//go:build baseharbor_ci_operator_testonly`) stamp a synthetic verified operator for a disposable gate. It engages ONLY when ALL of these hold (line 102-105):

- `BASEHARBOR_DEMO_OPERATOR_GATE` env is set AND `== GATE` env
- `BASEHARBOR_TEST_RUNTIME` in {`docker`, `podman`} — **strictly, static is excluded**
- `target.Name == "atomic-" + runtime + "-" + gate` (e.g. `atomic-docker-policy`)
- `target.Name == BASEHARBOR_TARGET`
- `target.AccessProvider == "local"`
- `target.TenantID == ""` (empty)
- `target.RuntimeProvider == runtime`

Plus a `managedWorkload` admission for the exact canonical command (lines 114-240: `config organization set`, `policy explain`, `app inspect .`, `target -o json`, `app list --all-targets`, `app exec demo-app`, root init/destroy/destroy-preview, `down`, doctor read-only, guided MCP-serve + footprint parity, etc.). When it engages, `ciIntegrationOperatorContext` (line 557-564) injects a verified principal (`Issuer: "https://issuer.test", IssuerVerified: true, Groups: [editor]`) + a membership provider resolving to `tenant-ci-acceptance/editor` — a verified authenticated operator, so `authorizeMachineOperation` takes the claim-membership branch (235-269) and allows the operation. It is NOT a trusted-local fail-open; it is a verified-operator stamp for a narrow fixture-scoped workload.

## 2. The two gate classes' ACTUAL inputs

### 2a. Docker/Podman LIGHT runtime gates

Set by the demo atomic-gate harness (`baseharbor-demo/tests/atomic-bootstrap.sh`, `scripts/acceptance.sh`, `tests/guided/drive.py`):

- `BASEHARBOR_TEST_RUNTIME` = `docker` or `podman`
- `BASEHARBOR_DEMO_OPERATOR_GATE` = `<gate>` (guided / policy / connectivity / reconciliation / full-destroy / lifecycle / failure)
- `GATE` = same `<gate>`
- `BASEHARBOR_TARGET` = `atomic-<runtime>-<gate>` (e.g. `atomic-docker-policy`)
- target created via `target create <name> --provider <runtime> --access local-<runtime> ...` → `AccessProvider == "local"`, `TenantID == ""`, `RuntimeProvider == runtime`

**Every managed-local condition in §1b is satisfiable for the Light gates by env-seeding the existing fallback** (set `BASEHARBOR_DEMO_OPERATOR_GATE`, `BASEHARBOR_TEST_RUNTIME`, `GATE`, `BASEHARBOR_TARGET` to the atomic-<runtime>-<gate> target, and let the target resolve to a `local`/`TenantID==""` target). This is exactly the `ci-operator-testonly` tag binary route that #1825/`f14fb87c8` built with the tag.

### 2b. Static / mcp gate

- `runtime` = `static`, `gate` = `mcp`, `target` = `mcp-static` (demo `tests/mcp/new-edit-static.py:75-86` seeds `BASEHARBOR_STATE_DIR / XDG_CONFIG_HOME / XDG_DATA_HOME / BASEHARBOR_TARGET` but NOT operator-auth / test-only context).
- `BASEHARBOR_TEST_RUNTIME` is effectively `static` (not `docker`/`podman`).

**The managed-local condition `runtime ∈ {docker, podman}` (ci_integration_operator_enabled.go:102) is NOT satisfiable for `runtime=static`.** `ciIntegrationManagedLocalGateReason` returns non-empty for static, so the synthetic-operator stamp is never injected. The static/mcp operation therefore reaches `authorizeMCPOperation` → `ensureManagedEnvironmentOperatorBoundary` (mcp.go:314, 324) with no principal, and because the environment is not a name-derived trusted-local (ManagedEnvironment fails closed), it fails closed at the operator-auth boundary.

## 3. Verdict — ONE change vs TWO changes

**Verdict: (ii) TWO DIFFERENT changes are needed.**

| Gate | runtime | managed-local (tagged binary) engages? | Fix |
| --- | --- | --- | --- |
| Docker/Podman Light | docker / podman | YES, by env/target seeding the existing `ci-operator-testonly` fallback (all §1b conditions met) | env + target seeding of the EXISTING fallback — no new seam |
| Static / mcp | static | NO — `runtime=static` excluded by ci_integration_operator_enabled.go:102 | The existing fallback CANNOT cover it. Needs a separate decision (either extend the managed-local admit-set to the `mcp-static` fixture, or — correctly — treat the static/mcp gate as requiring a genuine authenticated operator, i.e. it must NOT be coverable by a trusted-local route) |

One owner-authorized change that clears BOTH is NOT possible with the current code: the managed-local fallback is hard-wired to `runtime ∈ {docker, podman}`. Seeding env on the static/mcp harness would still hit `ci_integration_operator_enabled.go:102` and fall through to the interactive operator-auth boundary -> the same `input is not a terminal` failure.

**Fail-closed risk flag (STOP-worthy, to be evaluated by owner):** A tempting "one change" — broadening the managed-local admit-set so `runtime=static` also stamps a synthetic verified operator, or adding any `!ManagedEnvironment(...)` name-based fail-open — would let an unauthenticated managed op through on the static path. At the current base this is prevented (config.go:89-91 fails closed for every name; authorization.go:285-295 fails closed with no principal; the synthetic operator is a *verified* principal, not a trust-by-name). Any change that makes `runtime=static` pass through a synthetic-operator stamp is therefore security-relevant: it widens the operator-auth blast radius from a fixture-scoped verified operator to a non-interactive static gate with no verified OIDC principal. **Recommendation: the static/mcp gate should NOT be made coverable by the trusted-local route; it should be resolved either by genuine operator authentication on that gate or by scoping it out of the operator-auth seam entirely with a documented, explicit policy source — not by name-based fail-open.** This is a STOP-worthy fail-closed consideration, not an implementation to make unilaterally.

## 4. 'input is not a terminal' — where the auth flow tries a terminal

The failure string `operator authentication needs interactive setup but input is not a terminal` is the CI non-interactive symptom: a non-interactive (piped) stdin triggers a fallback interactive OIDC setup instead of a verified principal being present.

- Entry: `mcp.go:314` `ManagedEnvironment` is true for the managed seam; with no verified principal it calls `ensureManagedEnvironmentOperatorBoundary` (`mcp.go:324`) -> `ensureOperatorAuthForBoundary`.
- The managed-local synthetic-operator injection (`ci_integration_operator_enabled.go:56` `ciIntegrationManagedLocalGateReason(...) == ""`) is the ONLY non-interactive escape on the docker/podman path; it is gated by `runtime ∈ {docker,podman}` (line 102).
- For `runtime=static` the injection never fires, so the operation proceeds to the operator-auth boundary with no principal -> the non-interactive terminal fallback fires (`input is not a terminal`).

The exact line of the terminal-try string is outside this checkout (it lives in the operator-auth login/OIDC bootstrap path, not in `authorization.go`); this desk confirms the *mechanism* (no managed-local stamp for static -> boundary reached with no principal -> interactive setup attempted on non-TTY stdin) but does NOT quote the literal string's defining line because the operator-auth login/OIDC file was not present in the checked-out baseharbor tree. **Finding for owner:** the literal `input is not a terminal` site must be located in the operator-auth login/interactive-OIDC bootstrap file in the product tree to cite its file:line; the mechanism above is verified by the two code paths read.

## repo-rule compliance

- Hosted-only / read-only: zero local test execution (no `go test`, no `python3 -m unittest`, no `scripts/ci-fast-check.sh`). No CI trigger, no workflow_dispatch, no rerun, no PR/merge/branch. No subagents (§4.8). No other session contacted.
- Evidence only in baseharbor-plan. Real remote URLs only (`git remote -v` resolved to github.com/mcpdev80; workers/baseharbor never cited). No containers / compose projects / volumes / networks started. No stray files in /home/marcel/dev/baseharbor-ecosystem.

## Evidence delivery witness

Command run as second-to-last action (output verbatim):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle6-2026-11-25/0428-283-fallback-applicability
From https://github.com/mcpdev80/baseharbor-plan
  * branch                main       -> FETCH_HEAD
evidence/r28-welle6-2026-11-25/0428-283-fallback-applicability/round-1.md
```

## Cleanliness

Read-only desk: created only this single evidence file under baseharbor-plan. No product/demo files edited, no branch, no PR, no CI action, no workflow dispatch. No containers / compose projects / volumes / networks started on this host (`docker ps -a`: 0 containers; this lane started none). No scratch/checkouts/extracts created under /home/marcel/dev/baseharbor-ecosystem. No subagents.

## PLAN

- Read mission file w100-0428-283-fallback.txt; confirm READ-ONLY Befund scope and no-edits/no-PR/no-CI/no-subagents rules
- Verify planning repo remote (baseharbor-plan only; workers/baseharbor-plan is a quarantine dir)
- Fetch reality SHAs via ls-remote: develop f14fb87c8, demo develop c23bd9ac
- Read internal/operatorauth/authorization.go authorizeMachineOperation trust decision (lines 144-307) + config.go ManagedEnvironment (89-111)
- Read cmd/baha/ci_integration_operator_enabled.go ciIntegrationManagedLocalGateReason (96-107, 557-573)
- Read cmd/baha/mcp.go authorizeMCPOperation managed boundary (300-373) + operator_auth_boundary.go
- Enumerate EXACT conditions for the non-interactive/managed-local path (1a authorized decision + 1b CI synthetic operator)
- Compare Light (docker/podman) vs static/mcp (runtime=static) inputs against those conditions
- Determine ONE-change vs TWO-changes verdict + fail-closed risk flag (STOP-worthy)
- Locate the 'input is not a terminal' terminal-try site in the auth flow; state verified mechanism, flag the literal-line gap
- Write evidence round-1.md (conditions table + Light-vs-static verdict + recommendation + fail-closed flag) with ## PLAN + native todos
- Commit+push single evidence file atomically; pull --rebase origin main first
- Verify evidence path present on origin/main (ls-tree witness) before END
- Post END_DONE inline to Coordinator (00d66002)

## Handoff

END_DONE w100-0428-283-fallback posted to Coordinator (00d66002) at 2026-11-24.

Verdict: **(ii) two DIFFERENT changes.** The trusted-local / managed-local CI operator fallback does NOT correspond to a fail-open arm at `authorization.go:247` (that line is the claim-membership fail-close, 232-234; the real decision at 276-295 fails closed with no principal and explicitly forbids a `!ManagedEnvironment(...)` arm). The only non-interactive CI escape is the `ci-operator-testonly` synthetic operator (`ci_integration_operator_enabled.go:96-107`), gated strictly on `runtime ∈ {docker, podman}`:

- **Light (docker/podman) gates: COVERABLE** by env + target seeding of the EXISTING fallback (all §1b conditions settable: `BASEHARBOR_DEMO_OPERATOR_GATE`/`GATE`/`BASEHARBOR_TEST_RUNTIME`/`BASEHARBOR_TARGET` = `atomic-<runtime>-<gate>`, `AccessProvider==local`, `TenantID==""`). No new seam, no fail-open.
- **Static/mcp gate: NOT COVERABLE** — `runtime=static` fails `ci_integration_operator_enabled.go:102`, so the synthetic operator is never stamped and the operation reaches the operator-auth boundary with no principal -> `input is not a terminal`. Needs a separate decision (genuine operator auth on that gate, or a documented explicit-policy scoping — NOT name-based fail-open).

Fail-closed risk flag (STOP-worthy, owner decision): broadening the admit-set to `runtime=static` or adding any name-based `!ManagedEnvironment(...)` fail-open would let an unauthenticated managed op through on the static path; at the current base this is prevented (config.go:89-91 fails closed for every name; authorization.go:285-295 fails closed with no principal). Recommend NOT making static/mcp coverable by the trusted-local route. Literal `input is not a terminal` line not cited (operator-auth login/OIDC file not in checked-out base; mechanism verified). Evidence SHA on baseharbor-plan origin/main: 5d9e71b6e (path verified present on origin/main).
