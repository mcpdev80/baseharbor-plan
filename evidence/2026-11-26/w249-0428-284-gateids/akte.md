# w249-0428-284-gateids — Read-only 14-gate id pre-flight audit

**Card:** 0428-284 (release-ops support — 14-gate id pre-flight)
**Mission:** READ-ONLY. No writes, no pushes, no CI triggers, no workflow_dispatch.
**Base witness (ls-remote):** `origin/develop` HEAD = `ae70964d7b80b779822b76107b70ea76782f998e`
**Base checkout HEAD (depth-1 clone):** `cddc81b34fe13d8befdde4c487b365a0309ba428` (fetched origin/develop at task start)
**Planning remote (verified github.com/mcpdev80):** `origin https://github.com/mcpdev80/baseharbor-plan.git`

## PLAN
- Gather witnesses: ls-remote current origin/develop HEAD; confirm planning remote
- Gate 1: scripts/release-requirements.json — list every gate id, verify 14 required IDs
- Gate 2: pre-release.yml — quote file:line ref/tag/demo_ref/only_gates consumption + unknown-id behavior
- Gate 3: resolve demo ref at fire time from develop docs/releases/v0.4.28.demo-ref; state #1842 implication
- Gate 4: cross-check gate->job mapping (each of 14 ids → runnable job)
- Write akte via baseharbor-plan PR branch path with git show witness
- Verify evidence on origin/main via ls-tree, then post END_DONE witness

## Read-only 14-gate pre-flight audit

### Witness: base
- origin/develop HEAD (ls-remote): `ae70964d7b80b779822b76107b70ea76782f998e`
- Clone HEAD (fresh depth-1 of origin/develop): `cddc81b34fe13d8befdde4c487b365a0309ba428`

### Gate 1 — scripts/release-requirements.json gate ids
`gates` is a **list** of `{id, schema, jobs[], required_for[], dependencies[]}`. Every gate id found on develop (cddc81b):

```
atomic/static/config-matrix, atomic/static/init, atomic/static/mcp, atomic/static/agent, atomic/static/shell-ux
atomic/docker/guided, atomic/docker/lifecycle, atomic/docker/policy, atomic/docker/connectivity,
atomic/docker/reconciliation, atomic/docker/failure, atomic/docker/full-destroy,
atomic/docker/data-capabilities, atomic/docker/observability, atomic/docker/identity, atomic/docker/security,
atomic/docker/backup-restore, atomic/docker/rabbitmq-runtime, atomic/docker/mongodb-runtime,
atomic/docker/durable-key-value, atomic/docker/control-plane-recovery, atomic/docker/loki-runtime, atomic/docker/tempo-runtime
atomic/podman/{same 7 as docker above + data-capabilities, observability, identity, security, backup-restore,
rabbitmq-runtime, mongodb-runtime, durable-key-value, control-plane-recovery, loki-runtime, tempo-runtime}
adoption/{conformance, realworld-compose, realworld-quadlet, realworld-kubernetes}
ha/docker/{data, identity, observability, routing}
ha/podman/{data, identity, observability, routing}
journey/{docker, podman}
integration/static/{public-contracts, configuration-policy, browser-terminal}
integration/{docker,podman}/remote-target, integration/static/live-console
integration/{docker,podman}/core-bootstrap, integration/{docker,podman}/coreless-lifecycle
```

**The 14 required IDs — EXACT match check (PASS):**
- `atomic/docker/{guided,lifecycle,policy,connectivity,reconciliation,failure,full-destroy}` (7) → **all present**
- `atomic/podman/{guided,lifecycle,policy,connectivity,reconciliation,failure,full-destroy}` (7) → **all present**
- Missing id strings: **none**
- Extra id strings relative to the 14: the file legitimately contains many more gate ids (static, ha, adoption, integration, heavy, journey); this is expected catalog breadth, not a defect. The 14 required ids are present verbatim.

### Gate 2 — .github/workflows/pre-release.yml consumption
Definition source vs candidate semantics, quoted with file:line (on cddc81b):

- `inputs.ref` → checkout ref: line 37 `ref: ${{ inputs.ref || github.sha }}`. In `develop_mode`, line 59 enforces `[[ "${{ inputs.ref }}" =~ ^[0-9a-f]{40}$ ]]` then line 61 `test "$core_sha" = "${{ inputs.ref }}"` — `inputs.ref` **IS** the candidate core SHA in develop mode (exact-40 SHA, must equal fetched develop tip). In release mode line 134 `if [ -n "$INPUT_TAG" ]` else derive tag from CHANGELOG.
- `inputs.tag` → line 125 `INPUT_TAG: ${{ inputs.tag }}`; line 128-129 selects tag or falls back to CHANGELOG `## [x.y.z]`; line 132 validates tag format. Tag is the **release identity**, candidate source is the checked-out SHA.
- `inputs.demo_ref` → line 60 `INPUT_DEMO_REF: ${{ inputs.demo_ref }}`; resolution at line 205 `pinned_demo_ref="$(tr -d '[:space:]' < "$demo_ref_file")"` from `docs/releases/${tag}.demo-ref` (line 200). In non-24/25/26 tags the pinned file is the **definition source**; `inputs.demo_ref` is only *validated* to equal the pin (line 209-214: mismatch → `exit 1`). For 24/25/26 the pin comes from `ecosystem_release_pins.py` consumer pins (line 169-181).
- `inputs.only_gates` → line 327 `ONLY_GATES: ${{ inputs.only_gates }}`; when the validation ref is `validation/pre-release/selected/gates/*` it overrides from the branch name (line 313-315); otherwise from `docs/releases/$TAG.selected-gates.json` (line 316-318). Passed to `pre-release-check-plan.py --only-gates` (line 321).
- **Unknown-id in `only_gates`: line that decides → `scripts/pre-release-check-plan.py` line 32:**
  ```python
  if (any(not key or key.strip() != key for key in selected) or
          len(selected) != len(set(selected)) or not set(selected) <= set(required)):
      raise ValueError('selected checks must be unique exact required check IDs')
  ```
  An unknown id is **not** silently skipped — `set(selected) <= set(required)` fails and the job **errors out (fail-closed, exit 1)**. Verified by executing the script with `--only-gates "atomic/docker/guided,atomic/docker/does-not-exist"` → `ValueError: selected checks must be unique exact required check IDs`, exit 1.

