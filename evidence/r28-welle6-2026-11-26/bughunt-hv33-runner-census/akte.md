# Bug-hunt H-V33 — Runner prerequisites census (CI cells)

Lane: w159-0428-224-hunt-v33 · Mission: coordinator/missions/hunt-v33-runner-census.txt
Date: 2026-11-26 · Type: pure FINDING duty, no product changes, no PR.

## PLAN

1. Read mission file and establish numbered plan in all plan places (board JSON file written;
   native todowrite tool NOT exposed by this session, so leg (0) skipped per dispatch instruction).
2. Establish remote truth: baseharbor develop SHA via `git ls-remote` on the GitHub remote. DONE.
3. Fresh read-only checkout of develop in own zone under workers/. DONE.
4. Census workflow jobs: external programs invoked (docker, podman, go, git, python3, ssh, oras, jq, gh, ...). DONE.
5. Trace code paths per cell to external program invocations (exec sites in Go). DONE.
6. Flag invocations lacking availability guards or version pins; flag undocumented prerequisite cells. DONE.
7. Cleanliness witness before/after (no containers started). DONE — see ## cleanliness.
8. Write this akte, commit with lane identity, push to baseharbor-plan origin/main. IN PROGRESS.
9. Verify evidence on origin/main and post END line. IN PROGRESS.

## base attestation and witnesses

Real planning repo check (`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`):

    origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
    origin  https://github.com/mcpdev80/baseharbor-plan.git (push)

Remote truth for the source examined:

    $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
    f7540e591609e0db6453e9b690fbb5d6686448a2    refs/heads/develop

Read-only checkout: workers/w159-0428-224-hunt-v33-wt/bh (depth-1 clone of develop, HEAD f7540e591609e0db6453e9b690fbb5d6686448a2).
No branch was created and no PR opened (findings-only mission), so branch-provenance tests do not apply.
The `git remote -v` run in the workers bookkeeping repo showed both `origin` and `lane-origin` point at
ssh://git@github.com/mcpdev80/baseharbor.git; all fetches in this lane used the explicit GitHub HTTPS URL.

## Method

- Enumerated every job and `runs-on` in the 20 workflows under .github/workflows (develop f7540e59).
- Extracted external program invocations from workflow `run:` steps and `scripts/*.sh` / `scripts/*.py`.
- Extracted host-side invocations from Go sources: exec.Command/CommandContext and exec.LookPath sites
  (187 CommandContext + 90 Command call sites), and distinguished them from in-container execs
  (`docker/podman exec` into provider images — those depend on image contents, not on the runner).
- Compared each invocation against availability guards (LookPath / `command -v` / install step) and version pins.

## Runner image facts used (GitHub-hosted ubuntu-latest / ubuntu-24.04 / ubuntu-26.04)

Preinstalled by GitHub: git, curl, wget, tar, jq, unzip, zsh, gh, docker (CLI+compose plugin), python3, node.
NOT preinstalled: podman, quadlet/system-generator, oras, uidmap, slirp4netns, dbus-user-session,
bao, valkey-cli/redis-cli, psql client tools, pg_dump/pg_isready, certutil, update-ca-certificates,
dockerd-rootless-setuptool.sh, go (on ubuntu-26.04 without actions/setup-go).

## Per-cell census (external programs, guard status)

Legend: guard = explicit availability check (exec.LookPath / `command -v` / install step) or version pin;
"none" = invoked directly with no check found in the develop sources examined.

### .github/workflows/ci.yml (CI · Source & Quality)

- Most jobs: actions/checkout + actions/setup-go + `go build/test/vet` — go pinned via setup-go; git preinstalled. Guarded adequately.
- Targeted HA · docker (l.179, ubuntu-latest) and Targeted HA · podman (l.221, ubuntu-26.04):
  run scripts/ci-install-oras.sh (oras pinned 1.3.6 + sha256 + version print — good pattern) then baha doctor;
  podman cell relies on the ubuntu-26.04 image shipping podman (no explicit install/pin). H-33-02.
- Workflow policy job calls `jq` (preinstalled, unpinned). PR · Exact full Pre-Release (l.702–741) polls with
  `gh api` + `jq` inline, no `command -v` guard. Minor (H-33-07).
- ci.yml:454 invokes `docker compose` (compose v2 plugin preinstalled on ubuntu-latest); no `docker compose version`
  guard in that step. doctor.go:94 checks compose at runtime, but this is a direct workflow call.
