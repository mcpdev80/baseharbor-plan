# 0427-159 r4 — F2 ValidateDeploymentID gate + F3 production-path no-false-attribution + F4 CI-owned regression

- Card / mission: 0427-159 (task `t-20261108-bughunt-damaged-state-misleading-error`, kanban active), mission-159-r4
- Review judged (verdict = correction, approval withheld): `evidence/bughunt-damaged-state-misleading-error/act-1499-review-r3.md`
- Prior rebuttal (r3): `evidence/bughunt-damaged-state-misleading-error/round-3.md` (F1 fixed, F2/F3/F4 rebuttal filed; F2/F3/F4 remain genuinely OPEN per r3 review)
- Shift / planning repo verified (origin/main): see witness below (`git ls-remote origin main`)
- Product base (candidate branch base): `3187cea15728143146905c7238ad6e280ca11b3e`
- Candidate branch: `0427-159-damagedstate`, live head `9e211715187534d9939a39702cd28a726d83581e` (PR #1499)
- develop HEAD (drift to integrate): `20902f0a6ab016fd8fe6a501751e1becc5f334dd`

## PLAN

- Read mission r4, act-1499-review-r3 verdict, round-3 rebuttal; verify PR #1499 head 9e211715, develop 20902f0a6, base 3187cea15 ancestry
- Trace F2: listDeploymentRecords/DamagedDirectoryState accept non-UUID dirs; design ValidateDeploymentID gate
- Trace F3: registry path DamagedDeploymentState + EnrichNetworkForOwnIdentity fills identity from request params -> foreign orphan misattributed; design unknown-owner fix
- Implement F2 ValidateDeploymentID gate in deployment_list.go (malformed dir discarded, not advertised)
- Implement F3 fix: foreign/unknown-owner orphan never acquires request app identity; return unknown-owner not request app
- Add F4 regressions through real FindDeployment/resolvedRepositoryApplication path proving no app-A attribution for a foreign/unknown damaged dir, valid-UUID damaged, malformed discarded, BF-03 owned-app still reports exact network
- Local checks: go build, go vet, targeted tests; gofmt clean
- Integrate develop HEAD 20902f0a6 (rebase) into candidate chain; verify exact head; single chain, base ancestor
- Push to #1499; trigger hosted CI; monitor terminal (only 172-domains red allowed, STATE with line)
- Publish evidence to origin/main before END; ls-remote witness + cleanliness; bring down any stack; END only when terminal
- Post END in shared inbox (terminal only)

## Design (resolved against r3 review)

The r3 judge rejected the r3 rebuttals that declared F2/F3/F4 "not open." This round implements the r3 correction recipes rather than arguing them.

- F2 (malformed directory names): `listDeploymentRecords` currently calls `DamagedDirectoryState` on every directory entry before any shape check. Add a `ValidateDeploymentID` gate so a non-UUID entry is discarded (skipped), never advertised as deployment damage. The damaged-signature / artifact logic is unchanged for a valid UUID.
- F3 (production-path no false attribution): the registry path at `cmd/baha/app_context.go` fills the listing damaged error's identity from the *request* parameters (`m.ApplicationID`, `m.Name`, `m.Environment`) and then derives the workload network from that request identity, so a foreign/unknown-owner orphan's absent network is attributed to the requested app. The r3 recipe: preserve the orphan's owner as unknown until a trusted retained-identity source binds it to the requested app; if no such binding exists, return an explicit target-level / unknown-owner damaged-state conflict that does NOT name the requested app's record or network. Match the damaged entry using a retained identity source before returning an app-specific error.
- F4 (CI-owned regression): keep the regressions in the existing `go-unit-tests` / `deployment-package-tests` groups (`go test ./...`, `on: pull_request`) — no `.github/**` edit. The regression asserts ownership attribution through the actual resolver/listing path.

## repo-rule compliance

- Evidence lives only in baseharbor-plan. No product repo edits land outside the candidate branch; no `.github/**` edit; no rerun/dispatch; no containers/compose started on any host.
- Subagents: none (4.8) — every step executed inside this own session.
- Planning repo verified (origin/main) witness pasted below in the Run section.
- No markdown checkbox lines anywhere in this evidence file (plain bullets only).

## END

<state>in progress</state>