### Gate 3 — demo ref resolution at fire time
- **Correction to mission premise:** `docs/releases/v0.4.28.demo-ref` does **NOT** exist on develop (cddc81b / ae70964). The highest existing pin is `docs/releases/v0.4.27.demo-ref` = `f23b6e09be34601ba542a3087e19b80764a4165d`. The mission's v0.4.28.demo-ref / "develop pin is still b41127723 until #1842" refers to #1842, which is **still OPEN** (gh pr 1842: state=OPEN, mergeable=MERGEABLE, changes `docs/releases/v0.4.28.demo-ref` bumping the pin to `1a3c055`).
- What the workflow resolves at fire time for the current candidate (tag v0.4.27): `docs/releases/v0.4.27.demo-ref` = `f23b6e09...`. Verified `f23b6e09` is a real commit in baseharbor-demo and `git merge-base --is-ancestor f23b6e09 HEAD` against demo develop tip `5ca92a7c` → **reachable**.
- **Implication for a fire before #1842 merges:** the pinned demo ref is `f23b6e09` (the pre-#1842 pin, i.e. the #175 consent-retry-era commit), NOT the merged develop tip `1a3c055`. The workflow binds and validates exactly `f23b6e09`; it is a concrete, reachable demo SHA, so a fire before #1842 is **not void** — it fires against `f23b6e09`. The implication is that gate evidence is bound to the *older* demo revision `f23b6e09`; after #1842 merges the pin would move to `1a3c055` and a subsequent fire would bind to that instead. No fire today can resolve `1a3c055` (it exists only on #1842).

### Gate 4 — gate -> job mapping (each of the 14 ids maps to a runnable job)

| id | jobs in release-requirements.json | exists in workflow? |
| --- | --- | --- |
| atomic/docker/guided | runtime_candidate, runtime_light_gates_docker | YES (job at line 694, depends runtime_candidate) |
| atomic/docker/lifecycle | runtime_candidate, runtime_light_gates_docker | YES |
| atomic/docker/policy | runtime_candidate, runtime_light_gates_docker | YES |
| atomic/docker/connectivity | runtime_candidate, runtime_light_gates_docker | YES |
| atomic/docker/reconciliation | runtime_candidate, runtime_light_gates_docker | YES |
| atomic/docker/failure | runtime_candidate, runtime_light_gates_docker | YES |
| atomic/docker/full-destroy | runtime_candidate, runtime_light_gates_docker | YES |
| atomic/podman/guided | runtime_candidate, runtime_light_gates_podman | YES (job at line 723, depends runtime_candidate) |
| atomic/podman/lifecycle | runtime_candidate, runtime_light_gates_podman | YES |
| atomic/podman/policy | runtime_candidate, runtime_light_gates_podman | YES |
| atomic/podman/connectivity | runtime_candidate, runtime_light_gates_podman | YES |
| atomic/podman/reconciliation | runtime_candidate, runtime_light_gates_podman | YES |
| atomic/podman/failure | runtime_candidate, runtime_light_gates_podman | YES |
| atomic/podman/full-destroy | runtime_candidate, runtime_light_gates_podman | YES |

All 14 ids map to runnable jobs. `runtime_light_gates_docker`/`runtime_light_gates_podman` are aggregated into the final required `checks` job (line 2064, needs runtime_candidate + both light gates, line 2071-2072). The `select()` function (line 39-46) routes `atomic/{docker,podman}/` light gates into `light_<runtime>` arrays with a fail-closed "no executor" guard (line 49).

## readiness verdict
**FIRE-READY after #1842 (content-prepared): the 14 required gate ids are present verbatim and map to runnable jobs; unknown `only_gates` ids fail-closed. Caveat: the mission's `v0.4.28.demo-ref`/pin `b41127723` does not exist on develop — current pin is `v0.4.27.demo-ref = f23b6e09` (reachable, real commit); a fire today binds to `f23b6e09`, and gate evidence is bound to that demo revision until #1842 (#1842 OPEN, would bump pin to `1a3c055`) merges.**

## cleanliness
- No containers, compose projects, or daemon work started. Pure read-only inspection via `git clone` (depth-1) into `/tmp/w249-wt`, `/tmp/w249-demo` and a planning isolated worktree `workers/w249-0428-284-gateids-plan`.
- `docker ps -a`: n/a (no daemon started). No containers created.

## END
- status: END_DONE
- candidate SHA: ae70964d7b80b779822b76107b70ea76782f998e (origin/develop head)

<!-- coordinator relocation: lane w249 wrote its akte OVER README.md (wrong zone) via plan PR #48; content moved verbatim to evidence/2026-11-26/w249-0428-284-gateids/akte.md and PR #48 closed WITHOUT merging to protect README. -->
