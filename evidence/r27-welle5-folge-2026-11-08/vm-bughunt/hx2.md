# Bug-Hunt H-X2 — destroy / recreate paths on baha-podman-2

- Card/mission: mission-hunt-hx2.md (Bug-Hunt H-X2, pure findings, no product code, no PRs)
- Shift: r27-welle5-folge-2026-11-08 / round-1
- Worker session: laptop (podman), no subagents
- Planning repo verified (origin/main): ff38cf2e9b3a643ce8a7ee1350bd93e400a2c1c5 (`git ls-remote origin main`)
- Host: baha-runner-podman-2 (192.168.6.107), podman 5.7.0, NO docker, baha c87c8b644cc (commit c87c8b644cc98fe6abf1164d101f42a212558b9d)
- Target: w0427-owner-missing (podman). baseharbor-plan origin/main HEAD at commit time: 6ac728eb

## PLAN

- Read mission + AGENTS; attestation (host, binaries, podman/docker, baseharbor-plan origin/main)
- Baseline host state (app list, podman ps/net/volumes, quadlet units, ~/.baha)
- Build isolated workload-only app hx3app in /tmp/hx3app (root Dockerfile + go.mod so build context == repo root)
- Discover up-gates: --confirm-candidate digest, two-stage provider consent (needs pty), OpenBao Admin dead
- Cut #1 destroy -> immediate re-up (track volumes/records/state.json leftovers)
- Cut #2 destroy with DAMAGED state (record deleted + net removed) — fail-closed message
- Cut #3 control-plane-only up vs full up on one target
- Cut #4 SIGKILL workload container — systemd/DEGRADED/orphan behavior + recovery
- Record positive findings
- Per-finding BF-NN with file:#evidence + class
- VM sweep (baha app list, podman ps/net/volumes, ~/.baha) + cleanliness line
- Publish evidence to origin/main, END

## Baseline / attestation

- Planning repo (authoritative): origin/main = ff38cf2e9b3a643ce8a7ee1350bd93e400a2c1c5
- Product remote HEAD: baha c87c8b644cc (built 2026-11-07)
- Host: baha-runner-podman-2, podman 5.7.0, no docker daemon
- Workload-only app hx3app (app.id 34410441-1f93-4401-871a-57274e131a17), port 8099, local TLS
- No ~/.baha on host (baha stores state under ~/.local/share/baseharbor + ~/.config/baseharbor)

## Host baseline (captured before work)

- Existing lane demoapp (app.id f16b02cb) running; OpenBao Admin + member-1 + postgres + keycloak + caddy present.
- OpenBao Admin container (`bh-w0427-owner-missing-shared-openbao-admin`) PID 1 = `/bin/sh -ec trap : TERM INT; sleep infinity & wait` — the OpenBao server process is DEAD inside its container (0 listening sockets, 0 logs). Only member-1 is healthy. This took down the whole secret/PKI layer.
- demoapp workload (`bh-w0427-owner-missing-demoapp-dev-app.service`) died 2026-11-08 02:17 (SIGKILL/137) — hours before this session; environmental, not caused by this work.

## Findings

### BF-01 — up panics (Go stack printed) without --confirm-candidate; confirm-hash not surfaced to non-TTY
- class: ux
- command/exit/output (exit shown via PIPESTATUS):
  - `baha up --yes` inside hx3app repo:
    - prints a valid candidate block with `confirm-hash c172c96b148a65102338187053fdd561bb592bab4d96b0e4c66be48c7f60326e` and the re-run hint,
    - then prints a Go runtime stack (`main.recordDeploymentBeforeMutation ... deployment_record.go:209`) and exits 1 with `Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`.
  - Evidence transcript captured in-session; source of the panic: `internal/cli.(*Command).Execute` -> `app_apply.go:165` -> `deployment_record.go:209`.
- file:#beleg:
  - `cmd/baha/deployment_record.go` lines 190-215 (candidate choke point; prints stack at 209 via `runtime.Stack`).
  - `cmd/baha/app_candidate_consent.go` `promptConfirmCandidateSubmission` prints the digest only when `submission.SourceRevision != ""`; on a nil/legacy record it still prints, but the digest is not re-emitted on the fail-closed path.
- Impact: the operator sees a raw stack trace instead of the one-line `Re-run with --confirm-candidate <digest>` hint, which is already printed. The stack is noise.