- Runner Interface job (l.1022) prints zsh/fish via `command -v` — a diagnostics-only soft probe; cells that need
  zsh/fish (Validation matrix) do not hard-fail when they are absent. H-33-08.

### docker-runtime-acceptance.yml (Runtime · Docker Core)

- docker + compose plugin: preinstalled, no guard or version pin anywhere in the workflow. H-33-02.
- ci-install-oras.sh used in two jobs (guarded/pinned).
- Rootless jobs use scripts/ci-core-rootless-runtime.sh: `sudo apt-get install -y uidmap slirp4netns
  dbus-user-session` (l.7) unpinned and network-dependent, `apt-get install -y "docker-ce-rootless-extras=$extras_version"`
  (l.37) version-pinned after `command -v dockerd-rootless-setuptool.sh` check (guarded), `apt-get install -y podman` (l.63)
  unpinned. H-33-05.

### podman-acceptance.yml (Runtime · Podman Core)

- Runs on ubuntu-26.04; podman used with no install step, no version pin, no `command -v podman` in the workflow
  (Go-side doctor LookPaths it). quadlet generator located via `command -v podman-system-generator ||` fixed paths (l.239).
- ci-install-oras.sh pinned. `jq` used. Declares "podman compose is forbidden" (l.264) — consistent with Quadlet path. H-33-02.

### mcp-lifecycle-acceptance.yml, observability-acceptance.yml, nextjs-greenfield-e2e.yml

- Same pattern: docker/podman via image (unpinned, unguarded), oras pinned via installer, quadlet located with
  `command -v` + fallback paths, `docker compose` used directly in greenfield (l.48–57) unguarded.
- nextjs cell additionally depends on docker build of `node:24.21.0-alpine` base image (pinned in the adapter's
  generated Dockerfile, internal/development/nextjsadapter/adapter.go:206 — image pin OK).

### runtime-s3-acceptance.yml

- Uses container `entrypoint: ["sh", "-c"]` (l.114/224) inside images, plus `docker compose ... exec -T seaweedfs weed shell`
  (l.196) — provider-image dependency (weed) not documented as a cell prerequisite. Host side: docker only. H-33-03.

### runtime-broker.yml

- `docker compose ... down -v || true` cleanup (l.317/442), docker unguarded/unpinned. oras not used.

### host-trust-owned-e2e.yml

- ubuntu-24.04, docker + mkcert-style local CA flow; host-trust Go path uses LookPath guards
  (update-ca-certificates/update-ca-trust/certutil, internal/hosttrust/hosttrust.go:469–560) — guarded, with
  documented sudo fallback (LookPath("sudo") at l.556).

### pre-release.yml, pre-release-runtime-suite.yml, targeted-integration.yml, targeted-demo-acceptance.yml

- The heavy runtime matrix: docker (ubuntu-latest) / podman (ubuntu-26.04) via image, no pin/guard (H-33-02);
  oras via ci-install-oras.sh in many jobs (pinned); `jq` in suite l.452; `gh api` in suite l.100–103;
  `base64 --decode` in targeted-demo-acceptance l.107 (H-33-07).
- pre-release.yml l.1503/1720/1937: `uses: actions/setup-node@v6` — tag-pinned only, not SHA-pinned (H-33-04);
  setup-python in artifact-gc.yml l.28 and pre-release.yml l.395 also tag-ponly.
- Internal reusable-workflow calls (ci.yml, pre-release.yml, release.yml, targeted-demo-acceptance.yml) are
  path-only, which is inherent to same-repo reuse; noted as informational.

### release.yml / runtime-image.yml / pages.yml / renovate.yml / receipt-post-run.yml / artifact-gc.yml

