# Chain Live-Proof — Task t-20261027-r27-shadow-run

Worker lane o220. Owner-Auftrag 17:5xZ: Nachweis, dass Public Contracts ausgeführt
wurden und ein Receipt veröffentlicht wird. KEINE Approval vor geprüftem Receipt.

## PLAN

1. Git-Worktree `worktrees/o220` für den Kandidaten `work/r27-producer-extension-reserve`
   anlegen, dann `go test ./contracts/ -run 'TestExtension' -count=1` und `go vet ./contracts/`
   ausführen.
2. Echtes `git merge origin/develop` in den Zweig (kein Squash), Commit-Message:
   `merge develop 64d12492 into extension reserve (chain live-proof candidate)`.
3. `go test ./contracts/ -count=1` nach dem Merge erneut ausführen.
4. Zweig gegen origin pushen.
5. PR `gh pr create --base develop --head work/r27-producer-extension-reserve` öffnen,
   PR-Nummer notieren.
6. Producer-Run abwarten (alle 60s, max 12 min), run-id + PR-Check 'PR · Public Contracts'
   verifizieren (SUCCESS/executed). Bei SKIPPED: Debug-Payload einsammeln, BLOCKED melden.
7. Post-Run-Workflow capture: neue run-ids, Job-Abschlüsse (Producer Context /
   Extract Trusted Plan / Publish Receipt).
8. Receipt-Datei in planning identifizieren (Pfad + SHA).

## STATUS

Schritt 0 (Vorbereitung) abgeschlossen. Kandidat verifiziert:
- Branch `work/r27-producer-extension-reserve` @ b9ebc475 (Additiver Test-only-Kandidat).
- Additiv eingeführt: `contracts/extension_trust_test.go`.
- 19 Commits ahead von develop (f95b3446).
- Basis-Commit des Candidates: f95b3446.

## AUSFÜHRUNGSBELOGGUNG

Schritt 1 (exit 0):
- Worktree angelegt: `baseharbor/worktrees/o220` auf `work/r27-producer-extension-reserve` @ b9ebc475.
- `go test ./contracts/ -run 'TestExtension' -count=1` -> `ok github.com/mcpdev80/baseharbor/contracts 0.010s` (exit 0).
- `go vet ./contracts/` -> exit 0 (leere Ausgabe).

Schritt 2 (echter Merge, exit 0):
- `git merge origin/develop` -> `ort`-Strategie, kein Konflikt. Konfliktefrei, 4 Dateien (u.a. neue `contracts/connection_profile_trust_test.go`).
- Merge-Commit umgetauft auf `fc9e820b209a4fa6210f4d0c1f6b75444ac95631` mit Message:
  `merge develop 64d12492 into extension reserve (chain live-proof candidate)`.
- Parents korrekt: b9ebc475 (Candidate) + 64d12492 (develop).
- Candidate-Datei `contracts/extension_trust_test.go` nach dem Merge vorhanden.

Schritt 3 (exit 0):
- `go test ./contracts/ -count=1` nach Merge -> `ok 0.316s` (exit 0).
- `go vet ./contracts/` nach Merge -> exit 0.

Schritt 4 (exit 0):
- `git push origin HEAD:work/r27-producer-extension-reserve` -> `b9ebc475..fc9e820b  HEAD -> work/r27-producer-extension-reserve`.

Schritt 5:
- PR #1207 geöffnet: `https://github.com/mcpdev80/baseharbor/pull/1207`
  (base=develop, head=work/r27-producer-extension-reserve, State OPEN).

Schritt 6 (run completed, SUCCESS):
- Producer-Run-ID: 40900784834, Workflow "CI · Source & Quality" (workflow_id 352609139),
  Event pull_request, head_sha fc9e820b, created 2026-10-29T15:21:51Z, status completed,
  conclusion success, Laufzeit 2m32s.
