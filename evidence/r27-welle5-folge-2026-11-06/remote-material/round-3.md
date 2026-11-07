# remote-material round-3 — t-20261018-r27-remote-material (w287)

## Role / worker / own session (AGENTS 4.8)

Worker lane w287, own session only. No subagents. Evidence in baseharbor-plan only.

## Remote witnesses (measured)

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`:

```text
3fa6f7b0d0ba01943501627e4c5d811cc7bee848 (base recorded round-2)
6f43866e848b0653a11b01b5205075f62571d449 refs/heads/develop (current, drifted)
```

Local branch HEAD after commit:

```text
a9f2574640b550877d36a98906f034a9f202619e (HEAD -> work/r27-remote-material)
```

Pushed to `origin/work/r27-remote-material`. Draft PR #1418 (never marked ready — owner holds basis-freigabe):

```text
https://github.com/mcpdev80/baseharbor/pull/1418
```

CI run in progress on the PR branch:

```text
run number 4973, status in_progress, run-url 42329043647
https://github.com/mcpdev80/baseharbor/actions/runs/42329043647
```

## Round-3 actions

1. Committed three files on `work/r27-remote-material` (targeted `git add`, no `git add -A`):
   - `internal/application/backend_tls.go` (production: exposure serving material)
   - `internal/application/runtime_postgres.go` (production: gateway compose service + mount)
   - `internal/application/remote_exposure_serving_test.go` (new tests)
   commit `a9f257464`: `feat(remote): project exposure serving TLS via PKI owner into managed runtime (t-20261018-r27)`
2. Pushed the ast: `git push -u origin work/r27-remote-material` (new remote branch created).
3. Opened draft PR #1418 (base `develop`, `gh pr create --draft --base develop`). NOT ready-marked (owner holds basis-freigabe; develop currently rotating, owner fixing CI failures).
4. Cleaned second worktree `/tmp/w287sync` (see below).

## Fixing the local test suite (measured)

`go test ./internal/application/...` against the full suite is deferred until basis-freigabe (develop rotates; owner + chatgpt are fixing CI failures). Locally the isolated new tests were pinned against the real code:

- `go build ./internal/application/...` clean (rc=0).
- `go vet ./internal/application/...` clean (rc=0).
- `serviceaccess.VerifyCACertificate` does NOT exist (no export); the PKI protocol probe was rewritten to stdlib `x509.ParseCertificate` + `ca.Verify` proving the projected CA is the self-signed managed PKI anchor.
- Serving-key on-disk mode verified `0600`, serving-cert/ca verified `0644` against the real files (fixture `zz_inspect_mode_test.go` was removed after measuring). The original `0644` assertion was a wrong `copyServingMaterial` suffix check (material basenames end in `*.pem`, not `key`); fixed to key off the target basename.

The full-suite run stays deferred — it is not the acceptance evidence; the acceptance run is the GitHub CI job (#4973), which runs only after basis-freigabe.

## /tmp/w287sync cleanup

`/tmp/w287sync` was a second worktree on `work/r27-remote-material`. Removed with `git worktree remove` + `git worktree prune`. Justification: §0.2 persistent zone only; a stray worktree that is not the launch window is a cleanup target, not a second evidence lane. Not committed to workers/.

## END

`END_DONE w287-pr1410-remote-material: head=a9f2574640b550877d36a98906f034a9f202619e base=3fa6f7b0d0 pr=1418 run=42329043647 status=in_progress(draft,not-ready,wait basis-freigabe)`
`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` => `6f43866e848b0653a11b01b5205075f62571d449 refs/heads/develop`
