# 0428-164 — merge-window-audit-r2 (Worker, Verifikation, read-only)

- Aufgabe: vier seit 0428-150 neu auf develop gelaufene Merges (d5c11753e #1578, bbc937c8f1 #1580, 97abbe157 #1706, 15727ca88 #1595) mit derselben Pruefung wie 0428-150 verifizieren; B3 Doppelarbeit ueber OFFENEN PR-Slot; B4 Brett-Wahrheit (Card- vs. PR-Status).
- Read-only: KEIN PR, KEIN merge, KEIN PR-Schließen, KEINE VM, KEIN Container, KEIN Subagent (§4.8).
- Produkt-Base develop: `0b3ed079575a4e9893c6360957815d6efd9eb1a3` (origin/main Planning: `5161cfe22d8889f85db2417eec10101f1974a508`).
- Worktree (Klar): `/tmp/opencode/baseharbor-x164` (Produkt, `git fetch origin develop`); Akten-Clone Planning `/var/tmp/x164-planning-wt`.
- ls-remote (real): `git ls-remote origin develop` -> `0b3ed079575a4e9893c6360957815d6efd9eb1a3\trefs/heads/develop`.

## PLAN (nummeriert, KEINE Checkboxen)
1. Merge-SHAs und PR-Koeff der vier Merges (gh pr view headRefOid + mergeCommit) aufoesen.
2. B1 Blob-Identitaet je Merge: `git diff --name-only <pr-head> <merge>` = leer (inhalt unveraendet gelandet)?
3. B2 CODEX-Urteil am merge-sha: existiert eine verdict-datei unter `evidence/*/codex-review-wave/` fuer den sha?
4. B3 Doppelarbeit: offene prs, gleiche datei in gleicher richtung (blob-identisch) vs. entgegengesetzt.
5. B4 Brett-wahrheit: card-status (origin/main) vs. pr-state live (gh api) abgleichen.

## repo-rule compliance
- Read-only-verifikation; kein produkt-aenderung, kein `.github/**`-edit, kein pr/merge/schließen, keine vm/container, keine subagenten.
- Akten nur im `/var/tmp`-planning-clone; KEIN commit in `workers/baseharbor-plan` (quarantae); KEIN `git -A`.
- Branch-provenanz: origin/main `0b3ed079575a4e9893c6360957815d6efd9eb1a3` ist ancestor der ersten commits; keine fremde karte auf dem zweig.

## B1 + B2 — merge-window (vier merges seit 0428-150)
| PR | head-sha | merge-commit | `git diff --name-only <head> <merge>` | urteil-am-merge-sha |
|---|---|---|---|---|
| #1578 | `97689a75d54d2b28a04e002ccc3afd202b9d5210` | `d5c11753ea437495eb2469a02f80b91d788fef4f` | leer (0 dateien) | nein |
| #1580 | `522af6f4aa5ca1ec2119750be06f84d795612b85` | `bbc937c8f1b1f1604bd5b68f4c66259dc3a3e978` | leer (0 dateien) | nein |
| #1706 | `930df12a482595bba06748ded501fe082f0aab76` | `97abbe1572a74170e3414448fe2dce843309c10a` | leer (0 dateien) | nein |
| #1595 | `b1428b0b0ee41e9f90b55d768b5c86fdd6140614` | `15727ca8878938df7e924319c236c0bcc4a4201c` | leer (0 dateien) | nein |
- Befehl: `git -C /tmp/opencode/baseharbor-x164 diff --name-only <head-sha> <merge-commit-sha>` -> VIER mal 0 dateien.
- Feststellung urteil-am-merge-sha: NEIN fuer alle vier. Zahl der ohne urteil = **4** (`#1578 #1580 #1706 #1595`).
- Zeuge wave: `find evidence -path '*codex-review-wave*' -type f` (46 dated), keine mit einem der 4 merge-shas als verdict. Nächstgelegene verdicts sind #1702 und #1704 — andere prs.

## B3 — doppelarbeit (schliess-kandidaten, blob-shas)
Pruefung je pr: `gh pr diff <n> --repo mcpdev80/baseharbor --name-only` und blob-vergleich `git rev-parse <head>:<pfad>`.
Gleiche datei, BLEIBEND identische aenderung (blob-identisch = faktische doppelarbeit):
- `cmd/baha/app_status_result.go`
  - #1615 -> blob `4052832c2d6ee0f899892dcce01529f37237d805`
  - #1645 -> blob `4052832c2d6ee0f899892dcce01529f37237d805`  (identisch zu #1615)
  - #1597 -> blob `315fc6188bea7b9d6d08a10d2071160f7bdebc38` (same richtung, + `database_dashboards`)
  - #1606 -> blob `315fc6188bea7b9d6d08a10d2071160f7bdebc38` (same richtung, + `database_dashboards`)
  - Zeuge: `git -C /tmp/opencode/baseharbor-x164 rev-parse <head>:cmd/baha/app_status_result.go` je pr.
  - Schließ-kandidat: #1615 und #1645 tragen denselben `+perses`-trag im selben blob -> eine lane schließen.
- `cmd/baha/target.go`
  - #1591 -> blob `7df235639c8e805bc9947ab692ace0de251e140b`
  - #1594 -> blob `7df235639c8e805bc9947ab692ace0de251e140b` (identisch)
  - Zeuge: `git -C /tmp/opencode/baseharbor-x164 rev-parse <head>:cmd/baha/target.go` je pr.
  - Schließ-kandidat: #1591 vs #1594 teilen denselben ziel-policy/env-registry-aendert -> eine lane schließen.
- Gleiche datei, ENTGEGENGESETZTE richtung (konflikt, kein duplikat):
  - `cmd/baha/app_status_result.go`: #1614 vs #1645 -> #1614 entfernt `versions`, #1645 faegt `perses` an. net-diff `git -C /tmp/opencode/baseharbor-x164 diff 80d4df52..c781eb86 -- cmd/baha/app_status_result.go` nicht leer.
  - `cmd/baha/machine_coverage.go`: #1614 vs #1623 -> #1614 fuegt `isworkspacenamespaceclone()` ein, #1623 entfernt sie.
  - `internal/metrics/prometheus*.go`: #1693 vs #1695 -> verschiedene blobs, andere aenderung.
- Bekanntes paar #1614 vs #1645: widerlegt als "gleiche richtung" (entgegengesetzt, konkurrierend).

## B4 — brett-wahrheit (card-status vs. pr-state live)
Befehl pro karte: `gh api repos/mcpdev80/baseharbor/pulls/<n> --jq '.number,.state,.draft,.merged'` (origin/main stand der karte).
| karte/pr | draft | state | merged | diskrepanz? |
|---|---|---|---|---|
| #1665 | false | open | false | nein (draft=false; board open) |
| #1580 | false | closed | true | nein |
| #1578 | false | closed | true | nein |
| #1595 | false | closed | true | nein |
| #1690 | false | open | false | nein |
| #1693 | false | open | false | nein |
| #1704 | false | open | false | nein |
| #1707 | false | open | false | nein |
| #1697 | false | closed | true | nein |
| #1705 | false | closed | true | nein |
| #1706 | false | closed | true | nein |
- Feststellung: KEIN review/draft-mismatch mehr. Der heute frueher dreimal von hand zurueckgezogene fall (review bei draft=true) ist stand 2026-11-20 nicht aktiv; alle karte im review/closed tragen den korrekten pr-state (draft=false bei open, merged=true bei closed).

## cleanliness:
- keine container/compose/netzwerke/volumes/state angelegt; clone `/tmp/opencode/baseharbor-x164` nach pruefung entfernt.
- KEIN write in `workers/baseharbor-plan` (quarantae); KEIN `git -A`; kein produkt-aenderung.
- `/var/tmp/x164-planning-wt` und `/tmp/opencode` bleiben fuer die spaeter audit-karte.
