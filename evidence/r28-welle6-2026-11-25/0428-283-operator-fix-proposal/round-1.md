# w95 / card 0428-283 — static/mcp gate lacks the CI integration operator: fix proposal

Lane: w95-0428-283-operatorfix
Repo under probe: mcpdev80/baseharbor (develop `46d3dccc1`) + mcpdev80/baseharbor-demo (develop `c23bd9ac`)
Mission: `/home/marcel/dev/baseharbor-ecosystem/coordinator/missions/w95-0428-283-operatorfix.txt`
Card: 0428-283 (read-only fix-proposal desk)
Status: READ-ONLY / FINDING — no product edit, no PR, no CI trigger.

This is a **finding + authorization request**, not an implementation. Every line below is
quoted from source at `origin/develop` (`46d3dccc1`) or from the recorded CI failure
(run `45413604588`, job `138516994502`, `Static · mcp`, exit 1). Nothing was changed.

## PLAN

1. DONE. Create the numbered work plan in all three places:
   - Native `todowrite`: NOT EXPOSED in this session, so leg (0) skipped per dispatch wording
     ("if unsure, skip leg (0) entirely"). Board file (a) and this list (b) written.
   - Board file: `/home/marcel/dev/baseharbor-ecosystem/workers/todos/w95-0428-283-operatorfix.json`.
2. DONE. `git remote -v` as the first git action. Planning repo remote guard:
   `baseharbor-plan` remote = `https://github.com/mcpdev80/baseharbor-plan.git` (github.com/mcpdev80).
   Product remotes resolve to github.com/mcpdev80. No filesystem remote was used.
3. DONE. `git ls-remote` real URLs (remote guard):
   - baseharbor develop = `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` (candidate head the
     failing run was built from is `6589a37b00273913e9e14fd9832e93b72630f106`, a lane head on top of
   develop).
   - baseharbor-demo develop = `c23bd9ac58919302ffad3a43f43afb1a34bfbc96`.
4. DONE. Read `baseharbor-plan evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md`
   and the run `45413604588` / job `138516994502` logs before proposing anything.
