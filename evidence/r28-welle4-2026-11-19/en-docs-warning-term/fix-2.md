# fix-2 — 0428-131 EN marker term 'Warning' (take-over + exact-head CI on new base + docs-audit mapping hole)

- Task: t-20261119-r28-en-docs-warning-term (0428-131), PR mcpdev80/baseharbor#1697
- Session: 93521518 (codeman id 93521518-675e-4e06-b6c9-1c5189388eba, ornith / worker-ornith1.5 via AgentGateway)
- Handover: previous owner w131-0428-131-endocshowpf (codeman bbd9132d) no longer present (0 hits in `agent list`); PR #1697 open, no lane. Taken over on a fresh session — documented take-over, second run avoided. New PR head = `708f5c5c8acee5133e480d151544cb139bb3ded3` (fresh commit on current develop HEAD; old head `3448f73e` is NOT an ancestor).

## PLAN

- Read mission and card; verify planning repo origin/main and product remote witnesses before any write.
- Claim t-20261119-r28-en-docs-warning-term via scripts/plan.py (card already active under the documented take-over owner; claim is idempotent).
- Compute base-abstands-diff git diff --name-only da76c5cf9 origin/develop; write CI-touched lines literally into the akte.
- Run local documentation-audit against the three changed files; record result + test-id.
- Locate the pr-gate-plan.py DOC_CHECKS branch that misses docs/internal/*.json; record file:line as the Owner-draht-punkt (a); make NO change to scripts/** or .github/**.
- Perform the monotone merge-hopf: cherry-pick the previous owner's single commit onto current develop HEAD; verify develop HEAD is an ancestor and old head is NOT; merge-tree = 0 conflicts.
- Run one exact-head run to terminal; read cells literally.
- Write evidence to baseharbor-plan; commit to planning origin/main; update card.
- Set card to blocked with reason 'CI-pfad-mapping Loch, Owner-draht (a)'.

## Reality witnesses (measured, fresh fetch)

- Planning origin/main last 5:
  - 070ccc3b coord: 0428-131 lane angesetzt (hopf + exakter lauf, docs-only)
  - 6855ace8 kanban: t-20261119-r28-en-docs-warning-term -> active
  - 1cb0dc8a coord: 0428-089 inhaber bleibt b60c11a1, geplante korrektur-lane zurueckgezogen
  - d4e5381b kanban: t-20261114-r28-perses-secure-access -> active
  - 9c0c29e7 coord: 0428-131 review-zuordnung (read-only, exakter head) + blocker erneuert

- Product remote (origin/develop fetched in /var/tmp/baha-131-wt):
  - develop HEAD = 1019190d8dc0ecac7693f3461153e76be0e2cb8a (matches mission witness)
  - old PR head 3448f73e697cd7fdb1a338ef8422b5d484bbe814 on base da76c5cf9 (divergent)
  - new PR head = 708f5c5c8acee5133e480d151544cb139bb3ded3 on base 1019190d (monotone hopf)
  - PR #1697: baseRefName=develop, isDraft=false, state=OPEN, headRefName=lane-0428-131-en-docs-warning-term
  - PR author id 22537373 == repo owner id 22537373 (PR · Exact Candidate condition satisfied)

## Base-abstands-diff (why the old run is no longer evidence)

- diff command: git diff --name-only da76c5cf9 origin/develop
- CI-touched files in the diff:
  - .github/workflows/ci.yml
  - .github/workflows/docker-runtime-acceptance.yml
  - .github/workflows/podman-acceptance.yml
  - (plus targeted-demo-acceptance.yml, and many cmd/baha, contracts, docs, internal/* changes)
- merge-base(da76c5cf9, origin/develop) = da76c5cf9c963207038d5599bd130b89ecb1e8a4; da76c5cf9 IS an ancestor of develop HEAD but NOT equal (develop moved past it).
- Conclusion: the old run 44478483899 on the old base da76c5cf9 is no longer admissible evidence (base-abstand rule). The old head 3448f73e sits on a different base than the current develop HEAD 1019190d.

## Content (carried by the hopf)

- Three EN internal-doc JSON strings changed 'Achtung' -> 'Warning' (i18n drift after 0428-126).
- German docs intentionally keep 'Achtung' and are unchanged.
- Files (exactly these 3 in the diff):
  - docs/internal/v0.4.25-destruction-workspace-checkpoint.json
  - docs/internal/v0.4.25-external-provider-delivery-source-evidence.json
  - docs/internal/v0.4.25-installation-destruction-runtime-evidence.json
- Hopf invariants:
  - merge-base --is-ancestor origin/develop <new head> = 0 (YES, monotone on current base)
  - merge-base --is-ancestor 3448f73e <new head> = nonzero (old head NOT an ancestor — fresh commit)
  - git merge-tree --write-tree origin/develop <new head> = 0 conflicts (tree 861191a1050d829258126a805cc86da5b480a603)
  - git log origin/develop..<new head> = exactly one commit: 708f5c5c docs: use the shipped EN marker term 'Warning' in EN internal docs (0428-131)

## documentation-audit local run

- Command: bash scripts/documentation-audit.sh (repo path present; test-id: 'documentation-audit')
- Result: PASS — "EN/DE page coverage OK: 167 matched Markdown pages", "German technical integrity: PASS (167 paired pages)", Structure/Human-doc/Internal evidence/ADR/Governance/Runtime/Podman release/Brand all PASS.
- Note: local audit audits the whole repo tree (HEAD of /var/tmp/baha-131-wt = origin/develop, which already reads 'Warning' in these files). It does NOT by itself select the docs-audit CI check for a PR whose changed paths are docs/internal/*.json — that selection is the mapping question below.

## The mapping hole (Owner draht-punkt (a)) — finding, no change made

- scripts/pr-gate-plan.py maps public Markdown/RST/root-docs onto DOC_CHECKS, but docs/internal/*.JSON does NOT run through that branch and falls out unresolved.
- Exact location: scripts/pr-gate-plan.py line 1189:
  ```
  elif (path.startswith('docs/') and path.endswith(('.md', '.rst')) or
          path in ('README.md', 'CONTRIBUTING.md', 'CHANGELOG.md',
                   'mkdocs.yml', 'mkdocs.de.yml') or
          path.startswith('site/')):
      area = 'documentation'
      require(DOC_CHECKS)
  ```
  The condition matches only `docs/*.md` and `docs/*.rst`. The three changed files end with `.json` (not `.md`/`.rst`), are NOT in REGISTRATION_REFERENCE_FILES (only *.md refs), are NOT the contracts/machine/v1/control.golden.json special-case allowlist, and are NOT docs/releases/*.json consumer-pins paths. So they fall through the entire branch chain to the `unknown impact ... unresolved` classifier.
- Verified with the planner against the 3 changed paths: coverage_status = 'unresolved', broad_required = true, every path reports 'unknown impact for docs/internal/...json'. documentation-audit is never in required_validation_checks.
- The current plan's conservative broad fallback does NOT include documentation-audit.
- This is Owner scope (scripts/** + .github/**). No change was made. Reported to Owner for implementation.

## CI exact-head run (run 44559589447, terminal)

- Trigger: force-push of new head 708f5c5c to lane-0428-131-en-docs-warning-term (fast-forward from GitHub's perspective — new commit on a newer base; not a history rewrite; old head 3448f73e is not carried on top). ls-remote witness:
  - 708f5c5c8acee5133e480d151544cb139bb3ded3  refs/heads/lane-0428-131-en-docs-warning-term
- Run id: 44559589447 — CI · PR #1697 — CI · Source & Quality — pull_request — head_branch lane-0428-131-en-docs-warning-term — head_sha 708f5c5c — base_ref develop — status completed — conclusion success — started 2026-11-19T15:51:54Z
- Terminal aggregate job: PR Selected Checks (job id 135688040533) — status completed, conclusion success. Log line: "PR Selected Checks: PASS" (2026-11-19T15:56:44Z).
- pr-required-final.py inputs verified in the run:
  - EVENT_BASE = 1019190d8dc0ecac7693f3461153e76be0e2cb8a
  - PLAN_BASE = 1019190d8dc0ecac7693f3461153e76be0e2cb8a
  - CONTROLLER_SHA = 1019190d8dc0ecac7693f3461153e76be0e2cb8a
  - EXPECTED_HEAD = 708f5c5c8acee5133e480d151544cb139bb3ded3
  - expected integration parents validated; develop HEAD is an ancestor of the head (monotone hopf proven in-run)
- CI NEEDS map (from the run's CI_NEEDS env):
  - workflow_policy: success, source_format: success, pr_plan: success, pr_focused: success, pr_validations: success, pr_native_impact: success (required=false, matrix=[]), pr_unit_shards: success
  - pr_candidate: skipped, pr_consumer_pins: skipped, pr_demo_pin: skipped, pr_runner_interface: skipped, pr_runtime_selected: skipped, pr_selected_integration: skipped, pr_public_contracts: skipped, pr_owner_node_native: skipped, pr_native_selected: skipped
  - runtime_required=false, integration_required=false, candidate_advisory_required=false, owner_node_required=false, public_contracts_required=false, unit_scope=full
  - **documentation-audit is NOT present in CI_NEEDS** — the validation check was never selected for the three docs/internal/*.json paths on this exact head.
- Per the mission: 'documentation-audit' on this exact head = not selected (skipped / absent). This is NOT counted as green. Recorded as: 'documentation-audit nicht ausgewaehlt — verweis auf 114-draht-punkt (a)'.
- Success proof: the run's PR Selected Checks aggregate is SUCCESS on the exact new head 708f5c5c with actually executed required jobs (workflow_policy, source_format, pr_plan, pr_focused, pr_validations, pr_native_impact, pr_unit_shards all executed and passed; native/runtime/integration gates correctly skipped because runtime_required/integration_required=false for a docs-only change). SKIPPED != pass for the docs-audit cell, which is separately reported as not-selected.
- No new run needed on a newer base (only base moved; no .github/workflows/ci.yml / planner / scripts/test_pr_*|test_ci_* change in THIS head; acceptance does not demand a newer base than 1019190d).

## repo-rule compliance

- No edit to .github/** or scripts/** (Owner scope). Confirmed: the only product change is the 3 docs/internal/*.json strings carried by the hopf.
- No merge performed by this session (CODEX-MERGE only, after full acceptance).
- No subagents (§4.8). Every step run inside session 93521518.
- Evidence written only to baseharbor-plan (planning repo), never to a product repo.
- One integration candidate (PR #1697), single-commit hopf preserved.
- Branch provenance: base = 1019190d8dc0ecac7693f3461153e76be0e2cb8a (develop HEAD); 1019190d is an ancestor of the first hopf commit 708f5c5c; old head 3448f73e is not carried on top.
- Host besenrein: no containers/compose started by this session (pre-existing ambient bh-local-shared-* containers untouched).

## END

- status: END_DONE — take-over complete; monotone hopf onto current develop HEAD (708f5c5c); exact-head CI run 44559589447 TERMINAL SUCCESS (PR Selected Checks: PASS); docs-audit mapping hole documented as Owner finding (a) with file:line; card set to blocked (docs-audit not selected on this head — a skipped/absent check is not acceptance). No merge. No new run on a newer base (only base moved; no ci.yml/planner/test_pr_*|test_ci_* change).

## cleanliness:
- before (docker): 4 containers (all bh-local-shared-* ambient, started by other work), 64 volumes, 5 networks; (podman): 0 containers/volumes/networks.
- after: identical — 0 containers/volumes/networks started by this session; ambient bh-local-shared-* containers untouched; no compose projects started.
- cleanliness: before == after. No test containers, networks, volumes, or state directories created.
