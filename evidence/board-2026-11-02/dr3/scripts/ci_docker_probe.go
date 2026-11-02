//go:build ci_docker_probe

package runtime

import (
	"context"
	"strings"
)

// This build-tagged file is compiled only for the cmd/baha test that proves the
// hosted `validate` silent-drop root cause (dr3). It exposes a tiny, read-only
// probe of the SAME fail-closed product path that already lives in
// docker_engine.go:32-219 and is exercised by the existing unit tests there.
//
// No untagged file in this package references DockerEndpointMissingDaemon, so
// the symbol never leaks into the product runtime build. The probe does not
// start, retry, or fall back to any engine — it only asks the existing
// resolveDockerEngine once whether the given endpoint can be probed. A downed
// rootless daemon (the validate-job failure) returns a probe error; a reachable
// daemon returns a verified observation.
func DockerEndpointMissingDaemon(ctx context.Context, command, endpoint string) bool {
	_, err := resolveDockerEngine(ctx, command, DockerEngineSelection{}, runProbeOnce, func(string) string { return "" }, 1001)
	if err != nil {
		// The fail-closed "is unavailable; … no fallback to System Docker"
		// path is exactly the missing-daemon signal we assert on.
		return strings.Contains(err.Error(), "no fallback to System Docker")
	}
	return false
}

// runProbeOnce mirrors the product probe exactly (dockerBoundEnvironment, same
// flags) without adding any behaviour the tagged path does not already have.
func runProbeOnce(ctx context.Context, command string, args []string, env []string) ([]byte, error) {
	return dockerEngineOutput(ctx, command, args, env)
}
