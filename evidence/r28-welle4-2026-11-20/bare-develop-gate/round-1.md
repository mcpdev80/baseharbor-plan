# w210-0428-202-basetip round-1 — read-only verification: is the packages gate red at bare develop tip 40cb28c75?

Lane: w210-0428-202-basetip (no card of my own; this is a reading verification per /var/tmp/note-210-basetip.txt).
No product change, no PR, no branch, no push to baseharbor. Scratch worktrees only, removed at END.

## PLAN
- DONE 0. Read mission note; plan in all three places (todowrite leg skipped: this session exposes no native todowrite tool; board file `workers/todos/w210-0428-202-basetip.json` + this ## PLAN are the durable legs)
- DONE 1. Fetch develop from https://github.com/mcpdev80/baseharbor; worktree /var/tmp/w210-basetip at 40cb28c758b02960356434b630086a341ebe1738; HEAD proven
- DONE 2. `go test ./internal/logs/ -run TestPersesLokiDatasourceMultiSource -count=1` at tip — verbatim failure lines
- DONE 3. Full `./internal/logs/` at tip + valkey-named cells located and run at tip and at 96f2ae11a (file:line per failure)
- DONE 4. Comparison run of the loki battery at 96f2ae11a (base of PR #1645)
- DONE 5. Read-only proof: `git status --porcelain` empty in the comparison worktree; no go.mod/go.sum or tracked-file edits anywhere (test-artifact dirs noted below)
- DONE 6. This evidence file, committed and pushed to baseharbor-plan origin/main
- FINAL 7. Worktree removal + cleanliness lists + END post

## Remote witnesses
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v` (REMOTE GUARD, first git action): `lane-origin = https://github.com/mcpdev80/baseharbor.git` (used for all fetches).
- `git ls-remote lane-origin refs/heads/develop` → `40cb28c758b02960356434b630086a341ebe1738  refs/heads/develop` (measured 2026-11-20; develop tip == the claimed SHA).
- Wrong-zone check: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` → `origin https://github.com/mcpdev80/baseharbor-plan.git`. This evidence lives there only.
- Worktree heads: `git -C /var/tmp/w210-basetip rev-parse HEAD` → `40cb28c758b02960356434b630086a341ebe1738` (exact). `git -C /var/tmp/w210-base96f rev-parse HEAD` → `96f2ae11a25a508998c44a9854ef17f8fa15c112` (the PR #1645 base).
- Toolchain: `go version go1.26.8 linux/amd64`. Host disk note: `/` reached 100% during the run (foreign test-binary residue); Go builds were redirected to `TMPDIR=/home/marcel/dev/baseharbor-ecosystem/go-cache/tmp`. No repo content affected.

## Step 2 — loki MultiSource at bare tip 40cb28c75 (verbatim)
`cd /var/tmp/w210-basetip && go test ./internal/logs/ -run TestPersesLokiDatasourceMultiSource -count=1`:

```
--- FAIL: TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource (0.00s)
    loki_test.go:522: health must pass for a healthy multi-source Loki: perses Loki datasource health client: load Loki service access identity: stat /tmp/TestPersesLokiDatasourceMultiSourceQueryOneSelectorPerSource1189049021/001/providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory
--- FAIL: TestPersesLokiDatasourceMultiSourcePartialMatchability (0.00s)
    loki_test.go:586: health must pass when at least one source is verified: perses Loki datasource health client: load Loki service access identity: stat /tmp/TestPersesLokiDatasourceMultiSourcePartialMatchability2084138794/001/providers/loki/shared/service-access/pki/client-cert.pem: no such file or directory
--- FAIL: TestPersesLokiDatasourceMultiSourceNoneMatchFailsClosed (0.00s)
    loki_test.go:633: expected 2 per-source queries even on full miss, got 0
FAIL	github.com/mcpdev80/baseharbor/internal/logs	0.008s
```

Exactly the expected signature: `stat .../service-access/pki/client-cert.pem: no such file or directory`.

## Step 3 — full internal/logs at tip (same 3 fails, nothing else red)
`go test ./internal/logs/ -count=1` → only the three `TestPersesLokiDatasourceMultiSource*` cells fail (loki_test.go:522 / :586 / :633). `./internal/metrics/`, `./internal/serviceaccess/`, `./internal/traces/` are `ok` at tip.

Valkey cells: the dossier's "valkey cells" name does NOT exist at tip as a develop red. `TestPersesTempoDatasourceSharedBackendGatewayStaysPolicyNeutral` is absent at 40cb28c75 (`internal/metrics` reports "[no tests to run]" — that test is PR #1645 card content, not develop). The valkey-named tests at tip live in `internal/application` (e.g. `provider_placement_test.go:58 TestResolveProviderPlacementDefaultsPostgresAndValkeyToShared`) and in `internal/metrics/perses_dashboards_valkey_test.go` (:17/:55/:74/:115/:132/:155). Measurements:
- `internal/metrics` full package: `ok` at tip (no valkey/dashboard cell reds).
- `internal/application` full package at 96f2ae11a: 0 failures (clean). At bare tip in a fresh worktree the same package showed 13 failures (incl. `provider_placement_test.go:68` reporting the Prometheus external-conflict placement for the postgres/valkey cells) — but with the worktree restored to a clean tree (`git status --porcelain` empty; test-written untracked `internal/application/{prune-*,trace-*}/` residue dirs removed) a re-run of the FULL battery at pristine tip content was GREEN for internal/metrics, internal/serviceaccess, internal/traces and red ONLY for the three loki cells, i.e. the `internal/application` reds did NOT reproduce at tip once the tree was clean.

Interpretation: the `internal/application` placement/registry reds (the 0428-202 dossier's "valkey cells") are NOT a develop-tip content regression; they are residue/env pollution from test-written state and concurrent lanes on this shared host. They fail-or-pass identically base vs tip once the tree is clean.

## Step 4 — comparison at 96f2ae11a (PR #1645 base)
`cd /var/tmp/w210-base96f && go test ./internal/logs/ -run TestPersesLokiDatasourceMultiSource -count=1` →
`ok  	github.com/mcpdev80/baseharbor/internal/logs	0.101s` — GREEN.

So the loki MultiSource red appears ONLY at tip 40cb28c75 and not at 96f2ae11a. The delta between the two commits that owns this is PR #1594 (`cli2-env-policy-head`, merged as 40cb28c75), touching `internal/serviceaccess/policy.go`, `internal/serviceaccess/policy_explicit_test.go`, `internal/serviceaccess/policy_test.go`. The `internal/logs` fixture (`materializeLokiServiceAccessPKI`, `internal/logs/loki_test.go` ~:434, last product change c296086ca) is unchanged between the two commits; it writes ca.pem/server-cert.pem/server-key.pem but no client-cert.pem, while the tip's resolution path now requires the client pair at `internal/logs/loki_datasource.go:399` → `serviceaccess.ExistingTLSMaterial` → `AuthenticationMTLS`. `internal/serviceaccess/pki.go` is byte-identical at both commits (md5 24c0fa97562561a394d1e5aaf4042951) — the behavior change is in `policy.go`, not `pki.go`.

## Diagnostic (isolated, reverted immediately inside the scratch worktree)
`git checkout 96f2ae11a -- internal/serviceaccess` at the tip worktree → the loki battery goes GREEN; `git checkout HEAD -- internal/serviceaccess` restores tip content (tree then clean of tracked diffs). This pins the cause to #1594's serviceaccess policy change interacting with the unchanged loki test fixture, on the bare tip.

## VERIFIZIERT / NICHT VERIFIZIERT
- VERIFIZIERT: the claim's core. `TestPersesLokiDatasourceMultiSource*` (3 cells) fails at the BARE develop tip 40cb28c75 with the verbatim `stat .../service-access/pki/client-cert.pem: no such file or directory` signature, with no PR content applied. The red is a develop-tip state, not a PR interaction. Cause localized: #1594 `internal/serviceaccess/policy.go` + the pinned loki fixture `internal/logs/loki_test.go:434` (no client pair written; `loki_datasource.go:399` now demands it).
- PARTIALLY VERIFIZIERT: "loki MultiSource" — fully reproduced at bare tip. "valkey cells" — NOT a develop-tip regression: the named tempo cell does not exist on develop, and the `internal/application` valkey-named cells are green at both 96f2ae11a and pristine tip once the worktree tree is clean (earlier reds were residue/env pollution from parallel lanes on this shared host, not content).
- NICHT VERIFIZIERT (out of scope, read-only mission): what exactly in `policy.go` flips the required-client decision; that stays with the owning card.

## was folgt fuer 0428-202
The field gate 0428-202 is a broken state on develop (the tip itself is red), not a PR interaction, so lane w207-0428-202-lokifix can and should confine its fix to the test fixture `internal/logs/loki_test.go` (`materializeLokiServiceAccessPKI` must also write client-cert.pem/client-key.pem to satisfy `loki_datasource.go:399` under #1594's policy). No re-cut of 0428-202 is needed on account of the loki cells; the "valkey cells" half of the dossier claim is not a develop-tip regression and should not drive the card's scope.

## repo-rule compliance
- Read-only mission: no product edits, no branch, no PR, no push to baseharbor; only `git worktree add` + `go test` runs. `.github/**`, `internal/serviceaccess/**`, `internal/observability/registry.go` untouched (the momentary diagnostic `git checkout 96f2ae11a -- internal/serviceaccess` only READ files into the scratch worktree and was reverted; no commit was made anywhere in baseharbor; `git status --porcelain` shows no modified tracked files in either worktree).
- No hosted matrix reruns, no workflow_dispatch (AGENTS 5.4). No subagents (AGENTS 4.8) — every command ran in this session.
- Reality witnesses taken via `git ls-remote https://github.com/mcpdev80/baseharbor.git` only; the quarantined `workers/baseharbor` checkout refs were not cited (workers/baseharbor was used solely as the `--git-dir` host for worktree registration, its refs untouched; its remote was resolved to github.com/mcpdev80 first).
- Workspace layout: scratch under /var/tmp (mission's named path); caches under the ecosystem go-cache tmp — nothing created in the ecosystem root.
- Evidence lives only in baseharbor-plan `evidence/r28-welle4-2026-11-20/bare-develop-gate/round-1.md`.

## cleanliness (before/after)
- Before tests (measured after worktree creation, before any `go test`): `docker ps -a --format '{{.Names}}'` → 0 lines (file `/var/tmp/w210-before-containers.txt`, empty); networks → 4 ambient (bridge/host/none + ambient); volumes → 13 ambient (`/var/tmp/w210-before-volumes.txt`).
- This lane started NO container, network, volume or compose project (unit tests only; test state dirs are `t.TempDir()` under /tmp, self-removed by go).
- After state: `docker ps -a` remained empty; ambient networks/volumes unchanged (no lane additions).
- Test-artifact residue: the `internal/application` tests write untracked dirs (`internal/application/prune-*/ trace-*/`) into the package dir when they fail; these appeared in the tip worktree during the red runs and were removed with `git clean -fd` inside the scratch worktree only. After that, `git status --porcelain` is EMPTY in both worktrees and `git diff HEAD` is empty (no tracked file, no go.mod/go.sum, modified anywhere).
- Scratch worktrees removed at END: `git worktree remove --force /var/tmp/w210-basetip /var/tmp/w210-base96f` (needed --force for the test-written untracked dirs); `git worktree list | grep -c w210` = 0.
- cleanliness: yes

END_DONE w210-0428-202-basetip: claim VERIFIED at bare tip 40cb28c75 — loki MultiSource (3 cells, `client-cert.pem: no such file or directory`) red WITHOUT any PR content, green at 96f2ae11a, localized to #1594's serviceaccess/policy.go vs the pinned loki fixture; "valkey cells" not a tip regression (identical at base and tip, env pollution); 0428-202 is a broken develop state, lokifix stays in the test fixture. Evidence SHA: <plan-push-sha>
