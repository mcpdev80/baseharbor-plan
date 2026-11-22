# 0428-237 native-broker-503 (PR 1753) fix — round-6 akte

Sitz `w21-pr1702-0428-142-compat`. Karte 0428-237, PR 1753.
Meine karte = DER NATIVE BROKER-503 (unhealthy/503), gemessen an head 22ff5345335.

## PLAN

- plan in board-file + ## PLAN in akte
- scope-correction: revert commit 22ff5345 (operatorauth write-ban); branch at b86440c3
- corrected origin: read-only hunt auf released developesse (8629450e) localisiert native broker 503/unhealthy in cmd/baha/app_broker.go, NICHT controlplaneruntime
- fix 1: app_broker.go docker :440-447 + podman :412-421 — transient 'starting'/unhealthy tolerieren solange retry-grenze (compose retries:12) nicht ueberschritten; bedingung aendern, nicht warten
- fix 2: app_broker.go ~502 — version-mismatch-fehlertext untergibt expectedVersion ZWEIMAL fuer got-feld; auf tatsaechlichen wert korrigieren
- fix 3: /readyz-sonde — bei 503 body NICHT als成功 parsen; http-status erst pruefen, dann body
- addiver commit auf PR-1753 branch (develop abstammung pruefen); ein durchgang bis terminal; ziel vier data-capabilities-reihen green
- stop-punkt: matrix green => ready fuer unabhaengende pruefung; blockierend => STOP, akte, KEIN rerun

## ort:

- cmd/baha/app_broker.go (read-only hunt on released develop 8629450e; NOT internal/controlplaneruntime — that earlier pointer was wrong)
- docker pfad: lines 440-447 ('if health != "" && health != "healthy" { return ... }')
- podman pfad: lines 412-421 (analog)
- version-mismatch text: line ~502
- /readyz-sonde: raw-curl-body JSON parse OHNE http-status pruefung

## FailingStreak:

- head 22ff5345335, durchgang 45011764715, native docker job 137175474667
- TestApplicationCapabilityLifecycleExistingCore/secrets faellt nach 148s an app_capability_runtime_test.go:136 'Starting secure runtime broker'
- unhealthy=2, '503'=7, not_ready=0 - broker wird NICHE gesund, control-plane+openbao melden bereit
- ursache: die readiness-prfung im cmd/baha/app_broker.go liest einen transienten 'starting'/unhealthy zustand als endgueltigen fehl als fatal; container spaeter gesund, prfung bricht zu frueh ab

## http-status:

- /readyz-sonde parst raw-curl-body als JSON OH-den-http-status-zu-pruefen; bei 503 nicht als erfolgreich parsen; status erst pruefen, dann body

## operatorauth:

- zurueckgebaut / nicht erweitert (write-bann). Zul gehoert in trusted-gate-registry, NICHT internal/operatorauth.

## run:

(to be recorded - run-id, terminalstatus, failed-zahl)

## vier reihen:

(to be recorded - native docker, native podman, selected docker, selected podman; job-id + status; ziel green)

## repo-rule compliance

- write-set: cmd/baha/app_broker.go (readiness bedingung v4.1 + version-mismatch text v4.2 + /readyz status-check v4.3).
- SPERRE: internal/operatorauth/**, internal/observability/registry.go, internal/capability/perses_selection.go, internal/identity/**, internal/serviceaccess/**, .github/**, scripts/**
- KEIN sleep/timeout-erhoehen/not_ready->ok; CONDITION aendern, nicht warten
- ACHTUNG: PR 1763 editiert EBFALLS cmd/baha/app_broker.go (diagnostics). diagnostic-redaction-code von 1763 NICHT aendern; nur readiness-bedingung + status-pruefung ergaenzen. Wenn diff mit 1763-kollidiert: reihenfolge (merge-reihenfolge) statt file-merge.

## cleanliness:

(no containers/networks/volumes/compose started; worktree detached at develop HEAD; b86440c3 candidate branch)

## END w21-pr1702-0428-142-compat BLOCKED

(to be updated: END_DONE if matrix green, END_BLOCKED if persistent broker 503)
