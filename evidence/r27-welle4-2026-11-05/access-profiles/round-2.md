# WORKER EVIDENCE — Lane w167 (CODEX-WORKER role in pool) — t-20261018-r27-access-profiles RUNDE 2

- Lane: w167-profiles-r2
- Coordinator: f49a3303
- Card: t-20261018-r27-access-profiles (state active, owner coord-welle4 Lane w167)
- PR: baseharbor#1384 (draft), base develop @ 24c7d0492f34e58c2a6be505ba80b8bdfb151cb7
- Candidate head (pre-round-2): 06479fe042d4fa6c0512c2f81bbf320e08fdc7e5
- Mission file: coordinator/missions/w167-profiles-r2.txt
- Evidence dir: baseharbor-plan/evidence/r27-welle4-2026-11-05/access-profiles/

## Mission lock

Runde 2 REZEPT (bindend aus mission):
1. Erwartete Revision bei jeder Aenderung veruemmmen, veraltete Schreibvaenge ABWEISEN (kein last-write-wins).
2. Profil-Operationen an die BESTEHENDE Akteur-/Tenant-Autoritaet binden (team-auth/managementaccess-Pfad, nicht neu erfinden); Aufrufstelle mit datei:zeile in Evidence.
3. Profil-Edition darf effektive Rechte NICHT erweitern — Adapter vermitteltdumm; wenn Entscheidungslogik zurueck in den einen Autoritaets-Pfad muss, genau das.
4. Widerrufene Profile verweigern DURCH DENSELBEN Adapter (test verlangt wortlich).
5. Echter CLI-/Produktionspfad ist verbunden (kein test-only-Pfad als Beweiseratz).

6 Faelle (positiv/_negativ, wortlich BELEG): Zuweisung, Widerrufs-Wirkung, mehrdeutiger Name, veraltete Revision, fremder Tenant, keine Eskalation bei Edition.

4 MUTANTEN-GEGENPROBE: (a) Aenderung ohne Revision -> rot, (b) Profil-Edition mit Recht-Aufstieg -> rot, (c) fremder Tenant -> rot, (d) Widerruf via Adapter -> verweigert.

ROTE GRUNDLINIE: auf develop 24c7d049+ benannt (review-1384a §"Profile edition cannot escalate").

## repo-rule compliance (Owner + AGENTS)

- KEINE .github-Aenderung, KEINE workflow_dispatch/rerun (Runner = GitHub-shared-runner nur; Fehlschlag => STATE, stoppen).
- KEINE AGENTS.md- oder anderen getrackten Produkt-Aenderungen (Operational Text gehoert in Mission + Planning-Evidence).
- KEINE Subagenten; jeder Schritt in eigener Session.
- EXAKEIN zweiter Kandidat/PR — bleibt auf work/access-profiles.
- WORKSPACE: Worktree unter workers/<lane>-wt; kein Scratch im ecosystem-root.
- Provenance: ls-remote wortlich, ancestor rc=0, log-zeile NUR eigene commits.

## PLAN (worker steps, board file: workers/todos/w167-profiles-r2.json)

- Read mission + complete review-1384a + card; lock the 5-recipe constraints and 4 mutant counter-probes
- Set up isolated worktree under workers/ for access-profiles (main repo has foreign uncommitted changes); ls-remote witness of work/access-profiles 06479fe0 and develop 24c7d049
- Locate the single production authority: existing actor/tenant check on team-auth / managementaccess path (record file:line call site in evidence)
- Implement recipe (1): enforce expected revision on Manager.Update, reject stale writes
- Implement recipe (3): profile edition cannot widen effective ops — adapter held dumb, decision logic stays in the one authority path
- Implement recipe (2)/(4): bind profile operations to existing actor/tenant authority; revoked profiles deny THROUGH the same adapter
- Implement recipe (5): connect the real CLI/production caller (no test-only path as evidence substitute)
- Write 6 positive/negative cases + 4 mutants (a edit-without-revision red, b edition-escalation red, c foreign-tenant red, d revoke-via-adapter deny) with literal output
- Local checks: go build ./..., go vet, gofmt -l clean; go test ./internal/orgconfig ./internal/policy ./cmd/baha -count=1 -race-count=20 on new tests
- Merge real develop 24c7d049 into candidate if drift>0 (own commits only); ancestor rc=0; ls-remote + own-only name-only log witnesses
- Push draft PR #1384 (base develop @ 24c7d049); record PR head SHA
- Hosted CI to terminal (Eigenes-Run-Pflicht): PR Selected Checks NOT skipped incl. selected checks; record Run-ID/status/failing log line if any
- Post QUESTION to coordinator with candidate SHA + full evidence (autoritaet file:line, 6/6, mutants, CI run, ls-remote)

## END an f49a3303 (updated each stop)
END_DONE w167-profiles-r2: (pending)
