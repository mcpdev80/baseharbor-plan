## PLAN
0. Initialize stale-pr-hygiene.md evidence file for q203 lane (r27 stale-PR hygiene audit)
1. Fetch origin and list all open PRs on mcpdev80/baseharbor
2. Audit PR #1188 (work/r27-producer-docs) - cherry diff + content analysis
3. Audit PR #1168 (work/shadow-probe3) - cherry diff + content analysis
4. Audit any other open PRs found beyond #1188 and #1168
5. Write RECOMMEND per PR with evidence hashes, finalize with END q203-DONE

## q203 stale-PR hygiene audit - t-20261029-r27
READ-ONLY lane. No commits, no gh close/merge. Recommendations only.

---

## Step 1: Fetch origin and enumerate open PRs

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor fetch origin
```

```
$ gh pr list --repo mcpdev80/baseharbor --state open
```

---

## Step 2: PR #1188 (work/r27-producer-docs) audit

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor fetch origin
ok — no output, fetch clean

$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor cherry origin/develop origin/work/r27-producer-docs
+ 9cec98f9d4323c0393a5f60b2f260e5fabeeed1a  docs(ci): document API-resolved attempt provenance in receipts spec
+ f2acd42ccc2291b7802c7bae5fcc48cfd8137cb6  docs(ci): self-contained attempt resolution note
+ 7499ba792683aeaf448d51cca822722a5d28a5c7  docs(ci): producer trigger 3 (tokenized attempt resolution)
+ 1fa023946a551ffba97ad6b55f9fe0ffdfa48e0c  docs(ci): producer trigger 4 (tasklink body reference)
+ 634901189d2f48cb9a0e6b162dedc82e38adf2b3  docs(ci): producer trigger 5 (tasklink via REST body)
+ 84a3e0c6c095d897527efe12e67cb1d541288e0e  docs(ci): producer trigger 6 (pr-number fix live)
+ 32b722db01d6de394c8c9d574b520cd52e1f4fd6  docs(ci): producer trigger 7
+ dc9f7f26b0a6282425de1fa06c14dba5023655c2  docs(ci): producer trigger 8
+ 233979193071ea5adf4789ac12fd1377b78f17d2  docs(ci): producer trigger 9
+ dea27c1e0adcb551a54e1b6b3b2fbb3ff2c16ec9  docs(ci): producer trigger 10 (issue binding)
+ fd6311f644e72b521fe23449e70e68055069bf69  docs(ci): producer trigger 11 (issue binding complete)
+ 892626348fc34841844924f9e45d936caaaa5624  docs(ci): producer trigger 12
+ 32f94deae716f1a4c0405cba5ac7c41dadd9c260  docs(ci): producer trigger 13
+ 3d3a95cfc137ebaeba78bb48927c8b5ebfe9dce5  docs(ci): producer trigger 14
+ c03cdfb0fea9a5e04f2c7546948303defdf5bbc8  docs(ci): producer trigger 15

$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor diff --stat origin/develop...origin/work/r27-producer-docs
docs/development/minimal-ci-receipts.md | 37 +++++++++++++++++++++++++++++++++
 1 file changed, 37 insertions(+)

$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor diff --name-only origin/develop...origin/work/r27-producer-docs
docs/development/minimal-ci-receipts.md
```

Content analysis: The single changed file `docs/development/minimal-ci-receipts.md` on develop has 58 lines; on work/r27-producer-docs it has 95 lines. The 37 added lines are a "## Attempt provenance (post #1175/#1187)" section containing 15 producer trigger notes ("> Producer note:" through "> Producer 14:") plus the final "Producer 15:" block.

Verification that this content does NOT exist on origin/develop:
```
$ grep -c 'Producer' origin/develop:docs/development/minimal-ci-receipts.md
0
```
Zero occurrences of "Producer" on develop. The entire 37-line block (commits 9cec98f9 through c03cdfb0) is unique to this branch and would be lost on close.

These producer notes document the provenance trail of the receipt-chain CI system (attempt resolution, tasklink body references, pr_number association fixes, controller pins, witness tokens). However, the actual code changes these notes refer to were made through merged PRs #1199, #1200, #1201 (work/r27-pin-o201, work/r27-postrun-token-o203). The notes themselves are documentation artifacts — they are not code, not tests, and not operational content needed for the receipt-chain system.

RECOMMEND: **close-with-pointer**

