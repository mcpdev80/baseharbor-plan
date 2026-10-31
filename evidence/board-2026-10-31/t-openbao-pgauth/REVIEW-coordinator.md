# Coordinator Review t-openbao-pgauth — ABGELEHNT (2026-10-31)
END_DONE nicht akzeptiert: PLAN4/5 unbehuscht, "Podman HA pending CI dispatch" = KEIN beobachteter Run (§4.6 Eigenes-Run-Pflicht).
Diff = compose.yaml mount ./runtime.env -> /run/baseharbar/env (Tippfehler baseharbar) + `. ... || true` = No-op-Swallow;
behebt weder scram-SASL noch mTLS cert-unknown. Widerspricht der eigenen (guten) Root-Cause-Analyse.

## Korrekte Fix-Rezeptur (aus Worker-Analyse, für NEU-Lane nach CI-Migration)
1. openbao-init.sh / openbao_runtime_prepare.go psql-Aufruf: PGSSLMODE erbt verify-full, aber PGSSLROOTCERT fehlt ->
   Spilo-self-signed untrusted ("certificate unknown"). Fix: PGSSLROOTCERT auf die korrekte CA setzen ODER
   sslmode=verify-ca mit übergebener CA; durch HAProxy ggf. sslmode=require (TLS ja, no verify) — NICHT ssl=off/trust.
2. projectControlPlanePostgresTLS (stack.go:276-309) ueberschreibt bootstrap-CA mit material.CA nachdem Spilo-Container
   schon mit bootstrap-CA erzeugt sind -> CA-Mismatch. Fix: Reihenfolge/material konsistent halten.
3. BASEHARBOR_OPENBAO_DB_PASSWORD vs Postgres-Rolle: stale runtime.env kann abweichendes Passwort -> SASL 28P01.
   Fix: Quelle der Password-Injection für openbao-init + Rollen-Create deterministisch dieselbe.
Validierung: echter GitHub-hosted "Targeted HA · podman" GRUEN (nach Lane gh-ci-core Migration).
