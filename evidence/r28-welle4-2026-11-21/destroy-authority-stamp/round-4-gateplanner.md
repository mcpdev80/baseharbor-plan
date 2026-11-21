# Round 4 — Gate Planner `--diff` failure on stacked candidates (0428-214)

Rolle: Worker, DIAGNOSE only. Mission: `/var/tmp/gp.txt` (Karte t-20261121-destroy-authority-stamp, 0428-214).
Gegenstand: der PR-gate-Planner (`scripts/pr-gate-plan.py`) blockiert die gestapelten Kandidaten dieses Fensters.
Keine Produkt-/CI-/Script-Änderung. Kein Push. Kein `go test ./cmd/baha/`.

## PLAN

- [ ] Basis-fact: lane-origin refs + pr-gate-plan.py base-ref vs develop
- [ ] Runner call lokal reproduziert (exit-code + stderr)
- [ ] Hypothesen H1/H2/H3 geprüft
- [ ] Entscheidungsvorlage (ursache/beleg/owner-aktion)
- [ ] Evidence on origin/main verifiziert
- [ ] cleanliness (docker ps -a)

Hinweis: Markdown-Checkboxen sind hier im Evidence erlaubt (nicht in `todos/`); die Board-Datei enthält keine.

## Basis-Fact

Verified remote (first git action):
```
lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch)
lane-origin	https://github.com/mcpdev80/baseharbor.git (push)
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
```
`git -C baseharbor fetch lane-origin refs/heads/lane-0428-198-cli-shard-operator-env refs/heads/lane-0428-214-destroystamp refs/pull/1738/head`

