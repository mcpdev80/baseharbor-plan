# Bug-Hunt BF-01/BF-02 — up non-TTY panic + two-stage consent honours --yes

- Card/mission: mission-157.md (0427-157), blocker candidate (BF-01)
- Shift: r27-welle5-folge-2026-11-08 / round-1
- Worker session: laptop (mission-157), no subagents
- Planning repo verified (origin/main): ff38cf2e9b3a643ce8a7ee1350bd93e400a2c1c5 (`git ls-remote origin main`)
- Base SHA (cut-from, ancestor of first commit): 512dcd721ac3fb739bfd4cb0b990fd68d6794762 (`develop` HEAD at worktree cut)
- Product remote develop HEAD: cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c

## PLAN

- Read mission + akte hx2.md; attestation (base SHA, planning origin/main, product develop)
- Cut clean worktree from develop under /tmp/opencode/mission-157-wt
- Reproduce BF-01 on current develop with a failing Go test (Go stack trace before clean error)
- BF-01 fix: remove runtime.Stack panic path; return clean usage error that PRINTS the exact --confirm-candidate digest
- BF-02 fix: two-stage provider-impact consent honours --yes/non-TTY with fail-closed semantics (no data-deletion without explicit consent)
- CI-picked unit tests for both regression branches
- Local unit tests + VM smoke on named host + document CI job/trigger
- PR against develop HEAD (drift if needed), ls-remote + cleanliness, drop compose, post END

## Base attestation

- Product remote `origin develop` HEAD: `cdb4350a6b5ba614ec4f7fe6e9bd19e91055952c` (`git ls-remote origin develop`)
- Product remote `origin main` HEAD: `aff1532c2f6c6782a8c13afad83245d1351815e7` (`git ls-remote origin main`)
- Worktree cut from `develop` at `512dcd721ac3fb739bfd4cb0b990fd68d6794762` (`git log --oneline -1`). This SHA is an ancestor of the first commit.
- Planning repo `origin/main` (authoritative): `ff38cf2e9b3a643ce8a7ee1350bd93e400a2c1c5` (`git ls-remote origin main`)

## Findings

### BF-01 — up without --confirm-candidate panics (Go stack printed) on non-TTY; confirm-hash not surfaced
- class: ux / blocker-kandidat
- Reproduced on develop HEAD (512dcd721) with a failing test `TestM157ReproNoConfirmPanicPath` in `cmd/baha/m157_repro_test.go`.
- Output: `recordDeploymentBeforeMutation(ctx, r, "applying", "")` (empty confirm) prints 586 bytes to stderr BEFORE returning the error:
  - `goroutine 8 [running]:\n github.com/mcpdev80/baseharbor/cmd/baha.recordDeploymentBeforeMutation(...)\n\tcmd/baha/deployment_record.go:140 +0x10f4 ...`
  - Then error: `candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state` (exit 1).
- file:line (source of panic): `cmd/baha/deployment_record.go:140-141` — `n := runtime.Stack(buf[:], false); fmt.Fprint(os.Stderr, string(buf[:n]))` inside `if consent == nil` (lines 138-143).
- The digest IS printed once by `promptConfirmCandidateSubmission` (cmd/baha/app_candidate_consent.go:65-70) BEFORE the mutation, but the fail-closed path itself (line 142) returns only the generic message WITHOUT the digest, and the stack trace is noise.
- Impact: operator/automation sees a raw Go stack instead of the one-line `Re-run with --confirm-candidate <digest>` hint. Blocker candidate.

### BF-02 — two-stage provider-impact consent demands an interactive TTY; non-TTY auto-fails even with --yes
- class: ux / daemm
- Current behaviour at `cmd/baha/provider_change_confirmation.go:30`: `if noInput(ctx) || in == nil || !readerIsTerminal(in) { return ... impact-confirmation-required }`.
- `--yes` deliberately does NOT imply either acknowledgement (existing test `TestOrdinaryYesNeverAcknowledgesProviderEffects` asserts this fail-closed property).
- `invocationProviderChangeConsent` (cmd/baha/provider_change_context.go:40) reads `BASEHARBOR_PROVIDER_CHANGE_CONSENT` env (machine transport) or explicit context consent; it never promotes a generic `--yes` to a two-stage acknowledgement.
- Impact: automation (CI/scripts/dispatch) cannot converge an app whose provider impact plan has `confirmations_required == 2` (new managed provider / exposure gateway) without a pty.

## Scope decision: BF-02 yes-on-non-tty

- Mission 0427-157 item (2) is the authoritative driver: the two-stage consent stage must HONOUR `--yes`/non-TTY with the SAME fail-closed semantics as interactive; without `--yes` the refusal must remain correct.
- This changes an existing fail-closed property, so the fix is conservative: `--yes` grants the two consequence-acknowledgements only, and NEVER grants `DeleteData` (permanent data deletion still requires an explicit interactive/JSON decision). Non-destructive plans resolve; destructive plans without `--yes` still fail closed.
- Fail-closed is preserved at every layer: `ValidateProviderChangeConsent` still rejects incomplete consent; `DeleteData` still requires an explicit flag.

## END

END mission-157.md: (in progress — implementation + PR)
