# r27 diagnosis — tasklink "evidence published even when absent from remote main"

Task: t-20261022-r27-evidence-publisher. Lane: o231 (DIAGNOSE, no product write).
Candidate under claim: `c845caf6` (baseharbor, "ci(receipt): publish evidence as valid YAML list element (BF-W3-2)").
Reviewer: o231 independent Codex session. Date: 2026-10-29.

## (1) Befund: WAHR

The claim is TRUE. Commit `c845caf6` removed the durable remote read-back (F5) and
replaced it with a **local-only** read-back that reads the just-committed local HEAD.
`publish_evidence` now returns success and a publication SHA even when the edit was
never durably published to the remote.

### Root cause in the code

`baseharbor/scripts/receipt_tasklink.py`, `publish_evidence()` (current HEAD / c845caf6):

```python
publication = _git_fn(planning_root, "rev-parse", "HEAD").decode().strip()
require(sha40(publication), "durable publication is not a full SHA")

# Read back the durable task note from the publication revision ...
durable_text = _git_fn(planning_root, "show", f"{publication}:{task}").decode(errors="replace")
require(evidence_line.strip() in [l.strip() for l in durable_text.splitlines()],
        "evidence reference not present in the durable publication revision")
```

`_git_fn` defaults to `_git`, which runs `git -C <planning_root> ...`. The read-back
`git show {local_HEAD}:{task}` reads the **local** commit, never the remote. The
predecessor `c845caf6~1` (`b53632aa`) still contained the F5 guards:

```
_git_fetch_remote_head(planning_root, "origin", "main")   # remote fetch
require(remote_head == local_commit, "remote HEAD does not match ... — publication was not durably pushed")
durable_text = _git_fn(planning_root, "show", f"origin/main:{task}")  # remote read-back
```

`c845caf6` dropped `_git_fetch_remote_head`, the `require(remote_head == local_commit)`
check, the `git push origin ...` line, the `sha40` validation of `candidate_sha`/`plan_revision`
inputs, and `_front_matter_has_mapping_keys` — all F5 durable-publication / fail-closed
mechanisms. The commit message still *asserts* "not a local-only commit that was never
pushed", but the code no longer enforces that.

### Reproduction evidence (local bare remote, local reproduction)

Working dir: `/tmp/r27-diag/` (scratch; never pushed, no product write).

Setup: bare remote `remote/planning.git` with `main` at `9fd9515e4197d96aedf0e8452993159b23316fb2`.

**Scenario A** — `publish_evidence` with real `git` against the bare remote (no explicit
push beyond setup):

```
returned publication: 09f359f9b845517162f0e8e1b704292f951a09bb
remote HEAD AFTER publish: 9fd9515e4197d96aedf0e8452993159b23316fb2   (UNCHANGED)
remote file after: '---\ntitle: r27 evidence pilot\n---\n\nBody.\n'   (NO evidence line)
```

The function returned a publication SHA, but the remote `main` was **not** advanced and
the remote task note does **not** contain the evidence line — yet no error was raised.

**Scenario B** — same, but a `_git_fn` that never reaches the remote (a `push` would raise)
and a local commit:

```
publish_evidence returned SUCCESS (no error): 5cf71ff2a5d7ab108ac0ef84b7b7deb517b365d6
remote HEAD still: 9fd9515e4197d96aedf0e8452993159b23316fb2  (was 9fd9515... before) -> UNCHANGED
remote contains evidence? False
```

The publication report is success while the remote never received the edit. **Claim reproduced.**

**Test-mask demonstration** — simulate the readback assert being neutralised (the read-back
SHA is faked and the remote never receives the edit):

```
RESULT: publish_evidence SUCCEEDED, returned 441a24d1d3bf9e244e639bb57021d863f79fd906
>>> The readback assert did NOT catch missing evidence -> false 'published' claim
```

Under the old F5 code, a missing remote edit raised `TaskLinkError`
("remote HEAD does not match local commit — publication was not durably pushed"). Under
`c845caf6` it silently succeeds.

## (2) Minimales Rezept (for the o230 lane or a follow-up patch)

File: `baseharbor/scripts/receipt_tasklink.py`, function `publish_evidence`.

1. **Restore the push + remote read-back** (revert the F5 removal in `c845caf6`):
   - re-add `_git_fetch_remote_head(root, "origin", "main")` (or equivalent remote fetch).
   - `_git_fn(planning_root, "push", "origin", f"{local_commit}:refs/heads/main")` before read-back.
   - `require(remote_head == local_commit, "remote HEAD does not match local commit — publication was not durably pushed")`.
   - read-back from the remote: `durable_text = _git_fn(planning_root, "show", f"origin/main:{task}")`.
   - re-validate input SHAs at the top: `require(sha40(candidate_sha))`, `require(sha40(plan_revision))`.
2. **Fix the idempotency short-circuit** introduced by `c845caf6` — the expression
   `any(strip == "- evidence:" for strip in [evidence_line.split(" evidence:")[0] + " evidence:"])`
   is dead/buggy (`- evidence:` is never the canonical line) and should be removed; the
   additive `if not any(e.strip() == evidence_line.strip() for e in front_lines)` already guards dedup.
3. **Test requirement**: add a test that stands up a local **bare** remote, points the
   injected `_git_fn` at it, and asserts `publish_evidence` raises `TaskLinkError` when the
   push is rejected / the remote never receives the edit (fail-closed). This must fail on
   `c845caf6` and pass after the fix. Keep the existing YAML-list-element tests intact.
4. Note: `file://` remotes are classified by the Writer (`_is_real_remote`) as **non-network**;
   if that classification is what masks the bug in CI, the fix must not rely on a network
   push alone — the local commit must equal the remote HEAD after an explicit push to the
   bare remote used by the test, verified by `git show origin/main:{task}`.

## (3) Bezug zur GITHUB_AUTHORITY / r27 publication rule

r27 task note `baseharbor-plan/tasks/t-20261022-r27-evidence-publisher.md` line ~84 (authoritative
Planning contract):

> Publish the plan commit and receipt together through the existing ordinary fast-forward
> publication path. **Before reporting success, prove the referenced plan commit is reachable
> in the durable Planning history; no local-only commit counts.**

`c845caf6` produces exactly the forbidden artifact: a report of durable publication backed
by a **local-only** commit that is never proven reachable on the remote. This violates the
"no local-only commit counts" rule and the F5 fail-closed intent. The durable-publication
requirement is the "no durable publication claim" guarantee: a returned publication revision
must be verified against the remote, not the local ref that was just committed.

---

PLAN (numbered, no checkboxes):
0. Read o231 prompt and confirm scope (diagnose, no product write). DONE.
1. Pull remote/candidate state (git log, c845caf6 stat). DONE.
2. Diff c845caf6 to identify the F5 removal. DONE.
3. Build local bare remote, reproduce Scenario A/B. DONE.
4. Mask readback assert in a local test. DONE.
5. Write diagnosis evidence to this file. DONE.

o231-DONE
