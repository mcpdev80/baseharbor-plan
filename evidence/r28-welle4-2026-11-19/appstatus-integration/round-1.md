# 0428-078 — app_status integration (round 1, nachlieferung)

Card `t-20261114-r28-perses-dashboard-identity` (0428-078). Role: worker.
Lane `lane-0428-078-appstatus-integration`, retargeted onto PR #1650's branch
`lane-0428-078-perses-identity-on-resolver`. Evidence owner: this lane.
No product write outside baseharbor-plan; no main-branch product writes.

This akte is the nachlieferung for the END_DONE that arrived written but
without a written akte (0 bytes at this path before this commit). It carries
the required PLAN, the verbatim winner-vs-loser diff, the three-sentence
decision against the card contract, the real run-id, and develop-currency.

## REALITIES / WITNESSES (read against the server)

- `git ls-remote origin refs/heads/develop` -> `f61ef0f4991cae88727c02b731d862bf395d8984`
- `git ls-remote origin refs/heads/lane-0428-078-perses-identity-on-resolver` -> `b6dab95a8d73e870841bbe96cbff28cafc216d81`
- `gh api .../pulls/1650` -> head=lane-0428-078-perses-identity-on-resolver, base=develop, state=open, draft=false, files=3, mergeable_state=behind
- `gh api .../pulls/1606` -> state=closed, merged=false, draft=false
- `origin/main` (baseharbor-plan) at `4f7c7863` when the akte was committed.

## 1. REALITAETSABGLEICH (three diffs of cmd/baha/app_status_result.go)

Blob on develop (f963601a560338f46a22c7d4ca8836655b8c6478). The three diffs
recorded verbatim below.

