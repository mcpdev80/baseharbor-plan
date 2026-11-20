---
id: t-20261120-deployment-version-mismatch-masked
card_number: "0428-200"
card_short_title: "record version mismatch masked"
type: bug
areas: [cli, lifecycle]
release: v0.4.28
version: ""
parent: ""
owner: w200-0428-200-verrmask
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-200 · record version mismatch masked
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1727, mcpdev80/baseharbor#1728]
sources: []
blocker: ""
wait_reason: "HANDOFF VOLLSTAENDIG, PFLICHTCHECK KANN NICHT GRUEN WERDEN - DARUM wait, muster wie 177/199/201/083/143 (§3.7). EIN PR PRO KARTE JETZT WIEDER HERGESTELLT: #1728 (head 6e3122344f87, branch w200-0428-200-verrmask-2 == refs/pull/1728/head gemessen, base develop, draft=FALSE, 5 dateien, ancestry auf develop 40cb28c758b0 = JA). der DUPLIKAT-FALL: #1727 blieb draft, weil mein eigener auftragstext das falsche werkzeug nannte - 'gh api -X PATCH pulls/<n> -f draft=false' ignoriert GitHub; undraft ist 'POST /pulls/<n>/mark_ready'. die lane legte deshalb dieselbe aenderung als zweiten PR an, statt einen unueberpruefbaren kandidaten liegen zu lassen - inhaltlich richtig, formal ein verstoss, den ICH verursacht habe. Aequivalenzbeweis vor dem schliessen: 'git patch-id of develop..776812c21be0' == 'git patch-id of develop..6e3122344f87' == c0253bdb2b1a9383, identische 5 dateien, 260 diff-zeilen. #1727 ist damit geschlossen, mit kommentar und diesem beleg (https://github.com/mcpdev80/baseharbor/pull/1727#issuecomment-7049...), und das werkzeug-wissen ist als issue mcpdev80/codeman-coordinator-tooling#12 festgehalten (inkl. 'gh pr view --json isDraft' als selbst-beleg für lanes). RUN AM EXAKTEN HEAD (44804472715): go-build, go-vet, gofmt, deployment-package-tests, owner = success; cli-0..3 + packages + 'Selected Runtime' = der feld-gate 0428-198 mit der woertlichen operator-zeile; die packages-zeile traegt zusaetzlich das internal/logs Loki-trio = 0428-202. INHALT: version-1-record einer EXISTIERENDEN deployment.json nennt jetzt gefundene version + erwartete version + naechsten schritt (typ DeploymentRecordVersionMismatch, 2 treffer gemessen) statt 'no registered deployment'; fail-closed byte-identisch; regression ueber status/destroy/list durch die echte kommando-oberflaeche, eine datei pro oberflaeche gemeldet. AKTE 71 zeilen, 0 checkboxen, cleanliness zweimal, gate dreimal, beide PR-nummern genannt (1727 einmal als der geschlossene). TRIGGER FUER DIE NAechSTE KANTE: der pflichtcheck laeuft, sobald 0428-198 die sammelstelle liefert und 0428-202 entschieden ist; dann review (CODEX), dann merge in kettenordnung. sitz freigegeben."
resolution: ""
evidence: []
created: 2026-11-20
---

