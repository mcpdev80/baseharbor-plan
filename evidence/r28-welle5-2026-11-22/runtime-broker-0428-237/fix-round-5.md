# 0428-237 native-broker-503 (PR 1753) fix — round-5 akte

Sitz `w21-pr1702-0428-142-compat`. Karte 0428-237, PR 1753.
Meine karte = DER NATIVE BROKER-503 (nicht die fussnoten-zulassung, die ist 0428-227/241).

## PLAN

- plan in board-file + ## PLAN in akte
- scope-correction: revert commit 22ff5345 (operatorauth ist WRITE-BANNED); branch zurück auf b86440c3
- diagnose native broker 503 am head 22ff5345: run 45011764715, native docker job 137175474667, TestApplicationCapabilityLifecycleExistingCore/secrets an app_capability_runtime_test.go:136, unhealthy=2 / 503=7 / not_ready=0 nach 148s 'Starting secure runtime broker'
- fix in internal/controlplaneruntime/** (server_run.go ~163-219, server.go ~260): warum 503/unhealthy wenn core containers=0 und nur broker läuft. Die BEDINGUNG fixen, NICHT das warten. Verboten: timeout/retry/sleep/not_ready->ok/unhealthy unterdrücken
- addiver commit auf PR-1753 branch (develop abstammung prüfen); ein durchgang bis terminal; ziel vier data-capabilities-reihen green
- stop-punkt: matrix green => ready fuer unabhaengende pruefung; blockierend => STOP, akte, KEIN rerun

## scope correction (operatorauth reverted)

- commit 22ff5345 'admit app.footprint.show as read operation' had internal/operatorauth/local_runtime.go + -test angefasst. internal/operatorauth/** ist ein GESPERRTER pfad. revert auf b86440c3. der INHALT der kommando-zulassung ist laut owner-ci-log schon wirksam ('app footprint show -o json admitted'); selected-fehler ist CONTRACT/consent (0428-241), nicht meine karte.

## 503-pfad:

- head 22ff5345335, durchgang 45011764715, native docker job 137175474667
- TestApplicationCapabilityLifecycleExistingCore/secrets faellt nach 148s an app_capability_runtime_test.go:136 'Starting secure runtime broker'
- unhealthy=2, '503'=7, not_ready=0 - broker wird NICHT gesund, control-plane+openbao melden bereit
- im aktuellen head (b86440c3) ist dafuer KEINE aenderung enthalten - diagnose required

## operatorauth:

- zurueckgebaut / nicht erweitert (write-bann). Zulassung gehoert in trusted-gate-registry / data-capabilities-liste, NICHT internal/operatorauth.

## run:

(to be recorded - run-id, terminalstatus, failed-zahl)

## vier reihen:

(to be recorded - native docker, native podman, selected docker, selected podman; job-id + status; ziel green)

## repo-rule compliance

- write-set: nur internal/controlplaneruntime/** (server_run.go, server.go). SPERRE: internal/operatorauth/**, internal/observability/registry.go, internal/capability/perses_selection.go, internal/identity/**, internal/serviceaccess/**, .github/**, scripts/**
- KEINE timeout/retry/sleep/not_ready->ok/unhealthy unterdrücken; die BEDINGUNG fixen, NICHT das warten

## cleanliness:

(no containers/networks/volumes/compose projects started; worktree detached at develop HEAD; b86440c3 candidate branch)

## END w21-pr1702-0428-142-compat BLOCKED

(to be updated: END_DONE if matrix green, END_BLOCKED if persistent broker 503)
