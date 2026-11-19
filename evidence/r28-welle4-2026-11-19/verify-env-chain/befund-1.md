# befund-1 — verify-env-chain (r28-welle4, 2026-11-19)

Mission: `mission-verify-env-chain.md` — live-verify the merged environment chain (0428-115 / 0428-125 / 0428-126) on living develop. No product change, no PR, unit tests only.

Revision labels: r1 (this dossier, single pass, all theses confirmed; one sub-finding recorded under T4).

## Witnesses (W1-W2)

W1 reality check — live develop head (`git -C <clone> fetch origin develop && git -C <clone> ls-remote origin refs/heads/develop`):

    da76c5cf9c963207038d5599bd130b89ecb1e8a4        refs/heads/develop

Mission-pinned da76c5cf9 = live head. Working zone: fresh clone `file:` from GitHub `https://github.com/mcpdev80/baseharbor.git` at `/var/tmp/verify-env-chain-wt/repo`. NOTE: the local product checkout's develop refs are stale (clone from it first yielded `907f16713`, which lacks the chain); all inspection here goes through `git show origin/develop:<path>` in the fresh clone — never a stale local checkout.

W2 basis attestation (`git merge-base --is-ancestor <sha> origin/develop; echo $?`), all in the fresh clone:

    0428-115  50f87cfb8dd6e87913044f96cc0204af1423b61c  exit=0  (contained)
    0428-125  21161b101f66a47fb1a253ae17e87fe82567ba4d  exit=0  (contained)
    0428-126  da76c5cf9c963207038d5599bd130b89ecb1e8a4  exit=0  (contained, = head)

## T1 (0428-115) — both identity-write guards named in help text, EN and DE

BESTAETIGT.