- Check `PR · Public Contracts`: conclusion SUCCESS, completed 2026-10-29T15:23:59Z,
  job 123542333848, detailsUrl https://github.com/mcpdev80/baseharbor/actions/runs/40900784834/job/123542333848.
- Check `PR · Trusted Plan`: SUCCESS. Check `PR · Validation · source-contracts`: SUCCESS.
  Check `PR · Focused Python`: SUCCESS. Check `PR · Demo Pin`: SUCCESS. Check `Workflow policy`: SUCCESS.
  Check `PR Selected Checks`: SUCCESS. Andere Checks SKIPPED (Targeted HA docker/podman,
  Release Source Preflight, validate, PR · Exact Candidate, PR · Runner Interface,
  PR · Consumer Pins, PR · Selected Runtime).

Schritt 7 (post-run workflow capture, alle run-ids + conclusions):
- Nur ein Run für diesen Branch: 40900784834 (fc9e820b, PR #1207).
- Jobs (name | status | conclusion):
  Workflow policy | completed | success
  PR · Trusted Plan | completed | success
  Targeted HA · docker | completed | skipped
  Release Source Preflight | completed | skipped
  Targeted HA · podman | completed | skipped
  validate | completed | skipped
  PR · Validation · source-contracts | completed | success
  PR · Focused Python | completed | success
  PR · Demo Pin | completed | success
  PR · Exact Candidate | completed | skipped
  PR · Runner Interface | completed | skipped
  PR · Consumer Pins | completed | skipped
  PR · Public Contracts | completed | success   <- gesuchter Gate, EXECUTED/SUCCESS
  PR · Selected Runtime | completed | skipped
  PR Selected Checks | completed | success

Schritt 8 (Receipt in planning):
- Gefunden: `baseharbor-plan/evidence/receipts/public-contracts/40428162731-1.json`.
- SHA im origin/main-Baum: 80538d4d93ed6965f342441c75aa5b69034669b5.
- Commits: `06f25dc` (record) und `8411672` (approve).
- INHALT (origin/main):
  {"approved":{"at":"2026-10-27T02:52:00Z","by":"mcpdev80","receipt_commit":"06f25dcf1f9024a508f3beff0fb2e60bf7b0699f"},"gate":"public-contracts","plan":"5ecabc17797aaf21a454cb83fab20e4ddc49eb7c","run":{"attempt":1,"id":40428162731},"sha":"12f3c97ee9b593833aad5de223451e2e9d4f6dd3","status":"pass"}

## BLOCKER (Receipt-Nachweis NICHT für meinen Lauf erbracht)

Der Receipt in planning referenziert run-id 40428162731, sha 12f3c97e, created 2026-10-27.
Dieser Run existiert: er ist "CI · PR #1094" (workflow_id 352609139, head bd342b91, 2026-10-27).
ER IST NICHT MEIN LAUF:
- Meinen Lauf: run-id 40900784834, PR #1207, head_sha fc9e820b, created 2026-10-29T15:21:51Z.
- Kein Receipt existiert für 40900784834 (keine Datei evidence/receipts/public-contracts/40900784834*, kein git-log-Eintrag).
- Der Receipt "run.id" (40428162731) und "sha" (12f3c97e) decken sich weder noch mit meinem Lauf.

Zwischenfazit: Der Gate "PR · Public Contracts" ist für meinen Lauf tatsächlich EXECUTED/SUCCESS
(live proof: run 40900784834). Ein neuer Receipt für meinen Lauf (run.id 40900784834, sha fc9e820b)
ist jedoch noch NICHT in planning veröffentlicht. Nach Owner-Auftrag ist BEIDES nötig, und die
Receipt-Veröffentlichung ist die Bedingung vor ANY Approval. Daher: KEINE Approval. Candidate ist
für die Weiterverarbeitung vorbereitet; der Receipt-Einführungs-/Aktualisierungsschritt im planning
steht noch aus (kein workflow_dispatch durch mich, kein Merge durch mich).
