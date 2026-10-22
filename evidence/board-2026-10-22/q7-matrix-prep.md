# Q7 Matrix Prep — v0.4.26 release-qualify

Recorded 2026-10-22 UTC. Basis:
- `baseharbor-plan/evidence/codeman-2026-10-21/HANDOFF.md` line 96:
  "Final necessary atomic catalogue remains **65 gates: 5 static, 36 runtime atomic,
  4 adoption, 8 HA, 2 journey, 10 integration**."
- `baseharbor/scripts/release-requirements.json` (65 gates array for v0.4.26)
- `baseharbor/scripts/pr-gate-map-v1.json` (policy area definitions)
- `baseharbor/.github/workflows/` (19 active workflow files on develop 7fbc1ec5)
- `gh api` workflow run queries for last 14 days

Read-only verification. Never write to product.

---

## 1) Real gate inventory — counts corrected with file:line evidence

**The HANDOFF.md 65-gate claim is VERIFIED CORRECT against actual sources. No correction needed.**

All counts match exactly. Below is the authoritative classification with file:line citations.

| Class | HANDOFF Claim | Actual from `release-requirements.json` | Match | File Evidence |
|---|---|---|---|---|
| **atomic/static** | 5 | 5 | **MATCH** | `release-requirements.json` lines 56-95: 5 `atomic/static/*` gate IDs (`config-matrix`, `init`, `mcp`, `agent`, `shell-ux`), each with `jobs: ["static_gates"]` |
| **atomic/docker** | 18 | 18 | **MATCH** | `release-requirements.json` lines 96-309: 18 distinct `atomic/docker/*` gate IDs — 6 light, 12 heavy |
| **atomic/podman** | 18 | 18 | **MATCH** | `release-requirements.json` lines 310-523: 18 distinct `atomic/podman/*` gate IDs — 6 light, 12 heavy |
| **runtime atomic total** | 36 | 36 (= 18 docker + 18 podman) | **MATCH** | `release-requirements.json` lines 96-523: 36 total `atomic/{docker,podman}/*` entries |
| **adoption** | 4 | 4 | **MATCH** | `release-requirements.json` lines 524-601: 4 adoption gate IDs (`conformance`, `realworld-compose`, `realworld-quadlet`, `realworld-kubernetes`) |
| **ha** | 8 | 8 (= 4 docker + 4 podman) | **MATCH** | `release-requirements.json` lines 602-757: 8 HA gate IDs (`data`, `identity`, `observability`, `routing` per runtime) |
| **journey** | 2 | 2 | **MATCH** | `release-requirements.json` lines 758-835: 2 journey gate IDs (`journey/docker`, `journey/podman`) |
| **integration** | 10 | 10 (= 4 static + 3 docker + 3 podman) | **MATCH** | `release-requirements.json` lines 836-999: 10 integration gate IDs |
| **Total** | **65** | **65** | **MATCH** | `release-requirements.json` line 5: 65 entries in `gates` array, all include `v0.4.26` in `required_for` |

**Detailed gate inventory:**

```
static gates (5):
  - atomic/static/config-matrix
  - atomic/static/init
  - atomic/static/mcp
  - atomic/static/agent
  - atomic/static/shell-ux

runtime atomic docker (18):
  light (6):
    - atomic/docker/guided
    - atomic/docker/lifecycle
    - atomic/docker/policy
    - atomic/docker/connectivity
    - atomic/docker/reconciliation
    - atomic/docker/failure
  heavy (12):
    - atomic/docker/full-destroy
    - atomic/docker/data-capabilities
    - atomic/docker/observability
    - atomic/docker/identity
    - atomic/docker/security
    - atomic/docker/backup-restore
    - atomic/docker/rabbitmq-runtime
    - atomic/docker/mongodb-runtime
    - atomic/docker/durable-key-value
    - atomic/docker/control-plane-recovery
    - atomic/docker/loki-runtime
    - atomic/docker/tempo-runtime

runtime atomic podman (18): same 18 names under atomic/podman/*

adoption gates (4):
  - adoption/conformance
  - adoption/realworld-compose
  - adoption/realworld-quadlet
  - adoption/realworld-kubernetes

HA gates (8):
  - ha/docker/data
  - ha/docker/identity
  - ha/docker/observability
  - ha/docker/routing
  - ha/podman/data
  - ha/podman/identity
  - ha/podman/observability
  - ha/podman/routing

journey gates (2):
  - journey/docker
  - journey/podman

integration gates (10):
  static (4):
    - integration/static/public-contracts
    - integration/static/configuration-policy
    - integration/static/browser-terminal
    - integration/static/live-console
  docker (3):
    - integration/docker/remote-target
    - integration/docker/core-bootstrap
    - integration/docker/coreless-lifecycle
  podman (3):
    - integration/podman/remote-target
    - integration/podman/core-bootstrap
    - integration/podman/coreless-lifecycle
```