- DE, exact SQL form — `docs/de/decisions/0020-scoped-connector-enrollment.md:44` (W4, `git show origin/develop:... | sed -n '43,45p'`):
  ``certificate_serial IS NULL` und `consumed_at IS NOT NULL` in `RecordIssued` verhindern, dass ein konkurrierender``
  Both guards named at one place (line 43 names the consume-side `previous_certificate_serial` clause separately, as the ADR distinguishes consume vs identity write).
- EN, prose form — `docs/decisions/0020-scoped-connector-enrollment.md:43` (W4, sed 41,43):
  `serial-is-null guard plus consumed-grant predicate in the identity write prevent a`
  Both guards named: serial-is-null and the consumed-grant predicate (`consumed_at IS NOT NULL` in the identity-write subquery; the SQL itself is `internal/database/connector_enrollment.go:126,128` — `certificate_serial IS NULL` and `... token_digest=$5 AND consumed_at IS NOT NULL` in `RecordIssued`).
- Supporting store-contract comment — `internal/targetenrollment/authority.go:59`: names only `certificate_serial IS NULL` (r3 commit 711e04c3 deliberately kept this comment to the serial-race condition; the consumed-grant predicate is documented in the ADR, which is what the thesis names).

Why the witness carries the thesis: the thesis speaks of the help text (Hilfs-/ADR text) of the two shipped decision documents. Both EN and DE name the two identity-write guard conditions in parallel, at one sentence each, and the named conditions match the SQL that actually executes in `RecordIssued`. W2 proves commit 50f87cfb8 (the r5 DE-fix commit) is contained in the live head.

## T2 (0428-125) — environment in the key formula at one place; resource id derives; no collision

BESTAETIGT.

- Key formula at exactly one place — `internal/metrics/runtime_source.go:219` (`runtimeTargetFileName`):
  `sum := sha256.Sum256([]byte(e.environment + "\x00" + request.Application + "\x00" + request.CallerService + "\x00" + request.ResourceName))`
  Comment at line 207: "The key formula for a runtime-metrics target file is defined here and nowhere else."
- Resource id derives from the same formula — `internal/metrics/runtime_source.go:223` (`runtimeMetricsResourceID`) recomputes the identical `e.environment + \x00 + Application + \x00 + CallerService + \x00 + ResourceName` digest and prefixes `res-metrics-`. All `Create/Get/Delete` result paths return it (lines 58, 64, 70), so no second id formula exists.
- Targeted test run (W3, `-count=1` on the live head):
  `go test ./internal/metrics/ -run 'TestRuntimeSourceSeparatesTargetFilesPerEnvironment'`
  --- PASS: TestRuntimeSourceSeparatesTargetFilesPerEnvironment (0.00s)
  ok  github.com/mcpdev80/baseharbor/internal/metrics 0.005s
  The test writes dev+prod into ONE shared temp targets dir and asserts distinct file paths, distinct resource ids, and that a later prod write does not break the earlier dev `runtime.get` (the hunt-918 Befund-7 collision).

Why the witness carries the thesis: `environment` occurs once inside the single sha256 input of the file-key function; the resource-id function mirrors that exact input; and the shipped regression test exercises the two-environment collision scenario and passes on da76c5cf9.

## T3 (0428-126) — every acknowledging stage prints the Warning marker; gate semantics unchanged

BESTAETIGT.

- Marker construction — `cmd/baha/provider_change_confirmation.go:62-68` (W4): `providerImpactAttentionLead` returns `"Warning: "` iff `plan.Attention != ""`, else `""` (presentation only).
- Leads wired at every custom label (diff of da76c5cf, `git show da76c5cf -- cmd/baha/provider_change_confirmation.go`): apply stage both labels (lines 71, 73), single-confirmation non-destructive stage (line 91). All other stage labels come from `application.ProviderImpactConsentCatalog()` whose labels already lead with `Warning: ` (`internal/application/provider_change_consent.go:35-38`). Scope-derived call sites propagate `Scope.Attention` (e.g. `cmd/baha/runtime_destroy_impact.go:193`, `cmd/baha/target_definition_change.go:41`).
- Gate untouched: `internal/application/provider_change_scope.go:54-60` sets `Attention="Warning"` and two confirmations on incomplete/destructive scopes; `ValidateProviderChangeConsent` (`provider_change_consent.go:66-77`) keys only on plan id + First/Second/DeleteData — never on the lead. The lead function reads `plan.Attention` but the validation path never sees it.
- Marker test (W3): `go test ./cmd/baha/ -run 'TestProviderImpactMarkerPrintedOnEveryAcknowledgingStage'`
  --- PASS (0.00s)  ok  github.com/mcpdev80/baseharbor/cmd/baha 0.007s
- Counter-test, gate still hard (W3): `go test ./cmd/baha/ -run 'TestOrdinaryYesNeverAcknowledgesProviderEffects'`
  --- PASS (0.00s)  ok  0.008s — `--yes`/machine approval still never substitutes for stage acknowledgements.
  Additional gate-strength assertions run in the T4 cross test below.

Why the witness carries the thesis: the marker is unconditional at every acknowledging label (custom leads + catalog labels both keyed by attention presence), and the two passing tests together prove (a) the marker appears per stage and (b) the gate remains hard and unchanged.

## T4 (quer) — the three changes do not contradict each other

BESTAETIGT — with one sub-finding (see below).

- Single unit-level cross run (task-local test, lives only in `/var/tmp/verify-env-chain-wt/repo/cmd/baha/cross_verify_env_chain_task_local_test.go`, never committed to the product repo):
  `TestCross0428ChainEnvironmentMarkerGuards` binds two environments into one targets dir through the live `metrics.RuntimeSourceExecutor` (distinct resource ids + readable after cross-write, 0428-125 path), composes a scope (0428-126 attention semantics: complete plan -> no marker, incomplete -> `Warning` + 2 stages), asserts the marker on the apply stage both ways, hard-gates stage two and data deletion separately, and asserts both 0428-115 guard strings exist in the shipped EN and DE ADO text.
  --- PASS: TestCross0428ChainEnvironmentMarkerGuards (0.00s)
  ok  github.com/mcpdev80/baseharbor/cmd/baha 0.008s
- Mutation control: with `providerImpactAttentionLead` mutated to return `""`, the cross test FAILS and the shipped `TestProviderImpactMarkerPrintedOnEveryAcknowledgingStage` FAILS; after restore both PASS and `git diff` proves the product tree untouched. The tests are sensitive to exactly the chain's behavior.
- No shared-file conflict: 115 touches docs ADO EN/DE + authority.go comment; 125 touches internal/metrics; 126 touches cmd/baha + docs marker naming. Disjoint write-sets, and each shipped regression test passes on the combined head.

Sub-finding (documentation, not a contradiction): the EN consent hint was renamed German->`Warning` by 0428-126, but EN pages that render the DE catalog label verbatim still name the pre-rename marker: `docs/spec/capability-first-v0425.md` (line ~216/327 pattern "show **Achtung** and require two..."), `docs/reference/cli.md` and other EN pages carry `**Achtung**` where the shipped EN catalog strings say `Warning: ...`. Severity: low (purely presentational EN doc inconsistency; gate and CLI output unaffected). Kartenwuerdigkeit: yes, small EN-docs alignment card. Per mission (Widerspruchsfall -> QUESTION): noted, not fixed here.

## PLAN (mission work plan)

- DONE W1 reality check: fetch + ls-remote live develop (da76c5cf9 confirmed)
- DONE W2 basis attestation: all three chain SHAs ancestor-of origin/develop (exit=0 each)
- DONE T1 (0428-115): both identity-write guards in EN+DE help text — file:line witnesses
- DONE T2 (0428-125): environment once in key formula, resource-id derives, collision test PASS
- DONE T3 (0428-126): marker at every stage + gate-hard counter-test PASS
- DONE T4 (quer): single cross unit run + mutation control; sub-finding recorded
- DONE Evidence on origin/main (W5), cleanliness, END post

## Cleanliness

- No containers/compose/networks/volumes were started (unit tests only; R1 respected — nothing on this host).
- Own processes started by this lane: transient `go test`/`git` commands only; none remain (pgrep at end shows only this shell).
- Zone: `/var/tmp/verify-env-chain-wt/` (repo clone + task-local test + before/after snapshots). Deletable; nothing outside /var/tmp was created except this evidence file in baseharbor-plan.
- cleanliness: besenrein — no product-repo commits, no branches, no PRs, no CI triggers, no leftover processes.

END markers: see END line at the bottom of this file and the coordinator post.

W5 evidence-on-remote witness (`git -C baseharbor-plan fetch origin main && git -C baseharbor-plan show origin/main:evidence/r28-welle4-2026-11-19/verify-env-chain/befund-1.md | head -20`): first remote publication was commit dc8d85157b2cd76ff2f954f749c91d6f9fa9d329 and the head-20 lines returned the file (pasted in this dossier's history); the final act SHA on origin/main is d900706d843cb655fb0ee74609ad2845d262dc69.

END_DONE mission-verify-env-chain.md: develop da76c5cf9; T1 confirmed (W4 file:line EN 0020:43 / DE 0020:44, guards in live SQL connector_enrollment.go:126-128); T2 confirmed (W4 runtime_source.go:219/223 + W3 TestRuntimeSourceSeparatesTargetFilesPerEnvironment PASS); T3 confirmed (W3 TestProviderImpactMarkerPrintedOnEveryAcknowledgingStage PASS + counter TestOrdinaryYesNeverAcknowledgesProviderEffects PASS, W4 provider_change_confirmation.go:62-68); T4 confirmed (W3 cross TestCross0428ChainEnvironmentMarkerGuards PASS + mutation control FAIL-then-PASS; sub-finding: EN docs still name 'Achtung' in catalog-label renderings — low severity, kartenwuerdig, QUESTION-worthy only if you want the card now). No product change, no PR. cleanliness: besenrein.
