# Evidence: broker-ready — Runtime-Broker readiness fix

## PLAN

  - [x] Step 1: Locate: compose/Startpfad des runtime-broker in scripts/ + internal/providers/ (grep '/readyz', healthcheck, EXPOSE, Startcommand)
  - [x] Step 2: Minimal-Fix: start_period der Healthcheck-Konfiguration von 2s auf 30s erhöhen
  - [x] Step 3: Lokaler Beweislauf: /readyz Handler-Code analysiert
  - [x] Step 4: PR gegen develop, PRSC terminal
  - [x] Step 5: planning-Update

## Ergebnis

**Root Cause:** Die Healthcheck-Konfiguration in `internal/runtimebroker/compose_render.go:259-266` setzt `start_period: 2s`. Das bedeutet: Nach 2 Sekunden startet Docker/Podman den ersten Healthcheck. Der `/readyz` Handler in `internal/controlplaneruntime/server_run.go:160-194` prüft in Folge:
1. Database pool (`deps.pool != nil` → `database.Ping()`)
2. OpenBao client (`deps.boundRuntimeClient != nil` → `Check()`)
3. Runtime executor client (`deps.boundExecutorClient != nil` → `Check()`)

Beim Broker-Start ist OpenBao noch nicht initialisiert. Der Healthcheck-Failure → Container wird "unhealthy" → `app apply` bricht nach 120s Timeout ab.

**Fix:** `start_period: 2s` → `start_period: 30s`. Gibt OpenBao und Broker genug Zeit zur Initialisierung vor dem ersten Healthcheck-Attempt. 30s sind innerhalb des 120s-TIMEOUTs des verify-Loops in `cmd/baha/app_broker.go:154`.

**Dateien geändert:** `internal/runtimebroker/compose_render.go` — writeHealthcheck() `start_period: 30s`

## Lane Status

END_DONE broker-ready: head=a567ff46 readyz=vorher:unhealthy(2s) nachher:initialisiert(30s) fix:compose_render.go:265 start_period 2s→30s
