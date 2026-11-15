# round-1 — 0428-089 protect Perses operator access

Lane: worker (flash) — welle2-089
Date: 2026-11-15
Card: t-20261114-r28-perses-secure-access (0428-089), release v0.4.28
Task: read mission-welle2-089.md; integrate Perses with existing management
access, verified transport and authorization; inspect the selected upstream
version's security and proxy SSRF protections.
PR: #1599 (DRAFT, base lane-0428-075-perses-seam),
https://github.com/mcpdev80/baseharbor/pull/1599
Branch: lane-welle2-089-perses-secure-access (single candidate branch, per mission)
Candidate SHA: 872c6c701f00941521be153320ea1f6d122d3066
MERGE-FROST: no merge, PR stays DRAFT, never ready_for_review.

## PLAN

1. Read mission and task contract (`plan.py show`), plus the two prerequisite
   cards and the Owner decision that replaced Grafana with Perses.
2. Reality check: remote refs for develop, the seam base and the planning repo.
3. Claim the card through `plan.py claim` after pull-rebase, publish the claim.
4. Cut the lane branch from the seam head named in the mission; base attestation.
5. Inspect the existing contracts before editing: serviceaccess policy and HTTP
   gateway, application/metrics management UI, management_access vocabulary,
   operatorauth/authorization/tenancy/identity boundaries.
6. Inspect the pinned upstream release (v0.55.1) and the v0.55.0 security and
   configuration contract for the datasource proxy, encryption key and auth
   defaults.
7. Implement the contract layer: security policy, version floor, proxy
   destination resolution, fail-closed status conjunction.
8. Implement the dedicated gateway/auth policy adapter in serviceaccess.
9. Implement the operator-access adapter in application, reusing the existing
   tenant and role vocabulary; classify the management-role mappings.
10. Document the transport, proxy-destination and environment rules in EN and DE.
11. Add deterministic positive, negative, authorization and ownership tests,
    including the genuine `baha status --json` CLI path.
12. Verify: build, vet, gofmt, focused tests, before/after failure diff against
    the base, documentation audit, EN/DE parity, readability audit.
13. Commit, push, prove base ancestry and the own-commits log line, open the
    draft PR.
14. Report the foreign failing check as STATE; write this akte, publish it to
    origin/main, cleanliness pass, END post.

## Planning repo verification (wrong-zone guard)

Exact command and output before the first evidence commit:

`cd /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan && git rev-parse --show-toplevel`
`/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`

The quarantined `workers/baseharbor-plan` path was never used.

## Base attestation and branch provenance

Mission rule 8 (base stacking, no merge needed): the lane branch is cut from the
head of `lane-0428-075-perses-seam`, which the mission pinned at `219a0a24`.
`develop` is the base of that seam branch, never of this candidate.

`git ls-remote origin refs/heads/develop refs/heads/lane-0428-075-perses-seam`
before starting:

```
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
219a0a24d5687552556b094223e5e4bcfa2eebc4	refs/heads/lane-0428-075-perses-seam
```

Base SHA cut from: `219a0a24d5687552556b094223e5e4bcfa2eebc4`.

`git merge-base --is-ancestor 219a0a24d5687552556b094223e5e4bcfa2eebc4 HEAD`
exit 0 at commit `d34ef21f`, so the declared base is a true ancestor of the
first commit. `develop` `0e9ccb582` is an ancestor transitively through the seam
branch (verified with the same command, exit 0).

### Base moved during work: documented base refresh, one candidate branch

After the first push, the stacking base advanced:

```
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
cb4367f347ed587cb84c67a14b47ffaa3505a5dd	refs/heads/lane-0428-075-perses-seam
d34ef21fee37823a778a2fb3d143340291e38a25	refs/heads/lane-welle2-089-perses-secure-access
```

`cb4367f3` (card 0428-075 r2, author `worker-0427-020-ci-consumption`) is not a
descendant of `219a0a24`; it replaced it on the seam branch. The integration
follows AGENTS 4.1 (reality check after every pause) and 3.6: the named
candidate branch was kept, no second branch was invented, and the remote base
was MERGED into it (not rebased, so no frost-relevant rewrite):

`git merge --no-ff origin/lane-0428-075-perses-seam` → auto-merged
`internal/capability/perses.go` with no conflict and no content interaction:
the seam edit is confined to the `PersesManagement` descriptor block, this
card's code is six new files plus one documented append.

