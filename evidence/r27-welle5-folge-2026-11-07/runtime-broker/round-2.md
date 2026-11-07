# 0427-118 runtime broker — round 2 (corrections)

Lane: 0427-118-r2-correct (flash, fresh). Card: t-20261107-r27-runtime-broker-oras-missing-edge-readiness.
Chain: PR #1425 (mcpdev80/baseharbor). CODEX request-changes closed with this round.

Candidate SHA (final): 393a1969de2f5413920c5c1e3c2878f3c61cb93c
(first round-2 push: c24a3b1ef, continued — not replaced — by a test-only
commit pinning the executor-dependency decision matrix; same chain, same PR)

## PLAN

1. Reality check: fetch origin, verify origin/develop, PR #1425 head, card state — done.
2. Candidate continuity: origin/develop beb923fe6 merged into the #1425 chain (already at f1af4cded, verified ancestor) — done.
3. Fix (1): /readyz DEFAULT case mount-derived, env-waiver removed, genuinely-required stays RED — done.
   PLAN step notes: the round-1 waiver tests were replaced by mount-derived
   cells; the waiver env var no longer appears anywhere in the tree.
4. Fix (2): unverifiable OCI resolve can never qualify the mutable fallback; exec.ErrNotFound identity preserved errors.Is-capable — done.
5. Regressions: readyz-default-READY + unverifiable-oci-no-mutable-fallback cells, CI-collected (PR go-unit-tests) — done.
6. Evidence committed and pushed to baseharbor-plan origin/main — done (see commit below).
7. Push candidate to the PR head branch; ls-remote witness — done.
8. EIGNES-RUN: observe hosted CI run on the new SHA to terminal state — recorded below.
9. VM hygiene: no compose projects started by this lane; END posted.

## Base attestation and provenance (reality witnesses)

Planning repo verification (BEFORE first evidence commit):

    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
    https://github.com/mcpdev80/baseharbor-plan.git
    $ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote origin refs/heads/main
    67c0358c492f3fdf666ab0f7521fb571ce290eb6        refs/heads/main   (at start; advanced to 3d720629 meanwhile)

Product repo remote truth (measured via ls-remote / fetch ONLY; the quarantined
workers/baseharbor checkout was never cited):

    $ git ls-remote origin refs/heads/develop refs/heads/lane/0427-118-runtime-broker
    beb923fe6c4d8ede4d397a87490f3ac2eb2e65cc        refs/heads/develop
    f1af4cdedcb13d4d35d980c2c1ef36ec365ab1df        refs/heads/lane/0427-118-runtime-broker   (pre-push)

- Base ref cut point: the candidate continues the existing PR chain, whose merge
  commit f1af4cded already carries origin/develop beb923fe6 as a parent.
  `git merge-base --is-ancestor beb923fe6 HEAD` => true (witnessed).
- Ancestor proof for the new commit: `git merge-base --is-ancestor f1af4cded HEAD` => true.
- `git log --oneline origin/develop..HEAD` lists ONLY this chain's own commits:
    393a1969d test(controlplane): pin the executor-dependency decision matrix directly                        (this lane, round 2)
    c24a3b1ef fix(runtime): derive broker readiness from the mounts; hard-reject unverifiable OCI resolves   (this lane, round 2)
    f1af4cded Merge develop beb923fe6 into lane/0427-118-runtime-broker (base drift refresh)                  (same chain, base refresh)
    3ea8c055f fix(runtime): fail closed clearly on missing oras and name the blocking broker dependency      (same chain, round 1)
  No foreign candidate commit is carried.
- Post-push witness (final candidate):
    $ git ls-remote origin refs/heads/lane/0427-118-runtime-broker
    393a1969de2f5413920c5c1e3c2878f3c61cb93c        refs/heads/lane/0427-118-runtime-broker
  gh pr view 1425 => headRefOid 393a1969d, head repo mcpdev80/baseharbor.

## Branch-name note (exact-one-candidate)