### BF-02 — `up`/`app up` require an interactive TTY for the two-stage provider-impact consent; non-TTY auto-fails even with --yes
- class: ux / daemm
- command/exit/output:
  - `baha up --yes` (no TTY): `Error: provider change: impact-confirmation-required` (exit 1).
  - `baha app down hx3app --yes` (no TTY): same `impact-confirmation-required`.
  - With a pty (script): `printf "y\ny\n" | script -qec "$B up --yes" /dev/null` succeeds past consent; the two prompts are `Achtung: confirm the displayed outcome without a working alternative (1/2, plan <plan_id>)? [y/N]:` and `(2/2, ...)`.
- file:#beleg:
  - `cmd/baha/provider_change_confirmation.go` `readProviderImpactAcknowledgements` — reads two lines from a terminal reader; `noInput(ctx) || in == nil || !readerIsTerminal(in)` returns the consent-required error. `--yes` deliberately does not imply either acknowledgement.
- Impact: automation (CI/scripts/dispatch) cannot converge an app whose provider impact plan has `confirmations_required == 2` (a new managed provider / exposure gateway) without a pty. Non-destructive provider changes also require this.

### BF-03 — DAMAGED deployment state (deployment.json deleted + network removed) makes `up` return a misleading "repository inspection file limit exceeded: more than 10000 relevant files"
- class: ux / daemm / blocker-kandidat
- command/exit/output:
  - Setup: hx3app READY, then `rm deployment.json` and `podman network rm baseharbor-dev-workload-w0427-owner-missing-hx3app-dev`.
  - `baha up --yes`: `Error: inspect repository: repository inspection file limit exceeded: more than 10000 relevant files` (exit 1).
  - With the record present (control), `up` succeeds to READY.
  - strace (pid 1663884): the failing `repositoryinspect.Inspect` walks `/home/marcel` -> `.cache` -> `.cache/go-build/00..NN...` (thousands of dirs) instead of the repo `/tmp/hx3app`. The repo `/tmp/hx3app` is never opened.
- file:#beleg:
  - `internal/repositoryinspect/inspect.go:29` — the `budget.add` returns "more than %d relevant files" (>10000) during `collectSnapshot` WalkDir.
  - `cmd/baha/app_workload.go:96` `selectedRepositoryComposeSource` -> `repositoryinspect.Inspect(context.Background(), repositoryRoot)`.
  - `cmd/baha/app_context.go:51` `repositoryRoot()` returns `RepositoryRoot` (== `/tmp/hx3app`) when set; the damaged-record path yields a wrong root that walks the whole home dir.
  - `internal/application/environment.go:104` `environmentManifestCandidates(current)` walks up `envs/` candidates; `ResolveRepositoryEnvironment` walks parents to `/`.
- Impact: a legitimately damaged deployment record (e.g. disk truncation, partial write, manual cleanup) surfaces as an opaque "10000 files" budget error that walks the entire home directory — slow (strace showed a ~1s+ walk) and unactionable. The correct message would be "deployment record missing / cannot verify ownership; restore or re-init". Blocker for recovering that app.
- Note: the error is deterministic while the record is absent but the deploy dir remains; a second `up` after the dir is fully cleared falls back to a fresh-repo path (prints a different panic-free flow). This is a state-machine edge, not a crash.

### BF-04 — SIGKILL of a Quadlet workload: systemd marks the unit `failed (exit-code)`, container auto-removed, and `baha app list` reports stale `ready` while `baha status` correctly shows `STOPPED`
- class: ux / daemm
- command/exit/output:
  - `podman kill -s SIGKILL bh-w0427-owner-missing-hx3app-dev-app`
  - systemd: `bh-w0427-owner-missing-hx3app-dev-app.service: Main process exited, code=exited, status=137/n/a` then `Active: failed (Result: exit-code)`.
  - container auto-removed (unit uses `--rm`); no orphan process, no stray `:8099` listener.
  - `baha app list` (immediately after): `hx3app  dev  ready  OK` (STALE — workload is actually down).
  - `baha status`: `Application STOPPED  persistent application state preserved`.
  - Recovery: `baha up --confirm-candidate <hash> --yes` rebuilds the container and returns to READY.
- file:#beleg:
  - Quadlet unit `~/.config/containers/systemd/bh-w0427-owner-missing-hx3app-dev-app.container` (ExecStart has `--rm --replace`).
  - `status` reflects STOPPED; `app list` reflects applied intent, not live container health.
- Impact: `app list` "ready" is intent-based, not health-based. On a SIGKILL/OOM the operator scanning `baha app list` sees `ready` while the workload is STOPPED. `status` is the correct health view but is more verbose. Documented; positive: recovery is a single `up`, no orphaned containers or listeners.

