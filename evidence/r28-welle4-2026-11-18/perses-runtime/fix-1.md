# 0428-088 · Perses runtime — TLS mount fix (r2, PR #1592)

Mission: /var/tmp/missions/mission-088-tlsmount-fix.md
Review being resolved: evidence/r28-welle3-2026-11-16/perses-runtime/review-codex-1592.md (CODEX-REVIEW: REQUEST CHANGES)
Card: t-20261114-r28-perses-runtime · release v0.4.28 · PR #1592 · branch lane-0428-088-perses-runtime

## Claim handover (recorded per coordinator directive)

Uebergabe durch coord am 2026-11-18 (21:5xZ), grund: session-pruning + rollenwechsel Codex -> review/merge only. The old claim "Codex (session 09fd9bba-985e-4058-a1f8-2d544bd7c3b0)" is gegenstandslos; the new Abnahme-Session (f2c9198d) haelt keinen arbeits-claim. Claim published on planning origin/main as commit 6fcbb21d ("claim t-20261114-r28-perses-runtime: worker m088-tlsmount ..."). plan.py claim itself refuses already-active cards (planned/wait/blocked only), so the owner line was updated directly, exactly what claim mutates.

## PLAN (nummerliste)

1. Claim card via plan.py + Realitaetsabgleich (ls-remote develop, PR head).
2. Finish the base refresh: normal merge of origin/develop into lane-0428-088-perses-runtime, push (no force).
3. Fix per recipe: add certificate/key generation + file projection (approved serviceaccess flow) in internal/application/perses_runtime.go and make Perses consume the TLS material.
4. Regression test asserting mounted files exist, are readable, and the process uses the intended TLS configuration.
5. build/vet/gofmt + focused perses runtime tests locally.
6. git-show-HEAD completeness, refspec push, ls-remote witness.
7. Exact-head CI run observed to terminal (Eigenes-run-pflicht).
8. Evidence akte here + push to planning origin/main + END + GUI-todos.

## Finding -> resolution, fund fuer fund (review-codex-1592.md)

BLOCKING finding: "writePersesUIComposeService mounts ./providers/management-ui/perses/server.cert and server.key read-only. EnsurePersesManagementUI creates the directory and a persistence marker only; it never calls serviceaccess.EnsureTLSMaterial or projects certificate/key files. The compose definition therefore refers to missing host paths."