The mission names `work/r27-runtime-broker` as the candidate branch; PR #1425 in
fact points at `lane/0427-118-runtime-broker` (head f1af4cde, matching the
mission's SHA). `work/r27-runtime-broker` does not exist on the remote
(`git ls-remote --heads origin work/r27-runtime-broker` => empty). To keep one
candidate per chain I pushed to the PR's actual head branch instead of creating
the named one, which would have produced a second branch for the same card. The
local branch in my worktree is named `work/r27-runtime-broker` but pushes
HEAD:refs/heads/lane/0427-118-runtime-broker only; it was never pushed under
that name (witness above). Recording this as a mission-vs-remote discrepancy,
not a scope choice.

## Gap 1 — /readyz default case (internal/controlplaneruntime/server_run.go)

Defect in round 1: with no executor client the probe 503'd unless
BASEHARBOR_RUNTIME_EXECUTOR_NOT_REQUIRED=true — an env-waiver, not a fix; a
default broker (no executor URL, complete valid mounts) could never be READY.

Fix: the client-absent branch now asks the mounted configuration whether the
executor is a dependency at all (brokerRequiresExecutor):
- executor URL configured => dependency (and an unbuildable client stays RED);
- else consult the SAME authority the request router uses
  (runtimeresourceapi.NewStaticAuthorizer on the bound permissions projection):
  a capability beyond metrics makes runtime-executor required — RED and named;
  an empty/default projection => not a dependency => READY from the checks that
  exist, no env switch anywhere.
Genuinely broken required dependencies stay fail-closed RED: the live executor
Check branch is untouched, AppRole/login failures stay RED (openbao), and the
URL-configured-client-unbuildable and permissions-requiring-executor cells
prove the RED halves. The env waiver was deleted (grep:
BASEHARBOR_RUNTIME_EXECUTOR_NOT_REQUIRED has no occurrences in the tree).

## Gap 2 — oras/OCI fail-closed tighter

cmd/baha/application_registry_source.go: every UNPRUEFBAR resolution (empty
reply, no immutable digest, or a reply that drops the pin it claims) now carries
the distinct hard-rejection identity ErrRegistryUnverifiable (bare node
errRegistrySourceUnverifiable, unwrapping to ErrRegistrySourceUnavailable for
caller classification). isHardRejection walks the chain by NODE IDENTITY
(including one level of joined errors) precisely so the unavailable alias can
never hide it; resolveUnavailable therefore excludes it, and with the mutable
development opt-in ON the fallback pulls nothing: an unverifiable image never
qualifies. Only a truly unreachable endpoint stays merely-unavailable and keeps
the documented opt-in behaviour byte-for-byte (regression cell included).
The artifact path (application_artifact_resolution.go) inherits the gate via
the same resolveUnavailable; its denial/local-store cells stay green.

internal/orgconfig: the mission pointed at source.go:231, where
`fmt.Errorf("...: %v", err)` destroyed the exec.ErrNotFound identity. The
current chain had already routed that call through the identity-preserving
run() helper and an IsNativeToolNotFound branch (round-1 3ea8c055f); the
residual hole was that run() re-wraps the *exec.Error with
`fmt.Errorf("%w: %s", err, detail)` (source.go:320), whose Unwrap reaches
exec.ErrNotFound only through exec.Error's own Unwrap — a fact
errors.Is(err, exec.ErrNotFound) happens to traverse but a node walk or a
different redaction loses. IsNativeToolNotFound now recognises the identity
explicitly at every chain node (*exec.Error via errors.As on the node, plus
one level of joined errors), so classifyNativeToolFailure maps it to the
actionable ErrNativeToolNotFound regardless of redaction shape. The digest-less
reply of an organization OCI source additionally carries the new
ErrOrgSourceUnverifiable identity, listed by isHardRegistryRejection —
opt-in=true never turns an unverifiable resolution into a mutable pull.

## Tests and CI collection

New cells (all deterministic unit tests, no runtime services needed):
- internal/controlplaneruntime/server_readiness_test.go:
  TestBoundBrokerReadyzDefaultWithoutExecutorIsReady,
  TestBoundBrokerReadyzEmptyPermissionsMountOnlyIsReady,
  TestBoundBrokerReadyzDefaultMountsWithEmptyPermissionsFileIsReady (production
  prepareServerDependencies seam), TestBoundBrokerReadyzPermissionsRequiringExecutorStayRed;
  the old waiver cells replaced (TestBoundBrokerReadyzFailsClosedWithConfiguredExecutor
  keeps the URL-declared RED half).
  Gap-1 RED witness (measured): TestBoundBrokerReadyzDefaultWithoutExecutor-
  IsReady, dropped unchanged onto the ROUND-1 tree (f1af4cded), FAILS there
  (default case answered 503 through the env-waiver branch — the CODEX
  defect); on the candidate it passes with the env switch deleted entirely
  (grep BASEHARBOR_RUNTIME_EXECUTOR_NOT_REQUIRED => 0 occurrences in the tree).
- cmd/baha/application_registry_source_unverifiable_test.go:
  TestUnverifiableResolveNeverQualifiesMutableFallback (five unverifiable reply
  shapes x opt-in off/on, zero pulls asserted),
  TestUnreachableResolveKeepsOptInFallbackScope,
  TestIsHardRejectionCoversUnverifiableIdentity.
- internal/orgconfig/source_oci_round2_test.go:
  TestNativeToolNotFoundIdentitySurvivesRedaction (raw, %w-redacted and joined
  chains; the negative "other tool failure" cell),
  TestUnverifiableOCIDigestReplyIsHardRejection (fake-oras, the suite's
  existing pattern; no host oras needed).
- internal/controlplaneruntime: TestBrokerRequiresExecutorMatrix pins the
  dependency decision directly (URL / metrics-only / other-capability /
  default-empty).

CI collection: the PR-gated validation `go-unit-tests` (job
"PR · Validation · go-unit-tests", ci.yml:797 dispatching
scripts/pr-unit-database.sh, which runs `go test ./... -count=1` against an
ephemeral postgres, scripts/pr-unit-database.sh:33) executes EVERY package
including the three new test files, on every push to this PR. Trigger:
pull_request synchronize with base develop and non-draft (ci.yml:12-16,762).
No workflow or trigger change is needed => no .github finding. The `validate`
and `release_source_preflight` jobs show "skipped" on PR events by their own
push/dispatch gates (ci.yml:256,55) — that is their designed scope, not a
coverage gap: go-unit-tests carries the PR-time coverage.

RED-then-GREEN (measured, candidate tree c24a3b1ef):
- Gap 2, cmd/baha: new cells placed against the ROUND-1 production code =>
  FAIL in every shape (empty-reply, no-digest-in-reply, reply-drops-the-pin,
  malformed-digest, pin-mismatch) plus TestIsHardRejectionCoversUnverifiable-
  Identity FAIL: without the identity, resolveUnavailable let opt-in=true pull
  the mutable tag. On this candidate: PASS (all shapes, opt-in off and on).
- Gap 2, internal/orgconfig: TestUnverifiableOCIDigestReplyIsHardRejection
  against the round-1 classifier is a plain ErrSourceUnavailable message and
  isHardRegistryRejection answers false => the opt-in path could downgrade an
  unpruefbar image; PASS on the candidate.
- Gap 1: the round-1 tree had no default-READY cell (only waiver cells); the
  new TestBoundBrokerReadyzDefaultWithoutExecutorIsReady and
  TestBoundBrokerReadyzDefaultMountsWithEmptyPermissionsFileIsReady fail on
  round-1 logic by construction (round 1 answers 503 unless the env waiver is
  set) and pass here; the RED halves (configured URL unbuildable,
  permissions-requiring-executor, live executor down, openbao login) pass on
  both trees, proving the fix did not soften required dependencies.
  (Mechanical note: against the round-1 tree the new orgconfig cells do not
  compile — IsUnverifiableOCIResolution/ErrOrgSourceUnverifiable do not exist
  there — which is the RED witness for that file; the cmd/baha cells compile
  and FAIL with the old classifier, shown above.)

Local verification on the candidate:
- go build ./... PASS; gofmt -l clean; go vet (changed packages) clean.
- bash scripts/source-readability-audit.sh PASS (all three ratchets).
- go test ./internal/orgconfig/ ./internal/runtimeexecutor/ ./internal/runtimebroker/ PASS.
- go test ./internal/controlplaneruntime/ -run Readyz PASS (9 cells incl. new).
- go test ./cmd/baha (whole package) — sole failure
  TestAppEditCommandCompleteProviderEditRunsRealLifecycle, environment-gated:
  it needs the CI postgres service; it fails identically at base f1af4cded on
  this host (witnessed: stash + rerun), not caused by this change.
- TestRunStartsTLSHealthReadinessAndProtectedAPI fails ONLY for the missing
  BASEHARBOR_TEST_DATABASE_URL on this host (same t.Fatal at base, CI provides
  the service in ci.yml).
- Post-commit working tree: clean at c24a3b1ef; after the RED-proof checkout
  detour the tree was restored with `git reset --hard HEAD` and `go build` plus
  every focused cell above was re-run green on the committed candidate.

## VM/docker hygiene

No containers or compose projects were started by this lane on any host
(the local docker daemon shows no baseharbor projects; no SSH test host was
used — this card names no VM smoke cell). Nothing to bring down.

## EIGNES-RUN (hosted CI on the candidate)

Superseded run note: 42374119919 (head c24a3b1ef) was cancelled by the
workflow's own concurrency rule (`cancel-in-progress: true`, ci.yml:19-20)
when my test-only push 393a1969d arrived on the same PR. No check failed: go-
vet, go-build, cli-gofmt, Source format, Trusted Plan and Focused Python were
already success; only go-unit-tests was still running when the newer run took
over. That is the designed replacement, not a diagnosis-driven re-run.

Terminal observation of run 42374471424 (head 393a1969d, event pull_request)
via `gh run watch` + `gh run view --json status,conclusion,jobs` (this lane):
    Jobs completed so far on 42374471424: Workflow policy, PR · Source format,
    PR · Trusted Plan, go-build, go-vet, cli-gofmt, Focused Python => success;
    Exact Candidate / Selected Runtime / consumer pins => skipped (gates);
    go-unit-tests => the covering suite, in progress at evidence-commit time;
    terminal state recorded in the follow-up evidence commit on main.

Local regression roster on the candidate (this lane, `go test -v`, candidate
tree 393a1969d, all PASS):
- controlplaneruntime: ReadyzFailsClosedWithConfiguredExecutor,
  ReadyzGreenWithAllPresentDependencies, ReadyzRedWhenExecutorReadyzFails,
  ReadyzDefaultWithoutExecutorIsReady, ReadyzPermissionsRequiringExecutorStayRed,
  ReadyzExecutorRecoveryTurnsGreenWithoutRestart,
  ReadyzDefaultMountsWithEmptyPermissionsFileIsReady,
  ReadyzEmptyPermissionsMountOnlyIsReady, ReadyzRedWhenOpenBaoLoginFails,
  BrokerRequiresExecutorMatrix.
- orgconfig: NativeToolNotFoundIdentitySurvivesRedaction,
  UnverifiableOCIDigestReplyIsHardRejection, OCIUnreachableFailsClosedNoFallback,
  OCIPublicDefaultHardRejection.
- cmd/baha: UnverifiableResolveNeverQualifiesMutableFallback,
  UnreachableResolveKeepsOptInFallbackScope,
  IsHardRejectionCoversUnverifiableIdentity plus the existing broker/registry
  pull/denial/local-store cells (all PASS).

## repo-rule compliance

- Read development guidelines and the card contract first; work stayed inside
  the write-set: cmd/baha/application_registry_source.go,
  cmd/baha/application_artifact_resolution.go, the two new cmd/baha test files,
  internal/controlplaneruntime/{server_run.go,server_readiness_test.go},
  internal/orgconfig/{source.go,source_oci.go} and the new orgconfig test.
  internal/runtimeexecutor/client.go keeps only the round-1 test-transport
  seam (untouched this round). cmd/baha/serve.go untouched; no .github or
  scripts edits (scope split honored).
- Mutations were local-first: focused `go test` per package, gofmt, go vet,
  source-readability audit, then the single push to the named candidate chain.
- CI efficiency: one coherent verification candidate per push; the intermediate
  run was cancelled by the workflow's own cancel-in-progress rule (no failure
  diagnosis, no extra matrix).
- Planning-repo zone verified before the first evidence commit (attestation
  above); evidence lives only under baseharbor-plan/evidence/….

## END

State at this END post: run 42374471424 (head 393a1969d) was still executing
its covering job PR · Validation · go-unit-tests, so the END line below is
QUESTION (the lane stays accountable and the run keeps being watched) instead
of idling unrecorded. When the watcher reports the terminal state, the record
is appended here and END_DONE is posted.

QUESTION 0427-118-r2-correct: round-2 fixes shipped on PR #1425 candidate
393a1969d (readyz default READY mount-derived, waiver removed; unverifiable OCI
never qualifies the mutable fallback; ErrNotFound identity preserved);
red/green regressions in the tree, awaiting my run 42374471424 go-unit-tests
terminal state.

- Candidate: 393a1969d on lane/0427-118-runtime-broker (PR #1425).
- Write-set honored: cmd/baha/* + internal/{controlplaneruntime,orgconfig,runtimeexecutor}/*;
  cmd/baha/serve.go untouched; no .github/scripts edits.
- Ready for CODEX re-review.
