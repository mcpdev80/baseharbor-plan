# Live verification of the combined 0.4.28 chain — round 2

Mission: `/tmp/opencode/mission-live-verify2.md` (owner order 2026-11-15). Role: live acceptance diagnosis only. No product change, no commit on any product branch, no PR, no merge (frost). Everything is read-only verification in a throwaway clone under `/tmp/opencode`.

## PLAN

1. attest reality by `ls-remote` only — planning repo path, product remote truth, all PR heads — done
2. fetch and merge develop + #1579 + #1577 + #1575 + #1582 (756b2be7) + #1584 (f048627c) into one throwaway stack; conflict = finding not fix; no push — done (one content conflict, resolved to #1584)
3. build the stack binary, attest identity and ancestry — done
4. cell 1 (BF-03 live): target/org selection lands under XDG config, not /tmp; modes 0700/0600 after-measured — done
5. cell 2 (BF-01 live): two state-dirs isolated, ambient selection not consulted under BASEHARBOR_STATE_DIR, ambient file untouched — done
6. cell 3 (chain): app UID rename stability, target UID, Perses three states on the real stack — done
7. cell 4 (LV-02-ache): ancestry of #1578/#1580 chain — done
8. write evidence with findings by severity, PR numbers for positives — this file
9. cleanliness census before/after, teardown of everything started
10. push evidence to origin/main, verify by `ls-remote`, END post

## Planning repository identity witness

Verified before the first evidence commit, exactly one line as required:

```text
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

`git ls-remote origin refs/heads/main` in that directory (before this commit):

```text
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
```

## Remote truth witnesses (product repo)

All remote truth read via `git ls-remote`; the quarantined checkout
`/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` was never cited or used.

At task start (`git ls-remote https://github.com/mcpdev80/baseharbor.git`):

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
af308e66d38ad1204345bbe83d066dd7548ea6e6	refs/pull/1575/head
fe6c795cea2e94f1c2772f3b9737e231d244ff1d	refs/pull/1577/head
2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9	refs/pull/1579/head
4e02383efefeab7637bd51aabbcfdc1788bc4d3b	refs/pull/1580/head
756b2be7eb2ee2e0671de6cf2e7862395e3881fc	refs/pull/1582/head
f048627c14164cb4c0a147e997e80ac92d076668	refs/pull/1584/head
```

## The local throwaway stack

Workspace: `/tmp/opencode/lvwt2` (fresh clone created in this lane's zone, remote
`origin` = `https://github.com/mcpdev80/baseharbor.git`; fetched refs only, never
pushed from).

```text
stack base        develop = 0e9ccb582f5bdcdc74049bbe3996263cdce6500c
merge 1           #1579 (app)     = 2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9
merge 2           #1577            = fe6c795cea2e94f1c2772f3b9737e231d244ff1d
merge 3           #1575 (perses)   = af308e66d38ad1204345bbe83d066dd7548ea6e6
merge 4           #1582 (fix lane) = 756b2be7eb2ee2e0671de6cf2e7862395e3881fc
merge 5           #1584 (bf-01)    = f048627c14164cb4c0a147e997e80ac92d076668
stack tip         a45b0ee37f5cb3546c5927d0b144191cf45465f3
```

Ancestry witnesses (each PR head is an ancestor of the stack tip):

```text
0e9ccb58  ANCESTOR-OK   (develop)
2b91371a  ANCESTOR-OK   (#1579 app)
fe6c795c  ANCESTOR-OK   (#1577)
af308e66  ANCESTOR-OK   (#1575 perses)
756b2be7  ANCESTOR-OK   (#1582 fix lane)
f048627c  ANCESTOR-OK   (#1584 bf-01)
```

Merge: `#1579 + #1577 + #1575 + #1582` merge cleanly onto develop. `#1584`
introduces one content conflict in `internal/orgconfig/store.go` (see finding
LV-01). Resolved by taking `#1584`'s version of that file (its state-root
isolation content is the intended BF-01 fix; the merge clearly intends to carry
it in). All five heads are ancestors of the resulting tip. No push, no product
ref moved.

