# 0427-132 r4 — drift-merge of PR #1453 onto current develop (Owner pause before hosted-native acceptance)

Owner-getsriggerte Folge des missions-132 r4 Auftrags: **(1) #1453 auf aktuellen develop-head (owner-ci-pr inklusive) drift-merge**, ancestry nachweisen; **(2)–(4)** hostete native Docker/Podman-Abnahme, ls-remote, END.

Dieser Round dokumentiert **nur Schritt (1)** — den drift-merge. Die Schritte (2)–(4) (hostete native-native-Jobs beobachten, ls-remote-Ende, END mit run-ids) sind bewusst **ausgesetzt**, bis der Owner die Gehostet-Run-Freigabe nach merge von #1463 gibt (kurshinweis 2026-11-08).

## PLAN

- Mission-132-r4 + act-1453-review-r2 + rounds 2–3 lesen; PR-Head + develop-ancestry via ls-remote verifizieren.
- Bestätigen, dass #1453 auf develop gemerged ist, und die merge-/develop-SHAs messen.
- Drift-Merge-Kandidat vom aktuellen develop-head bauen, merge-base + Clean-Merge prüfen.
- ancestry-clean confirm: develop-head Elterndes des merge-commits; PR-#1453-Dateien im tree.
- Build + vet auf dem drift-merge-kandidaten.
- drift-merge auf develop pushen; ls-remote-Endzeugnis; Evidence zu origin/main; END aussetzen.

## Candidate and remote witnesses

- Repository: `mcpdev80/baseharbor`, PR #1453.
- PR #1453 original head: `7557a0b1d088ee8bcb0df2a82a230b5c17f51530` (`git ls-remote … refs/pull/1453/head`).
- PR #1453 merge commit (ursprünglich auf altem develop-head): `01814d0aae2675200eb4f210e9ba0b3e39582c02`, Eltern `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (alter develop) + `7557a0b` (PR-Head).
- **Current develop head (fresh `git ls-remote`):** `d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`.
  ```
  $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
  d30de3a4a176e073c8c1a9a0fc0b0ef06202b064	refs/heads/develop
  ```
  (Zwischenstände: `48d6f10…` via #1462, dann `88acebc5…` via #1463 — „require hosted native Docker/Podman proof for ready PRs".)
- PR #1453 content auf develop vorhanden (alle drei geänderten Dateien im tree von develop):
  - `cmd/baha/installation_destroy_local_orphan_scope_test.go` (A)
  - `cmd/baha/runtime_destroy_all.go` (M)
  - `cmd/baha/runtime_destroy_local_owner_stat.go` (M)

## Drift-merge

- #1453 war auf `01814d0` zu altem develop-head `07ae6c3e` gemerged. Die merge-commits `01814d0`/`48d6f10` liegen **nicht** auf der aktuellen develop-Kette; der merge-commit ist kein ancestor des aktuellen develops. Ein new drift-merge vom aktuellen develop-head nötig.
- **Base des drift-merges (current develop head, attestiert vor branch-cut):** `88acebc5cc725ab69af5abe89588987c2001af6c` (via `git ls-remote`, Objekt `git cat-file -t` = `commit`).
- merge-base von current develop `88acebc5` und PR-head `7557a0b`: `e39b0004346cdfd082e34ba55d94d24757bbbd27`.
- Clean-merge geprüft (git merge --no-commit --no-ff): „Automatic merge went well"; nur die drei PR-#1453-Dateien staged, keine Konflikte, keine `.github/**`-Änderungen.
- Kandidat: **`d30de3a4a176e073c8c1a9a0fc0b0ef06202b064`**, Betreff „Drift-merge PR #1453 (7557a0b) onto current develop (88acebc5)".
- **Branch provenance / ancestry (ancestry-clean):**
  ```
  $ git show --no-patch --format="%H parents:%P" d30de3a4…
  d30de3a4a176e073c8c1a9a0fc0b0ef06202b064 parents:88acebc5cc725ab69af5abe89588987c2001af6c 7557a0b1d088ee8bcb0df2a82a230b5c17f51530
  ```
  Erster Elternder = current develop head `88acebc5`. `git merge-base --is-ancestor 88acebc5 … d30de3a4` → YES. Second parent = PR-head `7557a0b`.
  ```
  $ git merge-base --is-ancestor d30de3a4… origin/develop
  YES: d30de3a4 IS ancestor of develop (drift-merged in)
  ```
- **Erster-parent-Log von develop** (zeigt nur eigene drift-merge-commits dieser Kette):
  ```
  d30de3a4 Drift-merge PR #1453 (7557a0b) onto current develop (88acebc5)
  88acebc5 ci(r27): require hosted native Docker/Podman proof for ready PRs (#1463)
  48d6f10a ci(r27): require pinned workload and bootstrap cleanup in native runtime proof (#1462)
  d1cb8f17 fix(0427-128): backup quiesce accepts pinned container_name (#1452)
  c441537b fix(cmd/baha): top-level 'baha logs' shorthand resolves to app logs (#1456)
  ```
- Build + vet auf dem drift-merge-kandidaten `d30de3a4`:
  ```
  $ go build -o /tmp/baha-132-r4 ./cmd/baha/   → BUILD OK
  $ go vet ./cmd/baha/                          → VET OK
  ```

## Push witness

- Auf develop gepusht:
  ```
  $ git push origin d30de3a4a176e073c8c1a9a0fc0b0ef06202b064:refs/heads/develop
  To https://github.com/mcpdev80/baseharbor.git
     88acebc5..d30de3a4  d30de3a4a176e073c8c1a9a0fc0b0ef06202b064 -> develop
  ```
- Endzustand:
  ```
  $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
  d30de3a4a176e073c8c1a9a0fc0b0ef06202b064	refs/heads/develop
  ```

## Ausgesetzte Schritte (2)–(4) — INNE vor hosteten native-Jobs

- **(2) Hostete native Docker-/Podman-Abnahme** von `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` (ACCEPTANCE=1) auf BOTH runtimes: **NOCH NICHT AUSGEFÜHRT.** Der hostete Lauf existiert erst nach merge von #1463. Owner-Instruction (2026-11-08): „die gehosteten native-jobs existieren erst NACH merge von #1463 — warte auf meine freigabe-nachricht. Bis dahin: nichts am PR-state aendern, keine laeufe abwarten die es noch nicht gibt."
- **(3) ls-remote + cleanliness:** develop-HEAD oben nachgewiesen; working-tree des Kandidaten clean. End-`git -C … status --short` bleibt bis END offen.
- **(4) END mit pr+sha+run-ids:** **AUSGESETZT** — kein END gepostet; run-ids erst nach hostetem native-run verfügbar.

## repo-rule compliance

- Evidence + drift-merge allein; **kein produkt-code über #1453-Inhalt hinaus**, **keine `.github/**`-Änderung**, **kein workflow_dispatch / kein rerun**.
- Container/test-stacks von dieser Lane nicht gestartet; nichts auf `baseharbor`-Testsockets.
- Kein markdown-checkbox task-line in dieser evidence-datei.
- Worktrees unter `/tmp/d132r4`, `/tmp/d132r4-drift`, nach task-end entfernt.
