package observability

import (
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
)

// zz_hunt918_b_test.go — BUG-HUNT 918 read-only probe (NOT committed to the
// product branch). Question: does List() carry any environment awareness at all,
// i.e. is the environment filter present on every list path or only on the
// prefix workaround added by #1677?
func TestHunt918ListHasNoEnvironmentDimension(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())
	for _, environment := range []string{"dev", "staging", "prod"} {
		if err := Update(MetricsSource{
			ID:               ApplicationMetricsSourceID("demo", environment, "web"),
			Provider:         capability.ProviderPrometheus,
			Class:            SourceApplication,
			Scope:            capability.ScopeApplication,
			OwnerApplication: "demo",
			Network:          "net-" + environment,
			Target:           "bhm-abc:9464",
			Path:             "/metrics",
			Verification:     capability.ObservabilityVerifyBackend,
		}); err != nil {
			t.Fatal(err)
		}
	}
	placement := capability.ProviderPlacement{Scope: capability.ScopeApplication}
	// Shared-scope caller (the shape used by shared-Prometheus render/verify):
	// applications list is the only selector; environment is not a parameter.
	got, err := List(SignalMetrics, placement, []string{"demo"}, true, false, false)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("List(applications=[demo]) returned %d source(s) for a single-environment caller", len(got))
	for _, s := range got {
		t.Logf("  id=%s network=%s", s.ID, s.Network)
	}
	if len(got) != 1 {
		t.Fatalf("environment selection on List(): got %d sources, want 1 (caller knows only one environment)", len(got))
	}
}