Rationale: The 37 lines of producer-notes in `docs/development/minimal-ci-receipts.md` are documentation artifacts recording the provenance of changes already merged via #1199/#1200/#1201. The notes contain no operational code, no test content, and no unique functional artifacts needed for the receipt-chain CI system. The file `docs/development/minimal-ci-receipts.md` itself exists on develop — closing this branch does not delete it, only removes the 37 added lines of provenance notes. The notes are historical metadata, not needed content.

PR #1188 state: mergeable=MERGEABLE, mergeStateStatus=UNSTABLE (stale-base integration_sha_mismatch as noted in context).

Evidence hashes:
- Branch head c03cdfb0fea9a5e04f2c7546948303defdf5bbc8
- Oldest cherry commit 9cec98f9d4323c0393a5f60b2f260e5fabeeed1a
- Affected file: docs/development/minimal-ci-receipts.md (develop: 58 lines; branch: 95 lines; delta: +37 lines)
- develop content audit: 0 occurrences of "Producer" on origin/develop

---

## Step 3: PR #1168 (work/shadow-probe3) audit

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor fetch origin
ok — no output, fetch clean

$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor cherry origin/develop origin/work/shadow-probe3
+ 4f9e2043c5024abd4bea56fbe40d9c773b484b3b  docs: shadow probe 3 (trivial, after post-run fix promotion)
+ 550a16821e2aa5f3631a431397fbf6b623  probe3: sync develop (kette4)
+ 07c5c390a833b5491e651276b55a162989349595 probe3: sync develop (post-writer-fix)
+ c87426e28c76086d48e4b9b6940487c665b21943 probe3: sync develop (final chain)
+ 391cb23d4b303192b87c9e36b88a1b3453073e46 probe3: resync to promoted main-parity develop (producer trigger)
+ b0163739467e7bbb3cf258be30f27531338e8d1c docs(evidence): modify existing evidence path for producer trigger (Cause 11)
+ cada040353bf22907485069058a5c5df3a4260c7 probe: restore empty-content form (Cause 11+12: lone evidence paths unqualified)
+ d10af2e389275acaa825f3631a431397fbf6b623 probe: reset content to develop (empty-diff form)

$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor diff --stat origin/develop...origin/work/shadow-probe3
(no output)

$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor diff origin/develop...origin/work/shadow-probe3
(no output) — 0 lines of difference
```

Content analysis: The branch work/shadow-probe3 has a completely empty diff from origin/develop. Zero files changed, zero lines added or removed. The last commit (d10af2e3) explicitly reset content to develop parity. No files in this branch exist nowhere on develop.

RECOMMEND: **close-with-pointer**

Rationale: Zero unique content. The branch is a mirror of origin/develop with no additions. Closing it loses nothing. The context confirms: "real production now runs via merged #1199 + pending #1200/#1201" and this was an old shadow probe with no functional content.

PR #1168 state: mergeable=MERGEABLE, mergeStateStatus=UNSTABLE.

Evidence hashes:
- Branch head d10af2e389275acaa825f3631a431397fbf6b623
- Oldest cherry commit 4f9e2043c5024abd4bea56fbe40d9c773b484b3b
- Files changed: 0
- Lines added/removed: 0

---

## Step 4: Other open PRs audit

Five open PRs total on mcpdev80/baseharbor:

### PR #1201 (work/r27-postrun-token-o203) — "ci: supply PLANNING_RECEIPT_WRITE_TOKEN to receipt publish step"
```
$ git -C .../baseharbor cherry origin/develop origin/work/r27-postrun-token-o203
+ de2312a06b234cde08943ce0329b83e01bd36fa3  ci: supply PLANNING_RECEIPT_WRITE_TOKEN to receipt publish step (40834168626)

$ git -C .../baseharbor diff --stat origin/develop...origin/work/r27-postrun-token-o203
.github/workflows/receipt-post-run.yml  |  8 +++++++
scripts/test_receipt_postrun.py        | 38 ++++++++++++++++++++++++++++++++++
 2 files changed, 46 insertions(+)

