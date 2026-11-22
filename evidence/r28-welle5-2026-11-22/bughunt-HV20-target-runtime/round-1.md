# H-V20 bug-hunt target/runtime selection — round-1 akte

Sitz `w21-pr1702-0428-142-compat`. REINE BEFUNDUNG, KEINE Produkt-Änderung, KEIN PR.
Objekt: develop `8629450ef3c5198bb675331c12f56b2c9377aa1c`.
Schnitt H-V20 'ziel-und-laufzeit-auswahl-desk': prüfen die freigegebene Oberfläche, an der die letzten
Merges gerüttelt haben, und melden, was dort FÄLSCH, MEHRDEUTIG oder STUMM ist.

## PLAN

- Plan in board-file + ## PLAN in akte
- ls-remote + base attestation: develop 8629450e
- Befund 1: `baha target` / Ziel-Definition + Abweisung nicht-registrierten Ziels (0428-214, 0428-209)
- Befund 2: `baha env delete` retained-running state runtime-retired/stopped (PR 1627, 0428-061)
- Befund 3: `baha apply/up --workload-port` auf develop (PR 1723, nicht mergen)
- Befund 4: Host-Config-Isolation Cleanup (PR 1762, 0428-233) Test-Verzeichnis im globalen Raum
- Akte ## funde + publish origin/main + END + Coordinator-Post

## Base attestation

- Real GitHub remote (verify via `git remote -v` in shared baseharbor worktree)
- develop HEAD: `8629450ef3c5198bb675331c12f56b2c9377aa1c`
- Keine offenen PRs / kein HA im Hunt-Objekt; v0.4.27 released (hunt-freigabe 2026-11-17)

## Funde

(separate sections below)

## Cleanliness

(no containers/networks/volumes created; `docker ps -a` empty; worktree detached at develop HEAD)

## Evidence remote line

(to be pasted after publish)
