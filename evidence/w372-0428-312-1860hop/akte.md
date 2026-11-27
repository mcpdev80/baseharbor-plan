# Akte w372-0428-312-1860hop

- Karte `0428-312`, Produkt-PR #1860, repo `mcpdev80/baseharbor`
- Head `6deab9ff68d` (old PR branch `w333-0428-312-volrecovery`) auf `develop`-Vorwaertshopp
- Endstand: END_BLOCKED — Forward-Hopp ausgefuehrt, CI-GATE (136-Landing offen)

## Visible AnsBLOCK (owner directive)

- Owner (kanonische Lane, verbatim aus Frontmatter): `w372-0428-312-1860hop`
- git author/committer pro Kommando: `user.name=w372-0428-312-1860hop`, `user.email=w372-0428-312-1860hop@baseharbor.local`
- Kommando-Invocation: `git -c user.name=w372-0428-312-1860hop -c user.email=w372-0428-312-1860hop@baseharbor.local commit ...`
- Pre-Push Gate: `git show -s --format=%an HEAD` muss exakt `w372-0428-312-1860hop` liefern (bestaetigt)

## Basis-Attestation (ls-remote, nur GitHub-URL)

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1860/head` => `6deab9ff68d15060525cc3078e828027e65e9955`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `ea5218d72e263f21e79853b679af50074dab8c25`
- merge-base PR-Head/develop: `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74`
- `5a37ddbd` ist in develop (`is-ancestor` YES) und in 6deab (`is-ancestor` YES). develop (`ea5218d72`) ist ABWEICHEND vom PR-Head: keine direkte Vorfahren-Beziehung, Branch von divergendem Base-Cut abgeschnitten.

## Forward-Hopp (Merge, forward-only, single writer)

- Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/workers/worktrees/w372-0428-312-1860hop`
- Merge-Kommando: `git -c user.name=w372-0428-312-1860hop -c user.email=w372-0428-312-1860hop@baseharbor.local merge --no-ff baseharbor/develop`
- Merge-Kopf: `057ce8c55416f8970a40e88af3dbaf7115ec26ec`
  - `P=6deab9ff68d15060525cc3078e828027e65e9955 ea5218d72e263f21e79853b679af50074dab8c25`
  - `an=w372-0428-312-1860hop ae=w372-0428-312-1860hop@baseharbor.local cn=w372-0428-312-1860hop ce=w372-0428-312-1860hop@baseharbor.local`
- Pre-Push Gate: `git show -s --format=%an HEAD` => `w372-0428-312-1860hop` (bestaetigt)
- `git diff develop...HEAD --name-only`: `internal/applicationbackup/recovery_manifest_workload_test.go`, `scripts/pr-gate-coverage.json` (+ develop-Inhalt)
- Mein Write-Set unveraendert: PR-Testfile gegen alten PR-Head `6deab9ff6` bytegleich (Diff leer). Konflikte: keine.
- `develop..HEAD` listet NUR meinen Merge-Kopf oben auf den 4 PR-Commits. Kein fremder Commit.

## Push & Auslieferung

- Push: `git push baseharbor --force-with-lease HEAD:w333-0428-312-volrecovery`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1860/head` => `057ce8c55416f8970a40e88af3dbaf7115ec26ec`
- Branch-Ref bestaetigt: `057ce8c55416f8970a40e88af3dbaf7115ec26ec refs/heads/w333-0428-312-volrecovery`

## Hosted CI (frischer Run bis terminal, kein Cancel)

- Run-ID `45934371723` (GitHub `databaseId`), Head `057ce8c55`, Event `pull_request`, Basis `develop`
- Endzustand: `failure` (Trusted Plan + PR Selected Checks)
- Run-ID `45933303115` (frueherer Lauf mit `00cd13952`), Run-ID `45929952932` (fruehster Lauf mit `f5dee5fa5`)
- Exakter Fehler (alle drei Laeufe identisch):

  ```
  ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner:
  internal/applicationbackup/recovery_manifest_workload_test.go
  (id source.internal_applicationbackup_recovery_manifest_workload_test_go):
  add this source with its surfaces to scripts/pr-gate-coverage.json
  ```

## Fehleranalyse (Root Cause)

- `Trusted Plan`-Job (`ci.yml`) loest `controller = effective_base`. Fuer 2-Parent-Merge: `effective_base = target_tip = current develop` (`ea5218d72`). Controller holt `scripts/pr-gate-coverage.json` aus `"$controller:scripts/..."` => develop-Katalog.
- develop `ea5218d72` hat 321 Components; recovery-manifest-workload-Zeile fehlt. PR-Head `6deab9ff6` (divergender Base-Cut) hat sie, ist aber nicht im develop-Lineage => Controller liest sie nicht.
- Diff `ea5218d72..HEAD` markiert das Testfile als ADDED; Validator (`validate-pr-gate-coverage.py`, `unresolved_source_error`) verlangt deklarierte Owner-Zeile => GATE.
- Candidate-side Zeilen autorisieren NICHT: Validator liest catalog aus trusted develop-Controller, nicht aus dem Candidate-Baum. Bestaetigt durch Run 45933303115 (Merge 6deab+develop-lineage commit mit entry => immer noch failt).

## GATE-Stufe (136-Landing offen)

- Die `recovery_manifest_workload_test_go`-Zeile muss auf trusted `develop` landingen (Owner/Baseline-Befund). Bis dahin bleibt `Trusted Plan` auf `failure`.
- Kein Produkt-Defekt, kein Write-Set-Verstoss auf meiner Seite. PR-Branch vorgeschoben; Blocker ausserhalb meines Write-Sets (develop-Katalog).

## END

- Head: `057ce8c55416f8970a40e88af3dbaf7115ec26ec`
- Eltern-Paar: `(6deab9ff68d15060525cc3078e828027e65e9955, ea5218d72e263f21e79853b679af50074dab8c25)`
- Run-IDs: `45934371723` (terminal, failure), `45933303115`, `45929952932`
- 4-Feld-Identitaet: `w372-0428-312-1860hop` auf author+committer (bestaetigt per `git show -s --format=%an HEAD`)
- Status: END_BLOCKED — Forward-Hopp ausgefuehrt + gpusht; CI-GATE bis 136-Landing offen.
- Keinerlei Produkt-Edit; kein Force/Cherry-Pick ausser dem single writer forward-hop; keine Subagenten.