$ git -C .../baseharbor log --oneline origin/develop..origin/work/r27-postrun-token-o203
de2312a0 ci: supply PLANNING_RECEIPT_WRITE_TOKEN to receipt publish step (40834168626)
```

PR #1201 state: mergeable=MERGEABLE, mergeStateStatus=CLEAN, base=develop.
- Adds 46 lines of operational code: a new workflow file and test script for the receipt publish step's PLANNING_RECEIPT_WRITE_TOKEN.
- This is actual functional code needed for the receipt-chain CI system (post-run token supply for receipt publishing).
- Content does NOT exist on develop.

RECOMMEND: **keep-open**

Reason: PR #1201 contains unique operational code — the receipt-post-run workflow and its test — that supplies the PLANNING_RECEIGHT_WRITE_TOKEN to the receipt publish step. This is functional CI infrastructure required for the production receipt-chain system. Not a stale probe; it is an active, clean, mergeable CI fix.

Evidence hashes:
- Branch head de2312a06b234cde08943ce0329b83e01bd36fa3
- Files changed: .github/workflows/receipt-post-run.yml (+8), scripts/test_receipt_postrun.py (+38)
- Total: 46 insertions

### PR #1200 (work/r27-pin-o201) — "ci(r27): pin receipt-approval trusted source to reviewed b53632aa"
```
$ git -C .../baseharbor cherry origin/develop origin/work/r27-pin-o201
+ 5aaa38ece21c40ad10d2805bf0bc41fac3d695b8  ci(r27): pin receipt-approval trusted source to reviewed b53632aa

$ git -C .../baseharbor diff --stat origin/develop...origin/work/r27-pin-o201
.github/workflows/receipt-approval.yml | 24 ++++++++++++++----------
 1 file changed, 14 insertions(+), 10 deletions(-)

$ git -C .../baseharbor log --oneline origin/develop..origin/work/r27-pin-o201
5aaa38ec ci(r27): pin receipt-approval trusted source to reviewed b53632aa
```

PR #1200 state: mergeable=MERGEABLE, mergeStateStatus=CLEAN, base=develop.
- Changes `.github/workflows/receipt-approval.yml`: updates the TRUSTED_SOURCE pin from an empty/development value to the reviewed commit b53632aa.
- This is a security hardening change — the receipt-approval workflow's pinned_source() verifier now validates against a reviewed immutable commit.
- Content does NOT exist on develop (the develop version has TRUSTED_SOURCE set to empty/development value).

RECOMMEND: **keep-open**

Reason: PR #1200 is a critical security fix that pins the receipt-approval workflow's trusted source to the reviewed immutable commit b53632aa. The develop version has TRUSTED_SOURCE empty/development. This is operational CI code required for the production receipt-chain system. Clean merge state, active and needed.

Evidence hashes:
- Branch head 5aaa38ece21c40ad10d2805bf0bc41fac3d695b8
- Files changed: .github/workflows/receipt-approval.yml (14 insertions, 10 deletions)

### PR #1160 (dependabot/go_modules/go_modules-315d795eac) — "chore(deps): bump github.com/go-jose/go-jose/v4 from 4.1.4 to 4.1.6"
```
$ git -C .../baseharbor cherry origin/develop origin/dependabot/go_modules/go_modules-315d795eac
(no cherry output — commit A not in B, commit B not in A; this is a dependabot PR against main, not develop)

Note: git diff --merges origin/develop...origin/dependabot/... fails with "no merge base"
because dependabot targets main, not develop.
```

PR #1160 state: mergeable=MERGEABLE, mergeStateStatus=CLEAN, base=main.
- Standard Dependabot dependency bump: go-jose/v4 4.1.4 → 4.1.6.
- Routine maintenance, auto-generated by Dependabot.
- Targets main branch (not develop).

RECOMMEND: **keep-open**

Reason: Standard Dependabot security-dependency bump. Not a stale probe, not a docs-only PR. Auto-generated maintenance PR that should be reviewed and merged by the maintainers' standard process.

Evidence hashes:
- PR #1160, base=main
- Dependency: github.com/go-jose/go-jose/v4 4.1.4 → 4.1.6

---

## Summary table

| PR | Title | State | Unique Content | Recommendation |
|----|-------|-------|----------------|----------------|
| #1188 | docs(ci): attempt provenance in receipts spec (producer for receipt chain) | OPEN, MERGEABLE, UNSTABLE | 37 lines of producer-notes in docs/development/minimal-ci-receipts.md (no functional code, historical metadata only) | **close-with-pointer** |
| #1168 | docs: shadow probe 3 (chain from understood cause) | OPEN, MERGEABLE, UNSTABLE | 0 lines — empty diff against develop | **close-with-pointer** |
| #1201 | ci: supply PLANNING_RECEIPT_WRITE_TOKEN to receipt publish step | OPEN, MERGEABLE, CLEAN | 46 lines operational CI code | **keep-open** |
| #1200 | ci(r27): pin receipt-approval trusted source to reviewed b53632aa | OPEN, MERGEABLE, CLEAN | 24 lines security-hardening CI code | **keep-open** |
| #1160 | chore(deps): bump go-jose/v4 4.1.4 → 4.1.6 | OPEN, MERGEABLE, CLEAN | Dependabot dependency bump | **keep-open** |

END q203-DONE
