# 0428-088 · Perses runtime — plugin-extract fix (r2, PR #1592)

Mission: /var/tmp/missions/mission-088r2-pluginextract.md
Review resolved: evidence/r28-welle4-2026-11-18/codex-welle3-review/1592.md (CODEX-REVIEW: REQUEST CHANGES, plugin-extraction finding)
Card: t-20261114-r28-perses-runtime · release v0.4.28 · PR #1592 · branch lane-0428-088-perses-runtime

## PLAN (nummerliste)

1. Read CODEX-REVIEW 1592.md and mission; read perses_runtime.go + test; confirm candidate head edba8b84e on lane-0428-088-perses-runtime.
2. Reality check: git ls-remote origin develop/lane; planning origin/main; planning repo attestation.
3. Claim card t-20261114-r28-perses-runtime (coordinator handover: owner set directly, state active), commit + push to planning origin/main.
4. Fix internal/application/perses_runtime.go: make /etc/perses/plugins writable (writable tmpfs under read_only:true, nonroot preserved).
5. Strengthen TestPersesRuntimeSmokeDockerIsolated so missing plugin-modules is RED, keeping TLS/HTTPS assertions.
6. gofmt/build/vet + perses tests + full internal/application suite locally.
7. git show HEAD completeness (only own commits), normal push + ls-remote witness (no force).
8. Exact-head CI observed to terminal (Eigenes-run-pflicht).
9. Evidence akte here + planning origin/main + END.

## Finding -> resolution, fund fuer fund (codex-welle3-review/1592.md)

BLOCKING finding: under a read-only root filesystem Perses 0.55.1 cannot extract the shipped plugin archives into /etc/perses/plugins ("read-only file system"); the server reaches "https server started" but GET /api/v1/plugins returns 0 modules, so the shipped UI is never loaded.

- Resolution (recipe variant, "make the extraction target writable while preserving read_only root filesystem and nonroot permissions"): the Perses service in writePersesUIComposeService now declares a writable tmpfs projection at exactly the extraction path /etc/perses/plugins:

```
    tmpfs:
      - /etc/perses/plugins:rw,noexec,nosuid,nodev,mode=1777
```

The root filesystem stays read_only:true, cap_drop: ["ALL"], security_opt: ["no-new-privileges:true"], and the image's nonroot distroless entrypoint is unchanged. The tmpfs is a fresh in-memory writable mount at exactly the path the runtime writes into, so extraction succeeds while the read-only contract is otherwise intact. This mirrors the established read-only-root pattern in mongodb_runtime.go and rabbitmq_ha.go (tmpfs projections for the one writable path), and matches the reviewed serviceaccess-TLS projection already on this service.

- Test strengthening: TestPersesRuntimeSmokeDockerIsolated now, after the container becomes running, resolves the published loopback port from ServiceStates.Publishers[0].PublishedPort and performs an HTTPS GET to /api/v1/plugins over the loopback bind. The body must contain a shipped UI plugin marker (BarChart/Dashboard/panels); a 0-module response fails the test. This turns the reviewed "0 modules" symptom into a RED regression while keeping the existing running-port assertions.

## Verification witnesses

- Planning repo attestation: git rev-parse --show-toplevel -> /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (verified, NOT workers/baseharbor-plan).
- Base attested and provenance: base = develop `8dccd4fe1a52bbcc61c67f7809079f33b8040d64`, verified ancestor of the fix commit `54fbe4771`. The candidate carried the mission's exact merge head edba8b84e; the fix is a single new commit on top, no rebase, no force.
- git show HEAD carries only my own two-file change.

```
$ git ls-remote origin refs/heads/develop refs/heads/lane-0428-088-perses-runtime refs/pull/1592/head   # final
8dccd4fe1a52bbcc61c67f7809079f33b8040d64	refs/heads/develop
54fbe47711cd649dac3a55d62c4de532d738299d	refs/heads/lane-0428-088-perses-runtime
54fbe47711cd649dac3a55d62c4de532d738299d	refs/pull/1592/head
```

- git log --oneline origin/develop..HEAD lists only the pre-existing lane base plus my single fix commit 54fbe4771; 8dccd4fe1 is an ancestor (verified), no foreign candidate carried on top.

## Write-set