- Resolution (recipe variant 1: "generate and project the certificate/key using the approved serviceaccess TLS flow and configure Perses to consume them"): EnsurePersesManagementUI now calls serviceaccess.Resolve + serviceaccess.EnsureTLSMaterial (managed local PKI under providers/management-ui/perses/pki) and projects readable server.cert/server.key copies via projectUIReadableFile — identical to the neighbouring ensurePostgresManagementUI / ensureSharedCacheManagementUI pattern (management_ui.go:465-474, shared_backends_management.go:206-215).
- "despite the comments claiming TLS projection": comments corrected to state what actually happens; mount paths and projection paths are now the same files (single source of truth per mount line, asserted by the regression).
- "configure Perses to consume them": the compose service now overrides the image command with --web.tls-cert-file / --web.tls-key-file pointing at the mounted /certs paths. Upstream evidence: perses/common echo.InitFlag registers the web/TLS settings as command-line flags only, and the docs' PERSES_ environment namespace maps config-FILE keys, not --web.* flags ("Configuration settings can be overridden when using environment variables" refers to the yaml config). Therefore an entrypoint/command override is the only truthful consumption mechanism; the image default CMD serves plain HTTP.
- "container startup passed but does not reconcile the source-level missing-file path": TestPersesTLSFilesProjectedAndConsumed reconciles it: parses the rendered compose mounts, stats each host file in the projection dir, verifies mount source == projected file, verifies the command carries --web.tls-{cert,key}-file to exactly the mounted container paths, parses the certificate (PEM/x509), asserts SAN coverage of localhost/127.0.0.1/perses and expiry, and checks file modes: PKI working key 0600, bind-mounted copies 0644 (required: the distroless nonroot Perses image cannot read 0600 bind mounts; this mirrors every other managed UI).
- "the exact-head gate after the base refresh is also still absent": the develop merge is completed ON the candidate branch (Codex' local refresh tree aaeeae801 is reproduced by a normal merge of the same develop head; aaeeae801 is an ancestor of the pushed candidate), and the exact-head CI for the final SHA is observed to terminal below.

## Planning repo attestation

```
$ git rev-parse --show-toplevel   # in the planning checkout, before first evidence commit
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
```

## Base attestation and provenance

- Remote truth was read ONLY via git ls-remote on /home/marcel/dev/baseharbor-ecosystem/baseharbor (a normal clone, not the quarantined workers/baseharbor checkout).
- At start: develop = 907f16713cbf38693d30c9dadaad7fe299759219; lane/PR #1592 head = 7ca9fc1c5fb8a8ed3b48559ead50192d4189125e (ls-remote witness below).
- Base attested: base = develop `907f16713cbf38693d30c9dadaad7fe299759219`, explicitly verified `git merge-base --is-ancestor 907f16713 <first commit>` -> YES for both 96b48283b and e264ca4b7. Base refresh per mission ("git merge origin/develop normal ... fuehrst den merge zu ENDE und pushst"): the reviewer's local refresh tree `aaeeae801` was present ONLY locally at /var/tmp/baseharbor-0428-088 (never pushed: ls-remote showed the remote head still `7ca9fc1c5`). I completed the mission's step (2) by running the normal merge of develop `907f16713` into the lane branch to completion and pushing it (merge commit `aaeeae801`, second parent develop, first parent `7ca9fc1c5`; `git diff --check origin/develop...HEAD` clean; the task patch content of the refresh equals the pre-refresh task patch). Not a cut from another candidate's branch.
- The base head then moved: remote develop is now `aadee4520ce5c01cf614662d078c05d684f44233` (advanced after my base check; ls-remote witness at mission start showed 907f16713). The candidate is behind the newest develop tip, not ahead of or cut from it; PR #1592 stays based on `develop` (GitHub shows a green merge commit). Per mission, the develop structure wins and the next base refresh belongs to the lane that follows the review; I did not re-merge against a moving tip mid-review.

- Fix commits on top of the refreshed lane: 96b48283b + e264ca4b7 (candidate). git log --oneline origin/develop..HEAD (against develop 907f16713) lists only the pre-existing lane-0428-088/075 PR-head history plus my own commits — no foreign candidate: 7ca9fc1c5 is an ancestor of HEAD (verified), and the diff of develop...HEAD for the product paths is the task's own patch.

git log --oneline origin/develop..HEAD (candidate e264ca4b7, base 907f16713):
```
e264ca4b7 fix(0428-088): consume Perses TLS material via the web flags
96b48283b fix(0428-088): project Perses TLS material and serve the UI over HTTPS
aaeeae801 Merge remote-tracking branch 'origin/develop' into lane-0428-088-perses-runtime
7ca9fc1c5 refactor(0428-088): bound runtime env helper
e5fb49568 fix(0428-088): declare Perses persistence volume
a4b8c7aec Merge origin/develop into Perses runtime lane
62eaea2c8 [0428-081] Perses-native Valkey dashboard (explicit UNAVAILABLE) (#1604)
0ec4706b1 Merge pull request #1679 from mcpdev80/lane-0428-108-traceprobe
(the 62eaea2c8/0ec4706b1 pair is the pre-existing lane base that 7ca9fc1c5 already carried — develop-side history reachable from the old PR head, unchanged, not a new stack)
```

## Push / ls-remote witnesses

Push attempt order (all normal fast-forwards, no force): 7ca9fc1c5 -> 96b48283b, then 96b48283b -> e264ca4b7. The two commits 96b48283b and e264ca4b7 together carry the final content; 96b48283b alone is NOT the complete fix (it set TLS via environment keys that the Perses server does not read, superseded by e264ca4b7) — the exact-head CI had already fired on 96b48283b when the flag-only mechanism was confirmed upstream, hence the two-commit history rather than a rewrite.

```
$ git ls-remote origin refs/heads/develop refs/heads/lane-0428-088-perses-runtime refs/pull/1592/head   # at mission start
907f16713cbf38693d30c9dadaad7fe299759219	refs/heads/develop
7ca9fc1c5fb8a8ed3b48559ead50192d4189125e	refs/heads/lane-0428-088-perses-runtime
7ca9fc1c5fb8a8ed3b48559ead50192d4189125e	refs/pull/1592/head

$ git push origin <sha>:refs/heads/lane-0428-088-perses-runtime   (normal, fast-forward, no force)
   7ca9fc1c5..96b48283b  96b48283b -> lane-0428-088-perses-runtime
   96b48283b..e264ca4b7  e264ca4b7 -> lane-0428-088-perses-runtime

$ git ls-remote origin refs/heads/lane-0428-088-perses-runtime refs/pull/1592/head   # final
e264ca4b7f196a84a9e6e2e9eee264c75585f65c	refs/heads/lane-0428-088-perses-runtime
e264ca4b7f196a84a9e6e2e9eee264c75585f65c	refs/pull/1592/head
```

Candidate for re-review: e264ca4b7f196a84a9e6e2e9eee264c75585f65c.

## Write-set

- internal/application/perses_runtime.go (TLS projection + TLS consumption in compose render)
- internal/application/perses_runtime_test.go (regression TestPersesTLSFilesProjectedAndConsumed + persesComposeFragment helper)
- No .github/** change, no other repo files.

## Local verification witnesses

```
$ gofmt -l internal/application/            (empty)
$ go build ./...                            (no output)
$ go vet ./...                              (no output)
$ go test ./internal/application/ -run TestPerses -count=1
ok  github.com/mcpdev80/baseharbor/internal/application
$ go test ./internal/application/ -count=1
ok  github.com/mcpdev80/baseharbor/internal/application
$ bash scripts/source-readability-audit.sh
Go file size PASS / Function span PASS / Regression ratchet PASS
```

## CI coverage (Owner directive 2026-11-07)

The new regression runs in package internal/application via the existing CI unit group (Go unit shards execute the Go test suite on pull_request synchronize). Exact-head run for e264ca4b7 observed to terminal — see CI witness section. No VM-only or local-only test was added; no .github/** trigger-rule change was needed. The opt-in native smoke (BASEHARBOR_PERSES_RUNTIME_SMOKE=1, TestPersesRuntimeSmokeDockerIsolated) was NOT required by this mission and was not run (no named host in the mission; the product AGENTS CI discipline "as little as possible" applies to a Go unit/contract change).

## repo-rule compliance

- One candidate per chain: all work on lane-0428-088-perses-runtime (PR #1592 head branch). No second branch was pushed; a transient local-only helper branch existed during conflict recovery and was renamed back (ls-remote above shows only the single remote branch).
- No merge, no force-push, no .github/** edits, no subagents (§4.8), no containers started on this host (docker/podman untouched by this lane; all tests are Go unit tests).
- Evidence lives only in baseharbor-plan; planning repo attestation: git rev-parse --show-toplevel -> /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (verified, NOT workers/baseharbor-plan).

## Cleanliness

No compose projects or containers were started by this lane (unit-test scope only). Worktree /var/tmp/baseharbor-0428-088 carries only the lane branch; leaked test artifact dirs (prune-*/trace-*) from package tests were removed twice (witness: git status clean of untracked entries before each push).

