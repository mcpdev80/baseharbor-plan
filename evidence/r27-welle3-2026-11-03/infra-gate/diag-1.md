# w79-infra-diagnosis: docker/podman lifecycle+backup-restore Selected-Runtime-Jobs failern — Diagnose

- [x] w79-infra-diagnosis · read-only Infra-Diagnose: genauer fehlerschritt im hosted-lauf + kette lokal nachgefuhrt + letzter gruener lifecycle-lauf verglichen + verdichtetes urteil (runner/workflow/demo-ref)
  <!-- lane w79 · coord f49a3303 · read-only, KEINE produkt-datei, KEINE worktree-aenderung, KEIN push -->

## Observable outcome

Die `Selected Runtime`-Jobs (docker/podman, lifecycle + backup-restore) in `pre-release-runtime-suite.yml`
**failern nicht an runner/workflow/matrix**, sondern an einem **repo-seed-seitigen owner-seam**: der
kandidat, den der gate-lauf ausfuhrt, tragt die `w2-state-owner`-Einbindung (`VerifyDeploymentOwner`,
`ErrDeploymentOwnerMissing`), die demo-state ist aber **vor** einer installation ohne Core-Installation
gespeichert — `coreinstallation.Load(runtime_root)` faillt → fail-closed. clean develop (2cadfcee) hat
diesen seam NICHT → gate lauft.

## 1. Genauer fehlerschritt im hosted-lauf (#1347, run 41726952160)

- Job (GH API): `PR · Selected Runtime (atomic/docker/lifecycle, docker, lifecycle) / Executed docker · lifecycle`
  `jobs/126235859955`; backup-restore `jobs/126235860060` (docker), `jobs/126236237937` (podman).
- Failing step = **"Run runtime gate"** (conclusion: failure). Alle vorschritte **success**:
  `Set up job / Validate candidate ref / Checkout / Prepare verified rootless runtime /
  Resolve candidate SHA / Set up Go / Reset runtime state / Load prebuilt runtime image /
  Checkout exact demo revision / Validate gate resource declaration`.
- Kommando (dokumentiert aus run-log, `set -euo pipefail`):
  `bash scripts/acceptance.sh "$GATE"` im demo-workdir mit `BASEHARBOR_SOURCE_REF="$CANDIDATE_SHA"`,
  intern `guided-up` via `tests/guided/drive.py:268` → `drive.py:194 run_tty` → `RuntimeError:
  guided-up failed with exit code 1`.
- Ausgabe / fehlerzeile (wortlich, run-log 41726952160, docker/lifecycle):
  `Error: record deployment before saving deployment inputs: deployment has no authoritative
  installation owner for its Target; the installation must be restored before its state is loadable`
  → `RuntimeError: guided-up failed with exit code 1` → `##[error]Process completed with exit code 1.`
  backup-restore (docker + podman) analog:
  `Error: missing deployment state for atomic-<runtime>-backup-restore/demo/dev [<uuid>]: deployment has no
  authoritative installation owner for its Target; the installation must be restored before its state is loadable`.
- Candidate-SHA im loop: `8236fe9ae15025cdbdbd726f8be16009273fca29` (Merge f3ea54e2… into 2cadfcee),
  PR_BASE_SHA = EVENT_BASE_SHA = `2cadfcee8161…` (develop), RUNTIME=docker, GATE=lifecycle/backup-restore.

## 2. Kette lokal nachgefahren (clean develop 2cadfcee vs. kandidat 8236fe9a)

- clean develop checkout 2cadfcee lokal: **kein** `VerifyDeploymentOwner`, **kein**
  `ErrDeploymentOwnerMissing`, **kein** `TenantOwnerResolver`, **kein** `recordBackendPlacementOwner`-owner-hook.
  → gate-Codepfad ohne owner-check → lifecycle+backup-restore laufen durch.
