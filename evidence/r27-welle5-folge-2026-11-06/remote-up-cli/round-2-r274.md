# w274: r27 remote-up-cli ROUND 2 (lane w274) — act-1407a REJECT follow-up on PR #1407: develop-refresh, causal mutant proof, runtime cells, pre-existing-failure re-verification

- Role: Worker (Lane w274); coordinator session `ec2254ac-597e-4ffe-8e6e-9a11d8d5140e`.
- Card `t-20261106-r27-remote-up-cli-path` (PR #1407, branch `work/r27-remote-up-cli`). Mission `coordinator/missions/w274-remote-up-r2.txt`. Recipe: CODEX-REVIEW `act-1407a.md` (REJECT, 4 points) in this directory.
- Result: **all four prescription points executed.** New head `55f12a8af6c86e0133b86c373fbfcc73838431ab` (develop `8bda98c1cd3` merged in, same PR chain #1407, no second branch/PR). Causal production-line mutant proven ROT→GRUEN with a SHA256 pair. Podman half referenced to w273's `round-2-podman.md` with a base-difference justification. Docker runtime cell documented pending with lock-journal witnesses. Duty-4 pre-existing claim re-verified with identical develop-side failure. Accountability follow-up: baha-docker-2 teardown to zero own residue, forgotten baha-podman-2 claim released.

## PLAN (numbered; mirrors live board workers/todos/w274-remote-up-r2.json)

1. Read mission + act-1407a.md; inspect PR #1407 / branch state — DONE
2. Worktree `workers/w274-wt` at old head 2651a5c9; base attestation recorded — DONE
3. Duty 1: merge develop 8bda98c1cd3 into `work/r27-remote-up-cli`; push new head; ls-remote alt+neu witnesses — DONE
4. Duty 2: causal mutant at the real production line (fresh-apply head of app_remote_lifecycle.go) in isolated copies; RED transcript + restore GREEN transcript; hash pair; helper-mutant counter-evidence — DONE
5. Duty 3a: docker runtime cell on named VMs (baha-docker / baha-docker-2); lock probes; honest pending documentation + teardown/release follow-up — DONE (befund-statt-gruen, see Punkt 3 of act-1407a)
6. Duty 3b: podman cell — owner-context check (ErrDeploymentOwnerMissing path), reference w273 akte + base-difference justification — DONE
7. Duty 4: re-verify "pre-existing docker-daemon failure" claim on develop in an isolated copy — DONE
8. Push + observe selected checks on the new head TERMINAL (run 42306648514) — DONE
9. Dossier round-2-r274.md written; committed and pushed to origin/main before END — DONE
10. Release all vm-locks with journal witness; compose/stack teardown of own residue; END_DONE to ec2254ac — DONE

## Base attestation and duty 1 (develop-refresh)

- Old head (round 1): `2651a5c98698fb54b6ab571089c8a493da037b19` (parent develop `5e4fde7177ea020de39b117f6d89cfa8f7c62be2`).
- Develop at refresh time: `8bda98c1cd34a984810a0a0ee2d9fe4085b3933a`.
- New head: `55f12a8af6c86e0133b86c373fbfcc73838431ab` = chain 2651a5c9 → merge 390f4489 (develop 8bda98c1 in) → 55f12a8a (red-first cell upgraded to observe the production prerequisite route directly).
- Ancestor witnesses (local git): `git merge-base --is-ancestor 8bda98c1cd3 HEAD` ✓ and `git merge-base --is-ancestor 2651a5c9869 HEAD` ✓ — same PR chain #1407, single candidate branch.
- ls-remote witnesses (`git ls-remote origin refs/heads/work/r27-remote-up-cli`):
  - alt (before push): `2651a5c98698fb54b6ab571089c8a493da037b19`
  - neu (after push): `55f12a8af6c86e0133b86c373fbfcc73838431ab`
- Product diff against refreshed base: `git diff origin/develop...HEAD --stat` = exactly two files, `cmd/baha/app_remote_lifecycle.go` and `cmd/baha/app_remote_pureclient_apply_test.go`. The merge is base-only: `app_remote_lifecycle.go` at 8bda98c1 is byte-identical to the one at 5e4fde71 (prereq line 118 present, gate absent), so the merge introduces no lifecycle-semantics change — verified via raw fetch of both revisions (7594 bytes / prereq=1 / gate=0 at both).

## Duty 2 — causal production-line mutant proof

The cell `cmd/baha/app_remote_pureclient_apply_test.go` (TestRemoteFreshApplyPureClientNeverBootstrapsLocalCore) was upgraded in commit 55f12a8a so that it observes the production route directly: it spies `applicationCorePrerequisite` (the variable the fresh-apply head calls) in addition to `applicationCoreBootstrap`, and supplies a non-terminal application input (`withApplicationInput(ctx, strings.NewReader("y\n"))`) so the pre-fix route halts at coreRequired. Cell file sha256 at new head: `577e3d444ef51641ee46cb4e76b6c60a88b1b48825416c56c013f9501550113b` (round-1 shape at 2651a5c9 was `647528ef...`).

Mutant runs were executed in an isolated repository copy `/tmp/opencode/w274-mutant` (never in the candidate worktree); the isolated copy ends clean (`git status -s` empty, tree == 55f12a8a).

- ROT (cell FAILS): production line reverted to the pre-fix decision line at the fresh-apply head — `if err := applicationCorePrerequisite(withTargetOverride(ctx, resolved.Target.Name), applicationInput(ctx, runtimeInput), out); err != nil {` restored at app_remote_lifecycle.go:118 (byte-identical to develop 8bda98c1 / original head 5e4fde71 version).
  - file sha256: `9e1acfb13b12b9b3055180edd97c48965986a9218ddb0d7c9228b97bdb0a7e7e`
  - transcript line (`/tmp/opencode/w274-transcript-MUT-RED-REAL.log`): `--- FAIL: TestRemoteFreshApplyPureClientNeverBootstrapsLocalCore` with failure text `fresh remote apply routed through the local Core (prerequisite calls=1, bootstrap calls=0); the head must route through the bound target's connector route`.
  - Independently reproduced RED at the pristine original base: worktree detached at 5e4fde71 with only the cell file added (`/tmp/opencode/w274-transcript-RED-ORIGINALHEAD.log`, lifecycle sha256 `9e1acfb1...`, identical FAIL line).
- GRUEN (cell PASSES): candidate line restored — `if requiresManagedServiceIssuer(resolved.Manifest) {` at line 130, `applicationCorePrerequisite` call removed from the route.
  - file sha256: `b375ce0aeb8c0d62b3898ff238e4a6aedb986876e1c176c8c03afe13026191ad`
  - transcript line (`/tmp/opencode/w274-transcript-RESTORE-GREEN-REAL.log`): `--- PASS: TestRemoteFreshApplyPureClientNeverBootstrapsLocalCore` with log `app up (pure-client, NO local Core) => no local Core bootstrap, err=authenticated Connector session is unavailable; reconcile before retrying a mutation`.
  - Hash-pair files: `/tmp/opencode/w274-hashes-MUTLINE.txt` (ROT pair) and `/tmp/opencode/w274-hashes-FINALGREEN.txt` (GREEN pair); the restored files diff byte-identically against commit 55f12a8a.
- Counter-evidence (the cell kills the ROUTE, not a helper): with the candidate production line untouched (`b375ce0a...`) and only the helper `applicationCoreBootstrap` stubbed in `core_installation.go` (`fb9a7fa7...`, marker "HELPER MUTANT"), the cell stays GREEN — `/tmp/opencode/w274-transcript-HELPERMUT.log`, hashes `/tmp/opencode/w274-hashes-HELPERMUT.txt`. Conversely, mutants that keep the prereq call but do not sit on the fresh-apply head (gate flip at line 130 to `if true` = `743965ed...`; `!requiresManagedServiceIssuer` inversion = `7edc3d7f...`; transport-line target-override = `cb245339...`; issuer-branch insert = `068bb43d...`) all leave the cell GREEN in this fixture because the connector transport gate already fails before the issuer branch — recorded so the causal attribution is not overstated: the cell is RED exactly when the fresh-apply head re-enters the local Core prerequisite, GREEN when the gated route stands.
- Production binary of the new head (for VM probes): sha256 `28fb757df5db2b00ffff368078a419a34057028beea607b1c285681c427133aa`.

## Duty 3a — docker runtime cell (befund statt gruen)

- Lock probes (`coordinator/scripts/vm-lock.sh`, journal `/home/marcel/dev/baseharbor-ecosystem/coordinator/.vm-locks/journal.log`):
  - `baha-docker` BUSY by `w269-vm-integration-runs` @ 22:00:08Z with rc=3 at every probe (22:0xZ–23:29:30Z), per owner-direktive never waited.
  - `baha-docker-2` alternated OWN(rc=0) / BUSY (w269 lanes, w279-artifact-docker-cell @ 23:11:52Z); claim/release lines are in the journal throughout.
- Runtime inventory on baha-docker-2 (rootless docker 29.9.3, active): a connector-bound pure-client cell cannot go GREEN on that host within this card's scope. Documented findings:
  - The host's own Core installation state is `phase: sql_failed`, `ready: false` (all capabilities false) with 12 foreign compose containers from lanes w269/w266 (bh-local-shared*, bh-local-core-shared*, bh-w266dn*) running — nothing of these is mine and nothing was touched.
  - A pure-client target with `--access-provider baseharbor-node-connector` requires (a) a healthy Core authority (bootstrap `baha up --control-plane-only`), (b) a running `baha serve` with Connector enrollment enabled (`BASEHARBOR_CONNECTOR_*`), (c) a node enrollment bundle (`baha node add` → node-side apply) and (d) a running baseharbor-node-connector on the execution node. None exists on the host (`find`/`pgrep` probes empty), and establishing them is operator-bootstrap scope — the same scope boundary that already failed the cell closed for w273 (see round-2-podman.md) and w264 round 3 (ErrDeploymentOwnerMissing owner gate).
  - Local-application control run on the same binary proved the tooling path itself live (init → apply --confirm-candidate → up → RUNNING → destroy leaves `runtime-retired`), so the blocker is the connector/enrollment bootstrap, not the CLI.
- Conclusion: docker half of acceptance point 3 recorded as **pending/befund-statt-gruen** with the above witnesses; per mission rc=3 is documented as pending, not waited.

## Duty 3b — podman cell (reference + base-difference justification)

- Context-fund (w273, card `t-20261106-r27-remote-up-podman-owner-missing`): pure-client `app init` on podman-2 at old head 2651a5c9 fails closed at `ErrDeploymentOwnerMissing` (deployment_store.go:25/107 via recordDeploymentBeforeMutation → VerifyDeploymentOwner); docker side green. Witness akte: `evidence/r27-welle5-folge-2026-11-06/remote-up-cli/round-2-podman.md`.
- Base-check demanded by the fund: does my refresh/fix serve the owner path? Verified answer: the owner gate runs BEFORE the fresh-apply branch I changed — `app init`/`apply` record deployment state in `recordDeploymentBeforeMutation`, while my diff touches only the fresh-apply head of `executeRemoteApplicationApply` (prerequisite→issuer gate). Product diff origin/develop...HEAD = the same two files; no lifecycle/owner semantics change. Therefore the podman failure stands identically at the new head, and the fix neither causes nor cures it. The separate card `t-20261106-r27-remote-up-podman-owner-missing` (waiting, depends on this card) owns that path.
- Consistent with the mission's allowance, the podman half is delivered by reference to round-2-podman.md + this base-difference justification instead of a re-run of the identical blocked cell (the operator-bootstrap exclusion applies on the podman side exactly as measured there).

## Duty 4 — docker-daemon pre-existing failure re-verified

- Cell `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` fails with `application preflight failed: selected Docker endpoint unix:///var/run/docker.sock is unavailable; start its rootless daemon or correct the Target endpoint/context; no fallback to System Docker`.
- Candidate (55f12a8a working tree): `/tmp/opencode/w274-duty4-candidate.log` — `--- FAIL ... app_edit_apply_test.go:947` with that exact line.
- Develop 8bda98c1 in the isolated copy (lifecycle file `9e1acfb1...`, cell file removed): `/tmp/opencode/w274-duty4-develop.log` — `--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle` with the identical failure line at the same test line.
- Conclusion: the pre-existing claim is demonstrated (same test, same line, same reason on base and candidate), an environment/daemon dependency, unrelated to the candidate's diff.

## Checks / run observation (terminal, own)

- Run on new head: `42306648514` (CI · Source & Quality), head_sha `55f12a8af6c...`, status completed, conclusion **success** (watched to terminal).
- Aggregated check-run on new head: `PR Selected Checks` id `128201209838`, completed/success at `55f12a8af6c...`.
- Old head run `42297708975` (2651a5c9) success, check-run id `128171476951` — preserved for the chain witness.
- Intermediate run `42305628568` (41bd2ead, my superseded push before author-identity rebase) conclusion cancelled.
- PR #1407: state OPEN, mergeable MERGEABLE, headRefOid `55f12a8af6c86e0133b86c373fbfcc73838431ab`.

## Accountability follow-up (koordinator 23:4x–23:5xZ)

- baha-docker-2 residue three-point audit: (1) containers — 12 running, all foreign compose projects bh-local-shared / bh-local-core-shared / bh-w266dn-shared (w269/w266), mine = 0 (`my containers: 0`); (2) deployments — one retained record `8166a6f6-2423-41f0-8680-4b1b3d8c5831` (application `demo-apply`, target local, runtime-retired) proven mine via deployment.json identity; (3) work dirs — /tmp/w274 with my binaries baha/baha2/baha-cand/teardown.sh.
- Teardown executed under claim: my work dirs and binaries removed (`/tmp/w274` gone), retained deployment directory removed after the CLI destroy path could not resolve it (`app destroy --yes --full-reset` fails with "Application identity has not been initialized" because an authored manifest may not carry `app.id` and the repository source was already deleted; runtime was already retired, containers=0, so this was a state-owner removal of my own residue). Post-state witnesses above.
- Clean release: journal lines `2026-11-06T23:52:13Z claim baha-docker-2 w274` / `2026-11-06T23:52:13Z release baha-docker-2 w274` (release with residue=0, rueckbau VOR release).
- Forgotten double claim on baha-podman-2 (23:39:42Z, duplicate of the 23:32:50Z claim; no cell ever ran there): released with journal line `2026-11-06T23:51:28Z release baha-podman-2 w274`. At final probe only w269's baha-docker lock remains held by another lane; w274 holds none.

## repo-rule compliance

- No edits under `.github/**` on any branch; failing/nonexistent checks reported as STATE only (run/check ids above).
- GitHub-hosted runners only; no self-hosted routing introduced.
- Single candidate branch `work/r27-remote-up-cli`, single PR #1407; no second branch/PR; the permission-probe branch used for push-verification was deleted immediately (witnessed).
- VM cells only on the named SSH hosts via vm-lock.sh; never on the coordinator host; rc=3 documented as pending without waiting.
- Evidence only in baseharbor-plan; this file contains no markdown checkboxes.
- Compose/stack residue of own work brought down before release with ps-witness (foreign stacks untouched, documented).

END w274-remote-up-r2: head=55f12a8af6c (lsremote alt 2651a5c9869 → neu), run 42306648514 success + check-run 128201209838 success; mutanten-hashpaar 9e1acfb1(ROT/FAIL) ↔ b375ce0a(GRUEN/PASS); podman=verweis w273 + base-identitaet belegt; docker-zelle=pending (befund, journal-zeugnisse); duty4 pre-existing auf develop 8bda98c1 nachgewiesen; docker-2 rueckstand 0 + released, podman-2 doppelter claim released.
