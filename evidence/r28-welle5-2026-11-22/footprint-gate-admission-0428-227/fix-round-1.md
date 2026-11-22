# 0428-227 footprint-gate-admission (PR 1753) code fix — round-1 akte

Sitz `w21-pr1702-0428-142-compat`. Karte 0428-227, PR 1753.
Diagnose bestaetigt (eigener Befund 0847d100 + Coordinator-Messung am exakten head): die vier runtime-reihen rot werden NICHT wegen Broker-Hang. Der native docker-job 137165488041 des durchgangs 45008538769 steht 'readiness timeout' NULL mal und 'not_ready' genau eins, aber 'confirm-candidate' ist da und zwei TestApplication-Faelle schlagen fehl. Die ursache: 'app footprint show' ist NICHT als lesende operation im trusted-gate-registry zugelassen, wird wie eine kandidaten-mutation behandelt und loest die consent-kaskade aus. PR 1753 fuegt das cli-kommando ein, aber nicht die registry-zulassung. SIE FIXEN NUN DIE REGISTRY-ZULASSUNG.

## PLAN

- Plan in board-file + ## PLAN in akte
- karte 0428-227 ueber scripts/plan.py claim (commit + push)
- ls-remote + attestation: develop 8629450e; origin/develop ancestor; admit-liste in internal/gate-registry.go:45-46 lokalisieren
- CODE: 'app footprint show' als READ-op in die zugelassenen dat-capability-kommandos (internal/gate-registry.go) ergaenzen; nur diese eine zeile + zugehoeriger test-fall; KEINE timeout/sleep/retry, KEIN not_ready->ok
- addiver hop: git merge --no-ff <develop-sha> (8629450e unmittelbar vor merge gelesen); KEIN amend/force; ein commit, normal push + delivery-witness
- hosted run bis terminal: run-id, failed-zahl, VIER runtime-reihen (nativ docker, nativ podman, selected docker, selected podman) mit job-id + status; ziel alle vier green
- stop-punkt: matrix green => ready fuer unabhaengende pruefung; blockierender zustand => STOP, akte, KEIN rerun

## base attestation

- develop: 8629450ef3c5198bb675331c12f56b2c9377aa1c (via ls-remote)
- PR 1753 head (vor fix): b86440c389b6f8f82b0a3a1dce284d315b4531c7
- origin/develop ancestor test: (noch einzutragen)

## readiness timeout:

- null mal im native-docker-job 137165488041 durchgang 45008538769; not_ready genau einmal; confirm-candidate vorhanden; zwei TestApplication-faelle fehlschlagen. Broker-Hang NICHT ursache.

## consent-kaskade:

- 'app footprint show' nicht als lesende operation im trusted-gate-registry zugelassen -> kandidaten-mutation -> consent-kaskade an allen vier runtime-reihen. Fix = registry-zulassung, nicht broker-readiness.

## vier reihen:

- (noch einzutragen: native docker, native podman, selected docker, selected podman — job-id + status; ziel green)

## repo-rule compliance

- write-set: nur internal/gate-registry.go (eine admit-zeile) + zugehoeriger test-fall. SPERRE: KEINE aenderung an internal/observability/registry.go, internal/capability/perses_selection.go, internal/identity/**, internal/serviceaccess/**, internal/operatorauth/**, .github/**, scripts/**
- KEINE timeout-/sleep-/retry-nderung, KEIN not_ready->ok

## cleanliness:

- no containers/networks/volumes/compose projects started (hosted CI only); worktree detached at develop HEAD. No orphaned test stack.

## END w21-pr1702-0428-142-compat BLOCKED

(to be updated: END_DONE if matrix green, END_BLOCKED if persistent blocker)