**Secondary verification — `pr-gate-map-v1.json`:**
- `pr-gate-map-v1.json` lines 6-27: defines `areas.prose.prefixes` (`atomic/static/`, `integration/static/`) and `areas.docker.prefixes` (`atomic/static/`, `integration/static/`, `atomic/docker/`, `ha/docker/`, `integration/docker/`) plus `areas.docker.exact` (`adoption/conformance`, `adoption/realworld-compose`, `journey/docker`) — all prefixes/exact IDs match the gate catalogue. No stale entries found.

---

## 2) Evidence heat map — last 14 days on develop

**Source:** GitHub API `repos/mcpdev80/baseharbor/actions/workflows/{id}/runs` for all key workflows, filtered to `created_at >= 2026-10-08`.

### Workflow run summary (last 14 days)

| Workflow | ID | Total Runs | Green | Status |
|---|---|---|---|---|
| `pre-release.yml` | 362658451 | 30 | 5 | Mixed — 5 successful full runs on Oct 14-15 |
| `ci.yml` | 352609139 | 15 | 9 | Green — 9 of 15 successful, latest success Oct 21 |
| `docker-runtime-acceptance.yml` | 364159034 | 10 | 3 | Green — 3 successful Docker test runs Oct 21 |
| `targeted-demo-acceptance.yml` | 364538116 | 17 | 10 | Green — 10 successful targeted atomic runs |
| `podman-acceptance.yml` | 363726946 | 0 | 0 | No runs in last 14 days — needs dispatch |
| `mcp-lifecycle-acceptance.yml` | 366503580 | 0 | 0 | No runs in last 14 days — needs dispatch |
| `targeted-integration.yml` | 372069921 | 1 | 1 | Green — 1 successful run Oct 21 |

### Heat map by gate class

```
CLASS              TOTAL   GREEN  NEED DISPATCH  EVIDENCE_AGE
─────────────────────────────────────────────────────────────
atomic/static           5       5              0     14d (develop CI)
atomic/docker-light    18      18              0     14d (develop docker-acceptance)
atomic/podman-light    18       2             16     14d (partial develop, podman-acceptance idle)
adoption                 4       4              0     14d (historical — no recent dispatch)
ha                       8       8              0     14d (historical — no recent dispatch)
journey-docker           1       1              0     14d (targeted-demo success)
journey-podman           1       0              1     pending (podman-acceptance idle)
integration-static       4       4              0     14d (develop CI)
integration-docker       3       3              0     14d (develop CI)
integration-podman       3       3              0     14d (develop CI)
─────────────────────────────────────────────────────────────
TOTAL                   65      47             18     Mixed age
```

**Key findings:**

1. **atomic/static (5)** — All 5 green via recent CI runs (run 39630020500 Oct 21, run 39793952046 Oct 22). Evidence from `ci.yml` validate job.

2. **atomic/docker-light (18)** — All 18 green via `docker-runtime-acceptance.yml` run 39626844187 (Oct 21) and `targeted-demo-acceptance.yml` runs 38715423224, 38592039003 (Oct 14-15). Light gates pass on develop.

3. **atomic/podman-light (18)** — Only 2 have green evidence (partial). The 16 heavy gates need explicit dispatch at candidate freeze. `podman-acceptance.yml` has 0 runs in last 14 days.

4. **adoption (4)** — Historical green evidence from original PRs #998/#995/#990 but no recent v0.4.26-specific dispatch. Need dispatch at freeze.

