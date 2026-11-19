package observability

import (
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
)

// zz_hunt918_repro_test.go — BUG-HUNT 918 read-only repro (NOT committed to the
// product branch). Question: does the environment filter act on the metrics
// list paths, or only the application filter?
func TestHunt918ApplicationMetricsEnvironmentFilter(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())

	for _, environment := range []string{"dev", "prod"} {
		source := MetricsSource{
			ID:               ApplicationMetricsSourceID("demo", environment, "web"),
			Provider:         capability.ProviderPrometheus,
			Class:            SourceApplication,
			Scope:            capability.ScopeApplication,
			OwnerApplication: "demo",
			Network:          "baseharbor-demo-" + environment + "-metrics",
			Target:           "bhm-abc:9464",
			Path:             "/metrics",
			Scheme:           "http",
			Verification:     capability.ObservabilityVerifyBackend,
		}
		if err := Update(source); err != nil {
			t.Fatalf("register %s: %v", environment, err)
		}
	}

	placement := capability.ProviderPlacement{Scope: capability.ScopeApplication, Ownership: capability.OwnershipBaseHarbor}
	sources, err := ListApplicationMetrics(placement, []string{"demo"})
	if err != nil {
		t.Fatalf("list: %v", err)
	}
	t.Logf("ListApplicationMetrics(applications=[demo]) returned %d source(s):", len(sources))
	for _, source := range sources {
		t.Logf("  id=%s network=%s target=%s", source.ID, source.Network, source.Target)
	}

	// The registry holds one dev and one prod source for the same application.
	// A caller whose manifest environment is "prod" receives BOTH.
	prodSeen, devSeen := 0, 0
	for _, source := range sources {
		switch source.ID {
		case "application:metrics:demo:prod:web":
			prodSeen++
		case "application:metrics:demo:dev:web":
			devSeen++
		}
	}
	if devSeen != 0 || prodSeen != 1 {
		t.Fatalf("environment filter: got dev=%d prod=%d, want dev=0 prod=1", devSeen, prodSeen)
	}
}
