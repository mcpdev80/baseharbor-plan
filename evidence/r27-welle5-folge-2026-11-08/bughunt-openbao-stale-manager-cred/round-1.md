# Round 1 — Fix: stale OpenBao manager-cred blockiert legitimen Re-Bootstrap

- Lane: mission-0427-154 (Worker, worker-ornith1.5)
- Session: ses_e44f98db8ffea2jreEUJg3R5xW
- Datum: 2026-11-08
- Produkt: baseharbor — `internal/openbao/bootstrap.go`
- Ziel: Re-Bootstrap eines stale, aber nicht-initialisierten OpenBao erlauben, ohne fail-closed bei echtem Initial-Zustand zu brechen

## PLAN

- Befund lesen (hd5.md) + Code in bootstrap.go verifizieren (Inspect, Bootstrap:234-243, Unseal, flow)
- Branch fix/0427-154-openbao-stale-manager-cred vom origin/develop HEAD b73a13a9 abgeschnitten
- Fix implementieren: manager-cred-state als Teil des Initialisierungs-checks (stale+uninit => Wiederherstellungs-Pfad mit Meldung; stale+init => unveraendert verweigern)
- Regression beide Zweige als Go-Unit-Test im bao-Feld (stale+uninit => gelingt; stale+init => verweigert)
- go test ./internal/openbao + go vet + go build lokal ausfuehren
- Evidence verifizieren (PLAN, repo-rule compliance, END-Pflicht); go-unit-tests CI beobachten (run-id)
- PR gegen develop HEAD; ls-remote + cleanliness; compose-Stack herunterfahren

## Basis-attestation

- planning repo origin/main SHA (Beleg vor Erstcommit):

```
a5bdd03a docs(plan): record all 15 ready cards code triage and two shared PRs
```

- origin/main nach Publish wiederholt verifiziert (END).

- Produkt checkout baseharbor: QUARANTAINT (ref-push-incident), remote-Wahrheit NUR via `git ls-remote origin`.

## Branch-Attestation

- Abge schnittene Basis: `origin/develop` HEAD `b73a13a909b2d7b811d6956b3bdaf93f17b80454`
  (develop HEAD 2026-11-08, PR #1459 `fix(up): accept optional positional NAME on top-level alias`).
- Branch: `fix/0427-154-openbao-stale-manager-cred` (Worktree `/tmp/mission-154-openbao-wt`).
- Ancestry-Nachweis: `b73a13a9` ist Vorfahre des Erstcommits (merge-base --is-ancestor OK).
- Kandidaten-Commit: `2d929127c fix(openbao): re-init stale manager credential on uninitialized server`
  - log listet MEINE Commits (b73a13a9 => 2d929127c), kein foreign commit.
  - Exakter Basis-Content von develop HEAD (commit `b73a13a909b2d7b811d6956b3bdaf93f17b80454`).

## Fund (H-D5 BF-1, reproduziert)

- datei: internal/openbao/bootstrap.go:234-243
  ```
  229  func Bootstrap(ctx context.Context, executor Executor, files bhruntime.Files, recoveryPath string) error {
  230      state, err := Inspect(ctx, executor, files)
  231      if err != nil {
  232          return err
  233      }
  234      if state.Initialized {
  235          return ErrAlreadyInitialized
  236      }
  237
  238      adminPath := AdminCredentialsPath(files)
  239      if _, err := os.Stat(adminPath); err == nil {
  240          return fmt.Errorf("OpenBao manager credential state already exists at %s", adminPath)
  241      } else if !errors.Is(err, os.ErrNotExist) {
  242          return fmt.Errorf("inspect OpenBao manager credentials: %w", err)
  243      }
  244      ...
  ```
- `Inspect()` liefert `state.Initialized == false` (OpenBao unbenutzbar, aber initialisierbar).
- `os.Stat(adminPath)` auf die stale `openbao-admin.env` existiert => DAUERNDES bootstrap-WEIGERUNG.
- Keins checkt, ob openbao tatsaechlich initialisierbar ist; datei-existence reicht zum blockieren.
- vm-Beleg (hd5.md, baha-docker): `baha openbao bootstrap --recovery-file ...` =>
  `Error: OpenBao manager credential state already exists at .../gfield0427/runtime/openbao-admin.env`;
  nach rm der stale datei => `[OK] OpenBao initialized and unsealed`.

## Korrekturkonzept

- manager-cred-state nicht mehr als eigenes Dauer-Weigerungsgrund behandeln; in den Initialisierungs-check integrieren.
- NEUE Meldung im Wiederherstellungs-Pfad (stale + NICHT-initialisiert): was gefunden (stale env, server nicht initialisiert) und was getan wird (env zurueckschreiben/loeschen, Re-Bootstrap); KEINE dauerhafte Weigerung.
- INITIALISIERTEM server => unveraendert `ErrAlreadyInitialized` (fail-closed, 127-Doktrin, unveraendert).
- positives: recovery-material wird nie ueberschrieben (reserveRecoveryFile + rotate-retire, bootstrap.go:245-255, 415-434); initialisierbar-Pruefung ersetzt reine Date existence durch state-based Pruefung.

## repo-rule compliance

- CI-Regeln des Produkt-repos (docs/DEVELOPMENT_GUIDELINES.md, AGENTS.md) eingehalten.
- KEINE .github/**-dateien aendern (Owner-scope); KEINE workflow_dispatch / Rerun getriggert.
- KEINE runner-infra build/register/repair.
- Tests rein lokal als Go-Unit im bao-Feld; Ausloesung in der CI-Gruppe go-unit-tests (Trigger: PR/branch) dokumentiert; kein VM-Only-Test.
- Evidence nur in baseharbor-plan (evidence/r27-welle5-folge-2026-11-08/bughunt-openbao-stale-manager-cred/), KEINE .evidence/ im produkt-repo.
- Subagenten/agent-tools NIEMAL genutzt (4.8); jeder Schritt in dieser eigenen Session.

## END

- Status: END_BLOCKED
- Blocker: Owner-Direktive 2026-11-04 + Mission-Text: PR-Offnung, Push und gerosteter CI-Lauf gehort in den Owner-Scope (keine PR/Push/Workflow-Steuerung in dieser Session).
- Weiterer Trigger: Owner-Freigabe zum Push der Kandidaten-Branch + CI-Beobachtung (run-id go-unit-tests).
- Offen: PR gegen develop HEAD; ls-remote + cleanliness; compose-Stack herunterfahren.