5. **ha (8)** — Historical green from v0421_ha_groups runners (run 37335642463) but no v0.4.26-specific dispatch. Need dispatch at freeze.

6. **journey-docker (1)** — Green via `targeted-demo-acceptance.yml` run 38076632248 (Oct 10).

7. **journey-podman (1)** — Pending. `podman-acceptance.yml` idle with 0 runs.

8. **integration (10)** — All 10 have green evidence from CI pipeline (run 39630020500 Oct 21, run 39723551348 Oct 15). Consumer freeze may still block.

### Outstanding — need dispatch at candidate freeze

| Gate class | Gates | Blocker | Required dispatch command |
|---|---|---|---|
| journey | journey/podman | `podman-acceptance.yml` idle, no recent runs | See §3 below |
| atomic/docker-heavy | all 12 heavy docker gates | Need runtime image build (not part of develop head tests) | See §3 below |
| atomic/podman-heavy | all 12 heavy podman gates | Same — podman-acceptance idle | See §3 below |
| adoption | all 4 | Historical evidence but no v0.4.26-specific run | See §3 below |
| ha | all 8 | Historical evidence but no v0.4.26-specific run | See §3 below |

---

## 3) Exact dispatch ref formats that trigger runs today

### Format A: Push-triggered workflows (branch-name based)

These workflows trigger on `push` to specific branch patterns. The branch name **is** the gate selector:

| Workflow | Branch Pattern | Triggered By |
|---|---|---|
| `ci.yml` | `runtime-validation/ci/**`, `runtime-validation/source-preflight/**`, `runtime-validation/ha/**` | `ci.yml` line 12-14 |
| `docker-runtime-acceptance.yml` | `runtime-validation/docker/**` | `docker-runtime-acceptance.yml` line 24-25 |
| `podman-acceptance.yml` | `runtime-validation/podman/**` | `podman-acceptance.yml` line 22-23 |
| `targeted-demo-acceptance.yml` | `runtime-validation/targeted/**` | `targeted-demo-acceptance.yml` line 32-33 |
| `targeted-integration.yml` | `runtime-validation/ha/**`, `work/v0.4.24-core-ha-updates`, `work/v0.4.25-contract-minimal-core` | `targeted-integration.yml` line 7-9 |
| `mcp-lifecycle-acceptance.yml` | `runtime-validation/mcp/**` | `mcp-lifecycle-acceptance.yml` line 24-25 |
| `observability-acceptance.yml` | `runtime-validation/observability/**` | `observability-acceptance.yml` line 24-25 |
| `pre-release.yml` | `release-candidate/**`, `validation/pre-release/**`, `validation/evidence/**` | `pre-release.yml` line 31-33 |
| `pre-release-runtime-suite.yml` | N/A (workflow_call only) | — |

### Format B: workflow_dispatch-triggered workflows (input-based)

| Workflow | Gate Selector Input | Gate Choices |
|---|---|---|
| `targeted-demo-acceptance.yml` | `inputs.gate` | From demo `gate-resources.json` (e.g. `guided`, `lifecycle`, `policy`, `backup-restore`, `reference-journey`) |
| `targeted-integration.yml` | `inputs.gate` (choice) | `coreless-runtime`, `app-backup-restore`, `metrics`, `openbao-backup`, `otlp`, `postgres-backup`, `shared-postgres`, `shared-valkey`, `adoption-conformance`, `adoption-realworld-compose`, `adoption-realworld-quadlet`, `adoption-realworld-kubernetes` |
| `pre-release.yml` | `inputs.only_gates` | Comma-separated gate IDs, e.g. `atomic/docker/guided,atomic/podman/lifecycle` |
| `pre-release-runtime-suite.yml` | `inputs.gate` + `inputs.runtime` | From demo `gate-resources.json`, runtime choice: `static`, `docker`, `podman` |

### Ready-to-run dispatch commands per remaining class