- kandidat `8236fe9a` = Merge `f3ea54e2` (PR #1347 w2-state-owner) into develop. In `f3ea54e`:
  - `cmd/baha/deployment_record.go:67`: `VerifyDeploymentOwner(Target, installationRootFor(TargetStateRoot), DeploymentID)`
    im `recordPendingDeployment`-pfad (firing: `record deployment before saving deployment inputs`).
  - `internal/deployment/deployment_store.go:82 VerifyDeploymentOwner` → `coreinstallation.Load(targetRoot)`
    → bei fehlender `installation.json` = `ErrDeploymentOwnerMissing` (Zeile 25, wortlich wie CI-Output).
  - `TenantOwnerResolver` (deployment_store.go) defaultt **fail-closed** (w2-state-owner, f3ea54e).
- Abreisspunkt der kette (nicht pull/compose/doctor/image): **`coreinstallation.Load(runtime_root)`**
  liefert `os.ErrNotExist` → `ErrDeploymentOwnerMissing`. Image-pull / compose / rootless-runtime /
  demo-checkout sind success (run-log). Der zustand ist **vor** einer Installation ohne installation →
  "doctor NOT APPLIED statt READY".

## 3. Vergleich mit letztem bekannten gruenen lifecycle-lauf (#1358-zeitfenster)

- #1358 (ci-pr-incremental-checks, head fddff70d) = **ci-reuse-/matrix-fix**, merge in develop 2cadfcee;
  aendert nur `scripts/pr-incremental-reuse.py` (+ test). Kein produkt-, kein seam-Änderung.
- develop-push CI (`CI · develop`) **skipped** die native runtime-gate auf push; gate-aktiv nur auf PR
  (`ci.yml:892 matrix = runtime_matrix`). Grune develop-runs (z.B. 41557864008) zeigen
  `Selected Runtime → skipped` auf push → kein gruner hosted lifecycle-run mit aktivem seam vergleichbar;
  vergleichbar ist der gate-Codezustand (identisch, reuse-fix beruht darauf).
- Geaendert zwischen gruen und fehlerhaft = **nur** der kandidat-seam (w2-state-owner #1347 in 8236fe9a),
  **nicht** umwelt/routing/matrixform: matrix-routing bleibt `pr-selected-runtime-matrix.py` +
  `pr-gate-plan.py` (file→gate map; z.B. `app_edit_apply.go → atomic/docker/lifecycle`, pr-gate-plan.py:136-139).

## 4. Verdichtetes urteil (je belegzeile)

- **[x] runner-seitig: NEIN.** Alle runner-seitigen schritte success; runner-version 2.338.2,
  hosted compute agent; docker.sock/podman rootless vorbereitet (run-log). Kein infra-/isoliert-/
  rootless-befund.
- **[x] workflow-yml: NEIN.** `pre-release-runtime-suite.yml` gate-step + matrix-scope unveraendert;
  matrix-shape-fix (#1360, in 2cadfcee) touched nur `scripts/pr-incremental-reuse.py`. Kein workflow-
  trigger-/matrix-befund.
- **[x] demo-repo-seitig (baseharbor.yaml ref drift): NEIN.** pinned demo_ref = `cd9176e0129f…`,
  current `baseharbor-demo` main HEAD = `cd9176e0129f…` (gh api ref/heads/main) → **kein drift**.
- **[x] repo-seitig (owner seam, w2-state-owner #1347, kandidat 8236fe9a): JA (schuld).**
  Beleg: `internal/deployment/deployment_store.go:25` `ErrDeploymentOwnerMissing` wortlich = CI-fehler;
  `cmd/baha/deployment_record.go:67` ruft `VerifyDeploymentOwner` im pending-pfad; clean develop
  (2cadfcee) hat diesen seam nicht → gate lauft, kandidat nicht. Demo-state ist vor installation ohne
  Core-installation → fail-closed.

## repo-rule compliance

- NUR evidence/datei geschrieben: `baseharbor-plan/evidence/r27-welle3-2026-11-03/infra-gate/diag-1.md`.
- Keine produkt-datei anagetastet, keine worktree-aenderung im produkt, kein push auf produktzweige.
- Hosts baha-docker/baha-podman nutzungspflichtig, bh-*shared* unangetastet; cleanup nach gebrauch.
- gh api nur lesend; lokale reproduction nur im read-only clone /tmp/baha-clean (ausserhalb des worktree).
- Befunde gegen neutrales clean develop (2cadfcee) verifiziert, nicht gegen eine sandbox-hypothese.

## END

_LANE w79: END_DONE · schuld=repo-owner-seam (w2-state-owner #1347 in kandidat 8236fe9a), nicht
runner/workflow/demo-ref · sicherheit=mittel (fail-closed-seam, demo-seed vor installation) · beleg=
baseharbor-plan/evidence/r27-welle3-2026-11-03/infra-gate/diag-1.md · CI-/hosted lifecycle+backup-restore
Selected-Runtime-Jobs faellen an dem repo-seed-seam: kandidat tragt VerifyDeploymentOwner/
ErrDeploymentOwnerMissing (f3ea54e/#1347), demo-state vor installation ohne Core-installation → fail
closed; clean develop 2cadfcee hat den seam nicht; runner/workflow/matrix/demo_ref (cd9176e) unveraendert.