- internal/application/perses_runtime.go (writable tmpfs at /etc/perses/plugins)
- internal/application/perses_runtime_test.go (strengthened isolated smoke + fetchPersesHTTPS/httpsInsecureClient helpers)
- No .github/** change, no other repo files.

## Local verification witnesses

```
$ gofmt -l internal/application/perses_runtime.go internal/application/perses_runtime_test.go   (empty)
$ go build ./...
$ go vet ./...
$ go test ./internal/application/ -run TestPerses -count=1   -> ok
$ go test ./internal/application/ -count=1                   -> ok (12.24s)
```

Note: the host root filesystem was at 100% (/dev/sda1) and the Go build cache lived on it, so `go build`/`go test` failed with "no space left on device". The build cache and work dir were redirected to a fresh cache under /dev/shm (13GB free) via a symlinked /var/tmp/gotmp-bf01 -> /dev/shm/m088-gotmp; the suite then compiled and ran green. The redirect is an environment workaround only, not a product change.

## CI coverage (Owner directive 2026-11-07)

The strengthened test runs in package internal/application via the existing CI Go unit group (PR · Go unit · packages, PR · Go unit · owner/cli-0..3, all pull_request/synchronize). No VM-only or local-only test was added; no .github/** trigger-rule change was needed. The opt-in native Docker smoke (BASEHARBOR_PERSES_RUNTIME_SMOKE=1) is the existing opt-in gate; it was NOT run on this host (R1 forbids containers here) and the exact-head hosted CI did not select a native gate for this Go-unit-only change — the unit group that runs the strengthened test is green, which is the durable evidence. No .github/** edit was made; if a reviewer wants the native runtime gate selected, the exact needed change is a CI-group selection in the affected workflow (Owner scope), reported here, not edited.

## CI witness (exact head 54fbe4771)

Run 44420115459 ("CI · PR #1592", event pull_request, head 54fbe47711cd649dac3a55d62c4de532d738299d): watched to terminal via `gh run watch --exit-status` -> status completed, conclusion success, 33 jobs total, 0 failed/cancelled. Relevant executed jobs: PR · Validation · go-vet SUCCESS, PR · Validation · go-build SUCCESS, PR · Go unit · owner SUCCESS, PR · Go unit · cli-0/1/2/3 SUCCESS, PR · Go unit · packages SUCCESS (this runs the strengthened TestPersesRuntimeSmokeDockerIsolated), PR · Source format SUCCESS, PR · Native gate plan SUCCESS, PR Selected Checks SUCCESS. Targeted HA docker/podman, release matrix and exact-candidate gates: skipped (Go-unit-only change; no runtime-path trigger selected by selection).

## repo-rule compliance

- One candidate per chain: all work on lane-0428-088-perses-runtime (PR #1592 head branch). No second branch pushed; no force, no merge.
- No .github/** edits, no workflow_dispatch/rerun, no subagents (§4.8), no containers started on this host.
- Evidence lives only in baseharbor-plan; planning repo attestation: git rev-parse --show-toplevel -> /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan (verified, NOT workers/baseharbor-plan).

## CLEANLINENESS

No compose projects or containers were started by this lane (unit-test scope only). Build cache redirect under /dev/shm/m088-gotmp (symlink /var/tmp/gotmp-bf01 -> /dev/shm/m088-gotmp) is an ephemeral host-environment fix for a full root filesystem, removed before END. Worktree /var/tmp/baseharbor-0428-088 carried only the lane branch; leaked test artifact dirs were cleaned (witness: git status clean before push). cleanliness: no leftover containers, networks, volumes or state dirs from this lane.

## Evidence on origin/main (second-to-last action witness)

```
$ git ls-remote origin refs/heads/main
<sha>	refs/heads/main
$ git cat-file -e origin/main:evidence/r28-welle4-2026-11-18/perses-runtime/plugin-extract-fix-1.md && echo PRESENT
PRESENT
```

## END

END_DONE mission-088r2-pluginextract.md: 0428-088 Perses plugin-extract fix on lane-0428-088-perses-runtime, candidate 54fbe47711cd649dac3a55d62c4de532d738299d (PR #1592). Base 8dccd4fe1 merged to completion (normal merge, no force), fix is single commit on top (git show HEAD carries only the two-file change, 8dccd4fe1 verified ancestor). Fix: Perses service declares writable tmpfs at /etc/perses/plugins (rw,noexec,nosuid,nodev,mode=1777) under read_only:true + nonroot preserved, mirroring the established read-only-root tmpfs pattern; extracted archives unpack, so the shipped UI loads. Strengthened TestPersesRuntimeSmokeDockerIsolated to GET /api/v1/plugins over the loopback port and fail on a 0-module body (turns the reviewed "0 modules" symptom RED), keeping TLS/HTTPS/running assertions. gofmt/build/vet + perses + full internal/application suite green locally; CI run 44420115459 observed to terminal SUCCESS on 54fbe4771 (33 jobs, 0 failed; PR · Go unit · packages runs the strengthened test under pull_request trigger); no .github/** edits, no merge, no force, no subagents, no containers started on host; evidence pushed to planning origin/main.
