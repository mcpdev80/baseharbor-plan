---
id: t-20261120-r28-bughunt-install-destroy-retry
kanban_title: 0428-170 · hunt install destroy retry
card_number: "0428-170"
card_short_title: "hunt install destroy retry"
type: review
areas: [release, runtime]
repos: [mcpdev80/baseharbor]
release: v0.4.28
version: ""
parent: ""
depends_on: []
blocked_by: []
superseded_by: []
owner: w170-pr0428-170-instdestroy
kanban_status: closed
kanban_lane: closed
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/bughunt-install-destroy-retry/round-1.md"]
prs: []
created: 2026-11-20
wait_reason: ""

---

- [x] t-20261120-r28-bughunt-install-destroy-retry · audit destroy vs interrupted retry #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/release #area/runtime #kind/review
    <!-- generated:card -->
    **Owner:** w170-pr0428-170-instdestroy  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/bughunt-install-destroy-retry/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w170-pr0428-170-instdestroy  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Ziel

Bug-Hunt H-V13 (reine Befundung, KEINE Produktänderung). Prüfschnitt über die
releasedesse von develop (nur CLOSED/merged Stand): native installation — destroy —
unterbrochener retry.

## Anker (develop, von mir gemessen)

- `.github/workflows/docker-runtime-acceptance.yml:146-148` — Job
  'Validate real installation destroy and interrupted retry',
  ruft `bash scripts/ci-native-installation-destroy.sh`
- `internal/deployment/config_target_recovery.go` (Datei existiert auf develop)
- `internal/deployment/target_id.go:67-80` — AcquireStateFileLock /
  'no-mutation in MigrateLegacyTargetUIDs' (#1580, Idempotenz-Vorbild)

## Schnitte, die die Lane prüft

1. destroy: was bleibt nach einem vollständigen destroy an state zurück
   (state-verzeichnisse, locks, registry-einträge, compose-projekte)?
2. retry nach abbruch: ein abbruch ZWISCHEN den schritten eines deploy/destroy
   — führt der nächste lauf durch denselben pfad, oder braucht er manuellen eingriff?
3. idempotenz: zweiter destroy-lauf ohne änderung am zustand (no-mutation wie bei
   target_id.go:88)?
4. nebenläufigkeit: zwei gleichzeitige zugriffe auf denselben state-lock —
   verliert einer stille information?

## Regel

Keine Produktänderung, keine Kartenentscheidung. Akte mit datei:zeile je Aussage,
vorher/nachher-liste der container/netzwerke/volumes + 'cleanliness:'-zeile.
Vorhandene Karten, die denselben raum betrifft, nicht doppelt gießen — verweisen.


jagd H-V13 BEFUNDLOS abgeschlossen, alle vier schnitte VERHALTEN KORREKT (fail-closed beim destroy, resume nach abbruch, Idempotenz des zweiten destroys, lock ohne umgehungspfad) — ein negativer beleg ist wertvoll, er hält die fläche gegen wiederholte jagd. akte auf origin/main baead951, cleanliness CLEAN (keine container/volumes/state-verzeichnisse dieses shifts). keine folge-karten aus diesem schnitt
