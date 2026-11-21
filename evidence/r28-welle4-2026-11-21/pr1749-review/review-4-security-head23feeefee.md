# CODEX-REVIEW — PR #1749 security re-review

## PLAN

1. Revalidate live PR #1749 refs and hosted CI at the exact reported head.
2. Inspect `pinnedEnv` and the etcdctl environment keys passed to child processes; determine whether inherited, unapproved `ETCDCTL_*` values survive.
3. Inspect the DCS boot probe environment construction and confirm actual last-wins behavior for duplicate keys.
4. Inspect the candidate tests and exact hosted CI selection for fail-first regressions covering inherited insecure TLS and CA overrides.
5. Issue a SHA-specific REQUEST CHANGES verdict with actionable correction/test requirements, and explicitly supersede the prior APPROVE HOP while preserving its historical record.
6. Publish this evidence only to the verified Planning `origin/main`, record remote path evidence, and post END.

## Planning remote and repository rules

Planning worktree remote, captured by `git remote -v` before the first evidence commit:

```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

The assigned Planning task is `t-20261121-child-env-inheritance` / card 0428-222. Its write-set permits the etcdctl/etcdutl and DCS source and package tests, while forbidding `.github/**` and `scripts/**`. This review made no product changes.

## Exact candidate and hosted run

- Fresh product refs: `513488eeb6d788f0e5eec054be89807505f05e08 refs/heads/develop`, `23feeefee58c5438ccd37fe5c0edc674c5d0a79b refs/heads/lane-0428-222-child-env`, and the same SHA at `refs/pull/1749/head`.
- GitHub reports PR #1749 OPEN, non-draft, base `develop`, mergeable, `CLEAN`, exact head `23feeefee58c5438ccd37fe5c0edc674c5d0a79b`.
- Run [44953630114](https://github.com/mcpdev80/baseharbor/actions/runs/44953630114) is `pull_request`, `completed/success` on that exact head: 36 jobs, 15 success, 21 skipped, 0 failures. `PR Selected Checks` job 136998017721 succeeded. Skipped jobs remain skipped and are not counted as passes.
- The existing `PR · Go unit · packages` job 136996874656 completed successfully; its hosted log reports `ok` for `internal/corebackup/etcd`, `internal/coreupdate`, and `internal/stableid`, followed by `PASS all non-CLI Go package tests`. This job executes package-discovered tests for the changed paths on the `pull_request` trigger. There is an existing CI route for the requested regressions, so no `.github/**` or `scripts/**` owner-scope finding is needed.

## Security findings at exact head

### P1 — unapproved etcdctl environment flags survive the pin helper

The candidate's `internal/testsupport/envpin/pin.go:12-18,26-35` copies `os.Environ()`, removes only keys present in `pins`, then appends the passed pins. The etcdctl snapshot and endpoint-status calls pass only PATH/API/endpoints/CA/cert/key in `internal/corebackup/etcd/etcdctl.go:102-110,167-172`; the DCS boot probe passes the same controlled set at `internal/coreupdate/dcs_boot_probe.go:63-68`. Consequently unlisted parent `ETCDCTL_*` values remain in each child environment. In particular, parent `ETCDCTL_INSECURE_SKIP_TLS_VERIFY=true` survives and selects etcdctl's `--insecure-skip-tls-verify` global flag, disabling TLS server-certificate verification. Upstream etcd v3.6.0 documents its `ETCDCTL_` + uppercase/underscore flag mapping in [etcdctl README](https://github.com/etcd-io/etcd/blob/v3.6.0/etcdctl/README.md#L177-L184), and reads `insecure-skip-tls-verify` in [global.go](https://github.com/etcd-io/etcd/blob/v3.6.0/etcdctl/ctlv3/command/global.go#L1374-L1384).

The same parent passthrough applies to the PATH-only `envpin.PinnedEnv("PATH=/usr/bin:/bin")` at `internal/corebackup/etcd/etcdutl.go:95-100`. The fix should preserve ordinary exported parent variables while dropping every unapproved `ETCDCTL_*` key, or explicitly setting each permitted flag to a safe value, across the etcdctl and etcdutl child calls. Continue to remove inherited copies of pinned keys and append their approved values after the retained environment.

Current tests exercise normal environment inheritance and pin precedence, but neither changed package test file contains `ETCDCTL_INSECURE_SKIP_TLS_VERIFY` or asserts that unapproved `ETCDCTL_*` keys are absent. Require a fail-first child-process regression that sets the parent value to `true`, observes the value reaching the child on this candidate, then passes after the fix. Retain the conflicting inherited `ETCDCTL_CACERT` assertion and demonstrate its regression sensitivity with the pre-fix/mutation failure record. Run both through `PR · Go unit · packages` on the resulting exact PR head; this existing `pull_request` job already covers the affected packages.

### The reported DCS pin-order failure is not present at this SHA

At `internal/coreupdate/dcs_boot_probe.go:60-68`, the exact candidate calls `envpin.PinnedEnv`, not `append(pins, os.Environ()...)`. The helper at `internal/testsupport/envpin/pin.go:26-35` filters inherited copies of the named pin keys and appends the pins last. Therefore a parent cannot override the currently listed `ETCDCTL_API`, `ETCDCTL_CACERT`, `ETCDCTL_CERT`, or `ETCDCTL_KEY` values at the DCS call site. The candidate test `TestDCSBootProbePinsOverrideInherited` also sets opposing parent values for those keys. Likewise `TestChildProcessEnvShowsPinNotInherited` covers inherited conflicting `ETCDCTL_CACERT` at the etcdctl site. The owner report's specific B claim is not reproducible from the exact remote source; it should not be listed as a confirmed finding. Unapproved keys such as `ETCDCTL_INSECURE_SKIP_TLS_VERIFY` still pass through at DCS, so the P1 remains.

## Superseding verdict

The earlier [review-3 hop record](review-3-head23feeefee.md) states APPROVE HOP. This security re-review explicitly **supersedes that approval**; it remains in Planning history and is not deleted. Verdict: **REQUEST CHANGES** for exact head `23feeefee58c5438ccd37fe5c0edc674c5d0a79b` because an inherited etcdctl environment flag can disable TLS verification and the required fail-first regression is absent. Do not merge until the filter/pins and hosted regression evidence are complete. This review did not merge, comment on, or close the PR.

## repo-rule compliance

- No product, workflow, or script files changed. No local suite tests, PR comment, merge, close, rerun, or workflow dispatch occurred. No subagents were used.
- Existing exact-head CI was inspected read-only. New regression coverage must be exercised by the existing `PR · Go unit · packages` job on the `pull_request` trigger.
- Evidence contains no Markdown task checkboxes.

## cleanliness

Shell PID 609042 ran `docker ps -a` before and after review. Both inventories showed the same eight pre-existing `bh-itest-*` containers, all exited. This review started no container or compose project.

## END

END_DONE codex-rev-1747: REQUEST CHANGES on PR #1749 security at exact candidate `23feeefee58c5438ccd37fe5c0edc674c5d0a79b`; run 44953630114 success; prior APPROVE HOP superseded.

## Exact origin/main evidence-path witness

First publication commit: `4231fed2b9e3e6a0b4e7dde559cc510c70587255`.

Command: `git fetch origin main && git ls-tree -r --name-only origin/main | grep 'evidence/r28-welle4-2026-11-21/pr1749-review/review-4-security-head23feeefee.md'`

Exact path output:

```text
evidence/r28-welle4-2026-11-21/pr1749-review/review-4-security-head23feeefee.md
```