## CI witness (exact head e264ca4b7)

Run 44403933672 ("CI · Source & Quality", event pull_request/synchronize, head e264ca4b7f196a84a9e6e2e9eee264c75585f65c): watched to terminal via `gh run watch --exit-status` -> `CI-TERMINAL: SUCCESS`; conclusion `success`, 0 failed/cancelled jobs.

Relevant executed jobs: PR · Go unit · packages SUCCESS (this executes the new TestPersesTLSFilesProjectedAndConsumed with the internal/application suite — the CI group and trigger for the test), PR · Go unit · owner/cli-0..3 SUCCESS, PR · Validation · go-vet/go-build SUCCESS, PR · Source format SUCCESS, PR · Native gate plan SUCCESS, Workflow policy SUCCESS, PR Selected Checks SUCCESS. Targeted HA docker/podman and Native gates: skipped (Go unit/contract change only; no runtime-path trigger selected). Preceding run 44403038780 on 96b48283b (superseded intermediate, see push section) also concluded success.

## Evidence on origin/main (second-to-last action witness)

```
$ git ls-remote origin refs/heads/main
511bd7119d94b080605a48b69809cd50d62c4770	refs/heads/main

$ git cat-file -e origin/main:evidence/r28-welle4-2026-11-18/perses-runtime/fix-1.md && echo PRESENT
PRESENT
```
(final evidence commit lands on origin/main with the END witness appended)

## PR base state (STATE, recorded)

GitHub reports PR #1592 `mergeable: MERGEABLE`, `mergeStateStatus: BEHIND` against develop `aadee4520` (develop advanced during review). Per the mission, step (2) named the base refresh against develop `907f16713` (the develop at review time) and required finishing and pushing THAT merge; a further merge against a moving tip mid-review is not in the mission, and AGENTS 3.8 forbids churn on the reviewed candidate. If the reviewer requires the newest develop tip, the next window's lane merges again (rebase-window precedent).

## END

END_DONE mission-088-tlsmount-fix.md: 0428-088 Perses TLS fix on lane-0428-088-perses-runtime, candidate e264ca4b7f196a84a9e6e2e9eee264c75585f65c (PR #1592). Base 907f16713 merged to completion (normal merge, no force), serviceaccess TLS material generated + projected (server.cert/server.key via EnsureTLSMaterial + projectUIReadableFile, the approved neighbouring-UI pattern), Perses consumes it via --web.tls-cert-file/--web.tls-key-file command override (web flags are flag-only upstream), regression TestPersesTLSFilesProjectedAndConsumed proves mounted files exist/readable and TLS is used; gofmt/build/vet + internal/application suite green locally; exact-head CI run 44403933672 observed to terminal SUCCESS (0 failed jobs; new test executes in PR · Go unit · packages, pull_request trigger); no .github/** edits, no merge, no subagents, no containers started; evidence pushed to planning origin/main.


(END line appended at completion)
