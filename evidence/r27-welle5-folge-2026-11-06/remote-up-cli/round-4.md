# 0427-116-cli-path: r27 remote-up-cli ROUND 4 — develop refresh to 934be499b + both-family VM cells (lane 0427-116-cli-path)

- Role: Worker (Lane 0427-116-cli-path, flash); coordinator `594fd2f5-4e80-43b6-9841-92879146a85e`.
- Card `t-20261106-r27-remote-up-cli-path` (PR #1407, branch `work/r27-remote-up-cli`). Mission `coordinator/missions/0427-116-cli-path.txt`. Recipe: CODEX-REVIEW act-1407b REJECT (both-family runtime proof missing, PR behind develop). Prior lane w285 killed by system reboot.
- Result: candidate refreshed onto current develop `934be499b9d2d894f80889fc23cd811884c8aec4` (merge commit `86f990a6`, PR #1407 head). Hosted run `42332668220` terminal **success** on the new head. Both VM cells executed on the named SSH hosts (docker + podman): the CLI up-path reaches the installation-owner seam and fails closed with `ErrDeploymentOwnerMissing` exactly as the mission's step-3 condition names; per mission this is **END_BLOCKED awaiting 0427-117** (lane 0427-117-podman-owner, PR #1409, card `t-20261106-r27-remote-up-podman-owner-missing`), not a self-fix at the owner seam.

## PLAN (numbered; mirrors live board workers/todos/0427-116-cli-path.json)

1. Read mission, card, prior akte (act-1407a/b, round-2-podman, round-2-r274, round-3-docker); verify planning repo zone — DONE
2. Fetch `work/r27-remote-up-cli` and current `develop`; ls-remote witnesses — DONE
3. Worktree `/tmp/opencode/0427-116-cli-path-wt`; merge develop `934be499b` into branch; no conflicts; no `.github/**` content by this lane — DONE
4. Provenance: develop ancestor of HEAD; diff vs develop = 2 files; own-commits list clean — DONE
5. Push head `86f990a6` to PR #1407; CI run `42332668220` watched to terminal (self-run) — DONE
6. Docker VM cell on `baha-docker-2` (baha-docker locked by 0427-107; one-after-other) — DONE (befund)
7. Podman VM cell on `baha-podman` — DONE (befund)
8. ErrDeploymentOwnerMissing confirmed on both families + hosted develop run 42328760203 fails with it — END_BLOCKED route per mission step 3 — DONE (this akte)
9. Evidence round-4.md published to baseharbor-plan origin/main — DONE (publication block below)
10. Teardown: hosts clean (0 containers/0 networks of own work, binaries/HOME removed), vm-locks released with journal witness — DONE
11. END post to 594fd2f5 — last action

## Planning-zone attestation (required)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` => `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (the real planning repo; `workers/baseharbor-plan` phantom zone NOT used).
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.
- Phantom SHA check (mission prompt): `9ca27c9f`, `aff1532c`, `e53eedd0` resolve as bookkeeping-style evidence commits on `baseharbor` refs/heads/main (paths like `baseharbor-plan/evidence/...` inside the product repo); `git merge-base --is-ancestor` shows none of them is an ancestor of develop or of this candidate — this lane carries none of them and cites none of them as evidence.

## Base attestation and develop refresh (mission step 2)

- Remote witnesses before work (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/work/r27-remote-up-cli refs/heads/develop`):
  - `c87c8b644cc98fe6abf1164d101f42a212558b9d refs/heads/work/r27-remote-up-cli` (w285's last head)
  - `934be499b9d2d894f80889fc23cd811884c8aec4 refs/heads/develop` (current develop, includes CI repair #1417)
- Method: fresh clone in this lane's own persistent zone `/tmp/opencode/0427-116-cli-path-wt/repo` (quarantined `workers/baseharbor` NOT used). Branch `work/r27-remote-up-cli` checked out at `c87c8b64`; `git merge --no-edit develop` produced merge commit `86f990a6997229c12e59537fcd07cb8e1fcfd6a1` with **zero conflicts** (the merge touched no file of the candidate write-set: diff `develop..HEAD` = `cmd/baha/app_remote_lifecycle.go`, `cmd/baha/app_remote_pureclient_apply_test.go` only). No `.github/**` content came from this lane: `git diff --name-only 934be499 HEAD | grep .github` => empty; the `.github` file deltas visible inside the merge commit are develop's own newer inputs carried by the merge (normal merge semantics), not edits by this lane.
- Push witness: `c87c8b64..86f990a6 HEAD -> work/r27-remote-up-cli` (fast-forward, no force). After: `git ls-remote` => `86f990a6997229c12e59537fcd07cb8e1fcfd6a1 refs/heads/work/r27-remote-up-cli`; PR #1407 API `headRefOid` = same; state OPEN, base develop, MERGEABLE.
- Ancestor witnesses: `git merge-base --is-ancestor 934be499b HEAD` = YES; `git merge-base --is-ancestor c87c8b64 HEAD` = YES (supersedes w285's head in-chain, single candidate branch — no second branch created, per exactly-one-candidate rule).
- Own-commits witness `git log --format="%h %s" develop..HEAD`:
  - `86f990a6 Merge branch 'develop' into work/r27-remote-up-cli` (this lane)
  - `c87c8b64 fix(r27 remote-up): pure-client app up routes through connector, no local Core bootstrap [carry original round-1 test shape]` (card's own chain, w285)
  - `fa7a6165 fix(r27 remote-up): pure-client app up routes through connector, no local Core bootstrap` (card's own chain, round-1)
  - No foreign commit appears in the list.
- Local verification on the merged head: `go build ./...` rc=0; `go vet ./cmd/baha/` rc=0; `go test ./cmd/baha/ -run TestRemoteFreshApplyPureClientNeverBootstrapsLocalCore` PASS.

## Mission step 4 — hosted run terminal (EIGNES-RUN)

- Push-triggered run `42332668220` ("CI · PR #1407", run_number 4975) on head `86f990a6`, created 2026-11-07T03:09:25Z, watched to terminal by this lane: **conclusion success**.
- Job outcomes: `PR · Source format`=success, `Workflow policy`=success, `PR · Trusted Plan`=success, `PR · Focused Python`=success, `PR · Validation · go-build`=success, `PR · Validation · go-vet`=success, `PR · Validation · cli-gofmt`=success, `PR · Validation · go-unit-tests`=success, `PR Selected Checks`=success; scope-skipped (path rule, not failures): `validate`, `Targeted HA · docker`, `Targeted HA · podman`, `Release Source Preflight`, `PR · Consumer Pins`, `PR · Runner Interface`, `PR · Demo Pin`, `PR · Public Contracts`, `PR · Selected Runtime`, `PR · Exact Candidate`.
- CI-coverage note (mission prompt, new-test rule): the card's test `TestRemoteFreshApplyPureClientNeverBootstrapsLocalCore` (`cmd/baha/app_remote_pureclient_apply_test.go:22`, package `cmd/baha`) is executed by the existing hosted job `PR · Validation · go-unit-tests` via `scripts/pr-check-runner.py` mapping `go test ./cmd/baha` (routing documented in act-1407a "CI routing"); trigger = pull_request opened/synchronize/reopened against develop (`ci.yml` PR trigger block). No new test was added by this lane and no `.github/**` change is needed by it.

## Mission step 3 — VM cells on both families (befund: the owner seam)

All runs use binary `baha` built byte-reproducibly from candidate head `86f990a6` (`go build -trimpath`, sha256 `f7235d3e5dbfbd26f6bb2ac0132dab4dbfbcb09f4d8e07bd7960875899e136be`), scp'd to the named SSH hosts only; isolated HOMEs under /tmp; never on the coordinator/dev host (`codeman`).

### Docker family — host `baha-docker-2` (docker rootless 29.9.3)

- vm-lock: claim `baha-docker-2` by `0427-116-cli-path` @ `2026-11-07T03:11:10Z`, release FREE @ this lane's teardown (journal). `baha-docker` itself was locked by lane `0427-107-docker-podman` @ `03:10:14Z` — the lock output explicitly directs to another host (EINER-nach-ANDERER rule), so the docker cell ran on `baha-docker-2`.
- Phase 1 (local docker target `cell`, isolated HOME): `baha app init --target cell --yes` => `Error: record deployment before saving deployment inputs: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable` — this is `ErrDeploymentOwnerMissing` at `deployment.VerifyDeploymentOwner` (`internal/deployment/deployment_store.go`) via `recordDeploymentBeforeMutation` (`cmd/baha/deployment_record.go:97`). `app apply`/`app up` then fail closed as unregistered/not-applied; `doctor` reports `NOT APPLIED` (no up-gap line).
- Phase 2 (connector-bound tenant target `node-a`, access-provider baseharbor-node-connector, valid UUID tenant-id, no enrolled connector daemon): `app init`/`app up` **pass the owner seam** (the TenantOwnerResolver grants Coreless tenant targets) and halt downstream at the operator-scope gate `applicationCoreTarget` (`cmd/baha/application_core_authority.go:62-66`) => "Remote application Target belongs to a different operator scope" — an authenticated-operator/connector-daemon precondition (operator bootstrap), not a code gap in this diff. `target create` with a tenant id is refused by policy without an enrolled node (config staged directly for the probe).
- Docker cell verdict: the mission's named condition `ErrDeploymentOwnerMissing` is reproduced live on the docker family at the owner seam for the non-tenant path; the tenant path is bounded by the operator-auth precondition.

### Podman family — host `baha-podman` (podman rootless 5.7.0, crun)

- vm-lock: claim `baha-podman` by `0427-116-cli-path` @ `2026-11-07T03:16:51Z` (after docker-host release, one-after-other), release FREE @ teardown (journal: `FREE host=baha-podman`).
- Phase 1 (local podman target `pcell`, isolated HOME): `baha app init --target pcell --yes` => identical `ErrDeploymentOwnerMissing` text; `app up` => `application runtime has not been applied`.
- Phase 2 (connector-bound tenant target `pnode`): `app up`/`app status` => same "different operator scope" halt as docker phase 2 — family-consistent boundary, no podman-specific new defect visible from the CLI path.
- Note: the sibling w288 finding (podman network routing defect on `baha-podman-2`) was not exercised here; this lane ran on `baha-podman`, created no runtime networks, residue 0.

### Hosted confirmation of the same defect on develop (STATE, no rerun)

- The #1417 CI repair made the lifecycle cells really run: hosted workflow run `42328760203` ("Targeted · Integration · runtime-validation/compose-isolation/... · 934be499b9d2...") at develop `934be499` concluded **failure** on both `Compose isolation · docker` and `Compose isolation · podman` jobs, step "Run mandatory repository lifecycles", with verbatim `deployment has no authoritative installation owner for its Target` in e.g. `TestRepositoryWorkflowRealLifecycle`, `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI`, `TestRepositoryComposeWorkloadOnlyLifecycleInCI`, `TestRepositoryBuildWorkloadRebuildsSourceChangesInCI` (fail lines quoted from that run's log). This is the same owner-seam defect card 0427-117 tracks.
- Per mission: this lane does NOT build at the owner seam; both docker and podman runtime acceptance cells cannot go green at this head until 0427-117 lands. Route: END_BLOCKED awaiting 0427-117.

## Teardown witness

- baha-docker-2: own containers `docker ps -aq --filter name=bh-` delta 0 from own work (host has 43 foreign shared-stack containers, untouched); `rm -rf /tmp/bh-0427-116-d2 /tmp/0427-116-baha` verified absent.
- baha-podman: `podman ps -aq --filter name=demo-116|bh-0427` = 0/0, `podman network ls | grep 0427` = 0; `rm -rf /tmp/bh-0427-116-p1 /tmp/0427-116-baha` verified absent. No compose project of this lane remained up at any point (nothing was started that outlived its command).
- vm-locks: all released; final `vm-lock.sh status` shows only 0427-107's claims.

## repo-rule compliance

- No edits under `.github/**` by this lane (diff vs develop at HEAD contains only the card's two Go files); no reruns, no workflow_dispatch; failing hosted state reported as STATE with run id + log line only (42328760203).
- GitHub-hosted runners only; no runner infrastructure touched.
- Single candidate branch `work/r27-remote-up-cli`, single PR #1407; base refresh by merge (no force-push, no second branch).
- VM cells only on named SSH hosts (`baha-docker-2`, `baha-podman`); never on the coordinator/dev host; phantom zone `workers/baseharbor-plan` and quarantined `workers/baseharbor` not used.
- Evidence only in baseharbor-plan; this file contains no markdown checkboxes.
- No subagents; every step executed in this session.
- No self-merge; PR left OPEN for CODEX-REVIEW.

## Publication block (second-to-last action)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan log --oneline origin/main..HEAD` before push: lists ONLY this lane's evidence commit.
- After push: `git ls-remote origin refs/heads/main` pasted in the END transcript; evidence path present on origin/main via `git ls-tree -r origin/main --name-only | grep remote-up-cli/round-4`.

## END

END_BLOCKED 0427-116-cli-path: owner-missing-wartet-auf-117 — beide Familien-Zellen am Kopf 86f990a6 ausgefuehrt, ErrDeploymentOwnerMissing auf docker UND podman reproduziert (local-target Pfad); Tenant-Pfad haelt an Operator-Auth-Vorbedingung; gehosteter develop-Run 42328760203 faellt mit demselben Seam-Fehler (PR-Run 42332668220 terminal SUCCESS am neuen Kopf, develop 934be499b aufgefrischt, PR #1407 head 86f990a6); Karte bleibt review/blockiert bis 0427-117 (PR #1409) landet; akte=evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-4.md