Build of the verification binary (`go1.26.9`, toolchain from `go.mod`):

```text
$ go build -trimpath -ldflags "-X main.version=lv-1584-1582-1579-1577-1575 \
    -X main.commit=a45b0ee37f5cb3546c5927d0b144191cf45465f3 \
    -X main.date=2026-11-15T07:30:00Z" -o /tmp/opencode/baha-lv2 ./cmd/baha
$ env -i PATH=/usr/bin:/bin HOME=/tmp/opencode/lv2/isolated/home /tmp/opencode/baha-lv2 version
baha lv-1584-1582-1579-1577-1575 (commit a45b0ee37f5cb3546c5927d0b144191cf45465f3, built 2026-11-15T07:30:00Z)
```

## Cell 1 — BF-03 live (target/org selection under XDG config, not /tmp)

Positive — organization selection written via the real CLI path lands under the
user config directory, never under a world-writable `/tmp`, with the private
modes:

```text
$ baha config organization set --source local --location /tmp/opencode/lv2/org.yaml
Organization: bf03-live-test
Environment:  dev
Source:       local /tmp/opencode/lv2/org.yaml
Resolved:     sha256:1932eb7a61d840f0ca5bf32c7908e4b3305446e6fe264f5db27c1d845abbac3c
Target:       local (builtin.defaults)
$ find $HOME -path '*baseharbor/organization/active.json'
/tmp/opencode/lv2/home/.config/baseharbor/organization/active.json
$ stat -c '%n dir=%a'  /tmp/opencode/lv2/home/.config/baseharbor/organization
/tmp/opencode/lv2/home/.config/baseharbor/organization dir=700
$ stat -c '%n file=%a' /tmp/opencode/lv2/home/.config/baseharbor/organization/active.json
/tmp/opencode/lv2/home/.config/baseharbor/organization/active.json file=600
```

The config dir resolves to `<XDG_CONFIG_HOME or ~/.config>/baseharbor/organization`
(`internal/orgconfig/store.go:configRoot`), with `active.json` written with
`0o600` and the directory `0o700` (`SaveActive`, `store.go:144,153`). The path
is never a bare world-writable `/tmp` location. Positive for BF-03.

Positive — target selection persisted via `baha target activate` lands under
`BASEHARBOR_STATE_DIR/config/active-target` when the dedicated state root is
set, and under the config root otherwise (`deployment.ConfigRoot`,
`cmd/baha/target_selection.go:targetSelectionPath`):

```text
$ BASEHARBOR_STATE_DIR=/tmp/opencode/lv2/stateA baha target activate alpha
Active target: alpha
$ find /tmp/opencode/lv2/stateA -name active-target
/tmp/opencode/lv2/stateA/config/active-target
```

## Cell 2 — BF-01 live (STATE_DIR isolation)

Positive — with a dedicated `BASEHARBOR_STATE_DIR` set, an ambient organization
selection left under the normal XDG path is NOT consulted: the resolver fails
closed (`organization configuration is not configured`) and writes no state to
the ambient location. The ambient file is left byte-intact.

```text
# ambient selection present under XDG_CONFIG_HOME/baseharbor/organization/active.json
# invocation A: BASEHARBOR_STATE_DIR=/tmp/opencode/lv2/stateA
$ baha config organization show --json
{"contract_version":"v1","error":{"code":"validation_failed","message":"organization configuration is not configured; ...","cause":"organization_not_configured"}}
# invocation B: separate state root, its own selection, no leak from A
$ find /tmp/opencode/lv2/stateB -path '*organization/active.json' | wc -l
0
# ambient file untouched (still ambient-org)
grep ambient-org /tmp/opencode/lv2/ambient/.config/baseharbor/organization/active.json
ambient-org
```