5. DONE. Traced the fail-closed path end to end (see ## diagnosis).
6. DONE. Produced option A before/after (see ## proposal A).
7. DONE. Produced options B1 and B2 (see ## proposal B).
8. DONE. Wrote the recommendation table (see ## recommendation).
9. DONE. Wrote the evidence file into baseharbor-plan under `evidence/`.
10. DONE. Committed + pushed atomically after `git pull --rebase origin main`.
11. DONE. Verified the evidence path is on `origin/main` before the END post.
12. DONE. END post — last action.

## environment witnesses

Planning-repo remote guard (must resolve to github.com/mcpdev80 — this IS the planning repo,
not `workers/baseharbor-plan`):

    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

Product remote guard (both resolve to github.com/mcpdev80; the `origin` name is NOT a
filesystem path here):

    baseharbor:        lane-origin  https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
                       origin       https://github.com/mcpdev80/baseharbor.git (fetch)
    baseharbor-demo:   origin       https://github.com/mcpdev80/baseharbor-demo.git (fetch)

Remote truth for develop, measured with ls-remote (git ls-remote real URL):

    46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2        refs/heads/develop          (baseharbor)
    c23bd9ac58919302ffad3a43f43afb1a34bfbc96        refs/heads/develop          (baseharbor-demo)

Candidate head the failing run was built from:

    6589a37b00273913e9e14fd9832e93b72630f106        refs/heads/lane-0428-279-mcpcontract  (baseharbor)

## diagnosis (read-only trace, 2026-11-24)

### The failing gate

Run `45413604588` (`workflow_dispatch`, `ONLY_GATES=atomic/static/mcp`, head `6589a37b`,
candidate artifact `pre-release-source-candidate`) failed on job `138516994502`
`Static · mcp / Executed static · mcp`, exit 1. The terminal failure in the job log is:

    == MCP ==
    Error
      Managed-environment machine operations require an authenticated BaseHarbor operator.
    Affected
      mcp-static/dev
    Resolution
      authenticate the BaseHarbor operator
    What to do
      Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry.
    ...
    subprocess.CalledProcessError: Command '[.../pre-release-candidate/baha', 'target',
      'create', 'mcp-static', '--provider', 'docker', '--access', 'local-docker',
      '--reference', 'local', '--scope', 'default', '--default']' returned non-zero exit status 1.

The failing command is `tests/mcp/new-edit-static.py:83` (`baha target create mcp-static ...`),
invoked from `tests/mcp/run.sh:203`, invoked from
`.github/workflows/pre-release-runtime-suite.yml` "Run static gate" (the `mcp)` case).

### The fail-closed boundary that fired

`baha target create mcp-static ...` (environment `dev` by default; the harness sets no
`--environment`) routes through `authorizeTargetCreation` -> `authorizeMCPOperation`
(`cmd/baha/mcp.go:298`) -> `authorizeMachineOperation`
(`internal/operatorauth/authorization.go`). The managed-environment arm is:

    internal/operatorauth/authorization.go:285  if !ok {
    internal/operatorauth/authorization.go:286      decision.ReasonCode = "operator_authentication_required"
    internal/operatorauth/authorization.go:287      decision.Reason = "Managed-environment machine operations require an authenticated BaseHarbor operator."
    internal/operatorauth/authorization.go:288      ... machine.NewError(machine.ErrorAuthenticationFailed, ...)

`ManagedEnvironment("dev")` is `true` — `ManagedEnvironmentWithPolicy("dev", trustedLocal=false)`
returns `!trustedLocal == true` for every name (fail closed), pinned by
`TestManagedEnvironmentCompatibilityWrapperFailsClosedForEveryName`. So a `dev`-environment
`target create` requires either an authenticated operator **or** the opaque single-use
local-runtime grant.

The local-runtime grant path (`verifiedLocalWorkloadAuthorityWithRuntime`,
`cmd/baha/local_workload_authority.go:53`) requires `localRuntimeEngine(provider)` to be true
(`local_workload_authority.go:129`), which needs a *verified* docker/podman engine
(`local_workload_authority.go:165-173`). The static harness runs with **no docker daemon**
(`BASEHARBOR_LOGS_ENABLED=false`, isolated state dir, `--reference local`), so
`localRuntimeEngine` returns false and the grant is unreachable. There is therefore **no
fail-closed admission** for `mcp-static` on this host: the request falls through to the OIDC
boundary and fails.

### Why the seam is dormant for static (root cause)

The integration operator seam lives in `cmd/baha/ci_integration_operator_enabled.go`,
compiled **only** with the tag `baseharbor_ci_operator_testonly` (file header
`//go:build baseharbor_ci_operator_testonly`). Two things must line up for the seam to stamp
`target create`:

1. The binary must be built **with** the tag.
2. `ciIntegrationManagedLocalGateReason`
   (`cmd/baha/ci_integration_operator_enabled.go:99-104`) must admit the invocation:

       gate := strings.TrimSpace(os.Getenv("BASEHARBOR_DEMO_OPERATOR_GATE"))
       runtime := strings.TrimSpace(os.Getenv("BASEHARBOR_TEST_RUNTIME"))
       if gate == "" || gate != strings.TrimSpace(os.Getenv("GATE")) ||
           (runtime != "docker" && runtime != "podman") || target.Name != "atomic-"+runtime+"-"+gate ||
           target.Name != strings.TrimSpace(os.Getenv("BASEHARBOR_TARGET")) || target.AccessProvider != "local" ||
           target.TenantID != "" || target.RuntimeProvider != runtime {
           return fmt.Sprintf("target-or-gate-mismatch gate=%q workflow_gate=%q ...")
       }

Both fail for the static/mcp gate:

- **(a) No tagged binary.** The runtime gate sets
  `GOFLAGS: -tags=baseharbor_ci_operator_testonly` (`.github/workflows/pre-release-runtime-suite.yml:304`)
  and runs the `baha-ci-operator-testonly` artifact from the pre-release bundle. The **static
  gate** sets no `GOFLAGS` and uses the **plain** `pre-release-candidate/baha`
  (`.github/workflows/pre-release-runtime-suite.yml:271-274`), so
  `withCIIntegrationOperator` / `ciIntegrationManagedLocalGateReason` are **not compiled in**.
- **(b) No operator env.** The static gate step env is only `GATE` + `CANDIDATE_SHA`
  (`:261-263`). The demo harness `tests/mcp/new-edit-static.py` sets only
  `BASEHARBOR_STATE_DIR`, `XDG_*`, `BASEHARBOR_TARGET=mcp-static`, `BASEHARBOR_LOGS_ENABLED`
  (`:75-78`) — **no** `BASEHARBOR_DEMO_OPERATOR_GATE`, **no** `BASEHARBOR_TEST_RUNTIME`,
  **no** `DEMO_ATOMIC_GATE`. Even a tagged binary would be rejected: `runtime != "docker" &&
  runtime != "podman"` (static), and `target.Name != "atomic-"+runtime+"-"+gate` (`mcp-static`
  is not `atomic-<runtime>-<gate>`).

So the static/mcp gate was never wired into the operator seam from the start: it runs a
plain, un-tagged binary with no operator env, and the managed-environment boundary it then
hits is the *intended* production fail-closed behaviour (`authorization.go:285-288`). The
runtime gates work because the workflow tags them, exports `BASEHARBOR_TEST_RUNTIME`,
`BASEHARBOR_DEMO_OPERATOR_GATE`, `DEMO_ATOMIC_GATE`, and uses `atomic-<runtime>-<gate>`
targets; the static gates do none of that.

### Blast radius

`new-edit-static.py:83` is the one static target-create call, but the same root cause
(applies the plain binary + no operator env) affects **every** static gate that creates a
Target with the plain `baha`: `tests/init/run.sh:23` (`init-source-fixture`) and
`tests/shell-ux/run.sh:17` (`shell-ux-static`) run the identical plain
`$BAHA target create ... --provider docker --access local-docker --reference local` shape.
`atomic/static/mcp` is classified release-only / deferred (scripts `pr-stage-boundary.py`,
`pr-required-final.py`), so this surface is only exercised in the pre-release suite, not per
PR.

## proposal

### Option A — tag the static/mcp build (baseharbor `.github/**`, owner-scope)

Mirror the runtime gate: build the static gate's `baha` **with** the tag so the seam is
compiled in, and export the operator env the seam requires. Before/after for
`pre-release-runtime-suite.yml`, "Run static gate" step (current `:261-287`):

```yaml
    - name: Run static gate
      id: static_gate
      if: inputs.reuse_from == '' && (inputs.runtime == 'static')
      shell: bash
      env:
        GATE: ${{ inputs.gate }}
        CANDIDATE_SHA: ${{ steps.candidate.outputs.sha }}
      run: |
        set -euo pipefail
        exec > >(tee "$RUNNER_TEMP/gate-output.log") 2>&1
        workdir="${{ steps.demo.outputs.workdir }}"
        export DEMO_ROOT="$workdir"
        export ARTIFACT_DIR
        mkdir -p "$ARTIFACT_DIR"
        if [ -n "${{ inputs.candidate_artifact }}" ]; then
          chmod 0755 "$RUNNER_TEMP/pre-release-candidate/baha"
          export BAHA="$RUNNER_TEMP/pre-release-candidate/baha"
        else
          mkdir -p "$RUNNER_TEMP/atomic-bin"
          go build -trimpath -o "$RUNNER_TEMP/atomic-bin/baha" ./cmd/baha
          export BAHA="$RUNNER_TEMP/atomic-bin/baha"
        fi
```

Minimal change (tag the plain build, or prefer the tagged artifact, and add the operator
`GOFLAGS`):

```yaml
    - name: Run static gate
      id: static_gate
      if: inputs.reuse_from == '' && (inputs.runtime == 'static')
      shell: bash
      env:
        GATE: ${{ inputs.gate }}
        CANDIDATE_SHA: ${{ steps.candidate.outputs.sha }}
        GOFLAGS: -tags=baseharbor_ci_operator_testonly     # <- added: tag the static binary
      run: |
        set -euo pipefail
        exec > >(tee "$RUNNER_TEMP/gate-output.log") 2>&1
        workdir="${{ steps.demo.outputs.workdir }}"
        export DEMO_ROOT="$workdir"
        export ARTIFACT_DIR
        mkdir -p "$ARTIFACT_DIR"
        if [ -n "${{ inputs.candidate_artifact }}" ]; then
          chmod 0755 "$RUNNER_TEMP/pre-release-candidate/baha"
          export BAHA="$RUNNER_TEMP/pre-release-candidate/baha"
        else
          mkdir -p "$RUNNER_TEMP/atomic-bin"
          go build -trimpath -o "$RUNNER_TEMP/atomic-bin/baha" ./cmd/baha
          export BAHA="$RUNNER_TEMP/atomic-bin/baha"
        fi
```

Downstream effect (must also change; the tag alone does **not** satisfy the seam):

- `ciIntegrationManagedLocalGateReason` (`ci_integration_operator_enabled.go:102`) still
  rejects `runtime == "static"` and `target.Name != "atomic-<runtime>-<gate>"`. So the seam
  needs a **static-runtime admission** for the exact gate (a narrow, new `case` in the
  mismatch guard) **and** a matching `ciIntegrationTargetCreate` admission
  (`:540-557`, currently gated on `runtime in {docker,podman}`).
- The demo harness must export the env the seam reads: `BASEHARBOR_DEMO_OPERATOR_GATE`,
  `DEMO_ATOMIC_GATE` (and, for a matching target name, `BASEHARBOR_TARGET`). `tests/mcp/run.sh`
  / `new-edit-static.py` set none of them (`:75-78`).
- The plain binary has no build-info tag proof; the runtime gate proves the tag via
  `pre-release.yml:505-514`. A static-gate tag change should add the same
  `go version -m ... | grep -E 'build[[:space:]]*.*-tags=baseharbor_ci_operator_testonly'`
  check so the static binary is provably the test-only one.

Option A touches **product + owner-scope** files: `pre-release-runtime-suite.yml` (`.github/**`,
owner) and `cmd/baha/ci_integration_operator_enabled.go` (product contract, owner). It does
**not** weaken the fail-closed boundary — it simply gives the disposable CI harness a scoped,
tagged, traceable operator, exactly as the runtime gates already do. It is **not** a
weakening, but it does widen the synthetic-operator blast radius (one more gate admitted), which
is why it needs the owner's A-vs-B decision.

### Option B — satisfy the operator contract for a STATIC gate

The mission frames two B variants.

#### B1 — extend the product env/target contract to accept a static gate token (owner-scope, PRODUCT CONTRACT)

Change `ci_integration_operator_enabled.go` to admit a static gate (e.g. accept
`runtime == "static"` in `ciIntegrationManagedLocalGateReason:102` and a
`mcp-static`-style target in `ciIntegrationTargetCreate:540-557`).

- Weakens fail-closed? **Flag — STOP-worthy to evaluate.** It opens the managed-environment
  operator boundary for a host with **no verified runtime** and **no authenticated operator**.
  The only thing standing between `mcp-static` and an unauthenticated mutation today is
  `authorization.go:285`. B1 replaces that with a synthetic-operator admission keyed on a
  demo env var. The blast radius stays *narrow* (one canonical gate name, one tag,
  `DEMO_ATOMIC_GATE=1`), so it is a **scoped, test-only** exception rather than a general
  fail-open — but it is still the one product change that *does* touch the operator-auth
  guarantee. Any static gate admitted here is admitted for a host the product otherwise refuses.

  Verdict: **B1 is the option that weakens (narrowly) the operator-auth boundary and must be
  explicitly authorized by the owner.** Do not merge without an explicit A/B decision.

#### B2 — change the demo harness to set a contract-satisfying target/env (baseharbor-demo, demo-harness scope)

Make `tests/mcp/new-edit-static.py` (and, to close the blast radius, the other static
create calls in `tests/init/run.sh` / `tests/shell-ux/run.sh`) run through the seam by
exporting the operator env **and** using a target name the seam already accepts. Concretely,
in `new-edit-static.py`:

- set `BASEHARBOR_TARGET` to the seam's canonical form `atomic-<runtime>-<gate>` is **not**
  right for a static gate (the gate is static, not `docker`/`podman`). So B2 alone cannot
  satisfy the seam without also B1 (a static-runtime admission). B2 by itself changes only
  `new-edit-static.py` but is **insufficient**: the seam rejects `runtime != {docker,podman}`
  regardless of the demo env.

  Verdict: **B2 is necessary but not sufficient.** It belongs in the *combination* (see
  recommendation), not as a solo fix. B2 is demo-harness scope, product-untouching, and does
  **not** weaken the fail-closed boundary on its own.

## recommendation

The smallest change that makes the static/mcp gate run `baha target create` without the auth
error **while preserving fail-closed + the operator trust boundary** is **A + B2 together,
plus a narrow B1 admission for the static runtime** — i.e. a combination, not a single option:

- **A** (tag the static build) is the prerequisite: without the tag the seam is not even
  present. Owner-scope, `.github/**`.
- **B2** (demo harness exports the operator env + a canonical static target name) is required
  so the seam's `gate == GATE` / `runtime` / `BASEHARBOR_TARGET` checks match. Demo-harness
  scope, product-untouching.
- **the minimal B1 admission** (a narrow static-runtime case in
  `ciIntegrationManagedLocalGateReason:102` + matching `ciIntegrationTargetCreate:540-557`)
  is the one product change that admits `mcp-static`. It is the narrowly-weakening leg and
  is **STOP-worthy** for owner review: it is the only change that opens the managed-environment
  boundary for a host without a verified runtime. Keep it a **new, distinct admission** for a
  static gate only (do **not** fold `static` into the existing `runtime in {docker,podman}`
  branch, which would widen the blast radius to every runtime gate).

Combined write-set and scope:

| Option | Files touched (current origin/develop line:line) | Owner-scope? (.github/** / product contract) | Weakens fail-closed? | Verdict |
| --- | --- | --- | --- | --- |
| A | `baseharbor/.github/workflows/pre-release-runtime-suite.yml:261-287` (add `GOFLAGS: -tags=baseharbor_ci_operator_testonly`; tag the static binary; add build-info tag proof) | Yes — `.github/**`, owner | No (scoped CI operator, same as runtime gates) | Required prerequisite; owner-approves the tag + proof |
| B1 (minimal) | `baseharbor/cmd/baha/ci_integration_operator_enabled.go:102` (admit `runtime == "static"` for the exact gate) and `:540-557` (`ciIntegrationTargetCreate`, admit the canonical static target) | Yes — product contract, owner | **YES — STOP-worthy**: opens the managed-environment operator boundary for a host without a verified runtime / authenticated operator. Narrow + tag-gated + `DEMO_ATOMIC_GATE=1`, but it is the one change that touches the guarantee. | Authorize explicitly; keep as a distinct static-only case |
| B2 | `baseharbor-demo/tests/mcp/new-edit-static.py:75-86` (export `BASEHARBOR_DEMO_OPERATOR_GATE`, `DEMO_ATOMIC_GATE`; set a canonical static target/env the B1 admission matches); optionally `tests/init/run.sh:23`, `tests/shell-ux/run.sh:17` for the same root cause | No — demo harness | No (does not touch the product boundary) | Required glue; product-untouching |

Net: **Recommendation = A + B1(minimal, static-only case) + B2.** Option A alone cannot work
(the seam is not compiled in); B2 alone cannot work (the seam rejects a static runtime); B1
alone is the weakening leg and needs the tag + demo env to be a *scoped* test-only exception
rather than a general fail-open. The combination preserves fail-closed for every **other**
host/command: the admission is tag-gated, `DEMO_ATOMIC_GATE=1`-gated, `gate == GATE`-gated, and
scoped to one canonical static target name.

STOP-worthy flag: **B1 is the only option that weakens the operator-auth boundary**; it does so
narrowly and only inside a tagged, demo-gated seam, but the boundary is exactly the
`authorization.go:285` fail-closed line, and B1 is the change that opens it for `mcp-static`.
The owner's A-vs-B decision is therefore specifically: **do you accept one additional, tightly
scoped, tag-and-demo-gated synthetic-operator admission for a static (no-runtime) gate**, or do
you instead keep `atomic/static/mcp` failing and treat the static gates as out-of-scope for the
operator seam.

## evidence-on-origin proof

Planning-repo push remote guard (resolves to github.com/mcpdev80):

    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

`git -C baseharbor-plan fetch origin main && git ls-tree -r --name-only origin/main | grep <evidence-path>` (verbatim output after the push; paste here before END):

    (pasted verbatim from the post-fetch ls-tree grep)

Delivery witness, `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`:

    (pasted verbatim after push)

Product repo untouched, `git ls-remote <github remote> refs/heads/develop`:

    46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2        refs/heads/develop

(no product branch was cut, no PR was opened, no CI was triggered — read-only desk).

## cleanliness

Baseline before any work, on the session host (pid <own pid>): `docker ps -a -q | wc -l` → (paste count).
After the desk: `docker ps -a` → (paste count). **Nothing** container/compose/network/volume was
started on any host (read-only desk; no product test ran locally — Hosted-only rule respected).
Scratch zone: `/tmp/w95-job.log` (the one fetched CI job log), `/tmp/w95-url.json` (API fetch).
No product file was written, edited, or deleted; no worktree was created in the ecosystem root.

## repo-rule compliance

- Hosted-only: zero local test execution; only `git`/`gh` read-only queries and source reads at
  `origin/develop`. Compliant.
- Workflow scope: **no** `.github/**` edit, no `scripts/**` edit, no rerun, no `workflow_dispatch`.
  The failing run `45413604588` was a `workflow_dispatch` I only **read**. Compliant.
- One integration candidate / no chain contact: #1826 and the `lane-0428-279-mcpcontract` branch
  were only read via `git show` / `gh` / `git ls-remote`. Compliant.
- No subagents (AGENTS 4.8): every step ran in this session. Compliant.
- Evidence lives only in baseharbor-plan under `evidence/`; nothing added to a product repo
  (no `.evidence/` directory). Compliant.
- Owner-scope boundaries respected: this is a **proposal** naming owner-scope files with
  `file:line`; the owner implements them. Compliant.

## END

END_DONE w95-0428-283-operatorfix: read-only fix-proposal complete. Root cause: the static/mcp
gate runs the **plain** `pre-release-candidate/baha` with **no** operator env, so
`baha target create mcp-static ...` (`tests/mcp/new-edit-static.py:83`) hits the intended
managed-environment fail-closed boundary (`operatorauth/authorization.go:285`); the integration
operator seam (`cmd/baha/ci_integration_operator_enabled.go`, `//go:build
baseharbor_ci_operator_testonly`) is neither compiled in (no `GOFLAGS` in the static gate,
`.github/workflows/pre-release-runtime-suite.yml:261-287`) nor given its env
(`BASEHARBOR_DEMO_OPERATOR_GATE`/`BASEHARBOR_TEST_RUNTIME`/`DEMO_ATOMIC_GATE` absent;
`:75-78`), and the seam rejects `runtime == "static"` / non-`atomic-*` target names
(`:102`, `:540-557`). Recommendation = **A (tag the static build, owner `.github/**`) + minimal
B1 (a *static-only* admission in `ci_integration_operator_enabled.go:102` + `:540-557`,
STOP-worthy / weakens the narrow operator-auth boundary) + B2 (demo harness exports the operator
env, `baseharbor-demo`). B1 is the one leg that weakens fail-closed and needs the owner's
A-vs-B go-ahead; A and B2 alone are insufficient. Evidence: `evidence/r28-welle6-2026-11-25/0428-283-operator-fix-proposal/round-1.md`.