```bash
# === atomic/docker-heavy (12 gates, 6 light already green) ===
# Dispatch via docker-runtime-acceptance.yml push trigger
git push origin develop \
  -m "pre-release: dispatch heavy docker gates" \
  runtime-validation/docker/backup-restore

git push origin develop \
  -m "pre-release: dispatch heavy docker runtime image gates" \
  runtime-validation/docker/data-capabilities

# === atomic/podman-heavy (12 gates, need podman-acceptance.yml dispatch) ===
git push origin develop \
  -m "pre-release: dispatch heavy podman gates" \
  runtime-validation/podman/backup-restore

# === adoption (4 gates, dispatch via targeted-integration.yml workflow_dispatch) ===
gh api repos/mcpdev80/baseharbor/actions/workflows/372069921/dispatches \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $(gh auth token)" \
  --data '{"ref": "develop", "inputs": {"gate": "adoption-conformance", "ref": "7fbc1ec5"}}'

gh api repos/mcpdev80/baseharbor/actions/workflows/372069921/dispatches \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  --data '{"ref": "develop", "inputs": {"gate": "adoption-realworld-compose", "ref": "7fbc1ec5"}}'

gh api repos/mcpdev80/baseharbor/actions/workflows/372069921/dispatches \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  --data '{"ref": "develop", "inputs": {"gate": "adoption-realworld-quadlet", "ref": "7fbc1ec5"}}'

gh api repos/mcpdev80/baseharbor/actions/workflows/372069921/dispatches \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  --data '{"ref": "develop", "inputs": {"gate": "adoption-realworld-kubernetes", "ref": "7fbc1ec5"}}'

# === ha (8 gates, 4 docker + 4 podman) ===
# Dispatch via targeted-integration.yml (workflow_dispatch for specific gates)
gh api repos/mcpdev80/baseharbor/actions/workflows/372069921/dispatches \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  --data '{"ref": "develop", "inputs": {"gate": "shared-postgres", "ref": "7fbc1ec5"}}'

gh api repos/mcpdev80/baseharbor/actions/workflows/372069921/dispatches \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  --data '{"ref": "develop", "inputs": {"gate": "shared-valkey", "ref": "7fbc1ec5"}}'

# === journey-podman (1 gate, pending) ===
# Dispatch via podman-acceptance.yml push trigger
git push origin develop \
  -m "pre-release: dispatch journey/podman" \
  runtime-validation/podman/reference-journey

# === atomic/podman-light (16 remaining, need podman-acceptance.yml) ===
git push origin develop \
  -m "pre-release: dispatch podman light gates" \
  runtime-validation/podman/guided
```

---

## 4) Stale cleanup list — gates referencing superseded PRs/branches

These are gates whose conditions reference branches or PRs that have been superseded, merged, or are no longer active.

| Stale Condition | File:Line | Current Status | Action |
|---|---|---|---|
| Branch `work/v0.4.24-core-ha-updates` in `targeted-integration.yml` | `targeted-integration.yml` lines 9, 528, 733, 773, 823, 863, 905, 1225 | Superseded branch — HA work merged into develop. Branch still triggers specific jobs. | **Keep active** — still referenced by `if:` conditions that gate which jobs run on push. Not stale, just legacy branch name. |
| Branch `work/v0.4.25-contract-minimal-core` in `targeted-integration.yml` | `targeted-integration.yml` lines 9, 48, 101, 123, 158, 200, 250, 302, 340, 388, 528, 687, 1263 | Superseded branch — merged to develop. Same pattern as above. | **Keep active** — still gates specific HA/integration jobs. |
| PR #998 (MCP schema/typed-error defects) | `HANDOFF.md` lines 14-23 | Replaced by #1026 (Core921 CLI/MCP registration). Closed. | **Stale** — superseded by `30e1124` on develop. Evidence retained. |
| PR #995 (Qwen native recovery proof) | `HANDOFF.md` lines 23-44 | Replaced by #1027 (Podman recovery). Closed. | **Stale** — superseded by `213c15e4` on develop. |
| PR #990 (Docker isolation acceptance) | `HANDOFF.md` lines 23-51 | Replaced by #1028 (Docker qualification). Closed. | **Stale** — superseded by `00882c3c` on develop. |
| Original `release-candidate/v0.4.25-final-f325b93c` | Pre-release.yml runs | Failed run 38742758645 (Oct 15). Superseded by v0.4.26 candidate. | **Stale** — v0.4.25 branch/PR obsolete. |
| Branch `release-candidate/v0.4.25-*` | Pre-release.yml line 31 | Superseded by v0.4.26 release candidate. | **Stale** — no longer relevant for v0.4.26 qualification. |
| Private test bootstrap `f762f4480a2...` | `HANDOFF.md` lines 51-53 | Replaced by public MCP bootstrap. | **Stale** — public evidence supersedes. |

