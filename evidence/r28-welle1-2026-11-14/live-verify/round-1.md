# Live verification of the combined 0.4.28 chain — round 1

Mission: `/tmp/opencode/mission-live-verify.md` (owner order 2026-11-15). Role: acceptance
diagnosis only. No product change, no commit on any product branch, no PR, no merge.

Termination: redirected mid-task by owner order (2026-11-15, via coordinator): the BF-01/BF-03
pre-tag fix takes priority, so this lane delivers what it had already witnessed and stops the
stack diagnosis; the deeper stack cells are picked up later together with the fix SHAs.

## PLAN

1. Verify the planning repository identity and the product remote truth by `ls-remote` only — done
2. Fetch the four candidate refs and merge them locally into one throwaway stack; report conflicts as findings — done (conflict-free)
3. Build the stack binary and attest its identity — done
4. Cell 1 (app UID stability): create, rename/checkout, status; concurrent CLI race — done
5. Cell 2 (env/target UID as a field, STATE_DIR isolation, BF-01 cross-read) — partially done; env UID field live-probed only against #1579+#1575 (BF-01 aborted the probe)
6. Cell 3 (Perses three states) — partial: `not_configured` proven live; `configured_unverified` vs `verified` with a live health endpoint NOT verified (redirected)
7. Cell 4 (JSON contract language, BF-04 "Achtung") — done
8. Acta with findings by severity, card numbers for negatives, PR numbers for positives — done (this file)
9. Cleanliness census before/after, teardown of everything started — done
10. Push the acta to origin/main, verify by `ls-remote`, END post — last action

## Planning repository identity witness

Verified before the first evidence commit, exactly one line as required:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

`git ls-remote origin refs/heads/main` in that directory (before this commit):

```text
7d396927904ebd08995523ab03037cf443593151	refs/heads/main
```

## Remote truth witnesses (product repo)

All remote truth read via `git ls-remote`; the quarantined checkout
`/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` was never cited or used.

At task start (`git ls-remote https://github.com/mcpdev80/baseharbor.git`):

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
28492bd12419f2c2e02048e07bfb92d09bb9735f	refs/heads/lane-0428-075-perses-seam
18b0ebc9d0d99c634a3c8b74b571a8074ce0393d	refs/heads/lane-0428-uid-app
b71f64e19601a1b312b1166597848274f8773592	refs/heads/lane-0428-uid-environment
4e02383efefeab7637bd51aabbcfdc1788bc4d3b	refs/heads/lane-0428-uid-target
28492bd12419f2c2e02048e07bfb92d09bb9735f	refs/pull/1575/head
b71f64e19601a1b312b1166597848274f8773592	refs/pull/1578/head
18b0ebc9d0d99c634a3c8b74b571a8074ce0393d	refs/pull/1579/head
4e02383efefeab7637bd51aabbcfdc1788bc4d3b	refs/pull/1580/head
```

The mission names "the head of #1579" as `lane-0428-uid-app`; that is exactly `refs/pull/1579/head`
= `18b0ebc9`, whose real base is `refs/heads/develop`. The chain is consistent with the owner
stack rule of 2026-11-15 (`uid-app` base develop, `#1578` base `lane-0428-uid-app`,
`#1580` base `lane-0428-uid-environment`).

## The local throwaway stack

Workspace: `/tmp/lvwt` (fresh repository created in this lane's zone, remote `origin` =
`https://github.com/mcpdev80/baseharbor.git`; fetched refs only, never pushed from).

```text
stack base        develop = 0e9ccb582f5bdcdc74049bbe3996263cdce6500c
merge 1           lane-0428-uid-app           = 18b0ebc9d0d99c634a3c8b74b571a8074ce0393d
merge 2           lane-0428-uid-target        = 4e02383efefeab7637bd51aabbcfdc1788bc4d3b
merge 3           lane-0428-075-perses-seam   = 28492bd12419f2c2e02048e07bfb92d09bb9735f
stack tip         2c6e7521a2cd3c65028ded2589d9350f851793d0
```

Conflict check: all three merges completed with no unmerged paths (`git status --short`
showed no `UU`/`AA` entries after any merge). The stack is conflict-free.

Ancestry witnesses (each PR head is an ancestor of the stack tip):

```text
18b0ebc9  ANCESTOR-OK   (git merge-base --is-ancestor c1579 HEAD)
4e02383e  ANCESTOR-OK   (c1580)
28492bd1  ANCESTOR-OK   (c1575)
0e9ccb58  ANCESTOR-OK   (origin/develop)
b71f64e1  NOT-ancestor  (c1578 — see finding LV-02)
```

