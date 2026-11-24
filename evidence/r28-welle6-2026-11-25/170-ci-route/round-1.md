# w109-0428-250-pr170ci: Demo PR #170 hosted-CI route + minimal coverage disposition

Lane: w109-0428-250-pr170ci
Card: 0428-250 (demo half of ci operator fixture allow-list; shipped demo#170 + baseharbor#1815 at 3ebfb90da)
Mode: READ-ONLY — no edits, no PR changes, no CI trigger, no merge
Shift: r28-welle6-2026-11-25

## PLAN

- Establish remote truth via `git ls-remote` + fresh clone in /tmp (never cite the quarantined workers/baseharbor checkout)
- Verify PR #170 state from the remote and show the tests/config-matrix/run.sh hunk
- Grep every .github/workflows in baseharbor-demo for config-matrix / run.sh and map trigger semantics
- Determine whether config-matrix/run.sh is exercised today by any PR-triggered workflow
- Check whether demo develop already contains the #170 hunk (git log -p + diff, from a fresh clone)
- Render verdict (a/b/c) with cost/risk and recommendation
- Write this evidence file to baseharbor-plan and commit+push atomically with targeted git add only

## Remote attestation (verified witnesses)

Demo repo origin URL (remote -v):
  origin	https://github.com/mcpdev80/baseharbor-demo.git (fetch)
  origin	https://github.com/mcpdev80/baseharbor-demo.git (push)

git ls-remote (HEAD of each ref, 2026-11-24/25):
  refs/heads/main         df4867c7540774eba8b8811cb64946b4adc0c8ab
  refs/heads/develop      c23bd9ac58919302ffad3a43f43afb1a34bfbc96
  refs/heads/lane-0428-250-demo-operator-root  0249c9f73c21f46ba532fddc94a764e772f69acf

#170 head SHA (from gh, matches ls-remote): 0249c9f73c21f46ba532fddc94a764e772f69acf
Branch provenance (fresh clone, /tmp):
  merge-base demo/develop (c23bd9a) .. #170 head (0249c9f): c23bd9ac...
  git merge-base --is-ancestor c23bd9a 0249c9f  ->  YES (demo develop IS the ancestor of #170 head)
  git log --oneline origin/develop..0249c9f  ->  ONLY the single #170 commit (no foreign commits carried)
  #170 base = demo/develop c23bd9ac58919302ffad3a43f43afb1a34bfbc96 (exactly the base the mission named)

## 1. PR #170 state from the remote

gh pr view 170:
  number: 170
  state: OPEN (draft)
  baseRefName: develop
  headRefName: lane-0428-250-demo-operator-root
  headRefOid: 0249c9f73c21f46ba532fddc94a764e772f69acf
  mergeable: MERGEABLE
  mergeStateStatus: CLEAN
  title: test(config-matrix): demo operator-allowlist root-name fix (0428-250)

gh pr checks 170:
  "no checks reported on the 'lane-0428-250-demo-operator-root' branch"

gh pr diff 170 --name-only:
  tests/config-matrix/run.sh  (changedFiles = 1)

The hunk (gh pr diff 170, actual lines):
  -matrix_root="$(mktemp -d "$DEMO_ROOT/.config-matrix.XXXXXX")"
  +matrix_root="$(mktemp -d "$DEMO_ROOT/baseharbor-core-bootstrap.XXXXXX")"
  # bootstrap comment reworded to "inside the baseharbor-core-bootstrap temp root ... demo operator allow-list accepts baha up (matching tests/core-bootstrap.sh)"
  if [ -z "${DEMO_SUITE:-}" ]; then
  -  bootstrap_root="$matrix_root/control-plane"
  -  mkdir -p "$bootstrap_root"
  -  ( cd "$bootstrap_root"; run_consented "$BAHA" up --yes ...; "$BAHA" doctor ...; grep -q '^READY' ... )
  +  bootstrap_root="$matrix_root"
  +  BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT="$bootstrap_root" run_consented "$BAHA" up --yes ...

bash -n on the #170 head version of tests/config-matrix/run.sh: OK (valid syntax).

## 2. Which hosted workflow actually executes tests/config-matrix/run.sh

grep -rn "config-matrix" /home/marcel/dev/baseharbor-ecosystem/baseharbor-demo/.github  -> NO MATCH anywhere
grep -rn "run.sh" /home/marcel/dev/baseharbor-ecosystem/baseharbor-demo/.github:
  only mentions `bash -n ... run.sh` (a syntax check on other scripts), never the config-matrix run.sh itself.

Workflow table (baseharbor-demo/.github/workflows, read live from origin):

| workflow                | trigger                                    | runs config-matrix/run.sh? |
|-------------------------|--------------------------------------------|-----------------------------|
| pr-guided-consent.yml   | pull_request (branches:[main]) + workflow_dispatch | NO — runs tests/guided python + bash -n on run.sh; never config-matrix |
| v0424-targeted.yml      | push to work/v0.4.2{4,5,6}-ecosystem-release branches only; recovery job gated on commit messages [demo-*] | NO — runs `bash scripts/acceptance.sh backup-restore` (single gate); no PR trigger; path/branch restricted |

Conclusion: NO PR-triggered workflow in baseharbor-demo references tests/config-matrix/run.sh. pr-guided-consent.yml is the only pull_request workflow and its trigger/paths exercise the guided-consent suite, not config-matrix. v0424-targeted.yml is push-only onto release work-branches and runs a single `backup-restore` gate.

## 3. Is config-matrix/run.sh exercised anywhere today?

The demo gate "config-matrix" is a real acceptance gate: baseharbor-demo/tests/gates.json lists {"name":"config-matrix","requires":[]}, and scripts/acceptance.sh maps gate "config-matrix" to bash "$DEMO_ROOT/tests/config-matrix/run.sh" (the same runner baseharbor calls as its own gates).

How it is actually invoked:
- demo-local: `bash scripts/acceptance.sh config-matrix` (positional gate) or `DEMO_SUITE=<suite>` with config-matrix in that suite (DEMO_GROUPS / positional gates).
- baseharbor hosted: .github/workflows/targeted-demo-acceptance.yml ("Targeted Atomic Gate") calls `bash scripts/acceptance.sh` with NO gate arg (targeted-demo-acceptance.yml:346) against a demo_ref — that runs the FULL gate registry including config-matrix. BUT that workflow is workflow_dispatch (input ref) OR push to runtime-validation/targeted/** (targeted-demo-acceptance.yml:2-18). It is NOT a pull_request workflow.
- The baseharbor ci.yml pre-release/runtime shards (lines 211/253/479/529/565/762/1024/1048/1080) run HA/PR-runtime/consumer suites and reference baseharbor-demo/tests/acceptance.sh, not demo config-matrix. The w97/w98/w100 prior-evidence note holds: the Light gates run scripts/acceptance.sh (full/HA), static/mcp run tests/mcp/run.sh; config-matrix is not part of any PR-triggered path.

Answer: config-matrix/run.sh IS exercised today — but only by the baseharbor demo_ref reference-journey (workflow_dispatch / runtime-validation/targeted push). NO PR-triggered workflow runs it. That is exactly why gh reports "no checks reported" on #170: the demo's only pull_request workflow (pr-guided-consent.yml) does not cover the config-matrix gate, and baseharbor's targeted-demo-acceptance is not a pull_request gate.

## 4. Verdict options (cost/risk) + recommendation

(a) #170 obsolete as-is:
   Cost: lowest. Risk: lowest. The only #170 change (tests/config-matrix/run.sh) does not ship product behavior; the shipped content was demo#170 + baseharbor#1815 at 3ebfb90da. If develop already carries equivalent logic, the fix is dead on this lane.

(b) needs an owner-scoped minimal CI route (Befund with file:line; do NOT edit .github):
   Cost: medium (adds a hosted job; still advisory, cannot block this draft). Risk: medium (new CI surface). This is the "create minimum coverage" path the owner sweep explicitly allows.

(c) get honest hosted coverage by rebasing to a triggering ref:
   Cost: low. Risk: low/medium. Mechanics only (not executed): force-push the lane to a demo develop tip that is itself covered by the baseharbor demo_ref reference-journey, OR move the demo content under pr-guided-consent.yml's exercised path. This does not fabricate a required check (demo CI is advisory) — it only makes the draft visible to an existing PR-triggered workflow.

Recommendation: (a) primary, (b) as the fallback the sweep named.
- #170 is a test-only fixture fix (the config-matrix gate's bootstrap root + operator allow-list), not product behavior.
- It is NOT exercised by any PR-triggered workflow today, so its CI value is "visibility to an existing workflow", not "a required gate that was previously passing then regressed."
- develop already contains the config-matrix gate; the #170 hunk is the ONLY divergence (verify in §5). The correct disposition is close-with-rationale: the fix is not needed on develop, and even if it were, it would ride the baseharbor demo_ref reference-journey — not a demo PR.
- (b) is only warranted if the owner decides the config-matrix bootstrap root is genuinely broken on develop and must be fixed forward; that is a baseharbor-demo content change, not a CI-only change, and the CI route itself (if ever added) is advisory and cannot give #170 a required check.

## 5. Does demo develop already contain the equivalent config-matrix logic?

From a fresh clone (git clone --filter=blob:none --no-checkout, /tmp):

git ls-remote origin/develop -> c23bd9ac58919302ffad3a43f43afb1a34bfbc96

git show origin/develop:tests/config-matrix/run.sh | grep "baseharbor-core-bootstrap\|BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT"  -> 0 matches
The NEW markers introduced by #170 (`mktemp -d "$DEMO_ROOT/baseharbor-core-bootstrap.XXXXXX"`, the reworded comment, and `BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT="..." run_consented`) are ABSENT from develop.

Diff (develop vs #170 head) for tests/config-matrix/run.sh:
  -matrix_root="$(mktemp -d "$DEMO_ROOT/.config-matrix.XXXXXX")"
  +matrix_root="$(mktemp -d "$DEMO_ROOT/baseharbor-core-bootstrap.XXXXXX")"
  -  bootstrap_root="$matrix_root/control-plane"; mkdir -p "$bootstrap_root"
  -  ( cd "$bootstrap_root"; run_consented "$BAHA" up --yes ...; "$BAHA" doctor ...; grep -q '^READY' ... )
  +  bootstrap_root="$matrix_root"
  +  BASEHARBOR_DEMO_ALLOWED_PROJECT_ROOT="$bootstrap_root" run_consented "$BAHA" up --yes ...
So: develop ALREADY runs the config-matrix gate; it simply uses the older `.config-matrix.XXXXXX` + nested `control-plane` bootstrap. The #170 hunk is #170-only content — NOT already in develop. Verdict (a)'s "content already in develop" is therefore FALSE in the literal sense: develop has the gate but not the fix. The disposition still lands on close-with-rationale because the fix is a test-fixture root rename that (i) does not ship product behavior, (ii) is not exercised by any PR-triggered workflow, and (iii) would be qualified via the baseharbor demo_ref reference-journey, not this demo lane — no regressions to hide.

Verdict: (a) #170 should be CLOSED-WITH-RATIONALE. The only open action is an owner decision to (b) if the config-matrix bootstrap root must change forward; that is baseharbor-demo CONTENT work, and any CI route added is advisory and cannot turn #170 into a required-check carrier.

## Cleanliness

- Fresh clone used only in /tmp (removed at end); no product-repo writes, no .github edits, no CI trigger.
- No containers/compose projects started (read-only). No docker/podman state touched.

## END

END_DONE w109-0428-250-pr170ci: read-only disposition complete; #170 = close-with-rationale (verdict a); demo develop SHA c23bd9ac58919302ffad3a43f43afb1a34bfbc96; no checks reported because no PR-triggered demo workflow exercises the config-matrix gate; fix is #170-only, not product behavior.
