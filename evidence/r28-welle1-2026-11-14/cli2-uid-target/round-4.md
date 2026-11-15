# PR #1580 — Round 4 (base nachgezogen: env-r5 `f353d1f73`)

## Kontext (Owner-Nachzug 2026-11-15)
- Base `lane-0428-uid-environment` Kopf war **nicht mehr** `b71f64e19`, sondern
  `f353d1f73` (env-r5). Rebase auf den frischen Stand war Pflicht (LV-02
  ancestry).
- Rebase-ziel war für den lokalen `git rebase --onto` nicht sauber mergbar
  (`target.go`/`target_mutation.go`/`config_target_recovery.go` haben in
  `f353d1f73` divergente Versionen → modify/delete-Konflikte). Combined
  candidate daher per **Cherry-Pick** meiner 3 target-commits auf frischem
  `f353d1f73` erzeugt (`/tmp/base-env-cherry`), ancestry sauber, content meiner.

## Ancestry-Zeugnis (LV-02 Pflicht)
```
git merge-base --is-ancestor f353d1f73 HEAD  => PASS
```
- Combined HEAD: `0770fbdbc17dd7b41f774aa36110e011bff91269`
- Meine 3 commits auf `f353d1f73` (env-r5) gepickt:
  - `2b7b45e1` feat(r28): stable target UID without runtime-ownership change
  - `21af0d30` target: idempotent legacy-target UID migration + real-CLI tests
  - `0770fbdb` target: fix CLI cmd/baha unit tests for read-triggered UID migration
- `f353d1f73` ist Ancestor des combined candidate (clean ancestry).
- Force-push auf DEINEN draft branch `lane-0428-uid-target` (#1580 draft):
  ```
  git push github 0770fbdbc17dd7b41f774aa36110e011bff91269:lane-0428-uid-target --force
  ```
  Remote HEAD #1580 = `0770fbdbc17dd7b41f774aa36110e011bff91269`.

## Combined candidate build
```
go build ./...  => ok
```

## CI-Ablauf (neuer Kopf)
- Manueller `workflow_dispatch` (Owner-Nachzug erlaubte Re-Push auf neuem Kopf):
  **Run 43686579374** — SHA `0770fbdb`, branch `lane-0428-uid-target`.
- Terminal: **FAIL**. Nur `validate` + `Workflow policy` lief; alles andere
  skipped (release-source selection: Native impact selection → skipped → Go/CLI/
  validation/native gates skipped).
- `validate` schlägt in **step 12, "Validate source readability"**, fehl:
  ```
  source readability: cmd/baha/target.go has 846 lines (limit: 800; baseline ratchet: 0)
  ```
  Danach: `Run unit and package tests` → skipped (gate blockiert die Kette).

## Attribution (definitiv, nicht content)
- Der gate-schlagende Faktor ist die **line-count-Grenze (800)** für
  `cmd/baha/target.go`.
- Pure base **env-r5 `f353d1f73`** (KEINE meiner commits): `target.go` = **843
  Lines** → überschreitet die 800er-Grenze. Der failure ist Base-Stain.
-环境-r5 commit `3312597be` (`r5: findings 2-4 fix`) hat `targetEnvCommand()`
  (komplete neue CLI-Subcommand mit vollem `Run:`-Handler) direkt in
  `cmd/baha/target.go` eingefügt: 732 (old env-stand `b71f64e19`) → 843 Lines.
- MEINE R1-commits fügen an `cmd/baha/target.go` nur **+5 Lines** (843 → 846).
  Der gate-schlagende Anstieg stammt aus der base, nicht aus meinem content.
- `scripts/source-readability-audit.sh`: `max_file_lines=800`,
  `baseline ratchet: 0` (kein prior baseline für `target.go`) → 843/846 > 800
  schlägt fehl.

## Parity-Hinweis (Q-RUNTIME/Q-CIFIRE nicht erreichbar)
- Ein grüner PR-CI-Lauf ist durch Q-RUNTIME/Q-CIFIRE **nicht** erreichbar.
- Die native runtime-integration suite (6 `*InCI`/`RealLifecycle` tests in
  `cmd/baha` + `internal/application`) schlägt ohnehin an infra fest
  (ORAS-Mangel runner-seitig, `postgres-analytics runs as root` aus der
  env-stand, shared-daemon state-leaks im sandbox).
- Kein endloses re-pushing; status steht wie besprochen.

## Status
- Combined candidate `0770fbdb` force-pushed auf draft #1580.
- CI-run 43686579374 terminal **FAIL** an `source readability` gate
  (`target.go` 846 > 800 Lines) — Base-Stain (env-r5), nicht content.
- Keine grüne pr-run erreichbar; keine weitere CI-Aktion ohne neue Owner-Entscheidung.
- Next End an `594fd2f5`, sobald ein pull_request-lauf auf dem neuen Kopf
  terminal grün ODER als base-stain belegt ist (base-stain hier belegt).

## Round-5-Vermerk (Owner-Entscheidung B, warm gehalten)
- **B-Entscheidung (owner 08:4xZ):** `envUid` wird EIGENE `environment.json`
  identity record pro target (kein feld in deployment-records). Mein #1580-stand
  `0770fbdb` ist laut owner korrekt auf dieser base (env-r5 `f353d1f73`) aufgebaut.
- **Aufgabe:** auf den neuen #1578-head der 051-lane (post von mir selbst per
  rebase) rebase auf lane-0428-uid-target, merge-base-ancestry zeugen, run
  terminal, akte round-5, END. Bis dahin warm halten, nichts pushen.
- **Befund (2026-11-15 ~08:5x):** 051-lane noch NICHT im repo (keine
  branch-ref, kein neuer commit auf uid-environment). Draft #1580 steht
  unverändert bei `0770fbdb`.环境 build repaired (stales `/var/tmp/gotmp-bf01`
  recreated) + unit-scope grün (`internal/deployment` ok, `cmd/baha` UID-Tests ok).
  Kein push — post #1578 der 051-lane folgt erst. Warm gehalten.