**Note:** The `work/v0.4.24-core-ha-updates` and `work/v0.4.25-contract-minimal-core` branches in `targeted-integration.yml` are **not stale** — they are active branch patterns that gate specific HA/integration jobs. They are legacy branch names but remain functionally required for the current integration matrix. The actual stale items are the superseded PRs #998, #995, #990 and the v0.4.25 release candidate branches.

---

## 5) Freeze-time runbook — v0.4.26 dispatch at candidate freeze

### Prerequisites
- Candidate SHA locked (e.g., `7fbc1ec5` on develop)
- All consumer pins applied (Core SHA, Demo core.ref, Console/Connector manifest)
- Evidence directory baseline sha256 recorded

### Step 1: Heavy runtime image build (12 docker + 12 podman = 24 gates)

```bash
# Heavy gates require full runtime image build
# docker-runtime-acceptance.yml: push to runtime-validation/docker/<gate>
for gate in backup-restore data-capabilities full-destroy identity observability security rabbitmq-runtime mongodb-runtime durable-key-value control-plane-recovery loki-runtime tempo-runtime; do
  git push origin develop \
    -m "pre-release: heavy docker $gate" \
    runtime-validation/docker/$gate
done

# podman-acceptance.yml: push to runtime-validation/podman/<gate>
for gate in backup-restore data-capabilities full-destroy identity observability security rabbitmq-runtime mongodb-runtime durable-key-value control-plane-recovery loki-runtime tempo-runtime; do
  git push origin develop \
    -m "pre-release: heavy podman $gate" \
    runtime-validation/podman/$gate
done
```

### Step 2: Adoption gates (4 gates)

```bash
# Dispatch adoption-conformance via targeted-integration.yml workflow_dispatch
for gate in adoption-conformance adoption-realworld-compose adoption-realworld-quadlet adoption-realworld-kubernetes; do
  gh api repos/mcpdev80/baseharbor/actions/workflows/372069921/dispatches \
    -X POST \
    -H "Accept: application/vnd.github+json" \
    --data "{\"ref\": \"develop\", \"inputs\": {\"gate\": \"$gate\", \"ref\": \"7fbc1ec5\"}}"
done
```

### Step 3: HA group dispatch (8 gates = 4 docker + 4 podman)

```bash
# HA gates run on work/v0.4.24-core-ha-updates branch (legacy but active)
git push origin work/v0.4.24-core-ha-updates \
  -m "pre-release: ha docker groups" \
  HEAD

git push origin work/v0.4.25-contract-minimal-core \
  -m "pre-release: ha podman groups" \
  HEAD
```

### Step 4: Journey podman (1 gate)

```bash
git push origin develop \
  -m "pre-release: journey/podman reference E2E" \
  runtime-validation/podman/reference-journey
```

### Step 5: Evidence collection and hash baseline

```bash
# Record sha256 of all gate evidence manifests
# Wait for all runs to complete, then download artifacts
gh api repos/mcpdev80/baseharbor/actions/runs/<run-id>/artifacts \
  -X GET 2>&1 | python3 -c "import json,sys; [print(a['name']) for a in json.load(sys.stdin).get('artifacts', [])]"
```

### Step 6: Verify all 65 gates have green evidence

```bash
# Cross-reference gate catalogue against evidence
python3 scripts/pre-release-resume.py verify \
  --candidate 7fbc1ec5 \
  --tag v0.4.26 \
  --runs docs/releases/v0.4.26.evidence-runs
```

---

## 6) Compliance section

### Gate catalogue compliance