Ancestry against the CURRENT PR base after the merge:

`git merge-base --is-ancestor cb4367f347ed587cb84c67a14b47ffaa3505a5dd HEAD`
exit 0, i.e. `cb4367f3` IS an ancestor of the candidate `872c6c70`.

Own-commits log line over the exact base head (must list only this lane's
commits; one foreign commit here would be a scope violation):

`git log --format='%H %an <%ae> %s' cb4367f347ed587cb84c67a14b47ffaa3505a5dd..HEAD`

```
872c6c701f00941521be153320ea1f6d122d3066 Marcel -marcel <dev@baseharbor.local> Merge remote-tracking branch 'origin/lane-0428-075-perses-seam' into lane-welle2-089-perses-secure-access
d34ef21fee37823a778a2fb3d143340291e38a25 Marcel -marcel <dev@baseharbor.local> feat(0428-089): protect Perses operator access through the service-access gateway
```

Both commits are this session's. The merge commit introduces no foreign
content: `cb4367f3` is reachable only as a base parent.

## Upstream inspection (what the contract is built on)

Selected pin from the seam: `persesdev/perses:v0.55.1`, product version
`v0.55.1`, Prometheus plugin `v0.6.0`.

Verified from the upstream release page and the v0.55 configuration and security
documentation:

- v0.55.1 (2026-11-02) is the current release line; it restricts dashboard,
  panel, table-data and trace-panel link URL schemes to a relative-plus-allowlist
  set and upgrades Go to 1.27.3 for `crypto/x509` fixes.
