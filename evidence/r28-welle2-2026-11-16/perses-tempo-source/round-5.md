# round-5 — perses-tempo-source (mission-tempo-r5)

**ROLE:** Worker (w091) · 2026-11-16 · no merge, no GitHub review mutation, no .github edits, no force-push, no retarget, no subagent.
**Card:** `t-20261114-r28-perses-tempo-source` · **PR #1610** · exact head to fix: `601f3c3af26a7aec00551f8d37899c30918b9939`.
**Branch:** `w091-0428-091` (fast-forward on top of PR #1610 head).
**Task:** Fix the Go package-selection CI failure. The candidate embeds eight `.go` witness files under `internal/metrics/testdata/.../upstream/`. The changed-package selector treats that directory as a Go package and cannot discover/build it. Fix: rename the embedded `.go` witness files to non-Go suffixes (`.go.txt` / `.tmpl`), preserve their content and update the `//go:embed` paths and any embed/validation paths accordingly. Then targeted local tests + exact-head PR run green.

## PLAN (work plan, §4.4)

- 1. First action: fresh clone to /tmp/opencode/tempo-r5-wt, `ls-remote` witness, `rev-parse`==`601f3c3af26` as proof, confirm it is the PR #1610 head.
- 2. Confirm exact HEAD `601f3c3af26` is an ancestor of the branch I cut; record base SHA in evidence.
- 3. Identify all eight embedded upstream `.go` witness files and every `//go:embed` + validation path that references them.
- 4. Rename each `.go` witness to a non-Go suffix, preserving content; update embed paths and validation paths accordingly.
- 5. `go build ./...` + focused Perses tests locally; verify selector loads no `.go` under testdata (run `scripts/pr-draft-go-packages.py` if local, else structural argument).
- 6. Record exact SHA of PR #1610 head as the base; fast-forward commit on `w091-0428-091`.
- 7. Push `HEAD:refs/heads/w091-0428-091`, capture `ls-remote` witness AFTER push.
- 8. Get an exact-head PR run green; record Run-ID/status.
- 9. Commit evidence to baseharbor-plan `origin/main`; run `git log origin/main` as second-to-last action; paste exact output.
- 10. Down any docker/podman compose I started (none expected); post formal END post.

## repo-rule compliance

- Product change only: rename of eight `testdata` witness files + embed/validation path edits. No `.github/**` touched.
- No merge, no ready_for_review, no force-push, no retarget.
- No subagents (§4.8): every step executed inside this session.
- Planning evidence published only on baseharbor-plan `origin/main`.

## END status

DONE