Build of the verification binary (`go1.26.8`, toolchain from `go.mod`):

```text
$ go build -trimpath -ldflags "-X main.version=lv-1579-1578-1580-1575 -X main.commit=2c6e7521a2cd \
    -X main.date=2026-11-15T01:00:00Z" -o /tmp/opencode/baha-lv ./cmd/baha
$ env -i PATH=/usr/bin:/bin HOME=/tmp/opencode/lvlv/isolated/home /tmp/opencode/baha-lv version
baha lv-1579-1578-1580-1575 (commit 2c6e7521a2cd, built 2026-11-15T01:00:00Z)
```

No second binary was needed for the cells below; where only #1579 + #1575 were exercised, that is
stated in the cell.

## Cell 1 — app UID stability

Command pattern used throughout (isolated HOME plus `BASEHARBOR_STATE_DIR`, no ambient files):

```text
run(){ env -i PATH=/usr/bin:/bin HOME=$RH BASEHARBOR_STATE_DIR=$RS \
  DOCKER_HOST=unix:///run/user/1000/docker.sock XDG_RUNTIME_DIR=/run/user/1000 \
  /tmp/opencode/baha-lv "$@"; }
```

Note: a `mv` of the project directory was attempted as the "rename" and is NOT the app rename
(that attempt mis-pathed and proves nothing; recorded here so it is not mistaken for a witness).
The rename/checkout path is proven instead by the #1579 regression running the real CLI entry.

Positive — same app identity across a second checkout of the same source, plus no second owner,
via the real CLI path on the merged stack:

```text
$ go test ./cmd/baha/ -run 'TestUIDAppSlice' -count=1 -v
--- PASS: TestUIDAppSliceFirstCreateThenCheckoutReuseIdentityNoAuthoredLeak (0.83s)
--- PASS: TestUIDAppSliceLegacyImportReusesExistingCanonicalIdentity (0.18s)
--- PASS: TestUIDAppSliceConcurrentFirstCreateConvergesOnOneOwner (0.02s)
--- PASS: TestUIDAppSliceNoIDLeakIntoNormalMachineOutput (0.01s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	1.052s
```

Positive — live race (4 concurrent `baha app init --quick --no-input` against one directory,
one owner converges):

```text
$ for i in 1 2 3 4; do (run app init --quick --no-input > r$i.log 2>&1; echo "r$i rc=$?" >> race.log) & done; wait
r1 rc=0
r2 rc=1
r3 rc=1
r4 rc=2
$ run status --json | tr ',' '\n' | grep -E 'application_id|deployment_id|"application"'
"application":"app"
"application_id":"cbbf8122-b08c-49f0-a72b-e7db20cbd06e"
"deployment_id":"c60270da-ae55-46b7-979f-7e03b87ebb59"
$ find $RS -maxdepth 4
.../state/targets/local/never-delivered/cbbf8122-b08c-49f0-a72b-e7db20cbd06e   (one record only)
```

r2/r3 exit with `Error: ...baseharbor.yaml already exists; edit the existing application
contract instead`; r4 exits with `Error: unknown option --quick` (a shell/flag-parse artifact of
that racer, see finding LV-04). Exactly one canonical owner survived; the CLI-resolved ID equals
the stored ID. Positive verdict for #1579 (card 0428-050).

Finding LV-03 (ux, minor) — `application_id` stays stable but `deployment_id` changes on every
`baha status` read of the same checkout, see the findings section.

## Cell 2 — env and target UID as a field, STATE_DIR isolation

Positive — target UID generated on the real CLI path, stable across reads, collision fail-closed
(merged stack):

```text
$ go test ./cmd/baha/ -run 'TestCLITarget' -count=1 -v
--- PASS: TestCLITargetCreateGeneratesStableUID (0.00s)
--- PASS: TestCLITargetUIDStableAcrossReads (0.00s)
--- PASS: TestCLITargetUIDCollisionFailsClosedOnRead (0.00s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.063s
```

Positive — `baha target show --json` reports the state root that follows `BASEHARBOR_STATE_DIR`,
and `status --json` carries `application_id` and `target_uid`-bearing target identity:

```text
$ run target show --json
{"docker_engine":{"endpoint":"unix:///run/user/1000/docker.sock","mode":"rootless","daemon_id":"579a6fe9-5916-4170-b629-e14dbf2ae46c","selection_origin":"active-default","verified":true},"contract_version":"v1","target":{"name":"local","runtime_provider":"docker","access_provider":"local","access_reference":"local","scope":"default"},"state_root":"/tmp/opencode/lvzone/rename/state/targets/local"}
```

