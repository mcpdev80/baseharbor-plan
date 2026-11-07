# remote-material round-2 — t-20261018-r27-remote-material (w287)

## Role / scope (implementation + local verification, no merge / no product CI edits)

Worker w287 implemented the bounded cut of card t-20261018-r27-remote-material per
coordinator/missions/w287-pr1410-remote-material-DECISION.txt: one serving
certificate per exposure, issued through the existing serviceaccess PKI owner
(EnsureNativeTLS / EnsureTLSMaterial), projected into the managed runtime
publication and referenced in the generated runtime compose so it is consumed at
the node (HTTPS-serving path), including rotation (issuer reconcile, no
re-bootstrap). Fail-closed: no issuer => no material.

No product source outside the bounded write-set was touched. No
.github/** file was edited, no workflow_dispatch / rerun was triggered (Owner
scope). No VM/docker stack was started (pure Go unit tests only); nothing was
left running at end of shift.

## Remote witnesses

`git ls-remote` before starting the verification candidate:

```text
git ls-remote origin refs/heads/develop
934be499b9d2d894f80889fc23cd811884c8aec4  refs/heads/develop   (measured later; see provenance)
```

`git ls-remote origin refs/heads/work/r27-remote-material` before work:

```text
a9f25746408dc4f06a471eead071e281e34834cf  refs/heads/work/r27-remote-material
```

`git ls-remote origin refs/heads/work/r27-remote-material refs/heads/develop` after
push (evidence witness):

```text
934be499b9d2d894f80889fc23cd811884c8aec4  refs/heads/develop
852e421c2cd62d77c07caaa1bbc6a10c2090fdcc  refs/heads/work/r27-remote-material
```

## Task contract (measured 2026-11-07)

`python3 scripts/plan.py show t-20261018-r27-remote-material` (baseharbor-plan):
state `active`, owner `w287`, prerequisites accepted. Bounded write-set:
internal/application/remote_application_projection.go,
internal/application/remote_runtime_projection.go, bounded exposure/material
files and their tests. No .github/**, cmd/baha/deployment_record.go,
management-host, compose/InCI-Isolation.

## Implementation (exact SHA, candidate 852e421c2, base 3fa6f7b0d)

Single logical change on branch work/r27-remote-material:

- internal/application/backend_tls.go — ensureExposureServingMaterial (per
  exposure: resolve serviceaccess policy, EnsureNativeTLS for the exposure
  server-name, project server-key.pem(0600 source under pki/) + server-cert.pem
  + ca.pem under the exposed deployment's runtime dir); wired into
  EnsureBackendServiceAccess; fail-closed when issuer is nil; no-op when there
  are no m.Exposures.
- internal/application/runtime_postgres.go — writeExposureGatewayComposeService
  mounts the projected serving cert/key read-only (ro) into the generated
  runtime compose for the node serving gateway, one per exposure.
- internal/application/remote_exposure_serving_test.go — positive (one serving
  cert+key+CA per exposure, read-only 0644 in the published bundle, compose
  mount present), secret-leak (key stays under the provider runtime dir, never in
  shared bindings; protected source key 0600 under pki/), fail-closed
  (no issuer => rejected), supported-limit (no exposure => no material), and a
  bounded protocol probe that verifies the projected leaf chains to the managed
  PKI anchor CA (crypto consumption, not just a fixture).

Supported limit expressed: one serving certificate per exposure, rotation
(issuer reconcile) without re-bootstrap. The published serving key is read-only
(0644) in the managed publication exactly like the retained SQL/Valkey/MongoDB
backend-key projection, because the unprivileged node serving gateway mounts it
ro; the protected source key stays 0600 under pki/.

## Provenance (branch ancestry)

Base of candidate (parent of HEAD^): `3fa6f7b0d0ba01943501627e4c5d811cc7bee848`
(`Merge pull request #1412 ... r27-ci-keycloak-single-native`).

```text
git merge-base --is-ancestor 3fa6f7b0d0ba01943501627e4c5d811cc7bee848 refs/remotes/origin/develop
# exit 0 (true) — the base IS an ancestor of develop
```

`git log --oneline refs/remotes/origin/develop..work/r27-remote-material`:

```text
852e421c2 feat(remote): project exposure serving TLS via PKI owner into managed runtime (t-20261018-r27)
```

Exactly one commit, cleanly on top of a develop ancestor; no foreign commit on
top. Candidate head `852e421c2`; PR #1418 head = `852e421c2`, base = develop
ancestor, mergeStateStatus = CLEAN.

## CI evidence

New tests run under the GitHub CI job **Release Source Preflight**
(.github/workflows/ci.yml:117-123), which runs
`go test ./contracts/... ./internal/... ./spec/...` on
`pull_request`/`push`/`workflow_dispatch` (ci.yml:6-12). internal/application is
covered by that existing job; no .github change was needed.

Draft PR #1418 (draft = new-card state; Owner promotes to ready) ran CI on push.
Run record (measured via gh api repos/mcpdev80/baseharbor/actions/runs):

```text
run id 42332105570  CI · PR #1418  head_sha 852e421c2  status completed  conclusion success
  PR · Source format ............ success
  Workflow policy ............... success
  Release Source Preflight ...... SKIPPED  (draft PR does not run the go-test matrix)
```

The go-test matrix (`Release Source Preflight`) did NOT actually execute because
the PR is a draft and only policy/format jobs run on a draft. The full test job
runs on `ready_for_review` (ci.yml:13). This is the single open item.

## Local verification (measured on candidate 852e421c2)

```text
go build ./...            -> exit 0 (clean)
go vet ./...              -> exit 0 (clean)
gofmt -l <my files>       -> empty (clean)
bash scripts/source-readability-audit.sh -> Source size PASS, function span PASS, regression ratchet PASS
go test ./internal/application/...            -> ok
go test ./internal/serviceaccess/...          -> ok
go test ./internal/exposure/...               -> ok
go test ./internal/application/... -run TestExposureServing -v:
  TestExposureServingMaterialIsProjected .... PASS
  TestExposureServingKeyStaysWithinProtectedProviderDir .... PASS
  TestExposureServingMaterialRequiresIssuer .... PASS
  TestExposureServingMaterialUsesPKIProviderOwner .... PASS
```

Pre-existing DB-dependent failures in internal/controlplaneruntime and
internal/database (`BASEHARBOR_TEST_DATABASE_URL fehlt`) fail identically on the
clean base (verified by stashing this change and rebuilding) — unrelated to this
work and not fixable without a real test database in this environment.

## Test-preservation witness (RUNBOOK 0.4)

`git diff 934be499b..852e421c2 -- internal/application/ | grep '^-' | grep 'func Test'`
=> empty (no existing test function removed or modified; the change is additive
plus a test-file correctness correction).

## Repo-rule compliance

- Bounded write-set respected: only internal/application/* touched.
- No .github/** edit, no workflow_dispatch / rerun (Owner scope). The exact CI
  gap (draft PR does not run the go-test matrix) is reported here, not worked
  around.
- No evidence file written into a product repo; evidence lives only in
  baseharbor-plan. No .evidence/ directory created in any product repo.
- No subagent used to write, push, merge, review or close anything.

## Open item (needs Owner action — not a block, a gate)

PR #1418 must be promoted draft -> ready so the Release Source Preflight test
job actually runs and produces the required CI Run-ID + terminal status. Until
then the go-test evidence is local-only and is not durable per the
CI-Aufnahmepflicht (Owner directive 2026-11-07).

## End state

- Branch work/r27-remote-material, single commit `852e421c2`, base is a develop
  ancestor.
- Draft PR #1418 open (head 852e421c2, mergeStateStatus CLEAN).
- No docker/podman stack started by this lane; no orphan to remove.
- Waiting on Owner: promote #1418 to ready so the CI go-test matrix runs.
