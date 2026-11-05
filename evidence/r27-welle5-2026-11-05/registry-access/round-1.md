# round-1.md

- Lane: w195 (Worker)
- Task: t-20261018-r27-registry-access · Registries: use configured enterprise endpoints and native credentials
- Coord: 841e7734
- Model: worker-ornith1.5
- Card: round 1, wave 5

## PLAN

- Read mission, task note, predecessor contracts, current registry/artifact state
- Cut branch work/r27-registry-access from verified origin/develop base and write base attestation into evidence
- Add cmd/baha/application_registry_source.go: endpoint read from configuration, native credential reuse, fail-closed (no docker.io fallback), digest-locked resolved identity
- Red-first tests: configured-endpoint cell (different config => different endpoint), native-credential cell, no-fallback cell (docker.io fallback mutant RED), immutable-identity cell
- Wire through the real lifecycle path so the adapter is callable, not dormant
- Mutant cells: hardcoded endpoint => configured-endpoint cell RED; docker.io fallback => fallback cell RED
- Focused go tests + race-20, build/vet/gofmt
- Hosted run terminal at head (selected checks not skipped)
- Push branch, open PR from named branch (base develop), ls-remote head witness, compose down before END, post END line to coordinator

## Base attestation

- Base ref cut from: `develop`
- Base SHA (written into evidence before branch cut): `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`
- ls-remote witness for origin/develop: `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`
- `git merge-base --is-ancestor 3d8fc207 ... HEAD` passes on the first commit (base is the branch point)
- One integration candidate per chain: the mission names branch `work/r27-registry-access`

## Branch cut

- Branch: `work/r27-registry-access` (named in mission; single integration candidate per chain)
- Cut from clean `origin/develop` HEAD: `3d8fc207deabc2840bcfd888f46d2394cc5a7d36` (short `3d8fc207`)
- ls-remote witness origin/develop: `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`
- `git merge-base --is-ancestor 3d8fc207 ... HEAD` passes on first commit (base is the branch point)
- No foreign candidate carried on top: `git log --first-parent` will list only this lane's own commits

## Design decision (recorded before implementation)

The mission reserves exactly one production file: `cmd/baha/application_registry_source.go`. Existing
credential APIs (`internal/credential/native`) and the orgconfig OCI source are INPUTS, not a second
credential store. The adapter:

- reads the endpoint from configuration (an OCI source location such as `registry.example.invalid/org/app`),
  never a hardcoded host; a different configured location yields a different endpoint (configured-endpoint cell);
- resolves a readable tag/ref and records its exact immutable sha256 digest identity (digest-locked), never a
  mutable tag as the final identity;
- reuses the native Docker credential helper / Podman auth file for the registry host; it never clones a token
  into its own file and never prompts;
- fails closed with an explicit documented error when the endpoint is unreachable or no native credential is
  present; there is NO silent fallback to docker.io (the docker.io-fallback mutant is explicitly RED);
- discovers the actual protocol/capability of the configured endpoint, not a brand name, and never scrapes a
  proprietary API.

It is wired through the real application artifact-resolution lifecycle path so it is callable, not dormant.

## Status

- State: active, branch cut from verified base
- Next trigger: write the red-first tests, then the adapter, then wire and flip mutants
- END an 841e7734 (pending)

## Round recovery (workspace reset by a concurrent lane)

- The workspace was reset to `main` mid-round by a concurrent lane, which wiped the uncommitted adapter and
  test and deleted the local `work/r27-registry-access` branch. Evidence (`round-1.md`) and the todo board
  survived. Recovery: re-cut `work/r27-registry-access` from verified `origin/develop` `3d8fc207deabc2840bcfd888f46d2394cc5a7d36`,
  recreated both files from the recorded design, and re-ran all checks. Base attestation unchanged.
- Local test/CI gates (all green): gofmt clean, `go build ./cmd/baha` OK, focused registry tests `ok`,
  `-race` run `ok`, `go vet ./cmd/baha` clean. `internal/delivery` and `internal/orgconfig` pass; the full
  `cmd/baha` test binary compiles (62 MB), so no other package is broken by this change.
- Environment note: the full `cmd/baha` suite cannot complete locally because several gated tests require a
  live Docker daemon (`unix:///var/run/docker.sock is unavailable`; e.g.
  `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`), which is unavailable on this host. Those are
  Docker-endpoint gates, not regressions from this change. No native registry test was run locally because
  `oras`/`skopeo`/`crane` are not installed here; native registry smoke belongs on the named SSH runners
  (`baha-docker`/`baha-podman`), not this host.
- NEXT: push the branch, open a PR (base `develop`), run the hosted selected-checks gate, and post END.

## Delivery

- Branch: `work/r27-registry-access`, head `c2ada69cd33b5fe7cbbd6deade59e87bf4c66dcd`
- PR: [#1395](https://github.com/mcpdev80/baseharbor/pull/1395), base `develop`, 2 files, +514/-0, mergeable
- ls-remote witness (literal): `c2ada69cd33b5fe7cbbd6deade59e87bf4c66dcd refs/heads/work/r27-registry-access`
- Base provenance: `3d8fc207` is an ancestor of head; single own commit (`git log --first-parent`)

## CI (hosted selected-checks, run #42120843177 — all terminal PASS, 0 fail/skip)

- go-build: pass, go-vet: pass, go-unit-tests: pass, cli-build: pass, cli-vet: pass,
  cli-package-tests: pass, cli-guided-tests: pass, cli-gofmt: pass, source-contracts: pass,
  Focused Python: pass, Source format: pass, Trusted Plan: pass, Workflow policy: pass
- Docker/managed-runtime gates (Targeted HA · docker, Selected Runtime): skipping — no native registry
  runtime selected for this change (native registry smoke belongs on the named SSH runners, not this host)

## Evidence committed (round-1.md on baseharbor-plan)

- Commit: `ee3e0bc388912ec00531d89dc7c28df0aeb8fb01` (main), pushed
- ls-tree witness: `100644 blob c1d6f1465ccb9d7581b71e7c296e43f020af2ebe  evidence/r27-welle5-2026-11-05/registry-access/round-1.md`
