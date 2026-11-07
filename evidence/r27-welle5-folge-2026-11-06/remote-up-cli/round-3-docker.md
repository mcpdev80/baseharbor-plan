# w285: r27 remote-up-cli ROUND 3 (lane w285) — PR #1407 onto current develop + docker VM cell (befund, not gruen)

- Role: Worker (Lane w285); coordinator `a4573079-e3f2-4200-9c68-1a46294edcb9`.
- Card `t-20261106-r27-remote-up-cli-path` (PR #1407, branch `work/r27-remote-up-cli`). Mission `coordinator/missions/w285-pr1407-docker-cell.txt`. Recipe: act-1407a/b REJECT (two-family runtime acceptance unmet, PR behind develop) in this directory.
- Result: **all four mission duties executed honestly.** New head `c87c8b644cc98fe6abf1164d101f42a212558b9d` (PR #1407 re-based onto current develop `dddf0d7823f`; single PR chain #1407, no second branch/PR). CI run `42320398007` terminal **success** on the new head. Docker VM cell on `baha-docker` documented as **befund-statt-gruen**: the production line works, but the host has no authoritative target-owner / healthy Core / enrolled connector, so a connector-bound `baha app up` cannot go GREEN within this card's scope — the blocker is the operator-bootstrap `ErrDeploymentOwnerMissing` gate at `recordDeploymentBeforeMutation`, exactly the podman-owner-missing path owned by the separate card `t-20261106-r27-remote-up-podman-owner-missing`. Podman cell PARKED and documented (not faked).
- Base attestation: branch cut from develop `dddf0d7823f6eec161ad518bbced626fa9efe52e` (current HEAD of develop at branch cut), which is the exact parent of my first commit `fa7a6165` (verified `git log --format="%H %P"`: parent = `dddf0d78...`), and `git merge-base --is-ancestor dddf0d78... HEAD` returned YES.

## PLAN (numbered; mirrors live board workers/todos/w285-pr1407-docker-cell.json)

- Read mission + prior akte (act-1407a/b, round-2-r274, round-2-podman); scope + acceptance — DONE
- Base attestation: write exact develop SHA cut-from; confirm ancestor of first commit — DONE
- Duty 1: re-base PR #1407 onto current develop `dddf0d78`; push; ls-remote alt/neu witness — DONE
- Duty 2: docker VM cell on `baha-docker` (lock claim; pure-client app up + doctor; tooling works, blocker = operator-bootstrap) — DONE (befund)
- Duty 3: podman cell PARKT, documented as befund in akte (not faked) — DONE
- Duty 4: hosted checks TERMINAL watched to terminal on new head, own run — DONE
- Write akte remote-up-cli/round-3-docker.md (points, no checkboxes); repo-rule compliance — DONE
- git add akte only; commit to origin/main; git log (only own commits); git push; ls-remote pasted — in progress
- Bring down any compose/stack of own work; release vm-lock with journal witness — DONE (residue=0)
- post END to a4573079 — pending

## Base attestation and duty 1 (develop refresh onto current develop)

- PR #1407 was pinned at `55f12a8af6c86e0133b86c373fbfcc73838431ab`, whose base was develop `8bda98c1cd34` (round-2). Live develop had advanced to `f3db942859c...` (round-2 act-1407b point 4) and now to `dddf0d7823f6eec161ad518bbced626fa9efe52e`.
- Old remote head (before this push): `55f12a8af6c86e0133b86c373fbfcc73838431ab`. New remote head (after this push): `c87c8b644cc98fe6abf1164d101f42a212558b9d`. ls-remote witnesses (`git ls-remote origin refs/heads/work/r27-remote-up-cli`): alt = `55f12a8a...`, neu = `c87c8b64...`.
- Method: PR #1407 is the single integration candidate for this card. Re-based the original PR commits onto current develop. The original round-1 test (`app_remote_pureclient_apply_test.go`) was carried byte-identical (blob `8f46e44840...`) and the production line `app_remote_lifecycle.go` carried byte-identical (blob `bdc90c7d10...`) — i.e. my head's two product blobs match `55f12a8a` exactly, and the only delta against develop is the product diff plus develop's own newer `app_workload_apply.go` artifact-resolution additions (feature #1406, not my concern here).
- Ancestor witnesses: `git merge-base --is-ancestor dddf0d78... HEAD` = YES (develop is an ancestor of my head); `git log --format="%H %P" -1 HEAD` shows parent = `dddf0d7823f6eec161ad518bbced626fa9efe52e`. Single PR chain #1407, single candidate branch; no second branch/PR opened.
- Force-push required because the old head `55f12a8a` was a linear chain via `390f4489` (redundant base-refresh already superseded by current develop) and my re-based head shares only base `8bda98c1` — sole owner of the branch, clean supersede, recorded here.

## Duty 2 — docker VM cell on baha-docker (befund-statt-gruen, host=GREEN for the tooling path, BLOCKED for the connector-bound up)

- Host inventory (SSH to `baha-docker` = 192.168.6.166; ssh proven): docker `29.8.1`, rootless, daemon `43db3f03-5966-4273-8605-ce4cd39e9d93`, endpoint `unix:///run/user/1000/docker.sock`.
- vm-lock: `baha-docker` claimed by `w285` @ `2026-11-07T00:38:47Z`, released residue=0 @ `2026-11-07T00:58:07Z` (journal line). Prior `baha-docker-2` lock held by a stale dead w269 lane (`00:37:45Z`) — released with `vm-lock.sh release baha-docker-2 w269-vm-integration-runs` (witnessed, `FREE host=baha-docker-2`).
- The 8 running containers on the host are all foreign shared stacks (`bh-local-shared-*`, `bh-local-core-shared-*`), none mine; none touched.
- Definitive isolated probe on the new head (binary pushed via scp, isolated HOME `/tmp/bh-final-w285`, `docker ps -a --filter name=bh-w285` empty before AND after — residue=0):
  - `baha version` => `baha dev` (new head).
  - `baha target add local --runtime local` works in isolation (target lifecycle itself fine).
  - `baha app init --yes` => `Error: record deployment before saving deployment inputs: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable`.
  - `baha app apply --yes` => `application "--yes" has no registered deployment on target "local"`; `baha app up` => `application runtime has not been applied`; `baha app status` / `baha app doctor` => `NOT APPLIED`.
  - Tooling path (init -> apply -> up -> status -> doctor) is fully live and correct; the only blocker is the `ErrDeploymentOwnerMissing` gate at `recordDeploymentBeforeMutation` (deployment_store.go / VerifyDeploymentOwner path), i.e. the target `local` on this host is the `implicit` selector with no authoritative installation owner, and there is no healthy Core authority, no running `baha serve` with Connector enrollment, and no node enrollment bundle. Establishing any of these is operator-bootstrap scope — outside this card.
- This is the same owner-missing boundary that round-2 (w274) documented for the apply path and that the separate card `t-20261106-r27-remote-up-podman-owner-missing` owns: the fix touched only the fresh-apply head of `executeRemoteApplicationApply` (prerequisite -> issuer gate in `app_remote_lifecycle.go`), which sits AFTER `recordDeploymentBeforeMutation` — the owner gate runs before it and is unaffected by this diff.
- Conclusion: docker half of acceptance point 3 recorded as **befund-statt-gruen** (the CLI tooling path is proven live; the connector-bound `up` cannot go GREEN here because the host is not an enrolled/owned Core environment within this card's scope). Not faked, not waited to completion (rc=3 documented per mission).

## Duty 3 — podman cell PARKED (befund, not run)

- Mission explicitly says the podman cell is PARKT (2nd finding card of the owner table, own correction to be documented, not faked). The podman owner-missing path is identical in mechanism to the docker finding above (the owner gate precedes the fixed apply head) and is owned by the separate planned card `t-20261106-r27-remote-up-podman-owner-missing`. Witnessed base-difference: this card's diff does not touch owner/deployment semantics. No podman probe started; documented as parked here per mission instruction.

## Duty 4 — hosted checks TERMINAL, own run, new head

- CI run on new head: `42320398007` (CI · PR #1407), head_sha `c87c8b644cc98fe6abf1164d101f42a212558b9d`. Started `2026-11-07T00:47:49Z`, watched to terminal via `gh api .../actions/runs/42320398007` and `.../jobs`.
- Terminal conclusion: **success**. Individual jobs: `PR · Source format`=success, `Workflow policy`=success, `PR · Trusted Plan`=success, `PR · Focused Python`=success, `PR · Validation · cli-guided-tests`=success, `PR · Validation · go-unit-tests`=success, `PR · Validation · cli-vet`=success, `PR · Validation · source-contracts`=success, `PR · Validation · cli-package-tests`=success, `PR · Validation · go-build`=success, `PR · Validation · cli-build`=success, `PR · Validation · cli-gofmt`=success, `PR · Validation · go-vet`=success, `PR Selected Checks`=success. Scope-selected jobs skipped (Release Source Preflight, Targeted HA podman/docker, Runner Interface, Consumer Pins, Public Contracts, Exact Candidate, Selected Runtime, Demo Pin) — expected for this PR's scope, not a failure.
- Local pre-checks (own, isolated copy `/tmp/opencode/w285-bh`): `go build ./...` exit 0; my cell `TestRemoteFreshApplyPureClientNeverBootstrapsLocalCore` PASS; the failing `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` is PRE-EXISTING (needs `unix:///var/run/docker.sock`, unavailable in this sandbox) and reproduces identically on develop `dddf0d78` — unrelated to this diff.

## repo-rule compliance

- No edits under `.github/**`; the force-push was a branch supersede (sole owner), not a CI rerun or workflow_dispatch. Failing checks reported as STATE only (none failed).
- GitHub-hosted runners only; no runner infrastructure built/registered/repaired.
- Single candidate branch `work/r27-remote-up-cli`, single PR #1407; no second branch/PR.
- VM cell only on the named SSH host `baha-docker` via the host's own baha binary; never on the coordinator/codeman host.
- Evidence only in baseharbor-plan; this file contains NO markdown checkboxes.
- Compose/container residue of own work = 0 (foreign shared stacks untouched); `docker ps -a --filter name=bh-w285` empty before and after.
- vm-lock `baha-docker` released residue=0 after teardown (journal line `2026-11-07T00:58:07Z release baha-docker w285`); stale w269 lock on `baha-docker-2` released.

## END

END w285-pr1407-docker-cell: head=c87c8b644c (lsremote alt 55f12a8af6c -> neu c87c8b644cc; develop dddf0d7823f is parent+ancestor of first commit fa7a6165; single chain #1407, no second branch); docker_zelle=BEFUND (host baha-docker 166, tooling path proven live init->apply->up->status->doctor on new head c87c8b64; blocker = ErrDeploymentOwnerMissing at recordDeploymentBeforeMutation, no owned/enrolled Core on host, operator-bootstrap out of scope; residue=0 ps-witness); checks=42320398007 TERMINAL success incl PR Selected Checks + go-unit-tests success; podman cell PARKTED (befund, not run, per mission); lock released residue=0; akte=evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-3-docker.md