Recorded SHAs:
- lane-0428-198-cli-shard-operator-env (PR #1738 base): `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4`
- lane-0428-214-destroystamp (PR #1738 head): `a25a74c23c237c5f2966ad23f73b66a57848d2a0`
- refs/pull/1738/head: `a25a74c23c237c5f2966ad23f73b66a57848d2a0`
- develop: `40cb28c758b02960356434b630086a341ebe1738`

`pr-gate-plan.py` sha256 comparison (mission step 1):
```
git -C baseharbor show e45430f2f1b7:scripts/pr-gate-plan.py | sha256sum
99de6408ee210693904bffe45fab064d599a7c263085448dfa6c4c47b8fdf015  -
git -C baseharbor show 40cb28c758b0:scripts/pr-gate-plan.py | sha256sum
99de6408ee210693904bffe45fab064d599a7c263085448dfa6c4c47b8fdf015  -
```
Identical. H1 (different planner version on the base ref) is refuted by construction: the planner on the base ref is byte-identical to the develop version, so a missing map entry introduced only in develop cannot be the cause.

## Runner call reproduced

`ci.yml` `PR · Trusted Plan` step (lines 713-830). For a lane base, `target_tip = BASE_SHA`. The `plan` step computes `effective_base` from the integration commit's parents, then runs `git merge-base --is-ancestor effective_base HEAD_SHA` under `set -euo pipefail`.

Exact trace (branch B: 2 parents, INTEGRATION_SHA == HEAD_SHA):
```
+ read -r -a parents <<< "$(git rev-list --parents -n 1 a25a74c23c23...)"
+ echo 'parent count=2'
parent count=2
+ effective_base=e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4
+ git merge-base --is-ancestor e45430f2f1b7... a25a74c23c23...
+ git merge-base --is-ancestor e45430f2f1b7... a25a74c23c23...
<<< set -e fails here: exit 1, no stderr, ~0.2s <<<
```
The command shown in the failing CI log (`python3 "$RUNNER_TEMP/pr-gate-plan.py" --diff`) is the *next* step; the actual abort is the fast `git merge-base` fail-closed just before it. This matches the reported "exit code 1 nach 0.2 s, keine weitere Fehlerzeile".

Root topology (witnessed):
- `c2f9f2f32fd6bd27c0c0b4e269ad02fde6d643b5` = common ancestor of base and head.
- lane-198 tip `e45430f` = `c2f9f2f32 → 80dc49879 → 46017060d → e45430f` (4 commits past the fork).
- PR head `a25a74c` = `c2f9f2f32 → bdc3fcb639... → a25a74c` (2 commits past the fork; first parent `bdc3fcb` != `e45430f`).
- `git merge-base --is-ancestor e45430f a25a74c` => **NO** (they are siblings, not parent/child).
- `git merge-base --is-ancestor origin/develop lane-198-tip` => YES; `origin/develop a25a74c` => YES.

Candidate diff `git diff e45430f2f1b7 a25a74c23c23 --name-only` (9 files, all new):
```
cmd/baha/config_org_test.go
cmd/baha/core_installation_runtime_test.go
cmd/baha/mcp_json_parity_test.go
cmd/baha/mcp_platform_tools_test.go
cmd/baha/mcp_secret_tools_test.go
cmd/baha/provider_external_removal_test.go
cmd/baha/runtime_destroy_impact_test.go
cmd/baha/secure_profile_export_command_test.go
cmd/baha/target_hotfix_test.go
```

## Hypotheses

H1 (base ref carries a planner version expecting a `cmd/baha/operator_..._native_test.go` that exists only in #1743/develop) — REFUTED. `pr-gate-plan.py` is byte-identical on base (`e45430f`) and develop (`40cb28c`); see sha256 above. No develop-only map entry can be the trigger.

H2 (the candidate diff produces a path the planner cannot map, e.g. a `_test.go` with no rule in the coverage catalog) — REFUTED for the failure path. Running the planner against a valid `pr-diff.json` with the 9 paths (context `GITHUB_REPOSITORY=mcpdev80/baseharbor`, `GITHUB_BASE_REF=lane-0428-198-cli-shard-operator-env`, from base-ref copy in `/tmp/0428-214-gateplandiag-run`):
```
"target_base_sha": "e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4"
"selected_gates": []
"broad_required": true
"coverage_status": "unresolved"
"fallback_used": null
```
The planner resolves the 9 new `cmd/baha/*_test.go` files to the conservative `broad_required` Go unit/vet/build fallback and exits 0. `pr-gate-map-v1.json` is read-only (`policy: explicit-path-and-package`; executable mappings live in `pr-gate-plan.py`). The failure is not a coverage-mapping miss.

H3 (`--diff` input is empty/wrong on the stacked PR — `pr_merge` vs branch-diff — so the planner falls to exit 1 instead of "no changes") — PARTIALLY VALID as an independent failure mode, but NOT the observed one. Reproduced the empty-input path in isolation:
```
python3 pr-gate-plan.py --diff <empty>
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0), exit 1
```
This is a genuine fail-closed on a malformed/empty diff, but the CI log aborts at the `git merge-base` guard *before* the planner runs, and the diff (`changed-paths`/`pr-diff.json`) is produced by the runner, not empty. H3 explains a different symptom.

## Decision template

- ursache = PR #1738 head `a25a74c23c23` is NOT a descendant of its base ref `e45430f2f1b7` — it is a sibling branch that diverged at `c2f9f2f32` (base added 3 commits after the fork, head only 2). The planner's fail-closed guard `git merge-base --is-ancestor "$effective_base" "$HEAD_SHA"` in `ci.yml` step `PR · Trusted Plan` (line ~783, `plan` step) aborts the run under `set -e` before `pr-gate-plan.py` runs. Not a planner bug, not a missing coverage entry.
- beleg = `git merge-base --is-ancestor e45430f2f1b7 a25a74c23c23` => NO; parents `git rev-list --parents -n 1 a25a74c23c23` => `a25a74c bdc3fcb639...`; first parent `bdc3fcb63912a7a9be69be7bc10149deef07b5cf` != base `e45430f2f1b7`; identical `pr-gate-plan.py` sha256 on base and develop (99de6408...); planner run on the 9-path diff exits 0 with `broad_required:true, selected_gates:[]`.
- benötigte Owner-Aktion = none in `cmd/baha/` or a planner data file owned by a card. The fix is branch hygiene on the lane: rebase the destroy-stamp candidate so its first parent is the current lane-198 tip `e45430f` (i.e. make `a25a74c` a real descendant of the base, not a sibling). This is a git-lane operation, not a code change. If the intent is to keep both lanes, the stacked candidate must be cut from the live lane-198 tip. No `.github/**`, `scripts/**`, or `cmd/baha/` edit is required for the planner to succeed — only a correct stacked base.

Scope note: the failing guard lives in `ci.yml` (Owner scope) and the planner/data files are Owner scope. No change was made to any of them (this was a read-only diagnosis). If the guard itself is considered too strict for legitimately stacked lanes, that is a policy decision for the Owner; the finding is that the current candidate is simply not a descendant of its declared base.

## Cleanliness

No containers, images, networks or compose projects were created. Host was not touched.
`docker ps -a` before (pid 2986175):
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
`docker ps -a` after:
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
cleanliness: clean. Scratch zone `/tmp/0428-214-gateplandiag*` only (outside the ecosystem root). No git branch cut, no push.

## Repo-rule compliance

- Read-only diagnosis; no change to `scripts/**`, `.github/**`, `cmd/baha/`, or any product file.
- No push, no branch cut, no workflow dispatch/rerun.
- No `go test ./cmd/baha/`.
- Verified remote `lane-origin` = github.com/mcpdev80/baseharbor before any git read.
- No subagents (4.8). Evidence written only in baseharbor-plan.
- `todos/` board file `0428-214-gateplandiag.json` created and ticked.
