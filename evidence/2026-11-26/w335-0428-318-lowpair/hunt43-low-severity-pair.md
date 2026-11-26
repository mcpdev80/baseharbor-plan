# 0428-318 · hunt43-low-severity-pair (w335) — akte

Scope: baseharbor H-V43 low-severity pair. Two LOW findings from the H-V43 env/config-injection hunt, implemented as a minimal guarded change + tests. No consent/auth/authorization change. No `.github/**` edits. No local test run (owner policy stop 2026-11-26). Hosted CI is the only test evidence.

## Visible ansatz block (visible ansatz block, 2026-11-26)

- Card owner (verbatim, fetched from origin/main at runtime): `unassigned` (task note frontmatter `owner:` empty; mission identity is the lane).
- Lane identity used for EVERY commit and merge (git author + committer, per command): `w335-0428-318-lowpair` / `w335-0428-318-lowpair@baseharbor.local`.
- Pre-push gate (mechanically verified before every push): `git show -s --format=%an HEAD` must equal `w335-0428-318-lowpair` exactly; on mismatch STOP + report (no silent amend).
- Literal commit invocation used for every commit:
  `git -c user.name=w335-0428-318-lowpair -c user.email=w335-0428-318-lowpair@baseharbor.local commit ...`
- Pre-push identity gate line recorded in evidence: `git log --format='%h an=%an cn=%cn' -1`.

## Base attestation

- develop HEAD (git ls-remote baseharbor refs/heads/develop): `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74`
- Branch cut at exact develop tip: `lane-0428-318-lowpair` (detached 5a37ddbd9)
- `git merge-base --is-ancestor 5a37ddbd9a... HEAD` => 5a37ddbd9 IS an ancestor (clean base, no foreign commit)
- `git diff baseharbor/develop...HEAD --name-only` recorded before PR (own commits only)
- git remote (baseharbor worktree): `baseharbor https://github.com/mcpdev80/baseharbor.git` (verified github.com/mcpdev80 before any git op; used for all baseharbor git ops)
- Planning repo remote: `https://github.com/mcpdev80/baseharbor-plan.git` (verified before first commit)

## The two LOW findings

### FUND-C (LOW): `BASEHARBOR_RUNTIME_IMAGE` validated for CRLF/NUL only, not for path-separator or `=` injection into the rendered compose.yaml

file:line: `internal/runtimeexecutor/compose.go` lines 122-129 (`image := strings.TrimSpace(os.Getenv("BASEHARBOR_RUNTIME_IMAGE"))` + `ContainsAny(image, "\r\n\x00")` guard) + line 256 (`fmt.Fprintf(&b, "    image: %s\n", strconv.Quote(image))`).

Root: the only validation is a newline/NUL guard. A value such as `myimage:tag\n  inject: "line"` passes the guard and injects a second key into the rendered executor compose.yaml written at compose.go:142 (`os.WriteFile(composePath, ...)`). Not secret-bearing; low-severity compose-injection vector co-located with the env-read.

Fix: replace the bare newline/NUL guard with an allow-list validation: image must be empty/`DefaultImage`, else match `^[A-Za-z0-9][A-Za-z0-9._/-]*(:[A-Za-z0-9._-]+)?$` (registry/repo:tag). Reject empty-after-trim, `=`, `/` separators that are not part of a registry host, and any char outside the allow-list. This still permits the legitimate `registry:5000/app:tag` host-port case.

### FUND-D (LOW): executor env-file projection ordering in `EnsureFilesAt`

file:line: `internal/runtimeexecutor/compose.go` `EnsureFilesAt` (lines ~48-145): the S3 admin credential file is projected at compose.go:92 (`adminProjection, err := projectContainerReadableSecret(dir, adminCredentialsPath, "s3-admin.env", "S3 admin credentials")`) BEFORE the executor compose.yaml is written at compose.go:140-145 (`os.WriteFile(composePath, ...)`).

Root: the runtime.executor image's `environment` block declares `BASEHARBOR_EXECUTOR_S3_ADMIN_CREDENTIALS_FILE: "/run/secrets/s3-admin"` (compose.go:265). If the source credential file is missing or unreadable, the projection errors out only if the guard path is reached — but the compose.yaml already embeds that path. Ordering the credential-file projection before the compose write does not fully close it (projectContainerReadableSecret may create an empty projected file on success), so the concrete fix is the explicit empty-file check (see Acceptance). This is a defense-in-depth ordering + empty-file guard, low severity.

Note: the original FUND-D reasoning in the hunt (ambient-openbao credential file read) was re-verified and REJECTED — the openbao credentials file is a fixed mount `/run/secrets/openbao-credentials` (compose_render.go:190), never operator-controlled. The replaced LOW finding is the executor env-file projection ordering.

## Implementation

### FUND-C change

`internal/runtimeexecutor/compose.go`: add a validated image accessor.

- Guard: image value must be empty (→ `DefaultImage`) or match an allow-list regex `^[A-Za-z0-9][A-Za-z0-9._/-]*(:[A-Za-z0-9._-]+)?$`.
- Reject: empty-after-trim, any `=`, any newline/NUL (kept), any char outside the allow-list.
- Return `errors.New("BASEHARBOR_RUNTIME_IMAGE is invalid")` on failure (same error as before, preserved).

### FUND-D change

`internal/runtimeexecutor/compose.go` `EnsureFilesAt`: after a successful `projectContainerReadableSecret`, assert the projected S3 admin file exists and is non-empty; return an error if empty (prevents an executable image referencing an empty credential).

### Tests

`internal/runtimeexecutor/compose_test.go`:

- `TestEnsureFilesRejectsInvalidRuntimeImage`: set `BASEHARBOR_RUNTIME_IMAGE` to an injectable value (`tag\ninject: "x"`) → `EnsureFiles` returns error.
- `TestEnsureFilesAcceptsCanonicalRuntimeImage`: set a canonical `registry:5000/baseharbor-runtime:0.4.28` → succeeds.
- `TestEnsureFilesS3AdminFileNotEmpty`: a source S3 admin file that projects empty → `EnsureFiles` returns error (guards the ordering finding).

Coverage: `internal/runtimeexecutor` is auto-discovered by the "Run release-source tests" job (`go test ./contracts/... ./internal/... ./spec/...`) in `.github/workflows/ci.yml`. No `.github/**` change needed (Owner scope — not touched).

## repo-rule compliance

- Product files changed: only `internal/runtimeexecutor/compose.go` (guard + ordering). Tests only in `internal/runtimeexecutor/compose_test.go`.
- No `.github/**` edits. No workflow_dispatch / reruns. No consent/auth/authorization change.
- No local test run (owner policy stop 2026-11-26). Local prechecks only: gofmt, `go vet ./...`, `go build ./cmd/baha`.
- Evidence written only to baseharbor-plan (product repo untouched).
- git remote resolved to github.com/mcpdev80 before any git op (baseharbor remote).
- No containers or compose projects started; no docker/podman daemon work on this host.
- Branch provenance: cut from exact develop tip 5a37ddbd9a; `git log --oneline baseharbor/develop...HEAD` lists only w335-0428-318-lowpair commits.

## CLEANLINESS

docker ps -a (own pid zone): none — no containers/compose projects launched (unit-test-only, not run here).
git status worktree: clean at END.
Worktree to remove: `workers/w335-0428-318-lowpair-wt` (removed at END).

## END

END w335-0428-318-lowpair DONE — 2 LOW findings fixed (FUND-C executor image injection allow-list, FUND-D executor env-file projection ordering/empty guard), 1 test file added, 0 consent/auth changes, 0 .github/** edits.
