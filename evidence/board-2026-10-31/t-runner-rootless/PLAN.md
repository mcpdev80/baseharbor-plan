# PLAN — Mission `t-runner-rootless` (Runner rootless-Infra: Diagnose + §6.2-Reparatur)

**Task-Tag:** t-runner-rootless
**Role label:** WORKER (Infra-Diagnose/Reparatur, kein Produkt-Repo)
**Datum:** 2026-10-31
**Evidence-Pfad:** `baseharbor-plan/evidence/board-2026-10-31/t-runner-rootless/`

## Kontext (aus Mission)
Critical-Path-Blocker: PR #1236/#1225 "PR Selected Checks" failen auf den self-hosted rootless
Runnern (Targeted HA docker + podman). o1241-Befund: "sudo denied" beim rootless-runtime.

RUNNER-HOSTS: baha-runner-docker-2 (rootless docker), baha-runner-podman-2 (rootless podman).
SSH-Zugriff (Config-Shortnames): `baha-docker` -> 192.168.6.166, `baha-podman` -> 192.168.6.148.
Jobs laufen als User `github-runner` (uid 1001). Workspace: `/home/github-runner/actions-runner/_work`.
Eigener Login als `marcel` (uid 1000, sudo-Gruppe) — Diagnosen als `github-runner` (`sudo -n -u github-runner`).

## §6.2-Regel (RUNBOOK)
- Rootless Docker als enabled User-Service + Linger=yes; Socket-Eigentum via ExecStartPost-Override.
- DESTRUKTIV (podman system reset, Unit-Wipe, workspace-rm) NUR nach DREI-PUNKTE-PRUEFUNG + Evidence.
- Bei Owner-/root-Rechten die ich nicht habe: exakten Befehl + Begründung als REZEPT liefern (END_BLOCKED/recipe_for_owner).
- shared Stacks `bh-*-shared-*` NIE anfassen.

## CHECKLISTE
- 0. Turn-Pflichtprogramm (basics-check, events --ack) DONE
- 1. SSH-Zugriff verifizieren (baha-docker, baha-podman) DONE
- 2. Lese-Diagnose auf baha-docker als github-runner (systemctl --user docker, XDG_RUNTIME_DIR, sock, linger)
- 3. Lese-Diagnose on baha-podman als github-runner (loginctl linger, stale netns, podman)
- 4. ECHTEN CI-Fehler belegen (gh run view 41203321449 --log-failed; gh api jobs 124543372909/124543373358)
- 5. Root-Cause-Zeiline exakt extrahieren (socket denied / linger off / netns)
- 6. Reparaturschritte planen — non-destructiv innerhalb meiner Rechte
- 7. (optional) destruktiv nur nach 3-Punkte-Prüfung; bei root/sudo-Need -> recipe-for-owner
- 8. Verifikation: docker/podman run hello-world als github-runner
- 9. REPARATUR-STATUS setzen ({fixed-and-verified | recipe-for-owner | still-blocked})
- 10. Handoff via `codeman agent post`
- 11. END-line in Evidence + Evidence-Publish (render + check)

## REPARATUR-STATUS
RECIPE_FOR_OWNER (Endstatus; Details in DIAGNOSIS.md / CI-ERROR.md / REPAIR.md)

## END-line
END <lane> BLOCKED t-runner-rootless: recipe_for_owner — CI sudo-Defekt (docker+podman rootless Runner gesund; github-runner hat kein sudo; scripts/ci-core-rootless-runtime.sh braucht sudo) — Rezept in REPAIR.md, Owner-Ausführung; Evidence committet fb81d22.
