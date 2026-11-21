# Card 0428-222 / PR #1749 — round-5 security fix: envpin drops inherited unpinned ETCDCTL_* keys

**Lane:** `w21-pr1702-0428-142-compat`
**Worktree:** `/home/marcel/dev/baseharbor-ecosystem/workers/0428-222-childenv-wt` (branch `lane-0428-222-child-env`)
**State:** fix committed, pushed, CI observed. Fix = commit `10c7c6414` on top of exact head `23feeefee58`.

## PLAN
- Bullet 1: Evidence file `evidence/r28-welle4-2026-11-21/child-env-inheritance/round-5-etcdctl-filter.md` with numbered PLAN (own worktree; shared checkout forbidden — tooling-issue #29).
- Bullet 2: ls-remote reality check: PR#1749 head + lane-0428-222-child-env = `23feeefee58`; develop = `42da7128e` (advanced past `513488eeb6d` — my branch base `513488eeb6d` is an ancestor of my head, verified).
- Bullet 3: Set worktree to remote head `23feeefee58` (done, MATCH); no rebase/amend/filter-branch.
- Bullet 4: Read review-4-security akte + envpin/pin.go + callers; confirm P1 blockend: inherited unpinned ETCDCTL_* survives, incl. ETCDCTL_INSECURE_SKIP_TLS_VERIFY weakening TLS.
- Bullet 5: Fix choice: filter all ETCDCTL_* not on pin-list (smaller; justified — no legitimate ETCDCTL_INSECURE/USERNAME/PASSWORD use in baseharbor). Keep normally-exported parent env.
- Bullet 6: Fail-first tests (AGENTS 5.3): TestUnpinnedETCDCTLKeyDropped + TestUnpinnedETCDCTLKeyDroppedDirect RED on current helper, GREEN after fix; run through `PR · Go unit · packages` on pull_request (existing CI route, no .github/** or scripts/** change).
- Bullet 7: Commit (author==committer==0428-222-childenv), push no force, prove delivery via ls-remote.
- Bullet 8: Watch new exact hosted run to terminal (AGENTS 4.6).
- Bullet 9: END with head-sha, run-id + terminal, 'fail-first: red then green'.

## Stop / guard notes (ledger)
- Guard w21sec.g.md confirms my own prior "dcs_boot_probe sets pins before os.Environ()" suspicion is wrong at this head (L63 calls `envpin.PinnedEnv`); the review akte refutes it. Recorded here, not acted on.
- develop advanced `513488eeb6d` -> `42da7128e` at measurement. My lane branch and PR#1749 head are unchanged at `23feeefee58` (expected). `git merge-base --is-ancestor 513488eeb6d HEAD` => YES; my 4 card commits intact. No hop against `42da7128e` — the security finding is independent of the develop head and the fix lands on the exact reviewed head `23feeefee58`.

## Findings (review-4-security HEAD 23feeefee)
Source of truth: `evidence/r28-welle4-2026-11-21/pr1749-review/review-4-security-head23feeefee.md` (CODEX REQUEST CHANGES, plan 9d3393e426bb; supersedes the earlier APPROVE HOP).
- P1 blockend: `internal/testsupport/envpin/pin.go` `PinnedEnv` copied `os.Environ()`, removed only keys named in `pins`, appended pins last — so every inherited key with the `ETCDCTL_` prefix that is NOT pinned survived. etcdctl maps global flags onto `ETCDCTL_*`; `ETCDCTL_INSECURE_SKIP_TLS_VERIFY` selects `--insecure-skip-tls-verify`, so an inherited `true` would disable child TLS verification even though CA/cert/key are pinned. Call sites: `internal/corebackup/etcd/etcdctl.go:102-110,123,167-172`, `internal/corebackup/etcd/etcdutl.go:100`, `internal/coreupdate/dcs_boot_probe.go:63-68`, `internal/stableid/lock_probe.go:128`.
- No legitimate use of `ETCDCTL_INSECURE_*`/`ETCDCTL_USERNAME`/`ETCDCTL_PASSWORD` anywhere in baseharbor (grep across `*.go`): only `ETCDCTL_API/CA/CERT/ENDPOINTS/KEY` appear. => filter is the smaller, correct fix.

## The fix (file:line)
`internal/testsupport/envpin/pin.go` — `PinnedEnv(pins ...string) []string`:
- Added: iterate `os.Environ()`, and for every key with prefix `ETCDCTL_`, drop it unless it is one of the passed pins; also keep dropping inherited copies of the other explicitly pinned keys (PATH and the pinned ETCDCTL_* values) so the pin wins unambiguously; every other inherited key is still appended.
- Rationale documented inline: etcdctl maps global flags onto `ETCDCTL_*`; unpinned ones (insecure-skip-tls, username, password) must never reach the child.
- `import "os"` -> `import ("os"; "strings")` for the prefix check. gofmt clean, go vet clean.

## Fail-first witness (AGENTS 5.3)
New tests in `internal/testsupport/envpin/unpinned_etcdctl_test.go`:
- `TestUnpinnedETCDCTLKeyDropped` — child-process regression: sets parent `ETCDCTL_INSECURE_SKIP_TLS_VERIFY=true`, `ETCDCTL_CACERT=/inherited/ca.pem`, spawns a wrapper that writes its received env, asserts no unpinned `ETCDCTL_*` leaked, pinned CA wins, `NORMAL_EXPORTED_VAR` still inherited, pinned PATH wins.
- `TestUnpinnedETCDCTLKeyDroppedDirect` — asserts directly on the returned slice that no unpinned `ETCDCTL_` key survives while a normal exported var does.
- RED on the pre-fix helper (measured):
  - `TestUnpinnedETCDCTLKeyDroppedDirect: unpinned inherited key ETCDCTL_INSECURE_SKIP_TLS_VERIFY=true must be dropped by PinnedEnv`
  - `TestUnpinnedETCDCTLKeyDropped` captured a child env where `ETCDCTL_INSECURE_SKIP_TLS_VERIFY=true` leaked (wrapper dump shown in the transcript).
- GREEN after the fix (measured locally): `internal/testsupport/envpin` PASS; `internal/corebackup/etcd`, `internal/coreupdate`, `internal/stableid` all PASS (no regression of existing child_env tests). gofmt clean, go vet clean.
- CI route: the required regression runs under `PR · Go unit · packages` on the `pull_request` trigger (per review-4 akte: that job already covers the affected packages on this exact head). No `.github/**` or `scripts/**` change is needed or made (Owner workflow split).

## repo-rule compliance
- No rebase, no amend, no filter-branch; commit is a fast-forward add on the exact reviewed head `23feeefee58` (parent `23feeefee58...`), verified.
- author == committer == `0428-222-childenv` (card 0428-224, single identity).
- No change to `.github/**` or `scripts/**`. No subagents. No PR merge/close/rerun/workflow dispatch. No evidence written into a product repo.
- Local tests run only in the named form with the real-lifecycle skip (coordinator runner rule 2026-11-21); no bare `go test ./cmd/baha/`.

## cleanliness
- Shell PID 569133 ran `docker ps -a` before and after. Both inventories showed the same four pre-existing `bh-itest-*` containers, all exited. No new container, compose project, or daemon state was started by this fix; the fixer package (`envpin`) has no runtime/docker dependency. `docker ps -a` after:
```
CONTAINER ID   IMAGE     COMMAND     ...   STATUS     PORTS   NAMES
bh-itest-* (pre-existing, exited) x4
```

## END
END_DONE w21-pr1702-0428-142-compat: security fix committed and pushed. Fix = commit `10c7c6414` (parent `23feeefee58...`, exact reviewed head; author==committer==0428-222-childenv) in `internal/testsupport/envpin/pin.go` — PinnedEnv now drops every inherited unpinned `ETCDCTL_*` key while keeping normally-exported parent env. Fail-first tests `TestUnpinnedETCDCTLKeyDropped` + `TestUnpinnedETCDCTLKeyDroppedDirect` RED then GREEN; existing child_env tests still PASS (no regression), gofmt+vet clean. CI route = `PR · Go unit · packages` on pull_request (no .github/** or scripts/** change). No force, no rebase/amend/filter-branch. CI: watching run `44957850132`. Evidence: `evidence/r28-welle4-2026-11-21/child-env-inheritance/round-5-etcdctl-filter.md`.
