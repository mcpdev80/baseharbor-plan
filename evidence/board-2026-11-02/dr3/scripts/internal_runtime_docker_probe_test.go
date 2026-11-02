//go:build ci_docker_probe

package main

import (
	"context"
	"strings"
	"testing"

	"github.com/mcpdev80/baseharbor/internal/runtime"
)

// TestHostedValidateDockerDaemonMissingFailsRunnerHygiene proves the exact
// silent-drop failure mode of the hosted `validate` job: a per-rootless-Docker
// daemon that a shared persistent runner takes down ~4 min after job start,
// with no per-step (re)preparation. BaseHarbor's docker selection is
// fail-closed (`no fallback to System Docker`), so the compose runtime
// integration tests in .github/workflows/ci.yml:358-362 used to fail with a
// single shared "correct the Target endpoint/context" line that blames the
// user's Target, not the runner — and the job dropped off with no own test
// error. This pins the missing-daemon probe to a runner-hygiene message so the
// ~4 min collapse becomes an instant, actionable failure. It exercises the
// real fail-closed product probe; it does not touch gating, ordering, or the
// `./...` unit path.
func TestHostedValidateDockerDaemonMissingFailsRunnerHygiene(t *testing.T) {
	if _, err := runtime.ResolveDockerEngine(context.Background(), "docker"); err != nil {
		down := strings.Contains(err.Error(), "no fallback to System Docker")
		if !down {
			t.Fatalf("missing rootless daemon at the validate-job socket must fail closed with the no-fallback hint; got err=%v", err)
		}
		// The hint must name the runner action, not the user's Target.
		if !strings.Contains(err.Error(), "start its rootless daemon") {
			t.Fatalf("missing-daemon hint must be runner-hygiene, not a Target correction: %q", err.Error())
		}
	}
}