### BF-05 — Destroyed-but-retained deploy record with a deleted repo => `app list` shows `MISSING`
- class: doku
- command/exit/output:
  - Deleted repo `/tmp/hx2app` while deploy record `97e33e1e…` retained.
  - `baha app list`: `hx2app  dev  failed  MISSING`.
  - `baha inspect`: `Error: inspect repository: open /tmp/snap-private-tmp: permission denied` (when cwd is `/tmp`).
- file:#beleg:
  - `deployment/…/deployments/97e33e1e-…/deployment.json` (record.source.repository = /tmp/hx2app, now absent).
- Impact: dangling deploy records for removed repos surface as `MISSING`; the operator must reconcile (remove the record). Also the `/tmp/snap-private-tmp` permission error on inspect from `/tmp` is a host quirk, not product.
- POSITIVE: destroy retains protected runtime files (application.env, bindings, applied-*.sha256, workload.override.yaml) with explicit "retained" notices — recovery owner is preserved and no data deletion is authorized by runtime removal.

### BF-06 (POSITIVE) — workload-only app recovers from destroy->immediate re-up in ~2s; state retained and re-verified
- class: doku / positive
- command/exit/output:
  - `baha destroy --yes` -> `hx3app  dev  runtime-retired  OK`; containers gone, workload container gone, workload network gone, but runtime state files + quadlet units retained.
  - immediate `baha up --confirm-candidate <hash> --yes`: `[OK] Starting repository workload - done (2.1s)`; `state.json` restored; network recreated; `baha status` READY.
  - Compare fresh `up` earlier took ~6.6s; re-up after destroy ~2.1s (image cached, network recreated).
- file:#beleg:
  - deploy dir retained at `deployments/<id>/state/hx3app/runtime/{application.env,bindings,compose.yaml,runtime.env,applied-control-state.sha256,applied-desired-state.sha256,workload.override.yaml}`.
- Impact: destroy->re-up is a clean, fast lifecycle; the retained-state recovery owner model works.

### BF-07 (POSITIVE) — control-plane-only up on one target starts SQL+Secrets+Identity and reports Core READY without a workload
- class: doku / positive
- command/exit/output:
  - `baha up --control-plane-only`: `[OK] postgres verified TLS …`, `[OK] openbao initialized, unsealed …`, `BaseHarbor Core READY: SQL + Secrets + Identity.`
  - Works on the same target where a workload app was already up.
- Impact: operators can bring up / verify the control plane independently of any workload on one target.

## Host fault (environmental, not product)

- OpenBao Admin process dead inside its container (`sleep infinity` only, 0 logs, 0 listeners) since before this session; took down the shared secret/PKI layer. Every app requiring secrets/PKI/identity failed at the `managed service PKI` preflight with `OpenBao AppRole login failed … EOF`. Workload-only apps (hx3app, demoapp) are unaffected at the workload layer but demoapp's own workload died at 02:17 for the same host reason.
- This is the demoapp lane's shared Core state; repairing it is out of scope for a findings lane (must not touch other lanes' resources). Documented so the coordinator can route a recovery card.

## repo-rule compliance

- Pure findings: no product code changed, no PRs opened, no `.github/**` edits, no reruns/workflow_dispatch.
- Evidence written only in baseharbor-plan (repo `mcpdev80/baseharbor-plan`), not in any product repo. No `.evidence/` dir in a product repo. No main-branch writes in product repos.
- One integration candidate per chain: no product branch was cut (findings-only). No PR.
- Subagents: none used (4.8).
- Host runners only; no runner infrastructure touched.

## VM sweep (before END)

- `baha app list`: only `demoapp` remains (failed, environmental); my hx2app/hx3app records removed.
- `podman ps --name`: `no hx3 containers` / clean (no hx2/hx3).
- `podman network ls`: `no hx3 nets` / clean.
- `podman volumes ls`: no hx2/hx3 volumes (my app declared none; workload-only).
- `~/.baha`: does not exist (state under ~/.local/share/baseharbor + ~/.config/baseharbor); no leftover hx2/hx3 entries.
- cleanliness: DONE — no test containers, networks, volumes, deploy records or scratch dirs for hx2/hx3 remain.

## END

END mission-hunt-hx2.md: 7 findings (BF-01..BF-07) incl. 1 blocker-kandidat (BF-03) + host OpenBao fault -> meldefenster met.