- [ ] t-20261120-deployment-version-mismatch-masked · record version mismatch masked #task #release/v0-4-28 #status/wait #view/wait #area/cli #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** w200-0428-200-verrmask  
    **PR:** [baseharbor#1727](https://github.com/mcpdev80/baseharbor/pull/1727), [baseharbor#1728](https://github.com/mcpdev80/baseharbor/pull/1728)  
    **Waiting:** HANDOFF VOLLSTAENDIG, PFLICHTCHECK KANN NICHT GRUEN WERDEN - DARUM wait, muster wie 177/199/201/083/143 (§3.7). EIN PR PRO KARTE JETZT WIEDER HERGESTELLT: \#1728 (head 6e3122344f87, branch w200-0428-200-verrmask-2 == refs/pull/1728/head gem…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w200-0428-200-verrmask  
**Priority:** not set  
**PRs:** [baseharbor#1727](https://github.com/mcpdev80/baseharbor/pull/1727), [baseharbor#1728](https://github.com/mcpdev80/baseharbor/pull/1728)  
**Source:** 
<!-- /generated:links -->

## Found by bug hunt H-V21 (2026-11-20, develop `40cb28c758b0`)

Hunt akte: `evidence/r28-welle4-2026-11-20/bughunt-hv21-shipped-surface/round-1.md`, slice "upgrade from outside".

When the shipped binary starts on a state written by an older shipped version (`deployment.json` carrying
`"version": 1` while `DeploymentRecordVersion` is 2), failing closed is correct - nothing is migrated or promoted.
The message is the defect:

- `internal/deployment/deployment_store.go:656` `loadDeploymentRecordFile` raises
  `unsupported deployment record version 1` as a `DeploymentRecordStateError` with `Kind="corrupt"`.
- `ListDeploymentsForDisplay` (`deployment_store.go:751`) collects it as a best-effort warning.
- `resolveRegisteredApplication` (`cmd/baha/app_context.go:360`) and the final warning loops
  (`cmd/baha/app_context.go:427-455`) map only the kinds `access-denied` and `malformed` - `corrupt` falls
  through, so the user reads `application X has no registered deployment`.

Measured with the shipped binary: `baha app status olddeploy` and `baha app destroy olddeploy --yes` both print
`no registered deployment on target local` for a version-1 record. The real decision (version gate) is hidden
behind a statement that is false.

## Acceptance

1. A version-mismatched deployment record is reported with its own reason on the human surface: the message names
   the version found, the version expected, and the supported next step (upgrade path or operator action).
   `no registered deployment` must not be shown for a record that exists but is version-gated.
2. Fail-closed behavior stays: nothing is migrated, nothing is promoted, no state is rewritten.
3. A regression builds the older record on disk, runs the real command surface, and asserts the version reason
   appears for status, destroy and list - one distinct failing test per surface.
4. One hosted run at the exact head shows the owning shard executed, 0 failure. Gate failures from `0428-198` are
   recorded and reported, not fought.

## Boundaries and stops

- Allowed to write: `internal/deployment/deployment_store.go` (error kind plus message only),
  `cmd/baha/app_context.go` (the kind mapping), and their test files.
- Locked (other owners): `internal/observability/registry.go` (0428-078 plus 0428-189..194),
  `internal/machine/**` and `internal/operatorauth/**` (#1594/#1615/#1650 owner stack),
  `internal/metrics/**` (#1714), `internal/serviceaccess/**` (#1684), `cmd/baha/context_terminal*.go` (#1718).
- This card must not introduce a migration: an upgrade writer would need its own card and an owner decision.
- No subagents (AGENTS 4.8), no `git add -A`, no merge, no force-push on develop/main.

ARBEITET JETZT, kante gegen session gemessen (w200-0428-200-verrmask, laptop, worktree aus develop 40cb28c758b0): die MELDUNG wird repariert, nicht die entscheidung - version-mismatch eines bestehenden deployment-record bekommt eigene ursache ( gefundene version, erwartete version, naechster schritt) statt 'no registered deployment'; fail-closed bleibt byte-identisch; regression pro oberflaeche (status, destroy, list) durch die echte kommando-oberflaeche. schreibfeld absichtlich eng: internal/deployment/deployment_store.go (fehler-art + meldung) und cmd/baha/app_context.go (kind-abbildung). internal/serviceaccess/** ist EXPRESS verschlossen, weil dort gerade der policy-befund 2af892e4e (#1594-rail, karte 0428-202) liegt - lesen erlaubt, aendern nicht.

ABNAHME ZURUECKGEWIESEN, DARUM BLEIBT active (kein wait, kein review): inhalt ist gut gemessen (branch == refs/pull/1727/head == 776812c21be0, 'git merge-base --is-ancestor 40cb28c758b0 <head>' = JA, 5 dateien, akte 63 zeilen, 0 checkboxen, cleanliness), aber DREI PFLICHTEN SIND OFFEN, alle mit eigenem zeugen belegt: (1) PR #1727 IST draft=TRUE ('gh api pulls/1727'), und solange das so ist, faehrt GitHub nur den draft-pfad - gemessen am head laufen exakt die zellen 'PR · Draft Go · cli-2 / cli-3 / packages' (run 44802438861, 1 success / 5 in_progress / 26 skipped). die Required-checks kommen bei draft=TRUE UBERHAUPT NICHT ZUM AUSFUEHREN, also ist punkt 1 eine vorbedingung und keine formsache (§5.2: drafts sind keine kandidaten). BEFOHLEN: 'gh api -X PATCH .../pulls/1727 -f draft=false' + titel/body mit kartennummer + head-sha + aktenpfad auf demselben weg ('gh pr edit' scheitert an Projects-classic-GraphQL). (2) plicht-check am exakten head bis zum terminalen zustand SELBST beobachten (§4.6) und run-id + conclusion je zelle in die akte. (3) die AKTE NENNT WEDER PR-NUMMER NOCH RUN-ID (gemessen: '1727' = 0 treffer, 'run <zahl>' = 0 treffer) - beide zeilen nachziehen. GATE-REFERENZ in der akte steht schon 3x richtig (0428-198). TRIGGER FUER DIE naechste KANTE: draft=false + beobachteter run in der akte; dann wieder entweder review (wenn die Required-cells ausserhalb des feld-gates gruen sind) oder wait mit den namen 0428-198/0428-202 (muster wie 177/199/201/083).