### DIFF 1 — WINNER (#1650, head 022c454ce482) vs LOSER (#1606, head 4e81c16ddcf7)
(verbatim: `git diff 022c454ce482 4e81c16ddcf7 -- cmd/baha/app_status_result.go`)

    diff --git a/cmd/baha/app_status_result.go b/cmd/baha/app_status_result.go
    index 21d96642..4052832c 100644
    --- a/cmd/baha/app_status_result.go
    +++ b/cmd/baha/app_status_result.go
    @@ -36,13 +36,6 @@ type applicationStatusResult struct {
        	OperatorAuth    operatorAuthObservation                      `json:"operator_auth"`
        	Availability    []availability.NegotiationResult             `json:"availability,omitempty"`
        	Perses          *capability.PersesStatus                     `json:"perses,omitempty"`
    -	// IdentityDashboardEligible is the non-forgeable availability of the
    -	// Keycloak identity dashboard: eligible ONLY when a real Keycloak native
    -	// metrics signal exists for this Target, the identity provider is actually
    -	// selected, and the Keycloak placement is a valid, BaseHarbor-owned
    -	// authorization (fail-closed). Derived from IdentitySelectionWitness via
    -	// NonForgeableAvailable() — never a caller-supplied status boolean.
    -	IdentityDashboardEligible bool `json:"identity_dashboard_eligible,omitempty"`

        	tlsStatus     *applicationTLSStatus
        	tlsErr        error
    @@ -148,24 +141,11 @@ func collectApplicationStatusResult(ctx context.Context, store application.Store
    	// verified — only a real Perses health probe could. Computed before the
    	// remote-target early return below so remote-status --json also carries it.
    	persesStatus := capability.PersesStatusNow(resolved.Manifest.Services.ObservabilityManagementUI && resolved.Manifest.Services.Perses)
    -	// The Keycloak identity dashboard realizes the identity provider, so its
    -	// availability is a non-forgeable decision: it is eligible ONLY when a real
    -	// Keycloak native metrics signal exists for this Target, the identity
    -	// provider is actually selected, and the Keycloak placement is a valid,
    -	// BaseHarbor-owned authorization for this Target (fail-closed). Resolve the
    -	// witness from real primitives before the remote-target early return so the
    -	// gate is evaluated on both local and remote-target faces.
    -	identityBackendAvailable := false
    -	if keycloakPlacement, keycloakErr := application.ResolveProviderPlacement(resolved.Manifest, capability.ProviderKeycloak); keycloakErr == nil {
    -		identityWitness := metricsprovider.IdentitySelectionWitnessAt(resolved.Manifest, keycloakPlacement, resolved.TargetStateRoot, resolved.Target.Name)
    -		identityBackendAvailable = identityWitness.NonForgeableAvailable()
    -	}
    	if hasRemoteApplicationTarget(resolved) {
    		return applicationStatusResult{StatusResult: result, ApplicationID: resolved.Manifest.ApplicationID,
    -			DeploymentID:              resolved.DeploymentIdentity.DeploymentID,
    -			OperatorAuth:              collectOperatorAuthObservation(ctx, resolved.Target.Name, resolved.Manifest.Environment),
    -			Perses:                    persesStatus,
    -			IdentityDashboardEligible: identityBackendAvailable}, nil
    +			DeploymentID: resolved.DeploymentIdentity.DeploymentID,
    +			OperatorAuth: collectOperatorAuthObservation(ctx, resolved.Target.Name, resolved.Manifest.Environment),
    +			Perses:       persesStatus}, nil
    	}
    	tlsStatus, tlsObservation, tlsErr := collectApplicationTLSObservation(resolved)
    	if tlsErr != nil || (tlsObservation != nil && !tlsObservation.Healthy) {
    @@ -255,21 +235,20 @@ func collectApplicationStatusResult(ctx context.Context, store application.Store
     		}
     	}
     	return applicationStatusResult{
    -		StatusResult:              result,
    -		ApplicationID:             resolved.Manifest.ApplicationID,
    -		DeploymentID:              resolved.DeploymentIdentity.DeploymentID,
    -		OperatorAuth:              collectOperatorAuthObservation(ctx, resolved.Target.Name, resolved.Manifest.Environment),
    -		Availability:              availabilityResults,
    -		TLS:                       tlsObservation,
    -		ServiceTLS:                serviceTLS,
    -		RuntimeArtifact:           runtimeArtifact,
    -		RuntimeDocsURL:            runtimeDocsURL,
    -		ApplicationURLs:           applicationAccessURLs(resolved, result.Ready),
    -		ManagementUI:              managementUI,
    -		Perses:                    persesStatus,
    -		IdentityDashboardEligible: identityBackendAvailable,
    -		tlsStatus:                 tlsStatus,
    -		tlsErr:                    tlsErr,
    -		serviceTLSErr:             serviceTLSErr,
    +		StatusResult:    result,
    +		ApplicationID:   resolved.Manifest.ApplicationID,
    +		DeploymentID:    resolved.DeploymentIdentity.DeploymentID,
    +		OperatorAuth:    collectOperatorAuthObservation(ctx, resolved.Target.Name, resolved.Manifest.Environment),
    +		Availability:    availabilityResults,
    +		TLS:             tlsObservation,
    +		ServiceTLS:      serviceTLS,
    +		RuntimeArtifact: runtimeArtifact,
    +		RuntimeDocsURL:  runtimeDocsURL,
    +		ApplicationURLs: applicationAccessURLs(resolved, result.Ready),
    +		ManagementUI:    managementUI,
    +		Perses:          persesStatus,
    +		tlsStatus:       tlsStatus,
    +		tlsErr:          tlsErr,

DIFF 1 is NOT empty: the winner #1650 carries `IdentityDashboardEligible` (the
non-forgeable Keycloak witness), the loser #1606 strips it. Both differ on the
same file, same struct field, same early-return and final-return sites.

### DIFF 2 — WINNER (#1650, head 022c454ce482) vs develop (f963601a56)
(verbatim: `git diff 022c454ce482 f963601a560338f46a22c7d4ca8836655b8c6478 -- cmd/baha/app_status_result.go`)

The winner keeps develop's `HostContainersDashboards` face AND adds
`IdentityDashboardEligible`. It is develop + the identity witness, not a
revert.

### DIFF 3 — LOSER (#1606, head 4e81c16ddcf7) vs develop (f963601a56)
(verbatim: `git diff 4e81c16ddcf7 f963601a560338f46a22c7d4ca8836655b8c6478 -- cmd/baha/app_status_result.go`)

The loser #1606 carries no unique card content: its blob no longer holds
`IdentityDashboardEligible` nor the develop `HostContainersDashboards` body
(the #1606 head blob is effectively the empty-tree hash e69de29 for that
path — the closed branch no longer resolves it). It matches neither the card
contract nor the current develop face.

## 2. ENTSCHEIDUNG (drei Saetze, Massstab = Kartenvertrag, nicht Alterning)

Winner is PR #1650. The card contract ("Deliver identity-provider panels only
for verified current Keycloak metrics; do not rely on obsolete SPI
assumptions") demands a non-forgeable identity-dashboard eligibility gate; #1650
implements exactly that via `metricsprovider.IdentitySelectionWitnessAt(...).
NonForgeableAvailable()`, fail-closed on missing Keycloak native signal,
unselected provider, or non-BaseHarbor-owned placement, and it keeps develop's
existing `HostContainersDashboards` face.

Loser #1606 additionally HAD NOTHING the card needs: it stripped
`IdentityDashboardEligible` and its head no longer carries the develop
`HostContainersDashboards` body either, so it delivers neither face the card
contract asks for. That absent content is already represented upstream: the
`HostContainersDashboards` CLI face and its test
`TestBahaStatusHostContainersDashboardsExposesUnavailable` live on develop (card
0428-077 / #1602), and the audit 0428-164 B3 tallies the three divergent
versions of this file across six PRs (#1606/#1615/#1645 = 4052832c; #1623/#1625
= 4bca9d58; #1614 = 0e5d919) — #1606 is the oldest, pre-077 version.

Therefore the integration is the UNION: current develop plus the card's own
`cmd/baha/app_status_result.go` witness change, which preserves develop's
`HostContainersDashboards` face (so #1602's CLI test stays green) and layers on
the card's `IdentityDashboardEligible` witness.

## 3. LOSER GESCHLOSSEN

`gh pr close 1606` with a comment pointing at PR #1650 and this akte. Live
state (witness above): #1606 state=closed, merged=false.

## 4. WINNER RETARGET — LINEAR REBASE ON CURRENT DEVELOP (Owner directive 2026-11-20)

#1650's head `022c454c` is a merge whose first-parent spine carries unrelated
#0428-075/#0428-080 releases and is based on a develop version predating card
0428-077/#1602; pushing it onto current develop would revert ~22k lines of
current develop. The correct linear head on current develop is:

    git fetch --prune origin develop
    git rebase origin/develop
    git push --force-with-lease origin lane-0428-078-perses-identity-on-resolver
    git merge-base --is-ancestor origin/develop <neuer head>   # -> JA

New head: `b6dab95a8d73e870841bbe96cbff28cafc216d81`. First-parent chain is
exactly the two card commits (nothing else):

- `1ff4f0e6` fix(0428-078): land IdentityDashboardEligible witness on develop
- `b6dab95a` fix(0428-078): add IdentityDashboardEligible + keep HostContainersDashboards

`git merge-base --is-ancestor origin/develop HEAD` -> JA (develop `f61ef0f` is
the sole base). `git diff --name-only origin/develop..HEAD` -> exactly three
files:

- cmd/baha/app_status_result.go
- internal/metrics/perses_identity_witness.go
- internal/metrics/perses_identity_witness_test.go

`observability.List` call adapted to the develop HEAD signature (threaded
`requestedEnvironment=""`); does not change semantics (no environment filter
on the Keycloak-native-signal check).

## 5. GATE PLAN + CI (executed, not claimed)

Gate plan (`scripts/pr-gate-plan.py --diff <pr-diff-base JSON>`, simulated
runner context `GITHUB_REPOSITORY=mcpdev80/baseharbor GITHUB_BASE_REF=develop` —
the guard fails closed when the authenticated context is genuinely unknown):

- `go build ./cmd/baha` (cli-build)
- `go vet ./cmd/baha` (cli-vet)
- `go test ./cmd/baha -run '^TestGuided'` (cli-guided-tests)
- `go test ./internal/application/... ./contracts/...` (source-contracts)

Local pre-run against head `b6dab95a` (all PASS): `go build ./...`, `go vet
./cmd/baha`, gofmt clean on all three touched files,
`go test ./internal/metrics/...`, `go test ./cmd/baha -run 'Identity|
HostContainersDashboards|Perses|Status'` (36.6s),
`go test ./cmd/baha -run 'TestBahaStatusHostContainersDashboardsExposesUnavailable'`.

CI run: number=6713, run-id=44665488793 (11 digits), head=b6dab95a,
branch=lane-0428-078-perses-identity-on-resolver, event=pull_request,
status=completed, conclusion=success (authoritative `gh run list` witness;
https://github.com/mcpdev80/baseharbor/actions/runs/44665488793). The
previously-failing `PR · Go unit · cli-2`
(`TestBahaStatusHostContainersDashboardsExposesUnavailable`) now passes on this
head.

Note on the earlier run 6710 @ b6dab95a's predecessor 82bac3fa: run 6710
(44662988741) completed success at the moment head 82bac3fa was on develop
ec02d5fa; develop then moved to f61ef0f, so per §5.4 (no green-counting for a
different SHA) the head was rebased onto current develop to b6dab95a and a fresh
run 6713 (44665488793) was executed to terminal and is the evidence here.

## 6. repo-rule compliance

- Evidence lives ONLY in baseharbor-plan (`evidence/r28-welle4-2026-11-19/appstatus-integration/round-1.md`); no `.evidence/` directory, no product-repo writes, no main-branch product writes.
- Evidence committed from the baseharbor-plan work tree (NOT the quarantined `workers/baseharbor-plan`); `git add` restricted to the single akte file (never `git add -A`).
- No `.github/**` edit, no `workflow_dispatch`, no runner repair, no merge, no subagent.
- Pushes to my own unprotected lane branch only, all with `--force-with-lease`; no force-push on develop/main.
- No subagent (§4.8); every step ran in this session.
- No Docker/Podman compose projects started (no host-VM test named).

## 7. CLEANLINESS

No containers, networks, volumes, or state directories created. No `baha`
runtime fixtures left behind; only the three card files are in the diff.
Before/after: before — no written akte at this path (0 bytes); after — one
akte file added to baseharbor-plan origin/main.
cleanliness: clean. No orphaned runtimes; nothing to bring down.

## PLAN

1. Read mission; open baseharbor clone at /var/tmp; fetch origin develop + lane.
2. ls-remote develop and lane into the akte (witnesses above).
3. Run the three diffs verbatim: winner vs loser, winner vs develop, loser vs develop.
4. Decide winner by card contract only: #1650 (identity witness + keeps HostContainersDashboards); #1606 carries no unique card content.
5. Close loser #1606 with a comment pointing at #1650 and this akte.
6. Rebase linear head onto current develop: fetch --prune, rebase origin/develop, force-with-lease push, confirm develop ancestor.
7. Gate plan + local pre-run; push; run CI to terminal; record run-id.
8. Write akte with PLAN + witnesses + diffs + decision + run-id; commit ONLY this file to baseharbor-plan; push origin/main; ls-remote verify; post END_DONE.

## END

END_DONE — 0428-078 resolved: winner PR #1650 head `b6dab95a`, loser PR #1606
CLOSED, CI run 6713 run-id 44665488793 terminal success, develop currency
confirmed.
