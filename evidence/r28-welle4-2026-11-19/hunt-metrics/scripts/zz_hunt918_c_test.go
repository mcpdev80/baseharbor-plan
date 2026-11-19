package observability

import (
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
)

// zz_hunt918_c_test.go — BUG-HUNT 918 cell (1c), read-only probe. NOT committed
// to the product branch.
//
// Question: #1677 added an environment-prefix skip inside the verify caller of
// ListApplicationMetrics. Is that environment filter therefore active on every
// listing path a real deployment takes, or does the unfiltered path still reach
// the shared-provider listing?
func TestHunt918EnvironmentPrefixOnlyGuardsVerifyCaller(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())

	// Two deployments of the same application in two environments, both bound.
	manifestEnv := "prod"
	for _, environment := range []string{"dev", manifestEnv} {
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

	// Path A: the raw listing that every render/inventory consumer uses.
	raw, err := ListApplicationMetrics(placement, []string{"demo"})
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("path A ListApplicationMetrics (no manifest in scope): %d sources", len(raw))

	// Path B: what the verify caller actually queries, i.e. the same list with
	// the #1677 prefix filter applied by the caller.
	prefix := ApplicationMetricsSourceID("demo", manifestEnv, "")
	filtered := 0
	for _, source := range raw {
		if source.ID[:len(prefix)] == prefix {
			filtered++
		}
	}
	t.Logf("path B after the caller-side environment prefix filter: %d sources", filtered)
	if filtered != 1 || len(raw) != 2 {
		t.Fatalf("expected the filter to be caller-side only: raw=%d filtered=%d", len(raw), filtered)
	}
}
