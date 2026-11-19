package metrics

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"github.com/mcpdev80/baseharbor/internal/application"
	"github.com/mcpdev80/baseharbor/internal/capability"
	"github.com/mcpdev80/baseharbor/internal/observability"
)

// zz_hunt918_j_test.go — BUG-HUNT 918 cell (1j): destroy-time pruning.
// PruneRegisteredApplicationTargetsAt deletes stale target FILES whose name is
// not in `desired`, then prunes registry entries whose ID is not in `keep`.
// `keep` is derived from m.Metrics.Sources (the authored manifest), not from the
// files that survived. Probe: a source that was removed from the manifest, and a
// registry entry whose file is gone.
func TestHunt918PruneKeepSetComesFromManifestNotFiles(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())
	dir := t.TempDir()
	m := application.Manifest{Name: "demo", Environment: "dev"}
	// Two sources once registered; the manifest now declares only "web".
	m.Metrics.Sources = []application.MetricsSourceRequirement{{Name: "web"}}
	for _, name := range []string{"web", "gone"} {
		if err := observability.Update(observability.MetricsSource{
			ID:       observability.ApplicationMetricsSourceID(m.Name, m.Environment, name),
			Provider: capability.ProviderPrometheus, Class: observability.SourceApplication,
			Scope: capability.ScopeApplication, OwnerApplication: m.Name,
			Network: "net", Target: "bhm-abc:9464", Path: "/metrics",
			Verification: capability.ObservabilityVerifyBackend,
		}); err != nil {
			t.Fatal(err)
		}
		if err := writeTestTargetFile(dir, m, name); err != nil {
			t.Fatal(err)
		}
	}
	desired := map[string]struct{}{targetFileName(m, "web"): {}}
	if err := pruneApplicationTargetsFromFiles(ProviderFiles{TargetsDir: dir}, m, desired); err != nil {
		t.Fatal(err)
	}
	left, err := observability.ListApplicationMetrics(capability.ProviderPlacement{Scope: capability.ScopeApplication}, []string{m.Name})
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("registry entries after prune: %d", len(left))
	for _, s := range left {
		t.Logf("  %s", s.ID)
	}
	if len(left) != 1 || left[0].ID != observability.ApplicationMetricsSourceID(m.Name, m.Environment, "web") {
		t.Fatalf("prune did not converge on the desired set: %#v", left)
	}
}

func writeTestTargetFile(dir string, m application.Manifest, source string) error {
	group := targetGroup{Targets: []string{"bhm-abc:9464"}, Labels: map[string]string{"job": "baseharbor-applications"}}
	data, err := json.MarshalIndent([]targetGroup{group}, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(filepath.Join(dir, targetFileName(m, source)), append(data, '\n'), 0o644)
}
