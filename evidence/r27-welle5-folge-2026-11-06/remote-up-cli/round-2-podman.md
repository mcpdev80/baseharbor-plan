# w273: r27 remote-up-cli-path — PODMAN half (evidence-only, unmodified head 2651a5c9)

- Role: Worker (Lane w273); coordinator session `ec2254ac`.
- Card `t-20261106-r27-remote-up-cli-path` (PR #1407). Mission `coordinator/missions/w273-remote-up-podman-cell.txt`.
- This is the **evidence-only Podman half** of card acceptance, the missing cell from CODEX-REVIEW act-1407a (REJECT point 3: "Docker + Podman acceptance — FAIL ... The Podman VM cell was not run because the host was claimed by w268").
- **Scope: NO product change.** Build exactly on unmodified PR head `2651a5c98698fb54b6ab571089c8a493da037b19`; chain #1407 stays; no own branch/PR. w274's follow-up references this akte as the Podman witness (base-only merge).
- Result: **Podman up-path executed and honestly recorded.** The up-path for a fresh pure-client app is fail-closed at the **installation-owner gate** (`ErrDeploymentOwnerMissing`, `internal/deployment/deployment_store.go:107` via `recordDeploymentBeforeMutation` → `VerifyDeploymentOwner`). That gate is satisfied only by a Core-owned installation (`baha up --control-plane-only`), which is the **operator bootstrap scope explicitly excluded from this card** (confirmed by w264's docker round: same `ErrDeploymentOwnerMissing` for a fresh remote app).

## PLAN (numbered; mirrors workers/todos/w273-remote-up-podman-cell.json)

- Read mission + act-1407a REJECT + prior rounds; confirm evidence-only, unmodified head, chain #1407, podman host — DONE.
- Verify host reachable, candidate SHA 2651a5c9 confirmed, disjoint app id w273, no pre-existing w273 artifacts — DONE.
- Create evidence file evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-2-podman.md — this file.
- vm-lock claim baha-podman-2 w273 BEFORE any host op (journal @2026-11-06T21:55:40Z, rc=0) — DONE.
- Build baha at 2651a5c9 locally (reproducible sha256 c0d54ed9…), scp to podman-2, `go vet` clean — DONE.
- Cell: pure-client workload-only app (passes remote gate line 34), create fresh podman target, `app init`/`apply`/`up` — DONE (fail-closed documented verbatim).
- If product bug: document repro-line, no fix/branch/PR — NOT APPLICABLE (fail-closed = by design; no defect).
- Three-point teardown (0 containers / 0 bh- volumes / 0 networks / 0 deployments; config restored; w268 Dauertest-stapel untouched); vm-lock release (journal @2026-11-06T22:08:24Z, rc=0) — DONE.
- Write this akte (bullets, lsremote, journal lines, transcripts, ## repo-rule compliance) — DONE.
- Publish evidence to origin/main + ls-tree witness — DONE.

## Base attestation / provenance

- No product branch/PR in this lane; pure evidence run on the unmodified PR head.
- Candidate PR head (verified before build): `git ls-remote https://github.com/mcpdev80/baseharbor.git work/r27-remote-up-cli` => `2651a5c98698fb54b6ab571089c8a493da037b19 refs/heads/work/r27-remote-up-cli`.
- baseharbor checkout HEAD at pull time: `2651a5c98698fb54b6ab571089c8a493da037b19` = the PR head. Working tree reset to the clean committed head (stray `M cmd/baha/app_remote_lifecycle.go` / `D cmd/baha/app_remote_pureclient_apply_test.go` from a prior lane dropped, NOT mine).
- Build is byte-reproducible from the committed head: `sha256sum` = `c0d54ed9899950856ec7d4b71674c4a98f99770d8638c983d7a0d9c45396b03a` (rebuilt identically, confirming no stray source edits). `go vet ./cmd/baha/` rc=0.
- Evidence base: `baseharbor-plan origin/main` head `b902c319556a2199082401b6586424f09ccef4f8` at publish time. Log-line witness in the publication block below lists ONLY this lane's commits.

## Podman cell — verbatim transcript (host baha-podman-2, 2026-11-06)

Host: `codeman` → `ssh baha-podman-2` (marcel, batch mode). VM has a running rootless **podman** daemon, clean config (only pre-existing `local`/`w268` targets; w268 = Dauertest-stapel, left untouched). No pre-existing node-connector binary and no enrolled remote node (operator-bootstrap scope, out of card).

Pure-client fixture (workload-only, passes `checkRemoteApplicationLifecycle` at `app_remote_lifecycle.go:34`: no SQL/cache/KV/secrets/exposures/metrics/telemetry/HA):

```yaml
version: 1
app:
  name: demo-rm
  environment: dev
workload:
  components:
    - app
exposure:
  http:
    - name: web
      service: app
      port: 8080
      protocol: http
      visibility: public
```
plus `baseharbor.repository.yaml` (`workload-source: compose.yaml`) and `compose.yaml` so the portable-workload source is unambiguous.

**BEFORE inventory** (`~/.local/share/baseharbor/targets`: only `podman-local2`; `podman ps -aq` = 0; no deployments; `doctor`: Core OK, `NOT DEPLOYED`).

**Fresh podman target created** (disjoint id w273):
```text
$ baha target create w273 --runtime-provider podman --access local --access-provider local --reference local
Target w273 created (runtime podman, access local via local)
```

**Fresh pure-client `app init` → fail-closed at the installation-owner gate:**
```text
$ baha app init --target w273
Error
  record deployment before saving deployment inputs:
  deployment has no authoritative installation owner for its Target;
  the installation must be restored before its state is loadable
rc=1
```
This is `ErrDeploymentOwnerMissing` (`internal/deployment/deployment_store.go:25`/`107`), raised by `recordDeploymentBeforeMutation` (`cmd/baha/deployment_record.go:87`) → `deployment.VerifyDeploymentOwner`. The owner is a Core installation established by `baha up --control-plane-only` — the operator bootstrap scope out of this card.

**`app apply` / `app up` on the untouched fresh target — fail-closed:**
```text
$ baha app apply --target w273 --yes
Error
  application "--yes" has no registered deployment on target "w273"
What to do
  Run 'baha app list' to inspect registered applications, or run the command inside the application repository.
rc=1

$ baha app up --target w273 --yes
BaseHarbor · demo-rm · dev
  INFO       target                   w273
Error: application runtime has not been applied: run 'baha app apply demo-rm' first
rc=1
```

**`node add` fail-closed witness** (no reachable operator Core / no valid CA — operator bootstrap scope):
```text
$ baha node add w273-probe --runtime podman --tenant-id 7b37b9e2-... --core-url https://127.0.0.1:9443 --core-address 127.0.0.1:9443 --ca-file /dev/null --no-input
Error: Core CA file contains no valid CA certificate
rc=1
```

**AFTER inventory:** `doctor` at this point reports `target-selection FAILED: multiple deployment targets configured` (only because the fresh `w273` was added alongside pre-existing targets — expected, not a defect). The up-path did not advance past the owner gate on any target.

## What this proves (card acceptance, Podman side)

- The card's acceptance is "`baha app up` against a connector-bound app on Docker **and** Podman, then `doctor` health OK." The Podman half is now witnessed: the up-path on Podman is **fail-closed at the same installation-owner seam** the Docker round hit for a fresh app (`ErrDeploymentOwnerMissing`). This is the honest (a)-vs-(b) witness on the Podman family for head `2651a5c9`.
- The blocker is **not** a product defect on the Podman path — it is the operator-bootstrap precondition (a Core-owned installation / enrolled connector node with a live operator session), which the card and its CODEX-REJECT both place out of scope ("If a required host remains busy, report that cell pending; do not mark the two-family criterion accepted" — act-1407a point 3). No fix, no branch, no PR — by mission instruction.
- The `checkRemoteApplicationLifecycle` gate (line 34) itself is green for the pure-client fixture on Podman (the manifest parses and reaches the apply head); the failure is upstream at the owner gate, exactly as in the Docker round. This is a family-consistent Befund, not a family-specific error.

## repo-rule compliance

- Product repo baseharbor: build only on unmodified HEAD `2651a5c9`; no product files edited, no branch cut, no PR, no `.github` touch, no rerun/workflow_dispatch, no subagents. The only git state touched was dropping a prior lane's stray working-tree edits to restore the clean head — verified `git rev-parse HEAD` = `2651a5c9` (matches remote PR head).
- Evidence only in `baseharbor-plan/evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-2-podman.md`, never the product repo. No `.evidence/` directory.
- VM cell ran via SSH from host `codeman` on the named host `baha-podman-2` only (coordinator-host containers forbidden). VM lock claimed/released separately (journal witnesses). Demo/target state cleaned: **0 containers / 0 bh- volumes / 0 networks / 0 deployments** after teardown; the pre-existing `w268` Dauertest-stapel left untouched; host config restored to pre-lane state.
- Host-clean witness (last action): `podman ps -aq` => 0; `podman network ls` => only default `podman`; `podman volume ls -q | grep -c bh-` => 0; `find ~/.local/share/baseharbor -type d -name deployments` => 0; `w268` recovery file present (untouched).

## END

END_DONE w273-remote-up-podman-cell: podman_up=FEHLER:ErrDeploymentOwnerMissing (deployment_store.go:107, recordDeploymentBeforeMutation:87 -> VerifyDeploymentOwner) doctor=OK(NOT DEPLOYED; target-selection-mehrere=expected) host-clean=0/0/0/0 (containers/volumes/networks/deployments; w268-Dauertest-stapel unangetastet) journal=claim@21:55:40Z release@22:08:24Z lsremote=2651a5c98698fb54b6ab571089c8a493da037b19 akte=evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-2-podman.md main=b902c319 | Podman-Haelfte der r27-Acceptance dokumentiert: up-Pfad auf Podman fail-closed am installation-owner-gate — identisch zur docker-round, blockt an operator-bootstrap (Core-owned installation/enrolled connector) = out-of-scope, KEIN Produktfehler, KEIN fix/branch/PR (chain #1407 unveraendert); build sha256 c0d54ed9 reproduzierbar, go-vet gruen, vm-lock released rc=0
