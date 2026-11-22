# 0428-063 index-carrier (PR 1623) — round-1 akte

Sitz `w21-pr1702-0428-142-compat`. Integrationstraeger fuer karte 0428-063, PR 1623.
Auftrag: die drei reservierten ERZEUGTEN dateien aus dem ausgelieferten command-baum NEU erzeugen
(Generator AUSFUEHREN, NICHT von hand aendern), nur diese drei dateien committen, pushen, kleinen PR
gegen develop. Der branch ist der TRAEGER: PR 1623 hoepft spaeter auf ihn.

## PLAN

- Plan in board-file + ## PLAN in akte
- ls-remote + base attestation: develop 8629450e; branch lane-0428-063-index-carrier
- Generator scripts/** lesen (NICHT aendern); erzeugende Befehle identifizieren
- Generator ausfuehren -> drei dateien: docs/cli/command-index.md, docs/de/cli/command-index.md, docs/reference/cli-machine-coverage.md
- Commit nur dieser drei dateien; push (normal); branch + head-sha melden
- Kleiner PR gegen develop (NU3 die drei dateien); hosted run bis terminal; run-id, failed-zahl
- END + coordinator-post

## Base attestation

- develop HEAD: `8629450ef3c5198bb675331c12f56b2c9377aa1c`

## generator:

(to be recorded: which command generated the files)

## funde / status:

(to be recorded)

## Cleanliness

(no containers/networks/volumes created; worktree detached at develop HEAD)

## Evidence remote line

(to be pasted after publish)
