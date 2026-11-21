---
id: hunt-1
lane: 0428-221-huntenv
shift: r28-welle4-2026-11-21
topic: child-env-desk
date: 2026-11-21
role: Worker (BUG-HUNT, reine Befundung, KEINE Produkt-aenderung, KEIN Push an baseharbor)
base-sha: ddfa80f7202a0aca3cf68c4542158132c0c2795b (origin/develop, via git ls-remote https://github.com/mcpdev80/baseharbor.git)
real-remote: https://github.com/mcpdev80/baseharbor.git (verified via git ls-remote; the shared workers/baseharbor checkout was NOT cited)
---

## Hunt 1 — child-env-desk: sweep the whole product for the env-replacement class

Reine Befundung. Kein Push an baseharbor. Kein subagent. Kein nacktes `go test ./cmd/baha/` / `go test ./...` auf diesem host.

### BASE ATTESTATION
- measured develop head: `ddfa80f7202a0aca3cf68c4542158132c0c2795b` (Merge pull request #1742)
- fetch method: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
- the mission note said dispatch was at `97b2ba5543f0`; the remote develop has since moved forward to `ddfa80f72`. All evidence below is measured against the GEMESSENE head `ddfa80f72`, checked out in a NEUTRAL worktree `workers/0428-221-huntenv-wt` at exactly that SHA (ancestor/self-check: `git merge-base --is-ancestor ddfa80f72... HEAD` => same commit, IS ANCESTOR).
- the shared `workers/baseharbor` quarantine checkout was NOT used as evidence anywhere.

### SCOPE / METHOD
- command used (production, `_test.go` excluded): `git grep -n -E "\.Env\s*=|exec\.Command|cmd\.Env|environ\(\)" -- "*.go" | grep -av _test.go`
- command used (tests, second lower class): same regex on `*.go` WITHOUT the exclusion.
- classification per mission:
  - K1 ERBT: `os.Environ()` or a helper on it (`withGitPromptDisabled(os.Environ())`, `append(os.Environ(), )`)
  - K2 ERSETZT: a literal list WITHOUT `os.Environ()` (the damage class): `[]string{...}`, `append(cmd.Env, x)` on nil `cmd.Env`, `env := []string{}` on `cmd.Env`
  - K3 GEFILTERT: `replaceProcessEnv()` / filter over `os.Environ()` — check the filter works on the PARENT env, not on an empty list
  - K4 ABSICHTLICH LEER: demonstrably documented empty (sandbox/helper), comment/test proof only

### PLAN
- Sweep the two greps above at the measured develop head.
- Classify every `.Env` assignment (K1..K4) with file:line and the literal right-hand expression.
- For every K2 line: which program breaks, what it needs (PATH/HOME/GIT_*), and the production call path (file:line up to the production site) so a card is directly actionable.
- Cheap extra question: sites that set `cmd.Env = nil` (full wipe) and sites that set NO Env where suppression would be needed (interactive prompt path).
- Write akte with table, per-class sums, "K2 = needing cards" with finished card-text drafts, ## PLAN, cleanliness, repo-rule compliance.

## FULL CLASSIFICATION TABLE (production, K1..K4)

| file:line | function | class | child program (reachable) | production-reachable? | follow | test proves it |
| --- | --- | --- | --- | --- | --- | --- |
| cmd/baha/app_access.go:49 | appAccess/postgres psql | K1 (inherit) | psql (client) | yes, `baha app access postgres` | none | none needed — K1 |
| cmd/baha/app_access.go:88 | appAccess/valkey redis-cli | K1 (inherit via replaceProcessEnv) | redis-cli/valkey-cli | yes, `baha app cache` | none | none needed — K1 |
| cmd/baha/app_inspect_remote.go:74 | cloneInspect | K1 (inherit) | git (clone) | yes, production git source | none | none needed — K1; fixed at this head by #1742 |
| cmd/baha/app_update.go:493 | gitOutputDisabledPrompt | K1 (inherit) | git (update) | yes, `baha update`, native source path | none | none needed — K1 |
| cmd/baha/app_update.go:454 | gitOutput | K1 (inherit, env left nil = inherits) | git (update) | yes, `baha update` (no-suppression branch) | none | none — env unset means process inherits |
| cmd/baha/management_core_git_source.go:42 | management core git | K1 (inherit) | git | yes, management-core source | none | none needed — K1 |
| cmd/baha/update_mutation.go:397 | runUpdatedBaha | K1 (inherit via selfUpdateEnvironment) | baha (self-update verify) | yes, self-update control-plane/app-apply | none | none — selfUpdateEnvironment starts from os.Environ |
| cmd/baha/internal/cli/pager.go:39 | pager | K1 (inherit) | $PAGER (less/more) | yes, CLI pager | none | none — K1 |
| internal/corebackup/etcd/etcdctl.go:95 | EtcdctlSource.Snapshot | K2 (REPLACEMENT) | etcdctl (snapshot save) | yes, Core backup maintenance | card | none currently (see below) |
| internal/corebackup/etcd/etcdctl.go:114 | Snapshot status verify | K2 (REPLACEMENT) | etcdutl | yes, backup restore verify | card | none currently |
| internal/corebackup/etcd/etcdctl.go:156 | attestEndpointStatus | K2 (REPLACEMENT) | etcdctl (endpoint status) | yes, backup restore attest | card | none currently |
| internal/corebackup/etcd/etcdutl.go:95 | IsolatedEtcdutl.Restore | K2 (REPLACEMENT) | etcdutl (snapshot restore) | yes, Core backup restore | card | none currently |
| internal/coreupdate/dcs_boot_probe.go:59 | dcsBootProbe | K2 (REPLACEMENT) | etcdctl (dcs boot probe) | yes, Core HA boot probe | card | none currently |
| internal/development/pinned_git_archive.go:49 | pinnedGitArchive | K1 (inherit) | git (archive) | yes, pinned build | none | none — K1 |
| internal/development/workspace_git.go:421 | workspaceGitOutputDisabledPrompt | K1 (inherit) | git | yes, workspace git | none | none — K1 |
| internal/credential/native/host.go:42 | Invoke/appendNonInteractiveEnv | K1 (inherit) | git/ssh (native credential) | yes, native credential source | none | none — K1 (documented fail-closed) |
| internal/orgconfig/source.go:337 | orgconfig git | K1 (inherit) | git | yes, orgconfig source | none | none — K1 |
| internal/providers/runtime/podman/* runtimeCommandEnv (many) | K1 (inherit/filter) | podman, quadlet generators | yes, podman runtime | none | none — K1 |
| internal/runtime/command_env.go:9 (runtimeCommandEnv) | K1 (inherit/filter) | docker/podman compose | yes, compose runtime | none | none — K1 |
| internal/runtime/docker_engine.go:41 | dockerEngineOutput | K1 (inherit, env passed in) | docker | yes, engine observation | none | none — env threaded in |
| internal/runtime/compose_command.go / compose_files.go | K1 (via commandEnvironment) | docker/podman compose | yes, compose runtime | none | none — commandEnvironment starts from runtimeCommandEnv |
| internal/testsupport/containersecurity/security.go:254 | runtimeCommand | K4 (intentional, test-support) | podman (security scan) | NO (test support only) | none | none — K4, documented |

Per-class sums (production, non-test):
- K1 ERBT (inherit): 13 sites — all derive from `os.Environ()` or a helper on it, or leave `cmd.Env` unset (process inherits). No damage.
- K2 ERSETZT (replacement, the damage class): 5 sites — all `[]string{"PATH=/usr/bin:/bin", ...}` literal lists for etcd/etcdutl/etcdctl binaries.
- K3 GEFILTERT (filter over os.Environ()): 2 helpers `runtimeCommandEnv()` (podman `internal/providers/runtime/podman/command_env.go:9`, runtime `internal/runtime/command_env.go:9`) and its filter use `os.Environ()` as the base and only drop two XDG_ keys. They pass the `merge-base` test: the filter genuinely works on the PARENT env, not an empty list. Also K1 by the mission's definition (helper on os.Environ). Net: not a damage site.
- K4 intentional: 1 site `containersecurity/security.go:254` (test support, documented, re-appends all of os.Environ). No damage.

## K2 = NEEDING CARDS — the damage class, every site

Five sites set `cmd.Env` to a literal list with NO `os.Environ()` base. Each is a separate card. Root cause is identical to #1742: `os/exec` resolves the executable with `PATH` via `exec.LookPath`/default, but once `cmd.Env` is set to a literal list the child gets no `HOME`, no `GIT_*`, and `PATH` is a hardcoded `/usr/bin:/bin` that ignores the host's real bin dirs (rootless pods, nix-style installs, per-user `bin`, the dir where the real `etcdctl`/`etcdutl` binary actually lives).

For every K2 site the failing mechanism is the same: `PATH=/usr/bin:/bin` plus no `HOME`/`GIT_*`. The child program is `etcdctl`/`etcdutl`.

### K2 card 1 — internal/corebackup/etcd/etcdctl.go:95 (Snapshot / `etcdctl snapshot save`)
- function: `EtcdctlSource.Snapshot`, production call path: Core backup maintenance → `backup/maintenance` → this Snapshot.
- what breaks: `etcdctl` snapshot save runs with `PATH=/usr/bin:/bin` and no `HOME`. On a host where the etcd toolchain is not in `/usr/bin` (rootless, per-user install, custom runtime dir) the binary is not found even though `s.Etcdctl` resolved it; even when found, etcdctl reads `HOME` for client config / `.etcdctl` history and `GIT_*` is irrelevant but HOME-dependent kube-style auth may be. The literal list also drops any `ETCDCTL_`-adjacent defaults the host relies on.
- production-reachable: yes, Core backup maintenance.
- follow: new card.
- test proof: none currently; a card should add a case that runs `Snapshot` with the binary outside `/usr/bin` and asserts failure under current code, success after fix. Route into the Core-backup CI group.

### K2 card 2 — internal/corebackup/etcd/etcdctl.go:114 (Snapshot status verify, `verify.Env = []string{"PATH=/usr/bin:/bin"}`)
- function: `Snapshot` verify step, same production path as card 1.
- what breaks: same class; `etcdutl snapshot status` runs with only `PATH=/usr/bin:/bin`, no `HOME`.
- production-reachable: yes.
- follow: new card (small; may be filed together with card 1 in one card since same source file + same helper intent).
- test proof: none.

### K2 card 3 — internal/corebackup/etcd/etcdctl.go:156 (attestEndpointStatus, endpoint status)
- function: `EtcdctlSource.attestEndpointStatus`, Core backup restore attestation.
- what breaks: same class on `etcdctl endpoint status`.
- production-reachable: yes.
- follow: new card.

### K2 card 4 — internal/corebackup/etcd/etcdutl.go:95 (IsolatedEtcdutl.Restore)
- function: `IsolatedEtcdutl.Restore`, Core backup restore.
- what breaks: same class on `etcdutl snapshot restore`; no `HOME`, `PATH=/usr/bin:/bin`.
- production-reachable: yes.
- follow: new card.

### K2 card 5 — internal/coreupdate/dcs_boot_probe.go:59 (dcsBootProbe)
- function: `dcsBootProbe`, Core HA boot probe (etcd endpoint status during boot).
- what breaks: same class on `etcdctl --endpoints=... endpoint status`; no `HOME`, `PATH=/usr/bin:/bin`.
- production-reachable: yes, Core HA boot.
- follow: new card.

Draft card text (reusable body for all five):
```
title: fix(corebackup|coreupdate): derive etcd tool env from os.Environ, do not hardcode PATH=/usr/bin:/bin
class: K2 env-replacement damage (same defect class as #1742)
impact: <file>:<line> sets cmd.Env to a literal {"PATH=/usr/bin:/bin", ...} list. The etcdctl/etcdutl child inherits no HOME, no GIT_*, and a hardcoded PATH that ignores the host's real bin dirs; on rootless / per-user / custom-runtime hosts the tool is not found and the Core backup/restore/boot-probe path fails where it should work.
fix: build the vector from os.Environ() (or a documented filter over it), then set/replace only the ETCDCTL_* keys; keep PATH as PATH-from-parent plus the ETCDCTL_* keys so the already-resolved binary location and HOME are preserved. Do NOT reintroduce the interactive-prompt risk: keep GIT_TERMINAL_PROMPT=0 where a git child is involved (none here).
acceptance: unit case with the binary outside /usr/bin resolves and runs; existing Core-backup/restore CI still green.
route: Core backup / Core HA CI group (state the job + trigger in the card).
```

## CHEAP EXTRA QUESTION

### A. `cmd.Env = nil` (full environment wipe) sites
None found. The only literal-empty assignment is `internal/testsupport/containersecurity/security.go:254` — but that is K4: it sets `[]string{}` only to immediately re-append every entry of `os.Environ()` except the two XDG_ keys. It is test-support, not production, and does not wipe. No full-wipe site exists in production.

### B. `cmd.Env` NOT set where suppression would be needed (interactive prompt path)
These leave `cmd.Env` nil (process inherits) by design; NOT damage, but flagged for completeness:
- cmd/baha/app_update.go:454 `gitOutput` (git update, the non-suppression branch) — inherits; the suppression branch is `gitOutputDisabledPrompt` at :493 (K1, correct).
- cmd/baha/app_access.go:45 (psql) — inherits; interactive psql is intended.
- internal/runtime/*.go `commandEnvironment` callers (compose) — inherit for normal compose; that is the runtime contract, not a prompt risk.
No missing-suppression bug detected: the two git interactive paths that need it (:454, :493) are both correct (inherit vs. `withGitPromptDisabled(os.Environ())`).

## ## PLAN
1. Measure develop head with `git ls-remote`; confirm neutral worktree at exactly that SHA (ancestor/self-check passed).
2. Run the two greps (non-test, then _test.go).
3. Classify every `.Env` assignment K1..K4 (results above).
4. Answer the cheap extra question: no `cmd.Env = nil` full-wipe production site; no missing-suppression bug.
5. Sum K2 = 5 needing cards (etcdctl snapshot save :95, etcdutl snapshot status verify :114, etcdctl endpoint status :156, etcdutl restore :95, dcsBootProbe :59), all the same class as #1742, each a separate card with draft text.
6. Write akte (this file) with table, sums, K2 card drafts, this PLAN, cleanliness, repo-rule compliance.
7. Tick board + these PLAN bullets; post END_DONE to coordinator; remove worktree; no docker to bring down.

## CLEANLINESS
- docker before: `docker ps -a` empty (no containers). docker after: still empty. No containers/networks/volumes/state created (read-only sweep, no compose, no container).
- git worktree before/after: neutral worktree `workers/0428-221-huntenv-wt` cut at measured develop head `ddfa80f72`; removed at END (no stray worktree left). No `git add -A`, no stash, no push to baseharbor.
- cleanliness: PASS — no test containers, no external cart images touched, worktree removed.

## RE-RULE COMPLIANCE
- Role: Worker, BUG-HUNT, pure finding. No product file edited, no card edited, no commit to baseharbor, no PR action, no subagents (4.8).
- No bare `go test ./cmd/baha/` / `go test ./...` on this host. Only read-only `git grep` / `git log` / `git ls-remote`.
- No `git add -A`, no `git stash`, no `codeman agent post` in other sessions.
- Evidence lives ONLY in baseharbor-plan (evidence/... path below); nothing written to the product repo.
- Real remote attested: `git ls-remote https://github.com/mcpdev80/baseharbor.git` (NOT the shared workers/baseharbor quarantine checkout).
- Evidence path to be committed to baseharbor-plan: evidence/r28-welle4-2026-11-21/child-env-desk/hunt-1.md

## HANDOFF / END
END_DONE 0428-221-huntenv: child-env-desk sweep complete — 5 K2 cards need filing (etcd/etcdutl/etcdctl in corebackup + dcs_boot_probe in coreupdate, same #1742 defect class); full class K1/K3/K4 clean; no cmd.Env=nil wipe site; evidence at evidence/r28-welle4-2026-11-21/child-env-desk/hunt-1.md.