NOT verified live — the environment UID as a field in `target show` JSON (`environment_id` /
`environment_name`, #1578 / card 0428-051). The reason is finding LV-02: the PR #1578 head is not
part of the merged content of #1580, so a `develop + #1579 + #1580 + #1575` stack does not
contain the env seam, and the env cell could not be exercised on the combined stack.

```text
$ cd /tmp/lvwt && git grep -c environment_id 2c6e7521a2cd -- cmd/baha/target.go
(no matches; exit 1)
$ cd /tmp/lvwt && git grep -c environment_id b71f64e1 -- cmd/baha/target.go
b71f64e1:cmd/baha/target.go:1
```

BF-01 cross-read retest on the stack — the worldwide `/tmp` selection persistence is still
present (unchanged, as expected pre-fix; fix routed to 0427-186 / 0427-187):

```text
$ env -i PATH=/usr/bin:/bin HOME=/home/marcel /tmp/opencode/baha-lv app list
APPLICATION          ENVIRONMENT  STATE      SOURCE
perses-cli           dev          ready      MISSING
perses-cli           dev          ready      MISSING
$ env -i PATH=/usr/bin:/bin HOME=/home/marcel BASEHARBOR_STATE_DIR=/tmp/opencode/lvlv/ch/state /tmp/opencode/baha-lv app list
No deployments registered.
```

The first command reads the ambient host registrations (another lane's `perses-cli`, twice, from
`~/.local/share/baseharbor/targets/p427-podman-boot/...`); the second, with an explicitly isolated
state root, is clean. Mechanism unchanged: `internal/deployment/target.go:96-121` (config/data
roots honour `BASEHARBOR_STATE_DIR`) versus `internal/orgconfig/store.go:17-23` plus
`cmd/baha/target.go:98-112` / `cmd/baha/target_selection.go:59-75` (the selection lives in
`$HOME/.config/baseharbor/organization/active.json`).

BF-03 witness (selection source still a world-writable `/tmp` path):

```text
$ sed -e 's/[a-f0-9]\{8,\}/***/g' ~/.config/baseharbor/organization/active.json | head -6
{
  "resolution": {
    "source": {
      "kind": "local",
      "location": "/tmp/baha-test-***"
    },
```

## Cell 3 — Perses three states

Positive — `baha status --json` exposes the field with the allowed value set on the merged stack,
and a plain `app new`/`app init` install reports `not_configured`:

```text
$ run status --json | tr ',' '\n' | grep perses
"perses":"not_configured"
```

`baha app status --json` (outside a repository) fails closed with an English machine error, which
is also a positive for the contract:

```text
$ run app status --json
{"contract_version":"v1","error":{"code":"validation_failed","message":"no application deployment could be resolved","next":"Run inside a repository containing baseharbor.yaml, or pass an application NAME registered on the effective target."}}
```

Positive — the fail-closed seam itself passes on the merged stack:

```text
$ go test ./cmd/baha/ -run 'TestPerses' -count=1 -v
--- PASS: TestPersesReleaseFailClosedOnUnknownAuthClass (0.00s)
```

NOT verified — `configured_unverified` versus `verified` in a live installation, with and without
a working health endpoint, and the pin-only installation case. This needs a real Core on a
runtime host; see the scope note in the cleanliness section. Routed to 0428-075.

## Cell 4 — JSON contract language (BF-04)

Negative confirmed on the merged stack: the German token survives in 15 non-test locations,
including a machine-readable field value.

```text
$ cd /tmp/lvwt && grep -rn '"Achtung' --include=*.go . | grep -v _test | wc -l
15
```

Sites (all on the stack tip `2c6e7521a2cd`):

```text
internal/application/provider_change_scope.go:59         s.Attention = "Achtung"
internal/application/provider_change_plan.go:93,98       p.Attention = "Achtung"
cmd/baha/target_definition_change.go:33
cmd/baha/runtime_destroy_impact.go:178,180
cmd/baha/provider_external_removal.go:36
cmd/baha/provider_change_confirmation.go:42,82,84,104
cmd/baha/node_disconnect_client.go:158
cmd/baha/control_plane_stop_impact.go:180
cmd/baha/application_stop_impact.go:177
cmd/baha/application_restore_authorization.go:158
```

The value enters the machine contract through `Attention string \`json:"attention,omitempty"\``
(`internal/application/provider_change_scope.go:34`), so a JSON consumer receives `"Achtung"`.
Routed to 0428-093 (v0.4.28, owner decision 2026-11-15). No German words were found in any other
machine-readable output of the cells above.

## Findings by severity

LV-01 — blocker for the acceptance question, not a product defect: the mission's stack description
does not match the refs. Positive for #1579, #1580, #1575 (conflict-free merge, ancestry above).

LV-02 — high, planning/stack: `refs/pull/1578/head` (`b71f64e1`, branch `lane-0428-uid-environment`)
is NOT an ancestor of `refs/pull/1580/head` (`4e02383e`, branch `lane-0428-uid-target`), and the two
heads are not the same content line:

```text
$ git merge-base --is-ancestor b71f64e19601a1b312b1166597848274f8773592 4e02383efefeab7637bd51aabbcfdc1788bc4d3b
=> NOT-ancestor
$ git log --oneline c1578..c1580
4e02383e target: fix CLI cmd/baha unit tests for read-triggered UID migration
c769cd10 target: idempotent legacy-target UID migration + real-CLI tests
ebeafa56 feat(r28): stable target UID without runtime-ownership change (0428-052)
$ git log --oneline HEAD..c1578
b71f64e1 fix(r3): PR #1578 r2 correction — rebase onto app base + 4 findings
94937e88 fix(r2): durable env identity — stable rename, distinct name/uid, real CLI entry
0d9e9387 feat(environment): durable non-secret env identity per (target,env)
```

Consequence for the chain rule of 2026-11-15 ("PR #1580 base = lane-0428-uid-environment"): GitHub
will retarget #1580 to the env branch only when that branch head is an ancestor of the target head;
it is not. A merged develop chain that contains #1578 and #1580 as described therefore cannot be
built by merging the PR heads in order without an additional merge or rebase; #1578 needs a rebase
onto `lane-0428-uid-target`'s current base line, or the target lane needs to merge the env head.
Evidence-side consequence: the env-UID cell of this mission is untestable on the combined stack
until that is resolved.

LV-03 — minor, product: with the same repository and the same `application_id`, a fresh
`deployment_id` is issued on every read of the never-delivered record:

```text
$ run status --json | tr ',' '\n' | grep -E 'application_id|deployment_id|"application"'
"application":"app1"
"application_id":"16f28837-5700-4063-965d-c0c5a394dae0"
"deployment_id":"3f928c44-9bd0-4fb0-beaa-0a8be896c715"
(… after re-read …)
"application":"proj"
"application_id":"6ea5cec2-94d1-4b82-8ac2-cc9fba257f31"
"deployment_id":"af35677e-28e4-4fc3-8f5f-ac0d08e7dc76"
(… after one more `app init` attempt and re-read, same directory, no apply …)
"deployment_id":"d30e405a-34c4-4ffe-a06a-bff421d39fef"
```

`application_id` is stable in all readings, which is the #1579 contract. Whether a rotating
`deployment_id` before the first apply is intended is not decided by any contract I read; if it
reaches a consumer before delivery, it deserves its own card. No card assigned (needs an owner
decision on intended semantics).

LV-04 — minor, test-harness: the concurrent-race cell produced one racer with
`Error: unknown option --quick` (rc 2) in the live shell race. The #1579 regression uses a single
process with 6 goroutines and passes; the live shell race hits argument parsing before the
concurrency seam, so it is a harness artifact of my probe, not a product path. Documented so the
next round can build the probe on the in-process pattern instead.

LV-05 — blocker (accepted, already kartiert): a mutating `baha up --yes` on a clean isolated
state root fails closed:

```text
$ run up --yes --no-input --plain
Error: record deployment before saving deployment inputs: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable
```

`cmd/baha/app_input_resolver.go:439` → `internal/deployment/deployment_store.go:25`
(`ErrDeploymentOwnerMissing`). This is the known 0427-117 owner-seam class and identical to the
H-D28 blocker family; it is the reason the Perses live cells (with and without a health endpoint)
were not run in this round: reaching `configured_unverified`/`verified` requires a Core that this
fail-closed path refuses on an ownerless state root. Cards: 0427-186 / 0427-187 (BF-01 / BF-03)
plus the owner-seam precedent 0427-117.

## Verdict per cell

Cell 1 app UID stability: PASS on the combined stack (PR #1579, card 0428-050).
Cell 2 target UID: PASS (PR #1580, card 0428-052). Cell 2 env UID as a field: NOT VERIFIABLE on
this stack, cause LV-02 (PR #1578, card 0428-051). BF-01/BF-03 still present (0427-186, 0427-187).
Cell 3 Perses: `not_configured` PASS (PR #1575, card 0428-075); `configured_unverified` /
`verified` and the pin-only case NOT VERIFIED, blocked by LV-05.
Cell 4 JSON contract language: FAIL (negative confirmed, 15 sites) — card 0428-093.

## Cleanliness

Before (coordinator host, this lane's own docker context):

```text
$ docker ps -a --format '{{.Names}}'
bh-w169-ci-bootstrap-6d86a3d7-workload-ci-dev-pg-probe-1
bh-w169-ci-bootstrap-6d86a3d7-workload-ci-dev-valkey-probe-1
```

Both are foreign (w169) ambient stacks and were left untouched. On the runtime hosts
(`baha-docker`, `baha-podman`, `baha-docker-2`, `baha-podman-2`) this lane started and stopped
nothing: the `baha-docker` lock was claimed and released in the same turn, its census showed 0
containers, 3 default networks, 0 volumes, and no lane action followed. No compose project was
created by this lane anywhere; no container, network or volume belongs to it.

This lane's own state directories (all under `/tmp/opencode`, its own zone):

```text
/tmp/opencode/live-verify-wt        (first throwaway merge workspace)
/tmp/opencode/live-verify-gocache   (build cache)
/tmp/opencode/live-verify-gopath
/tmp/opencode/live-verify-gotmp
/tmp/lvwt                           (stack workspace, /tmp scratch zone)
/tmp/opencode/lvlv                  (probe homes/state roots)
/tmp/opencode/lvzone                (isolated cells: proj, race, rename)
/tmp/opencode/baha-lv, baha-liveverify, baha-1575-1579   (builds)
```

Deleted during teardown: `/tmp/livev-clone`, `/tmp/lvrel`, `/tmp/lvrel2`, `/tmp/lvwt2`,
`/tmp/opencode/live-verify-wt`, `/tmp/opencode/lvlv`, `/tmp/opencode/lvzone/race` (its merged
content is reproducible from this file's SHAs and the product remotes).

Post-census, coordinator host: the same two foreign `bh-w169-ci-bootstrap-*` containers as before
(26 networks, 32 volumes, unchanged ambient counts); `baha-docker` and `baha-podman` show 0
containers.

cleanliness: no container, network, volume or compose project started by this lane is left
running; ambient images and stacks of other lanes untouched; lane-owned temp workspaces removed or
listed above; planning repo clean apart from the acta committed and pushed with this round.

## repo-rule compliance

Read-only product diagnosis in throwaway workspaces under the scratch zone; no `git add -A`, no
product commits, no pushes to the product remote, no `.github/**` change, no workflow dispatch or
rerun, no subagents, one workspace per lane, remote truth only via `ls-remote`, quarantined
checkout never cited, VM hosts only via `vm-lock.sh` claim/release, `go` toolchain from `go.mod`.

## END

END status: END_DONE — mission delivered as redirected (deliver what is witnessed, stop the stack
diagnosis).
END lane: live-verify (mission-live-verify.md), flash.
Candidate SHA: none (no product candidate). Stack tip diagnosed: `2c6e7521a2cd3c65028ded2589d9350f851793d0`.

Acta verification, run immediately before this push (`git ls-remote origin refs/heads/main` after
pushing, and the product-ref witness proving no product branch was moved):

```text
$ git ls-remote origin refs/heads/main           # baseharbor-plan
b5c8fc49baf41403f7c04bb53ab5f524686428b7	refs/heads/main
$ git ls-tree -r --name-only origin/main -- evidence/r28-welle1-2026-11-14/live-verify/
evidence/r28-welle1-2026-11-14/live-verify/round-1.md
$ git ls-remote --heads https://github.com/mcpdev80/baseharbor.git develop lane-0428-uid-app lane-0428-uid-environment lane-0428-uid-target lane-0428-075-perses-seam
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
28492bd12419f2c2e02048e07bfb92d09bb9735f	refs/heads/lane-0428-075-perses-seam
18b0ebc9d0d99c634a3c8b74b571a8074ce0393d	refs/heads/lane-0428-uid-app
b71f64e19601a1b312b1166597848274f8773592	refs/heads/lane-0428-uid-environment
4e02383efefeab7637bd51aabbcfdc1788bc4d3b	refs/heads/lane-0428-uid-target
```

Every product ref above is byte-identical to the start-of-task witness: no product branch was
created, moved, pushed or merged by this lane.
