# 0427-159 — Damaged deployment state: reintroduce the missing-network damage on the NETZ side

- Card / mission: 0427-159 (task `t-20261108-bughunt-damaged-state-misleading-error`, kanban active)
- Evidence round: round-3 (corrective implementation per `act-1499-review.md`, recipe plan `4dfe8184`)
- Source of the defect: bug-hunt dossier `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md` — BF-03, `deployment.json` deleted + network removed
- Shift / planning repo verified (origin/main): `57c8d9f520a3bb95df473d2319f208ebd290f459` (`git ls-remote origin main`)
- Product base (candidate branch base): `3187cea15728143146905c7238ad6e280ca11b3e`
- Candidate branch: `0427-159-damagedstate`, live head `452be76cec7122f27b3468850d780e232960d2f2` (PR #1499)

## PLAN

- Read mission, act-1499-review recipe, round-1/round-2, hx2.md BF-03, task note, AGENTS (product + coordinator)
- Attoselect: planning origin/main = 57c8d9f5; PR #1499 head = 452be76c; PR #1498 head = 934775f6, confirmed NOT an ancestor of #1499 and its diff does NOT cover the network case (only mentions "networks" in a comment about retained runtime state)
- Design a *verified* missing-network check: derive the workload project name from the repo manifest (not from the UUID deploy dir), gate on the managed BaseHarbor ownership label, scope to the resolved app identity, fail closed, never false-attribute a second app's orphan
- Implement the network check in `internal/deployment/damaged_state.go`, wired into `DamagedDeploymentNamespace`
- Update the CLI contract in `cmd/baha/app_context.go` so the damaged error names record + network and both recovery paths (no phantom commands)
- Regressions: netz-weg-fall (record present + net removed → damaged) unchanged intakter zustand + empty/never-delivered stays ignored; add a second-app orphan no-false-attribution case; keep the existing two tests
- Local checks: `go build ./...`, `go vet`, targeted unit/regression tests
- Smoke on baha-podman-1 (VM, smoke/validity only): damaged `up` reports record + network
- Commit on `0427-159-damagedstate` (base 3187cea15, only my commits), ls-remote provenance, push
- CI group/trigger for the new test; hosted CI terminal; 172-park native = STATE with link; drift vs develop HEAD; ls-remote + cleanliness
- Write this evidence, publish to baseharbor-plan origin/main, ls-remote before END, bring down smoke stack, END in shared inbox

## Design decision (resolved with Owner, 2026-11-08)

Choice C. A seamable `InspectNetwork` is added to the `bhruntime.RuntimeProvider`
interface (`internal/runtime/contract/api.go`) — the single interface the CLI
already calls; the one implementation is methods on `internal/runtime.(*Compose)`
(via `NewCLIBackend`). It returns a discriminated `NetworkState` (present /
absent / not-baseharbor-owned / inspect-error) and is gated on the managed
BaseHarbor ownership label `io.baseharbor.managed=connectivity` used by
`EnsureManagedNetwork`/`RemoveManagedNetwork`. The cmd/bahu regression exercises
the damaged-state path against a fake seam (present / absent / occupied-by-foreign)
so F1 is satisfied WITHOUT a live-runtime dependency in the unit matrix. No new
runnable cell is forced.

- Network name derivation: `baseharbor-dev-workload-<ResourceProject>`
  (`internal/application/network.go` `DevelopmentWorkloadNetworkNameForProject`),
  where `ResourceProject = RuntimeProjectName(m) = "baseharbor-<app>-<env>"`
  (`internal/application/runtime_postgres.go`). `<app>`/`<env>` come from
  `selection.Manifest`, which IS available in `resolvedRepositoryApplication`
  before the damaged scan — the deploy directory is a UUID and carries no name,
  so the network name CANNOT be derived from the deploy dir alone (this is the
  crux the recipe's "zustandsquelle: provider-liste, nicht datum-rerei" points
  at: the source of truth is the retained app identity in the manifest/record,
  not guessing at runtime).
- Scope / no false attribution: the check names the workload network for THIS
  resolved app's manifest identity and fails closed only when the record is
  damaged AND that specific network is absent. A retained-but-record-missing dir
  belonging to a DIFFERENT app (network still present, or a foreign project) does
  not become THIS app's damage — the namespace scan still flags the orphan as
  damaged (unchanged), but the network-absent clause names only the resolved app.
- Fail-closed, never fabricated: `InspectNetwork` returns absent only when the
  runtime inspects the named network and the label guard confirms it is not a
  BaseHarbor connectivity network; inspect failures are surfaced, not silenced.

## Outcome (pending)

Damaged-state detection will report BOTH halves of the observed BF-03 damage — the missing `deployment.json` record AND the absent workload runtime network — with the record + network named, the retained deploy directory named, and the two concrete recovery paths (re-up from source, or destroy-and-recreate) — before the generic repository-inspection budget check runs. The undamaged over-limit control and the empty/never-delivered ignore cases stay unchanged.

## END

<state>in progress</state>