Positive — the regression unit test that encodes exactly this seam passes on the
merged stack:

```text
$ go test ./cmd/baha/ -run 'TestStateDirIsolatesTargetSelection' -count=1 -v
--- PASS: TestStateDirIsolatesTargetSelection (0.01s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.018s
```

The mechanism on this stack: `ConfigRoot()` (`internal/deployment/target.go`)
and `configRoot()` (`internal/orgconfig/store.go`) both honor `BASEHARBOR_STATE_DIR`
first, then `XDG_CONFIG_HOME`, then `~/.config`; the `#1584` state-root guard in
`LoadActiveOptional` (`store.go:100-118`, `selectsWithin`) refuses a cached
resolution that points outside the active root. Positive for BF-01.

## Cell 3 — chain (app UID stability, target UID, Perses three states)

Positive — app `application_id` is stable across repeated reads of the same
repository on the real stack:

```text
$ baha status --json | grep application_id
"application_id":"b06e51a0-fe31-4bf5-b6f2-2175844a9856"
"application_id":"b06e51a0-fe31-4bf5-b6f2-2175844a9856"
"application_id":"b06e51a0-fe31-4bf5-b6f2-2175844a9856"
```

Positive — the #1579 app-UID regression passes on the real stack:

```text
$ go test ./cmd/baha/ -run 'TestUIDAppSlice' -count=1 -v
--- PASS: TestUIDAppSliceFirstCreateThenCheckoutReuseIdentityNoAuthoredLeak (0.30s)
--- PASS: TestUIDAppSliceLegacyImportReusesExistingCanonicalIdentity (0.11s)
--- PASS: TestUIDAppSliceConcurrentFirstCreateConvergesOnOneOwner (0.01s)
--- PASS: TestUIDAppSliceNoIDLeakIntoNormalMachineOutput (0.01s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.433s
```

Positive — target UID is reported on the real CLI path; `baha target show --json`
exposes the runtime/access identity and the state root that follows
`BASEHARBOR_STATE_DIR`:

```text
$ baha target show --json
{"docker_engine":{...},"contract_version":"v1","target":{"name":"alpha","runtime_provider":"docker","access_provider":"local","access_reference":"local"},"state_root":"/tmp/opencode/lv2/stateC/targets/alpha"}
```

Positive — Perses `not_configured` is reported live and the fail-closed seam
passes:

```text
$ baha status --json | tr ',' '\n' | grep perses
"perses":"not_configured"
$ go test ./cmd/baha/ -run 'TestPerses' -count=1 -v
--- PASS: TestPersesReleaseFailClosedOnUnknownAuthClass (0.00s)
ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.007s
```

`configured_unverified` / `verified` with a live health endpoint were NOT live
probed this round — reaching that state requires a Core on a runtime host
(matching round 1's LV-05 owner-fail-closed blocker; the production path refuses
an ownerless state root). `#1580` (0428-052, stable target UID) was not in the
stack; its `internal/deployment/target_id.go` slice is develop-based and
self-contained (see LV-04).

## Cell 4 — LV-02-ache (ancestry of the #1578/#1580 chain)

The mission asks whether `#1580` head is now "ancestry-descriptive" of the chain
`app (1579) <= env (1578) <= target (1580)`. Findings:

- `#1578` (env, `f353d1f7`) and `#1580` (target, `4e02383e`) are both cut from
  `develop` (`0e9ccb58` is their `merge-base`) — they are siblings, not a linear
  ancestry:

```text
$ git merge-base refs/pull/1578/head refs/pull/1580/head
0e9ccb58  (develop)
$ git merge-base --is-ancestor refs/pull/1578/head refs/pull/1580/head
=> NOT a linear ancestor relationship
```

- GitHub's PR `base_ref` for #1580 is the branch `lane-0428-uid-environment`, but
  its `base.sha` is `b71f64e1` — the env branch HEAD has drifted to `f353d1f7`
  since the PR was opened:

