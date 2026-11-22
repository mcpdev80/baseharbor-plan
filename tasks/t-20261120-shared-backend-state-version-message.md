---
id: t-20261120-shared-backend-state-version-message
card_number: "0428-201"
card_short_title: "shared state version message"
type: bug
areas: [lifecycle]
release: v0.4.28
version: ""
parent: ""
owner: (lane, PR wartet)
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-201 · shared state version message
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1725]
sources: []
blocker: ""
wait_reason: "PR 1723 muss zuerst in develop (seine dateien stecken als ahne in diesem diff)"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pulls/1725", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/workload-port-0428-199/hop-develop-c463edf8-w17235.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44995066580", "https://github.com/mcpdev80/baseharbor/actions/runs/44998846458"]
created: 2026-11-20
---

- [ ] t-20261120-shared-backend-state-version-message · shared state version message #task #release/v0-4-28 #status/wait #view/wait #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** (lane, PR wartet)  
    **PR:** [baseharbor#1725](https://github.com/mcpdev80/baseharbor/pull/1725)  
    **Waiting:** PR 1723 muss zuerst in develop (seine dateien stecken als ahne in diesem diff)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pulls/1725), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/workload-port-0428-199/hop-develop-c463edf8-w17235.md), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44995066580), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44998846458)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** (lane, PR wartet)  
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

## Exact current-base rerun — 2026-11-21

The refreshed PR head `cfd8851f730d356a75b3e65448f995f47284e7d9` includes latest `develop` at `77c1e60f51b91003ac3ddc391008c15e4a713a5c`. Exact pull-request run [44897015296](https://github.com/mcpdev80/baseharbor/actions/runs/44897015296) completed FAILURE: CLI shards 0–3 and `PR · Go unit · packages` passed; the selected rootless Podman data-capabilities runtime job [136825185177](https://github.com/mcpdev80/baseharbor/actions/runs/44897015296/job/136825185177) failed, so `PR Selected Checks` [136826810005](https://github.com/mcpdev80/baseharbor/actions/runs/44897015296/job/136826810005) failed. The runtime log shows candidate recording refused for missing `--confirm-candidate`, then `baha app footprint show -o json` could not configure target `atomic-podman-data-capabilities`; the managed test-only operator setup also reported interactive auth required on piped input. These are shared candidate-consent/CI-target authorization failures outside this card's state-version message scope. No production auth behavior or another owner's files were changed. Keep the card in Wait until its shared required gate is corrected and the exact current candidate can pass.

kandidat ist gehoepft bis develop 52a3c5446f4 (head 485103523b9, back=0). Am vorherigen head dd4e826f6c8 (run 449937224) likewise: go-shards und build SUCCESS, einziger fehler das data-capabilities-gate (0428-237). Review nach terminalen run und nach broker-klarung.

wartet auf denselben hop auf develop acc34323968 (back=2, diff jetzt 7 dateien statt 19). Gleiches bild wie bei 1723: der alte review-fehler war kontaminations-bedingt.

wartet auf denselben hop auf develop acc34323968 (back=2, diff jetzt 7 dateien statt 19). Gleiches bild wie bei 1723: das REQUEST CHANGES am head 485103523b9 (akte cli-sourcepull/... 47156bcd24a, run 44995066580, 7 failed jobs, '16 paths outside card write-set') zaehlt ab dem neuen develop nicht mehr als kandidatfehler.

wartet auf denselben hop auf develop acc34323968 (back=2, diff jetzt 7 dateien statt 19). Gleiches bild wie bei 1723: das REQUEST CHANGES am head 485103523b9 (run 44995066580, 7 failed jobs, '16 paths outside card write-set') zaehlt ab dem neuen develop nicht mehr als kandidatfehler.

kein re-cut noetig, rekchenreihenfolge loest es: der zensus meldete '1725 needs clean re-cut', aber die messung am neuen head d65e9a25419 zeigt 7 dateien, davon vier (cmd/baha/app_apply.go, app_workload_ports.go, runtime.go, workload_port_local_regression_test.go) das sind die OWN-inhalte von PR 1723, deren head als ahne in der kette steckt. Dreimal dieselbe lage wie bei 1627: sobald PR 1723 in develop liegt, schrumpft dieser diff auf die drei eigenen dateien (internal/application/shared_backends.go, shared_backends_state.go, shared_backends_state_version_test.go). Daher: 1723 zuerst mergen, dann 1725 hop auf den neuen develop, dann exact-head review. Kein paralleler merge, kein mischen der write-sets.

kein re-cut noetig, die reihenfolge loest es: der zensus meldete '1725 needs clean re-cut', aber die messung am neuen head d65e9a25419 zeigt 7 dateien, davon vier (cmd/baha/app_apply.go, app_workload_ports.go, runtime.go, workload_port_local_regression_test.go) sind die OWN-inhalte von PR 1723, deren head als ahne in der kette steckt. Dreimal dieselbe lage wie bei 1627: sobald PR 1723 in develop liegt, schrumpft dieser diff auf die drei eigenen dateien (internal/application/shared_backends.go, shared_backends_state.go, shared_backends_state_version_test.go). Beide hops sind gelaufen: run 44998829701 (#1723) und 44998846458 (#1725) sind FAILURE mit 2 jobs, am 1723-run ist 'PR . Selected Runtime (atomic/docker/data-capabilities)' job 137136024513 der fehler - derselbe broker-blocker (0428-237), nicht der kartenschnitt. Daher: 1723 zuerst mergen (nach broker-klarung), dann 1725 hop auf den neuen develop, dann exact-head review.