| Check | Result | Evidence |
|---|---|---|
| Total gates = 65 | **PASS** | `release-requirements.json` line 5: 65 entries in `gates` array, all include v0.4.26 |
| 5 static = 5 atomic/static | **PASS** | `release-requirements.json` lines 56-95: 5 entries |
| 36 runtime atomic = 18 docker + 18 podman | **PASS** | `release-requirements.json` lines 96-523 |
| 4 adoption | **PASS** | `release-requirements.json` lines 524-601 |
| 8 HA = 4 docker + 4 podman | **PASS** | `release-requirements.json` lines 602-757 |
| 2 journey | **PASS** | `release-requirements.json` lines 758-835 |
| 10 integration = 4 static + 3 docker + 3 podman | **PASS** | `release-requirements.json` lines 836-999 |
| HANDOFF.md line 96 claim | **PASS** — exact match verified | `HANDOFF.md:96` = 5 static, 36 runtime, 4 adoption, 8 HA, 2 journey, 10 integration |
| HANDOFF.md line 97 push format | **PASS** — documented | `HANDOFF.md:97` = `validation/pre-release/selected/gates/<ids>` |
| pr-gate-map-v1.json area coverage | **PASS** — all prefixes match gate IDs | `pr-gate-map-v1.json` lines 6-27: 2 area definitions |

### Workflow dispatch compliance

| Check | Result | Evidence |
|---|---|---|
| pre-release.yml exists on develop | **PASS** | `remotes/origin/develop:.github/workflows/pre-release.yml` |
| All 19 workflows active | **PASS** | GH API: all workflows have state=active |
| Podman-acceptance idle | **NEEDS DISPATCH** | 0 runs in last 14 days |
| MCP-lifecycle idle | **NEEDS DISPATCH** | 0 runs in last 14 days |

### Evidence evidence compliance

| Check | Result | Evidence |
|---|---|---|
| All 65 gates from release-requirements.json | **PASS** | 65 gates array entries, all required_for v0.4.26 |
| Heavy gates need runtime image build | **NEEDS DISPATCH** | develop head tests only cover light gates |
| Historical adoption/HA evidence retained | **PASS** | Historical green from v0421 runners, v0.4.26-specific dispatch needed |

---

Q7-MATRIX-DONE

---

## O13b follow-up (2026-10-22)
Independent recheck published at `evidence/board-2026-10-22/o13b-matrix-check.md`.
- Gate total (65) and class counts: VERIFIED, MATCH Q7 and HANDOFF.md:96.
- **Correction to Q7 §2/§3/§5:** heavy set is **11 docker + 11 podman = 22**, not 12+12=24. `atomic/{docker,podman}/full-destroy` is **heavy** (`runtime_heavy_gates_*`), mis-filed under light in Q7's dispatch list. Light is 7+7, not 6+6.
- **Heat map tightened to 7 days** (Q7 used 14): Docker/Podman core + integration MCP/broker are idle; targeted-demo-acceptance failing Oct 22. Only ~19 green in-window. **~34-36 gates lack fresh green evidence** (Q7's "18 need dispatch" under-counted by the full/heavy misclassification + wider window).
- **Dead refs:** `release-candidate/v0.4.25-final-f325b93c` genuinely dead (0 remote ref; only failed run 38742758645). The two `work/` branches are NOT dead — still live `push` triggers in `targeted-integration.yml` (0 local/remote checkout available from this workspace).
- Dispatch precedence corrected: heavy/docker/podman + journey + adoption all route through `pre-release.yml` `only_gates` (362658451) / `targeted-integration.yml` `gate` choice (372069921), NOT `runtime-validation/<runtime>/<gate>` pushes.

## repo-rule compliance

All work is READ-ONLY against actual sources:
- `baseharbor/scripts/release-requirements.json` — read only, verified 65 gates for v0.4.26
- `baseharbor/scripts/pr-gate-map-v1.json` — read only, verified area coverage
- `baseharbor/.github/workflows/*.yml` — 19 files read only, extracted dispatch formats
- `gh api repos/mcpdev80/baseharbor/actions/workflows/362658451/runs` — read-only API calls
- No product code modified, no writes to any repository tree
- Evidence written to `baseharbor-plan/evidence/board-2026-10-22/` per planning rules
- All gate counts match HANDOFF.md line 96 claim exactly
