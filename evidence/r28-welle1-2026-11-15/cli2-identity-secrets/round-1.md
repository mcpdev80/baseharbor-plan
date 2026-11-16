# r28-welle1 · t-20261114-r28-cli2-identity-secrets (0428-057) — round-1

Shift r28-welle1-2026-11-15 · card t-20261114-r28-cli2-identity-secrets · mission-welle2-057.md
Worker session: `2c3555a6-67f8-4c39-80df-6f22b2978d4c` · model: Ornith (pending spawn-verify)

## PLAN (numbered, per AGENTS 4.4)

1. Read mission, card, owner brief, command-map, code-entry-index; establish ground truth via git ls-remote.
2. Claim the task via `plan.py claim` before any change; push a claim witness.
3. Cut candidate branch from `cli2-env-policy-head` @ `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc` (single-base rule); attest base SHA is ancestor of first commit; `git log` shows only own commits.
4. Implement configured human authorization for service-credential reveal via OpenBao while keeping workload access independent; fail-closed; no secret in status/logging paths.
5. Map every added/changed test to an existing CI check + trigger; block until actual execution is proven.
6. Run `go build ./...`, `go vet ./...`, focused tests at candidate SHA; record actual results at exact SHA.
7. Draft PR (#1594 base retained; this chain base = cli2-env-policy-head) with `--draft`, title carrying 0428-057; keep draft flag.
8. Commit evidence to baseharbor-plan only; publish to origin/main; run `git log` witness.
9. Bring down any started compose/runtime projects by last action; post END.

## REALITY WITNESSES (git ls-remote, current)

- baseharbor develop: `0e9ccb582f5bdcdc74049bbe3996263cdce6500c`
- baseharbor main: `aff1532c2f6c6782a8c13afad83245d1351815e7`
- baseharbor cli2-env-policy-head (mission base): `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc`
- baseharbor-plan origin/main: `fecd71f84888170246f75fe851a127b7744f9c1e` (HEAD at start of shift)

## BASE ATTESTATION

- Base product ref (cut from): `cli2-env-policy-head` @ `018b4e58a3aaf417f61b6b1c2bb37c1c17a49ccc` (contains env-registry 054 AND env-policy 053 content — verified, mission single-base rule).
- PR base = `cli2-env-policy-head`.
- Will show `018b4e58a` is an ancestor of first commit and `git log` lists only own commits.

## CURRENT-STATE ANALYSIS (pre-implementation, read-only)

- Reveal path: `baha app env --reveal`, `baha app creds --reveal`, and `applicationsecret.Service.Get` resolve the app via `resolveApplication` (cmd/baha/app_context.go:99), which calls `localWorkloadScope`, then `authorizeApplicationOperation` -> `authorizeMCPOperation` (cmd/baha/mcp.go:267).
- For a local `dev` environment with no OIDC principal, `AuthorizeMachineOperation` (internal/operatorauth/authorization.go) reaches the `trusted-local` allow path at lines 247-251. The workload runtime read reaches the `local-runtime` allow path at lines 241-245.
- Consequence: a human reveal and a runtime read currently CONVERGE on the same authorization decision. There is NO distinct human-operator gate on reveal that the runtime identity cannot satisfy. The brief ("configure human authorization for reveal while keeping workload access independent; prevent unauthorized alternate path via env files, machine output, export, API") is open on the exact gate mechanism.

## DECISION POINT — scope lock with owner

- Posted a QUESTION to the coordinator (session `d4212c96`) at shift start asking to confirm the reveal-gate mechanism:
  - (A) explicit separate human-operator-auth gate on reveal (authenticated operator / guided interactive consent), workload reads keep trusted-local/runtime access; or
  - (B) a distinct machine op category (e.g. `secret.reveal`) that reveal routes through, separate from `app.environment`/`app.connection`; or
  - (C) tighten the trusted-local reveal path so a bare runtime identity cannot reveal.
- Also asked: local/dev only vs managed; whether a new machine op id / new internal seam is in-scope or reserved.
- Not proceeding to implementation until this is confirmed, per AGENTS (do not guess or quietly weaken policy).

## SCOPE / WRITE-SET (card + brief)

- Own: reveal authorization slice for `app secret` / `app env` / `app creds` reveal and the OpenBao read path that serves human reveal.
- Reserved (NOT edited): `cmd/baha/commands.go`, shared parser/machine registry, generated command index (CI-owned), `.github/**` (Owner scope), release notes, generated indexes.
- Frost: NO merge, NO ready_for_review.

## EVIDENCE LAYOUT (baseharbor-plan ONLY, never a product repo)

- Path: `baseharbor-plan/evidence/r28-welle1-2026-11-15/cli2-identity-secrets/round-1.md`
- No `.evidence/` directory in any product repo. No main-branch writes in baseharbor.

## END

- BLOCKED (awaiting owner scope lock). Posted QUESTION to coordinator; END line recorded.