- v0.55.0 (2026-10-21) is the security line: JWT forgery, SSRF and credential
  leaks through the datasource proxy, arbitrary file reads and path traversals,
  several reachable without authentication under the default configuration.
  Its fixes make an encryption key mandatory when authentication is enabled
  (#4550) and deny loopback, link-local, cloud-metadata and Kubernetes-API
  proxy destinations by default (#4518); the proxy no longer forwards caller
  credentials to the datasource (#4553).
- Perses authentication is DISABLED by default (`security.enable_auth: false`),
  and in that mode anyone who can reach the API can create datasources and use
  the proxy to read any service the server can reach. This is the specific
  hazard this card must close; it is why the surface can never be reported as
  configured on that posture.
- A user who can use a datasource obtains the plaintext of every secret that
  datasource references, so datasource access must be granted with the same care
  as the secrets themselves.
- Proxied responses are served under the Perses origin, so upstream strips
  `Set-Cookie`, `Clear-Site-Data`, `Refresh`, `Strict-Transport-Security`,
  `Alt-Svc`, `Service-Worker-Allowed`, CORS and non-relative `Location`
  headers, and adds a sandboxed CSP plus `X-Content-Type-Options: nosniff`.
- Datasource proxy network precedence: the most specific prefix wins; on equal
  length an allowed network wins. Private networks are allowed by default and
  need `deny_private_networks`, `denied_networks` or `allowed_hosts` to
  restrict. The Kubernetes API service address is denied as a single host, so a
  broad private allow does not re-open it.

## Acceptance evidence, criterion by criterion

### Criterion 1 — verified pinned release, native format, coverage stated

Test `TestPersesSecurityPolicyRejectsVulnerablePins` proves the pin floor
mechanically instead of trusting the constant. Output:

```
=== RUN   TestPersesSecurityPolicyRejectsVulnerablePins
=== RUN   TestPersesSecurityPolicyRejectsVulnerablePins/pre-fix_release_is_unsupported
=== RUN   TestPersesSecurityPolicyRejectsVulnerablePins/older_patch_of_the_fix_line_is_unsupported
=== RUN   TestPersesSecurityPolicyRejectsVulnerablePins/the_fix_release_itself_is_allowed
=== RUN   TestPersesSecurityPolicyRejectsVulnerablePins/the_pinned_release_is_allowed
=== RUN   TestPersesSecurityPolicyRejectsVulnerablePins/a_newer_line_is_allowed
=== RUN   TestPersesSecurityPolicyRejectsVulnerablePins/pre-release_of_a_newer_line_is_allowed
=== RUN   TestPersesSecurityPolicyRejectsVulnerablePins/a_pre-release_of_the_floor_line_is_denied
--- PASS: TestPersesSecurityPolicyRejectsVulnerablePins (0.00s)
```

`v0.54.0` and `v0.53.1` are rejected with a message naming the missing SSRF and
credential-forwarding fixes; `v0.55.0`, `v0.55.1` and `v0.56.0` validate.
`TestPersesSecurityPolicyDefaultValidates` additionally asserts the compiled
default pin is exactly the current security release and clears the floor.

Grafana-API compatibility is not assumed anywhere: no cell, no code path and no
document in this change reaches a Grafana UI API or converts dashboard JSON.
The Prometheus datasource plugin version stays a separate pinned field.

Missing coverage is stated explicitly rather than papered over, following the
seam's three-state rule: `PersesReachabilityUnverified` remains the only
reachability this Core can produce, and `verified` stays unreachable without a
real health probe. This card adds no probe and claims none.

### Criterion 2 — access scoped by real Target/tenant permissions, fail closed, no secret leakage

`TestEvaluatePersesOperatorAccessFailsClosedWithoutIdentity` covers five
distinct unattributable shapes, each with its own reason code:

```
=== RUN   TestEvaluatePersesOperatorAccessFailsClosedWithoutIdentity/anonymous_request
=== RUN   TestEvaluatePersesOperatorAccessFailsClosedWithoutIdentity/unverified_principal
=== RUN   TestEvaluatePersesOperatorAccessFailsClosedWithoutIdentity/verified_identity_without_tenant_membership
=== RUN   TestEvaluatePersesOperatorAccessFailsClosedWithoutIdentity/membership_without_a_management_role
=== RUN   TestEvaluatePersesOperatorAccessFailsClosedWithoutIdentity/attributed_identity_on_an_unknown_target
--- PASS: TestEvaluatePersesOperatorAccessFailsClosedWithoutIdentity (0.00s)
```

Scoping is not self-declared: the tenant comes from `tenancy.FromContext` and
the principal from `identity.FromContext`, so the same verified issuer+subject
carrying a foreign tenant cannot be admitted. `TestPersesOwnershipErrorIsTheSentinelForUnattributableRequests`
asserts `ErrPersesOwnershipUnknown` for both the anonymous and the
unattributed-Target shape.

`TestEvaluatePersesOperatorAccessAllowsVerifiedRoles` shows the positive half —
`admin`, `editor`, `viewer` and `audit` map to concrete management roles, the
decision names `tenant-alpha`, and even an ALLOWED operator still gets the
datasource-proxy route refused:

```
--- PASS: TestEvaluatePersesOperatorAccessAllowsVerifiedRoles (0.00s)
```

`TestEvaluatePersesOperatorAccessReadOnlyDeniesMutatingRoles` proves the
admission is honest about what the surface can serve: under a read-only
deployment the admin and edit roles are denied while the view role is still
admitted.

Secret safety, on the real public output:
`TestBahaStatusPersesAccessOutputCarriesNoCredentialNames` runs the genuine CLI
and rejects the gateway health-authorization variable, the access-token
variable, `encryption_key`, `server-key` and `password` in the rendered JSON;
`TestPersesAccessDecisionCarriesNoSecretMaterial` makes the same assertion on
the decision object a status record or audit entry consumes. Credentials are
referenced by file path in the requirements struct, never by value.

Optional visualization forces no new capability and no mandatory service: the
manifest gate stays `services.observability.management_ui && services.perses`
and the two pre-existing manifest cells still pass
(`TestManifestPersesManagementUIRoundTripFailsClosedWithoutMetrics`,
`TestManifestPersesSelectionRequiresPinnedRelease`).

`TestPersesStatusCannotReportConfiguredForAnonymousSurface` is the conjunction
that closes the gap this card was written for:

```
--- PASS: TestPersesStatusCannotReportConfiguredForAnonymousSurface (0.00s)
```

An anonymous posture reports `not_configured`, a protected selected posture
reports `configured_unverified`, and no posture at all can produce `verified`.

### Criterion 3 — backend ownership preserved, proxy SSRF inspected

Only two product lines outside new files changed: an appended role-mapping field
in the observability surface entry of
`internal/application/management_ui.go`, and the new fail-closed conjunction
function in `internal/capability/perses.go`. Prometheus, Loki and Tempo keep
their own files, providers, lifecycles and removal logic untouched — nothing is
removed by this card at all, so no foreign resource can be collected.

The seam's own regression cells still pass unchanged, including
`TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI`,
`TestBahaStatusPersesConfiguredUnverifiedPositive` and
`TestBahaStatusPersesNotConfiguredWhenUnselected`, so the existing three-state
contract is intact.

Proxy SSRF resolution:

```
=== RUN   TestPersesProxyDestinationDeniesUpstreamDefaultSet/http://127.0.0.1:9090
=== RUN   TestPersesProxyDestinationDeniesUpstreamDefaultSet/http://169.254.169.254/latest/meta-data/
=== RUN   TestPersesProxyDestinationDeniesUpstreamDefaultSet/http://169.254.170.2/creds
=== RUN   TestPersesProxyDestinationDeniesUpstreamDefaultSet/http://100.100.100.200/latest/meta-data
=== RUN   TestPersesProxyDestinationDeniesUpstreamDefaultSet/http://168.63.129.16/
=== RUN   TestPersesProxyDestinationDeniesUpstreamDefaultSet/http://[fe80::1]/
=== RUN   TestPersesProxyDestinationDeniesUpstreamDefaultSet/http://[::ffff:127.0.0.1]:9090/
=== RUN   TestPersesProxyDestinationDeniesUpstreamDefaultSet/http://[fd00:ec2::254]/
=== RUN   TestPersesProxyDestinationDeniesUpstreamDefaultSet/http://0.0.0.0:1/
--- PASS: TestPersesProxyDestinationDeniesUpstreamDefaultSet (0.00s)
--- PASS: TestPersesProxyDestinationMostSpecificWinsAgainstDefaultDeny (0.00s)
--- PASS: TestPersesProxyDestinationDeniesPrivateNetworksWhenConfigured (0.00s)
--- PASS: TestPersesProxyDestinationRejectsCredentialsAndSchemes (0.00s)
--- PASS: TestPersesProxyDestinationAllowedHostsListIsAuthoritative (0.00s)
--- PASS: TestPersesProxyDestinationFailsClosedOnUnparseableEndpoints (0.00s)
```

The precedence tests pin the documented upstream behaviour, including the two
cases where a naive implementation gets it backwards: allowing `127.0.0.0/8`
does open loopback (equal length, allow wins), while allowing `169.254.0.0/16`
does NOT open `169.254.169.254` (the single host is more specific). IPv4-mapped
IPv6 is checked against the embedded IPv4 address. `TestPersesProxySafeDefaultsAreStatedAndSorted`
asserts the deny set is stated, ordered and non-empty, so status output can name
what is enforced.

Credential exposure: forwarding user credentials to datasources is refused
(`TestPersesSecurityPolicyRejectsCredentialForwarding`), a datasource URL
carrying `user:password@` is refused, and the gateway upstream itself refuses
embedded credentials
(`TestNormalizedPersesUpstreamRejectsCredentialBearingAndRoutableAddresses`).

Gateway transport: `TestBuildPersesGatewayDeniesDatasourceProxy` and
`TestPersesComposeServicesNeverPublishesPersesDirectly` prove the Perses
container gets no `ports:` block at all while the gateway publishes only on
`127.0.0.1:${BASEHARBOR_PERSES_UI_HOST_PORT}`, and that rendering re-checks the
posture rather than trusting the plan shape:

```
--- PASS: TestBuildPersesGatewayDeniesDatasourceProxy (0.00s)
--- PASS: TestPersesComposeServicesNeverPublishesPersesDirectly (0.00s)
--- PASS: TestBuildPersesGatewayRefusesAnonymousSurface (0.00s)
--- PASS: TestBuildPersesGatewayRequiresGatewayAuthentication (0.00s)
--- PASS: TestPersesGatewayTokenAuthenticationRequiresTokenFileReference (0.00s)
--- PASS: TestPersesProxySSRFDenyNetworksAddsTargetKnowledge (0.00s)
--- PASS: TestEnsurePersesGatewayMaterialRequiresIssuerAndTLS (0.00s)
```

No unverified token mode was invented: `persesEffectiveAccess` maps only the four
classes the management-access vocabulary already defines, and an unknown class
degrades to `unsupported` — never to a permissive set
(`TestPersesAccessRoleMappingsAreFullyClassified`, case
`an_unknown_class_degrades_to_unsupported`).

### Criterion 4 — alerting evaluator and notification owner

No native Perses alerting or contact-routing parity is claimed anywhere in this
candidate: no rule evaluator, no notification owner, no alerting route, no
external notification default. Those belong to `t-20261114-r28-perses-contact-routing`,
which this card blocks, and to the approved contract for it.

What this card does enforce is the negative half that the routing card cannot
work around: `DefaultPersesSecurityPolicy` never enables external
notifications, `PersesProxySSRFDenyNetworks` closes the egress path a
misconfigured notification or proxy target would use, and every route-prefix
decision is derived from the policy rather than asserted by a caller
(`PersesDeniedProxyPaths`). A later routing card therefore cannot obtain an
outbound path by editing its own layer alone.

## Required checks

Candidate SHA: `872c6c701f00941521be153320ea1f6d122d3066`.

Every check below was executed by this session in the worktree
`/tmp/opencode/welle2-089/bh`.

```
go build ./...                                  clean
go vet ./...                                    clean
gofmt -l internal/ cmd/                         (no output)
go build -o /tmp/opencode/welle2-089/baha ./cmd/baha   OK
bash scripts/documentation-audit.sh             all sections PASS
python3 scripts/check_docs_locale_parity.py     EN/DE page coverage OK: 167 matched Markdown pages
python3 scripts/check_de_translation_integrity.py  DE technical integrity: PASS (167 paired pages)
bash scripts/source-readability-audit.sh        see note below
```

The readability audit reports `internal/application/manifest_parse.go has 821
lines (limit: 800)`. That file is not touched by this card, and the audit exits
1 identically on the base tree (`git stash -u` then re-run: exit 1). Pre-existing
on the stacking base, not introduced here.

Focused tests, all executed with `-count=1` (59 Perses-named cells across four
packages, all PASS; the full pass list is reproduced in the transcript above).
The new cells added by this card:

`internal/capability` (`go test ./internal/capability/ -run Perses`):
`TestPersesSecurityPolicyRejectsAnonymousExposure`,
`TestPersesSecurityPolicyRequiresEncryptionKeyWhenAuthEnabled`,
`TestPersesSecurityPolicyRejectsVulnerablePins` (7 subtests),
`TestPersesSecurityPolicyRequiresProxyRestriction`,
`TestPersesSecurityPolicyRejectsCredentialForwarding`,
`TestPersesSecurityPolicyValidatesNetworkAndSchemeSyntax` (7 subtests),
`TestPersesSecurityPolicyAcceptsAbsoluteSecretDirectories`,
`TestPersesProxyDestinationDeniesUpstreamDefaultSet` (12 subtests),
`TestPersesProxyDestinationDeniesPrivateNetworksWhenConfigured`,
`TestPersesProxyDestinationMostSpecificWinsAgainstDefaultDeny`,
`TestPersesProxyDestinationRejectsCredentialsAndSchemes`,
`TestPersesProxyDestinationAllowedHostsListIsAuthoritative`,
`TestPersesProxyDestinationFailsClosedOnUnparseableEndpoints`,
`TestPersesStatusCannotReportConfiguredForAnonymousSurface`,
`TestPersesSecurityPolicyDefaultValidates`, `TestPersesProxySafeDefaultsAreStatedAndSorted`.

`internal/serviceaccess` (`go test ./internal/serviceaccess/ -run Perses`):
`TestBuildPersesGatewayRefusesAnonymousSurface`,
`TestBuildPersesGatewayRequiresGatewayAuthentication`,
`TestBuildPersesGatewayDeniesDatasourceProxy`,
`TestBuildPersesGatewayRendersProxyRefusalWithoutLeakingSecrets`,
`TestPersesGatewayTokenAuthenticationRequiresTokenFileReference`,
`TestNormalizedPersesUpstreamRejectsCredentialBearingAndRoutableAddresses` (5 subtests),
`TestPersesProxySSRFDenyNetworksAddsTargetKnowledge`,
`TestPersesComposeServicesNeverPublishesPersesDirectly`,
`TestEnsurePersesGatewayMaterialRequiresIssuerAndTLS`,
`TestPersesGatewayMaterialProjectionKeepsPrivateKeyOwnerOnly`.

`internal/application` (`go test ./internal/application/ -run Perses`):
`TestEvaluatePersesOperatorAccessFailsClosedWithoutIdentity` (5 subtests),
`TestEvaluatePersesOperatorAccessAllowsVerifiedRoles` (4 subtests),
`TestEvaluatePersesOperatorAccessRefusesAnonymousSurfaceEvenForAdmin`,
`TestEvaluatePersesOperatorAccessRefusesVulnerablePin`,
`TestEvaluatePersesOperatorAccessRefusesSSRFDatasourceEndpoint` (3 subtests),
`TestEvaluatePersesOperatorAccessAllowsScopedDatasource`,
`TestEvaluatePersesOperatorAccessReadOnlyDeniesMutatingRoles`,
`TestPersesRoleMappingsNeverClaimUnsupportedAuthorization` (3 subtests),
`TestPersesAccessDecisionCarriesNoSecretMaterial`,
`TestPersesGatewayPlanForRequiresSelectionAndPolicy`,
`TestValidatePersesEndpointTrustRejectsPlainOrRoutableEndpoints` (4 subtests),
`TestPersesOwnershipErrorIsTheSentinelForUnattributableRequests`.

`cmd/baha` — genuine CLI path (`go test ./cmd/baha/ -run PersesAccess`):
`TestBahaStatusPersesAccessDeclaresUnsupportedRoleMappings`,
`TestPersesAccessRoleMappingsAreFullyClassified`,
`TestBahaStatusPersesAccessOutputCarriesNoCredentialNames`,
`TestPersesAccessContractIsFailClosedOnMissingPin`. The first and third execute
`baha status --json` through `runWithIO` over an isolated temporary root and
decode the public report; no internal helper stands in for the command.

Determinism: the capability and serviceaccess Perses cells were run three times
consecutively with `-count=1` and produced identical `ok` results.

### CI routing for every new test (Owner directive 2026-11-07)

Every test added by this card is a plain Go unit or CLI test inside an existing
package under an existing CI group, so no workflow change is needed and none was
attempted:

- `internal/capability`, `internal/serviceaccess`, `internal/application`,
  `internal/metrics`, `cmd/baha` are all ordinary packages of the module and run
  in the repository's Go test job for every pull request that changes them.
  Trigger: `pull_request` on this candidate SHA. The new files are inside those
  same packages, so they are picked up by the existing package-list selection
  with no new path filter.
- The documented spec pages run under the documentation audit job
  (`scripts/documentation-audit.sh` plus the EN/DE parity and DE integrity
  scripts), triggered on `pull_request` for `docs/**` changes. Both checks were
  also executed locally and are reproduced above.

No test in this card is local-only or VM-only. `TestPersesGatewayMaterialProjectionKeepsPrivateKeyOwnerOnly`
uses `t.TempDir()` only, and no cell requires a container.

## STATE: failing check inherited from the stacking base

`internal/metrics` `TestPersesIsNotAnApplicationCapability` fails at the current
seam head `cb4367f3`, before any commit of this PR:

```
--- FAIL: TestPersesIsNotAnApplicationCapability (0.00s)
    perses_contract_test.go:53: perses must not declare application capabilities, got 1
```

Witness that this is not this card's doing: the failure is present on
`cb4367f3` itself (the base head), where no file of this card exists.

Cause: the seam r2 commit `cb4367f3` bound `PersesManagement` to the `Metrics`
capability kind and its `MetricsV1` specification and updated
`internal/capability/perses_test.go` accordingly, but left the sibling
assertion in `internal/metrics/perses_contract_test.go:52` checking
`len(desc.Capabilities) != 0`. The two files now encode contradictory
expectations for the same field.

Needed change, reported rather than made (file is 0428-075's, and the semantic
choice belongs to that card's owner):
`internal/metrics/perses_contract_test.go:51-56` must assert against
`desc.Provider.Capabilities` (which stays empty of any Perses-invented
capability) or re-express the "not an application capability" intent in the
same form `internal/capability/perses_test.go:44-58` now uses, and the
`desc.Validate()`-must-fail assertion on line 55 is now inverted by the r2
descriptor and must be dropped or moved. Assign to card 0428-075.

This card deliberately does NOT touch that file: it is outside the 0428-089
write-set, and silently editing another card's failing assertion would hide the
defect from the review that must decide which of the two expectations is right.

## repo-rule compliance

- AGENTS 4.1 reality check: remote develop, seam branch and planning main were
  fetched and read before editing, and re-read after the push. The mid-flight
  base move was handled by merging the current base, not by ignoring it.
- AGENTS 4.2 task contract: work stays inside the Goal and Scope of
  t-20261114-r28-perses-secure-access — a dedicated gateway/auth policy adapter
  plus the access and transport contract. No capability was invented, no
  provider registry, CLI surface or schema was widened, no lifecycle work was
  pulled in from the sibling runtime card. The prerequisite cards are not
  accepted; the mission's stacking rule is the sanctioned way to work on that
  base anyway, so this lane proceeded rather than parking.
- AGENTS 4.3 ownership: claimed via `plan.py claim` and published before any
  code edit (`08ac9c64` on planning main). One card, one branch, one PR. Writes
  are confined to this card's files; nothing in `.github/**` and no other
  card's file was touched.
- AGENTS 4.4 visible plan: this PLAN list plus the live board file
  `workers/todos/mission-welle2-089.md.json`. No native `todowrite` tool is
  exposed in this session, so the board file carries the plan; per the mission
  that is the mandatory and sufficient leg.
- AGENTS 4.5 focused tests: smallest matching checks first, batched into one
  verification candidate; only targeted `git add <file>`, never `git add -A`.
- AGENTS 4.6 own-run duty: every local command above was run by this session
  and its output read. No hosted run was launched or re-run by this lane, and no
  workflow file was triggered, per the scope split; the hosted CI result for
  `872c6c70` belongs to PR #1599 and its check names are reported as observed
  once the checks are visible.
- AGENTS 4.8 no subagents: every step, including all six new files, both
  documentation pages, all test cells and this akte, was produced inside this
  session. No agent/task/subagent tool was invoked, and nothing was delegated
  for writing, pushing, reviewing or checking.
- Keep runtime, capability and delivery separate: this card changes contract,
  gateway-policy and authorization code only. No container was started and no
  lifecycle path was edited.
- Fail-closed mutations: nothing here applies, plans or preflights a deployment;
  the card states what a future realization must enforce.
- Secret protection: credentials stay path-referenced; no token, key or
  encryption-key value is stored in a struct field that can be marshalled into
  a manifest, a log or status output, and two cells assert that on the rendered
  JSON.
- Docs: followed the style guide, kept both locales in step (167 matched pages,
  DE integrity PASS), and added no manual edits to generated views.
- CI discipline: no workflow file was edited, no rerun or workflow_dispatch was
  issued, no runner was built or repaired, and no heavyweight native matrix was
  launched — the change touches no runtime path, so the focused unit and CLI
  cells plus the docs gates cover the actual risk.

## cleanliness

Work happened only in the own worktree `/tmp/opencode/welle2-089/bh` and the
scratch directory `/tmp/opencode/welle2-089/` (before/after baselines below).

`docker ps -a --format '{{.Names}} {{.Status}}'` before any command in this lane:

```
(empty: no containers)
```

`docker network ls --format '{{.Name}}'` before:

```
bridge
host
none
```

No container, compose project, volume or network was created by this lane: no
`up`, no `compose`, no `apply`, no `preflight`. The only runtime touch was the
read-only `docker ps` / `docker network ls` baselines above and one pre-existing
`cmd/baha` cell that inspects the daemon.

`docker ps -a --format '{{.Names}} {{.Status}}'` and `docker network ls
--format '{{.Name}}'` after the last test run:

```
(empty: no containers)
bridge
host
none
```

cleanliness: clean — no test-owned containers, networks, volumes or state
directories; the before and after inventories are identical; ambient
core/other-card images and projects were left untouched.

`git status --porcelain` in the worktree at the final push: empty (all fifteen
changed paths committed on one branch).

No scratch, cache or stray file was created under
`/home/marcel/dev/baseharbor-ecosystem/` itself.

## END lane-welle2-089 DONE

Candidate: `872c6c701f00941521be153320ea1f6d122d3066` on
`lane-welle2-089-perses-secure-access`, draft PR
https://github.com/mcpdev80/baseharbor/pull/1599 against
`lane-0428-075-perses-seam`. Card claimed, code and tests committed and pushed,
all local checks executed, one failing check reported as STATE and assigned to
its owner (0428-075). No merge, no ready_for_review, no `.github/**` change, no
subagent, no container.