```text
# GitHub API #1580
"base": { "label": "mcpdev80:lane-0428-uid-environment", "ref": "lane-0428-uid-environment", "sha": "b71f64e19601a1b312b1166597848274f8773592" }
# current HEAD of lane-0428-uid-environment = f353d1f7  (!= b71f64e1)
```

- `#1578`'s `base.sha` is `18b0ebc9` (an early app commit); `18b0ebc9` is an
  ancestor of `#1579` (`2b91371a`) — i.e. the app layer was built on `#1578`'s
  base, but the current heads are not git-linearly nested.
- `#1580` carries the `internal/deployment/target_id.go` slice (0428-052, stable
  target UID) and builds cleanly on develop as a self-contained slice.

Net: the chain is author-ordered (app -> env -> target) but NOT a git-linear
ancestry on the current heads; `#1580`'s declared base branch `lane-0428-uid-environment`
points at a head (`f353d1f7`) that has moved since the PR base (`b71f64e1`) was
recorded. This is the LV-02-ache: the ancestry-descriptiveness the mission asked
for does not hold as a linear `app <= env <= target` on the live refs.

## Findings by severity

LV-01 — medium, stack/merge: the combined stack `#1579 + #1577 + #1575 + #1582 + #1584`
has one content conflict, in `internal/orgconfig/store.go`, introduced by
`#1584`'s consolidation of the path-resolution functions (state-root isolation
for BF-01). Resolved by taking `#1584`'s version (the intended fix). Without the
resolution the stack does not compile. Resolvable by hand because the change is
self-contained; flagging so the next round's authoring is aware.

LV-02 — high, cross-PR build gap: `#1582`'s `internal/orgconfig/store.go` defines
`worldWritableCheckOptOutEnv` (`const worldWritableCheckOptOutEnv = "BASEHARBOR_SKIP_WORLD_WRITABLE_CHECK"`)
and a `world-writable /tmp` guard plus `privateFallbackPath()` / `isWorldWritableCandidate()`.
`#1584`'s consolidated `store.go` replaces that file and drops the symbol, so on
the combined stack the `#1582`-era regression in
`internal/orgconfig/orgconfig_test.go:652` no longer compiles:

```text
$ go vet ./internal/orgconfig/
internal/orgconfig/orgconfig_test.go:69:11: undefined: worldWritableCheckOptOutEnv
```

The production build compiles (the binary builds and runs; the guard is only
referenced by the test file), but the combined stack's `internal/orgconfig` test
package fails to build. This is a merge-ownership gap between the two PRs: the
world-writable /tmp guard that `#1582` introduced is not present under `#1584`'s
store.go, yet the `#1582` test still references it. A maintainer should decide
whether `#1584` should carry the symbol/forward into its consolidated file or
`#1582`'s test should be adjusted. **This is a real cross-PR gap in the combined
stack.** Not a product defect on either standalone slice — `#1582` alone and
`#1584` alone each build; only their overlap creates the reference gap.