- Third-party actions SHA-pinned with tag comments (goreleaser v7, docker/* v3–v6, actions/attest,
  actions/configure-pages, actions/deploy-pages) — good.
- scripts/publish-four-part-hotfix.sh:17 hard-checks `go git gh tar sha256sum` via `command -v` — the reference
  guard pattern other cells lack.
- artifact-gc.yml: python via setup-python@v5 (tag-pinned), talks to api.github.com with Python stdlib (no gh) — fine.

### Go host-side (baha on every runtime cell)

Guarded (LookPath before exec, or install-with-consent):
- git: 23 LookPath sites (internal/development/workspace_git.go:391/415/436, source_pull.go:253,
  cmd/baha/app_inspect_remote.go:51 …).
- podman: 8 LookPath sites (providers/runtime/podman/*, health/doctor.go:66).
- docker: 2 LookPath sites (providers/runtime/docker/provider.go, health/doctor.go).
- systemctl (3), sudo (hosttrust.go:556), certutil, update-ca-certificates/update-ca-trust, valkey-cli and
  redis-cli (cmd/baha/app_access.go:74–76), psql (app_access.go:34 — guarded INTERACTIVE path),
  xdg-open, journalctl, baseharbor-node-connector, podman-system-generator.
- oras host binary: LookPath + pinned 1.3.6 installer with checksum + consent prompt
  (cmd/baha/oras_setup.go:24/32/45); orgconfig falls back with classifyNativeToolFailure (source.go:206–236).

Unguarded host execs (invoke directly; failure is a raw exec error at runtime):
- internal/development/pinned_git_archive.go:48 `exec.CommandContext(..., "git", "-C", ..., "archive", ...)` —
  git without LookPath (22 other git sites guard it; inconsistent). H-33-01.
- internal/openbao/bootstrap_auth.go:163 and :248 `exec.CommandContext(ctx, "sudo", ...)` — sudo without LookPath
  (hosttrust.go:556 shows the guarded pattern). H-33-01.
- cmd/baha/dev_hosts.go:206 `exec.CommandContext(ctx, "sudo", "--", binary, ...)` — same. H-33-01.
- internal/stableid/lock_probe.go:146 `exec.Command("go", "build", ...)` — requires a go toolchain on PATH at
  product runtime; on production workstation targets go is NOT a documented prerequisite. H-33-06.
- Host `psql` in non-interactive paths: cmd/baha/runtime_credential_rotation.go:230/244 and
  internal/application/shared_backends_runtime.go (pg_isready) exec psql/pg_isready with no LookPath;
  app_access.go:34 guards the interactive path only. H-33-01.
- In-container python3 / id / sh / find / tar / curl (update_ha_recovery_source.go:162/172, app_broker.go:322,
  app_traces.go:178/200, volume_recovery.go:114/163) depend on the provider/helper IMAGE, not the runner —
  belongs to H-33-03 (image prerequisite documentation), not a runner gap.
- `bao` binary: referenced only in unquoted heredoc docs (e.g. cmd/baha/app_docs_ee.go) — no host exec found;
  not a gap.
- ssh/scp: no direct exec found in Go paths (git-over-ssh and HTTPS used instead); `git` remains the prerequisite. H-33-09 (no gap).

## Findings (each with a proposed card line)

- H-33-01 — Unguarded host execs: git (internal/development/pinned_git_archive.go:48), sudo
  (internal/openbao/bootstrap_auth.go:163,248; cmd/baha/dev_hosts.go:206), host psql/pg_isready
  (cmd/baha/runtime_credential_rotation.go:230; internal/application/shared_backends_runtime.go).
  Proposed card: "Add exec.LookPath guards and clear prerequisite errors to the remaining host-side
  exec sites (git archive, sudo fallback, psql/pg_isready probes), matching app_access.go/hosttrust.go patterns."
- H-33-02 — podman (and docker/compose) have no version pin or availability guard in any CI cell; they are
  implicit ubuntu-26.04/ubuntu-latest image contents (podman-acceptance.yml, pre-release matrix, targeted-integration.yml,
  nextjs-greenfield-e2e.yml:48–57 `docker compose` unguarded). Runner-image drift can silently change engine behavior.
  Proposed card: "Add a pinned engine-prerequisite preflight (podman/docker + compose version print and a
  minimum-version gate) at the top of each runtime CI job, or a documented supported-version contract."
- H-33-03 — Container-internal external-command dependencies are undocumented per provider image
  (python3/id via ExecProject in Patroni HA paths, sh -c in app_broker.go:322/app_traces.go:178 and
  runtime-s3-acceptance.yml:114/224, weed shell at runtime-s3-acceptance.yml:196, find/tar in
  internal/runtime/volume_recovery.go:163). A slim provider image breaks these paths with no CI until the runtime gate.
  Proposed card: "Catalogue in-container external-command requirements per provider image (Dockerfile/providers
  or docs/reference/platform-support.md) and add an image-prerequisite check step to the provider image CI."
- H-33-04 — Partial action-pinning inconsistency: `uses: actions/setup-node@v6` (pre-release.yml:1503,1720,1937),
  `actions/setup-python@v5` (artifact-gc.yml:28), `actions/setup-python@...` missing comment pin at pre-release.yml:395,
  while all third-party actions elsewhere are SHA-pinned. Proposed card: "SHA-pin every actions/* reference and add
  a workflow-policy.sh check that fails on tag-only pins for external (non-self) action references."
- H-33-05 — Unpinned apt-get prerequisites in CI: `sudo apt-get install -y uidmap slirp4netns dbus-user-session`
  (scripts/ci-core-rootless-runtime.sh:7) and `apt-get install -y podman` (l.63), network-dependent and version-drifting;
  contrast the pinned docker-ce-rootless-extras install at l.37. Proposed card: "Pin or checksum rootless/podman
  apt prerequisites in CI bootstrap, or document the accepted image-version drift risk."
- H-33-06 — Product code shells out to the `go` toolchain at runtime (internal/stableid/lock_probe.go:146
  `exec.Command("go", "build", ...)`) with no LookPath and no documented host-go prerequisite for workstation cells;
  the goadapter pins versions only as advisory strings (internal/development/goadapter/adapter.go:88).
  Proposed card: "Make the go-toolchain dependency of the lock probe explicit (LookPath + prerequisite error,
  or precompiled helper), and document whether `go` is a supported-host requirement."
- H-33-07 — Implicit base-image utilities without guard: `gh`+`jq` inline in ci.yml:720–741 and
  pre-release-runtime-suite.yml:100–103, `jq` in pre-release-runtime-suite.yml:452 and ci-workflow-policy.sh,
  `base64 --decode` in targeted-demo-acceptance.yml:107 (vs the Python-stdlib approach in develop-ecosystem-source.py).
  Low severity (preinstalled), but they belong in a documented prerequisite matrix. Proposed card:
  "Document the runner-preinstalled toolset each cell relies on (gh, jq, base64, zsh, fish) in a CI prerequisites reference."
- H-33-08 — Soft-only shell probes: zsh/fish only printed via `command -v` in PR · Runner Interface / Validation cells
  (ci.yml:349–350,1261–1262, pre-release.yml:345–346); if the image loses them the cells that actually exercise
  shell integration would not fail fast. Proposed card: "Hard-gate zsh/fish availability in cells whose tests
  require them, keeping the diagnostics-only jobs as soft prints."
- H-33-09 — No gap: direct ssh/scp exec was not found in Go host paths; remote git sources go through `git`/HTTPS.
  (Recorded so the census is complete, no card.)

Fund count: 8 findings (H-33-01 … H-33-08), plus one explicitly-checked no-gap line (H-33-09).

## repo-rule compliance

- No product files edited; read-only clone in workers/w159-0428-224-hunt-v33-wt (this finding-lane zone IS the
  deliverable location; no worktree needed since no candidate exists).
- No containers/networks/volumes started; no CI runs triggered; no PRs opened (mission is findings-only).
- Evidence lives only in baseharbor-plan; remote verified as https://github.com/mcpdev80/baseharbor-plan.git before commit.
- No subagents used; every step executed in this session. Session exposes no native todowrite tool, so the board
  JSON file (mandatory per dispatch) carries the plan.
- Language of akte: English (cards/akte rule).

## cleanliness

- `docker ps -q | wc -l` before: 0 (measured at lane start, shell pid 301462).
- `docker ps -q | wc -l` after: 0 (measured at stop, same host).
- cleanliness: besenrein — no containers/networks/volumes/state dirs were started by this lane on this host.
- No compose project started; nothing to tear down.

    (before) $ docker ps -q | wc -l
    0
    (after)  $ docker ps -q | wc -l
    0

## STOP / window-release note

Coordinator window-release order 2026-11-26: real card work exists again (#1832 hop/requalification), so the hunt
stops with Meldefrist. The census slice was already COMPLETE at stop time: findings H-33-01 … H-33-09 delivered in
full; nothing was started on a new slice. This lane's checkout zone
workers/w159-0428-224-hunt-v33-wt/bh is read-only evidence material; the seat is free once this akte is pushed.
The slice "re-arms later" per the order — no further hunt work taken by this session.

## END

END_DONE w159-0428-224-hunt-v33: H-V33 runner census complete (delivered at stop per window-release order, slice
full, not partial): 8 findings (H-33-01..08) + 1 no-gap check (H-33-09); no candidate SHA (findings-only),
source develop f7540e591609e0db6453e9b690fbb5d6686448a2; cleanliness: 0 containers before and after.
