# fix-engine-detect: PLAN

## Task background
BaseHarbor uses a hardcoded `"docker"` binary in `inspectTargetDockerEngine` to detect the Docker engine. When the runtime provider is `podman`, this causes the wrong binary to be invoked (docker instead of podman), leading to incorrect engine detection or failures.

## Root cause
In `cmd/baha/docker_engine.go`, line 131:
```go
engine, err := bhruntime.ResolveDockerEngine(targetDockerEngineContext(ctx, target), "docker")
```
The `"docker"` command string is hardcoded. When `target.RuntimeProvider == "podman"`, the code should use `"podman"` instead. The function already guards by checking `target.RuntimeProvider != "docker"` at line 128 — it returns early for podman, which means podman targets get `nil` engine observation, and the caller sees "docker-only-failure" instead of proper podman engine detection.

## PLAN steps
0. Read existing code: `docker_engine.go`, `docker_engine_test.go`, `docker_engine_runtime_test.go`, `docker_engine_binding_test.go`, call sites in `target.go`, `app_status_collect.go`, `app_doctor_collect.go`, `control_plane_operations.go`
1. Identify all places where `"docker"` is hardcoded as the engine resolution command.
2. Modify `inspectTargetDockerEngine` to resolve the correct engine binary based on `target.RuntimeProvider` — use `"podman"` when the provider is podman, `"docker"` otherwise.
3. Modify `ensureTargetDockerBinding` similarly — it already returns early for non-docker providers; adjust the early-return logic to support podman.
4. Add/update unit tests to cover the podman path (mock `ResolveDockerEngine` with podman command).
5. Run `go build ./... && go vet ./...` locally.
6. Run `go test ./cmd/baha/...` locally.
7. Commit, push to PR, observe CI.
8. Document evidence.
