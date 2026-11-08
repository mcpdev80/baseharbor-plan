# Bug-Hunt H-D6 — stillstands-semantik (stop/down/restart) + logs/eingriffsoberflaeche

- Shift: r27-welle5-folge-2026-11-08 · Lane mission-hunt-d6 · Datum: 2026-11-08
- Ziel: Reine Befundung der Stillstands-Semantik und Eingriffs-/Logs-Schnittstelle von `baha app` auf der Testmaschine baha-docker. Kein produkt-code, keine PRs, keine reruns.
- Host: baha-docker (SSH-Name), realer hostname `baha-runner-docker`, 192.168.6.166, User marcel. Docker 29.8.1, compose v5.5.1.
- Binary (develop, kein eigener build): `/home/marcel/.local/bin/baha` — version "BaseHarbor dev / commit none / built unknown".
- origin/main evidence base SHA (planning repo): 5fb42689e5f2bebab5503916a5fd8b93363b18e1
- Reale Remote-Wahrheit gemessen via `git ls-remote origin` oben.

## PLAN
- Host-Baseline: lock-protokoll + laufende Baha-Runtimes belegen
- Schnitt 1: app down — container/netz/datetraeger was bleibt, rueckweg, double-stop idempotent
- Schnitt 2: restart nach externem SIGKILL — wer startet neu, meldet befehl die tatsache?
- Schnitt 3: app logs — rotierende/leere/riesige logs, follow+abbruch, backend-falschauswahl
- Schnitt 4: app exec/enter fehlerpfade (gestorben, nicht gefunden, rechte)
- Schnitt 5: status nach jedem schritt (karte 160 reconciliation), positive notieren
- Evidence schreiben, BESENREIN, board ticken, END posten

## Setup / Reproduktion
- Environment: SSH-Host baha-docker (real `baha-runner-docker`). Docker 29.8.1, compose v5.5.1.
- Binary: /home/marcel/.local/bin/baha (BaseHarbor dev, commit none, built unknown)
- Test-Anwendung: bh-hd6-demo (Neubau aus baseharbor.yaml, target docker)
- Bisher laufende Runtimes beim Start: bh-gfield0427-shared (postgres/openbao member+admin) — extern, nicht touch.
- Befehl-Basis: alle Tests als `ssh baha-docker 'PATH=/home/marcel/.local/bin:$PATH; baha ...'`.

## Funde

### Fund 1

- BF-NN: (Klasse: )
- Beleg: datei:linie
- Beschreibung:

## Positive
-

## Belege (rohe Kommandoausgaben)

## BESENREIN
- Vorher:
- Nachher:

## END
- Lane: mission-hunt-d6 — STATE
