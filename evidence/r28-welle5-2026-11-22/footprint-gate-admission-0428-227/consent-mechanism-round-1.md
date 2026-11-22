# 0428-227 consent mechanism (PR 1753) - round-1 akte

Sitz `w21-pr1702-0428-227-consent`. Karten 0428-227 + 237 + 241, PR 1753.
Dritter hop (736319213853) run 45014558296 wieder FAILURE -> ursache auf mechanismus-ebene.
Gegessen am run 45014558296: beide selected data-capabilities jobs, 'app footprint show -o json' VERWEIGERT die kandidat-einreichung ohne --confirm-candidate, dann 'native CLI JSON/MCP Footprint contracts differ'. NEU: nativ docker + podman UND cli-1 + source-format FAILED.

## PLAN

- plan in board-file + ## PLAN in akte
- reproduce: run 45014558296 messen - 'app footprint show -o json' refusiert ohne --confirm-candidate, dann contracts differ
- fix A (consent class, 0428-227): beweisen WODURCH 'app footprint show' als mutation klassifiziert; klassifizierungs-pfad in app_broker.go + footprint-show registration + operatorauth/gate class pruefen; show=read-only darf KEIN --confirm-candidate brauchen; klassifizierung fixen, nicht test
- fix C (source-format/cli-1, neu): gofmt ueber diff; cli-1 fehl-zeile aus log benennen; format/build regression behoben
- fix B (contract divergence 0428-241): nach A footprint JSON/MCP mit baseharbor-demo tests/guided/new_edit.py:63 vergleichen; feld-abweichung melden, wenn nicht (karte 241, nicht mein consent-pfad)
- addiver commit auf PR-1753 branch (develop abstammung pruefen); ein durchgang bis terminal; ziel alle required green
- stop-punkt: verlangt A nach diesem versuch IMMER NOCH consent -> STOP, genauer kode-pfad (datei:zeile) melden, der show als mutation klassifiziert (moeglicherweise operatorauth/gate owner-scope)

## klasse:

(to be determined - prove site where 'app footprint show' is classified as mutation requiring --confirm-candidate)

## contract:

(to be determined - footprint JSON/MCP vs baseharbor-demo tests/guided/new_edit.py:63 field comparison, card 0428-241)

## source-format:

(to be determined - gofmt diff, cli-1 failure line from log)

## SPERREN:

KEINE aenderung internal/operatorauth/**, internal/observability/registry.go, internal/capability/perses_selection.go, internal/identity/**, internal/serviceaccess/**, .github/**, scripts/**. Keine subagenten. Kein merge/kommentar.

## run:

(to be recorded - run-id, terminalstatus, failed-zahl, job-ids)

## job-ids:

(to be recorded - native docker/podman, selected docker/podman, cli- shards, source-format je job-id + ausgefuehrt/skipped/gefailt)

## repo-rule compliance

- write-set: cmd/baha/app_broker.go + footprint-show command registration (read-only classification)
- SPERRE: internal/operatorauth/**, internal/observability/registry.go, internal/capability/perses_selection.go, internal/identity/**, internal/serviceaccess/**, .github/**, scripts/**
- fix die KLASSIFIZIERUNG (show=read-only), NICHT den test; kein test, das digest zwingt

## cleanliness:

(no containers/networks/volumes/compose started; b86440c3 candidate branch; docker ps -a empty)

## END w21-pr1702-0428-227-consent BLOCKED

(to be updated: END_DONE if all required green, END_BLOCKED if persistent consent requirement)