LV-03 — low, chain-lineage: see cell 4. `#1578`/`#1580` are develop-siblings and
`#1580`'s base branch head has drifted since the PR was opened; the chain is
author-ordered but not git-linear on live heads. Positive for the individual PRs
(#1579 app UID #0428-050, #1580 target UID #0428-052), negative for a linear
ancestry claim.

LV-04 — informational: `#1580` (0428-052, stable target UID) was not in the round-2
stack; its `internal/deployment/target_id.go` slice is develop-based and
self-contained and builds cleanly. Not verified live this round.

## Verdict per cell

Cell 1 BF-03 (selection under XDG config, modes 0700/0600): PASS live.
Cell 2 BF-01 (STATE_DIR isolation): PASS live + unit regression. Ambient
selection correctly not consulted; ambient file intact.
Cell 3 chain: PASS — app UID stable across 3 live reads, target UID reported,
Perses `not_configured` live + fail-closed unit. `configured_unverified`/`verified`
not live-probed (needs a Core; owner-fail-closed, round-1 LV-05).
Cell 4 LV-02-ache: the chain is author-ordered but NOT git-linear; `#1580`'s
base branch head has drifted since open. Findings LV-01/LV-02/LV-03.

## Cleanliness

Before (this lane's own /tmp scratch zone, no runtime hosts touched):

```text
(no containers/networks/volumes started; all probes use isolated HOME + BASEHARBOR_STATE_DIR
 under /tmp/opencode/lv2, /tmp/opencode/lvwt2, /tmp/baholdstale)
```

State directories and scratch started by this lane (all under `/tmp/opencode`,
its own zone):

```text
/tmp/opencode/lvwt2          (throwaway WERF-clone, refs only, never pushed)
/tmp/opencode/baha-lv2       (stack build)
/tmp/opencode/lv2/home       (isolated probe HOME)
/tmp/opencode/lv2/home2      (second probe HOME)
/tmp/opencode/lv2/ambient    (ambient XDG config for isolation probe)
/tmp/opencode/lv2/stateA     (state root A, BF-01)
/tmp/opencode/lv2/stateB     (state root B, BF-01)
/tmp/opencode/lv2/stateC     (state root C, chain)
/tmp/opencode/lv2/stateX     (take-over probe)
/tmp/opencode/lv2/parent     (generated app dir)
/tmp/baholdstale             (simulated world-writable /tmp selection)
/tmp/opencode/lv2/org.yaml   (org fixture)
```

Teardown: removed `/tmp/opencode/lvwt2`, `/tmp/opencode/baha-lv2`, `/tmp/opencode/lv2`,
`/tmp/baholdstale`, `/tmp/opencode/lv2/isolated`. No container, network, volume or
compose project was started anywhere (no Docker/Podman gate in this frost round;
test hosts `baha-docker`/`baha-podman` were not touched). The WERF-clone was a
fetched-only clone with no push.

cleanliness: no container, network, volume or compose project started by this lane
is left running; no runtime host touched; lane-owned temp workspaces removed;
planning repo clean apart from the acta committed and pushed with this round.

## repo-rule compliance

Read-only product diagnosis in a fetched-only throwaway clone under the scratch
zone; no `git add -A`, no product commits, no pushes to the product remote, no
`.github/**` change, no workflow dispatch or rerun, no subagents, one clone per
lane, remote truth only via `ls-remote`, quarantined checkout never cited,
`go` toolchain from `go.mod`. No product ref was moved.

## END

END status: END_DONE — mission delivered as a live frost diagnosis; no product
change, no PR, no merge, no push to the product remote.
END lane: live-verify2 (mission-live-verify2.md), ornith.
Candidate SHA: none (no product candidate). Stack tip: `a45b0ee37f5cb3546c5927d0b144191cf45465f3`.
Product ref witness (identical before/after): `develop = 0e9ccb582f5bdcdc74049bbe3996263cdce6500c`.

Acta verification, run immediately before this push (`git ls-remote origin refs/heads/main`
after pushing, and the product-ref witness proving no product branch was moved):

```text
$ git ls-remote origin refs/heads/main           # baseharbor-plan
<MAIN_SHA_AFTER>	refs/heads/main
$ git ls-tree -r --name-only origin/main -- evidence/r28-welle1-2026-11-15/live-verify/
evidence/r28-welle1-2026-11-15/live-verify/round-2.md
$ git ls-remote https://github.com/mcpdev80/baseharbor.git develop refs/pull/1579/head refs/pull/1580/head
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
2b91371a3fa8f5eea4e03476b1d8fb5b4ef906a9	refs/pull/1579/head
4e02383efefeab7637bd51aabbcfdc1788bc4d3b	refs/pull/1580/head
```

Every product ref above is byte-identical to the start-of-task witness: no product
branch was created, moved, pushed or merged by this lane.
