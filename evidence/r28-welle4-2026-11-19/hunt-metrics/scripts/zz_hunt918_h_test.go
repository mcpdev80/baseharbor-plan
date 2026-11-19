package metrics

import (
	"os"
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
	"github.com/mcpdev80/baseharbor/internal/observability"
)

// zz_hunt918_h_test.go — BUG-HUNT 918 cell (1h): can the app-class metrics
// source ever reach the Prometheus scrape config, i.e. is the #1677 registration
// real or a silent no-op on the file_sd side?
func TestHunt918AppClassSourceReachesScrapeFiles(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())
	dir := t.TempDir()
	src := observability.MetricsSource{
		ID:               observability.ApplicationMetricsSourceID("demo", "dev", "web"),
		Provider:         capability.ProviderPrometheus,
		Class:            observability.SourceApplication,
		Scope:            capability.ScopeApplication,
		OwnerApplication: "demo",
		Network:          "baseharbor-metrics-x",
		Target:           "bhm-abc:9464",
		Path:             "/metrics",
		Scheme:           "http",
		Verification:     capability.ObservabilityVerifyBackend,
	}
	if err := observability.Update(src); err != nil {
		t.Fatal(err)
	}
	// The provider-target writer, fed by what ListMetrics returns to the renderer.
	providerSide, err := observability.ListMetrics(
		capability.ProviderPlacement{Scope: capability.ScopeApplication}, []string{"demo"}, true, true)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("ListMetrics (renderer path) sees %d source(s) — app class must be 0 here", len(providerSide))
	if err := syncProviderTargets(dir, providerSide); err != nil {
		t.Fatal(err)
	}
	entries, err := os.ReadDir(dir)
	if err != nil {
		t.Fatal(err)
	}
	names := []string{}
	for _, e := range entries {
		names = append(names, e.Name())
	}
	t.Logf("provider--*.json written by the renderer path: %v", names)
	if len(names) != 0 {
		t.Fatalf("application-class source reached the provider file_sd writer: %v", names)
	}
}
