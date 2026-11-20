---
id: t-20261120-shared-backend-state-version-message
card_number: "0428-201"
card_short_title: "shared state version message"
type: bug
areas: [lifecycle]
release: v0.4.28
version: ""
parent: ""
owner: w201-0428-201-statever
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-201 · shared state version message
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1725]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
created: 2026-11-20
---

- [ ] t-20261120-shared-backend-state-version-message · shared state version message #task #release/v0-4-28 #status/active #view/active #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** w201-0428-201-statever  
    **PR:** [baseharbor#1725](https://github.com/mcpdev80/baseharbor/pull/1725)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w201-0428-201-statever  
**Priority:** not set  
**PRs:** [baseharbor#1725](https://github.com/mcpdev80/baseharbor/pull/1725)  
**Source:** 
<!-- /generated:links -->

## Found by bug hunt H-V21 (2026-11-20, develop `40cb28c758b0`)

Hunt akte: `evidence/r28-welle4-2026-11-20/bughunt-hv21-shipped-surface/round-1.md`, slice "upgrade from outside".

`internal/application/shared_backends.go:17` sets `sharedBackendStateVersion = 3`; `decodeSharedBackendState`
(`internal/application/shared_backends_state.go:31-32`) rejects any other version with
`unsupported shared backend state version N`. No migration from v1/v2, no discard: pure fail-closed. That is the
intended decision of the shared-backend cards, so the gate itself is right.

What is missing is the surface: two different state files (`deployment.json` and the shared-backends state) both
carry a version field that fails closed, but neither human message tells the operator that this is an
upgrade-from-outside situation. See the sibling finding `0428-200`, which shows the same class on the deployment
record where the message is not just generic but actively false.

## Acceptance

1. The shared-backends version failure names the version found, the version expected, and the supported next
   step, and is distinguishable from a corrupt or unreadable file.
2. Fail-closed behavior stays byte-identical: no migration, no discard, no rewrite.
3. A regression writes a v2 state file, runs the real command surface that loads it, and asserts the version
   reason (not a generic error) reaches the user.
4. One hosted run at the exact head shows the owning shard executed, 0 failure. Gate failures from `0428-198` are
   recorded and reported, not fought.

## Boundaries and stops

- Allowed to write: `internal/application/shared_backends_state.go` (message plus error kind) and its test files;
  `internal/application/shared_backends.go` only for the error type it exposes.
- Locked (other owners): `internal/observability/registry.go` (0428-078 plus 0428-189..194),
  `internal/application/perses_runtime.go` and `internal/serviceaccess/**` (#1684),
  `internal/machine/**`, `internal/operatorauth/**`, `internal/identityprovider/**` (#1594/#1615/#1650 owner),
  `internal/metrics/**` (#1714), `cmd/baha/context_terminal*.go` (#1718).
- Do not add a migration path without a card and an owner decision.
- No subagents (AGENTS 4.8), no `git add -A`, no merge, no force-push on develop/main.

ARBEITET JETZT, kante gegen session gemessen (w201-0428-201-statever, ornith, worktree aus develop 40cb28c758b0): die version-ablehnung von shared-backends state (shared_backends.go:17 = 3, decodeSharedBackendState shared_backends_state.go:31-32) bekommt gefundene version, erwartete version und den naechsten schritt in die human-meldung, unterscheidbar von corruption-/lesefehler - die fail-closed ENTSCHEIDUNG bleibt byte-identisch, sie wird nicht angefasst. meldungsform wird MIT der schwesterkarte 0428-200 abgestimmt (die repariert dieselbe klasse beim deployment-record), damit nicht zweimal verschieden erfunden wird. gateway-meldung waehrend des runs ist 0428-198/202, nicht ihr diff.

HANDOFF NAHE, EINE BELEGZEILE FEHLT - DARUM BLEIBT active (nicht wait, nicht review): inhalt ist durch, von mir gemessen: PR #1725 head 9bf4a72f742b == refs/pull/1725/head == branch, base develop, draft=FALSE (die lane schrieb 'draft PR', ist aber draft=false gemessen), 3 dateien, ancestry auf develop 40cb28c758b0 = JA. checks am head: 11 success / 7 failure / 16 skipped, run 44795772617; die sieben roten sind cli-0..3 + packages + Selected Checks + Selected Runtime (atomic/podman/data-capabilities) = der feld-weite gate 0428-198/0428-202, nicht ihr diff. AKTE nennt PR (3x) und 0428-198 (5x), 0 checkboxen, cleanliness - aber KEINEN EINZIGEN RUN-ID (§4.6): genau eine zeile fehlt, angefordert; KEIN neuer matrix-run dafuer (§5.4). ZWISCHENFUND, von MIR BEHOBEN: ihre akte hatte vier zeilen '- [ ] 1.' - eine checkbox AUSSERHALB von tasks/ legt den plan-checker flach ('would become a CardBoard card') und BLOCKIERTE DIE PUBLIKATION DES GANZEN BOARDS; mechanisch auf nummerierte zeilen gesetzt (text gleich, 71 zeilen vorher/nachher), sweep ueber alle 79 akten der heutigen welle: keine weitere checkbox-datei. board wieder 0 errors (000f3ed7f42b). Trigger: ihre nachgelieferte run-zeile -> dann wait mit den namen 0428-198/0428-202, muster wie 177 und 199.
