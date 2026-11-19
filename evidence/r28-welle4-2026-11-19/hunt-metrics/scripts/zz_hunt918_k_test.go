package metrics

import (
	"os"
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
	"github.com/mcpdev80/baseharbor/internal/observability"
)

// zz_hunt918_k_test.go — BUG-HUNT 918 cell (1k): a metrics source whose
// Verification is ObservabilityVerifyNone is dropped by the provider file_sd
// writer and by the provider-network collector. If such a source is the only one
// of its kind, the deploy path silently scrapes nothing and the verify path
// silently asserts nothing. Probe whether that silent-success window exists.
func TestHunt918VerifyNoneSourceProducesNoScrapeAndNoAssertion(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())
	dir := t.TempDir()
	if err := observability.Update(observability.MetricsSource{
		ID: "postgres:shared", Provider: capability.ProviderPostgreSQL,
		Class: observability.SourceApplicationProvider, Scope: capability.ScopeShared,
		SharingBoundary: "shared", Network: "baseharbor-shared",
		Target: "postgres:9187", Path: "/metrics",
		Verification: capability.ObservabilityVerifyNone,
	}); err != nil {
		t.Fatal(err)
	}
	sources, err := observability.ListMetrics(capability.ProviderPlacement{Scope: capability.ScopeShared, SharingBoundary: "shared"}, nil, true, true)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("ListMetrics returns %d source(s) for a requires-adapter provider", len(sources))
	if err := syncProviderTargets(dir, sources); err != nil {
		t.Fatal(err)
	}
	entries, err := os_ReadDirNames(dir)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("file_sd targets written: %v (empty means nothing is scraped)", entries)
	if len(entries) != 0 && len(sources) != 0 {
		t.Fatalf("a verify=none source unexpectedly produced a scrape target: %v", entries)
	}
	// And the verify path skips it entirely.
	for _, s := range sources {
		if s.Verification == capability.ObservabilityVerifyNone {
			t.Logf("verify path skips source %s", s.ID)
		}
	}
}

func os_ReadDirNames(p string) ([]string, error) {
	fs, err := os.ReadDir(p)
	if err != nil {
		return nil, err
	}
	out := []string{}
	for _, f := range fs {
		out = append(out, f.Name())
	}
	return out, nil
}
