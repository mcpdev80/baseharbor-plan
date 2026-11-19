package application

import (
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
	"github.com/mcpdev80/baseharbor/internal/observability"
)

func TestHunt918ReconcileWritesPrometheusLogSignal(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())
	m := Manifest{Name: "demo", Environment: "dev"}
	// metrics policy: enabled by default for dev
	if err := reconcileApplicationMetricsSource(m, "bh-demo-dev"); err != nil {
		t.Fatal(err)
	}
	// Now check what the registry actually holds under provider=prometheus.
	placement := capability.ProviderPlacement{Scope: capability.ScopeApplication}
	all, err := observability.List(observability.SignalMetrics, placement, []string{"demo"}, true, true, true)
	if err != nil {
		t.Fatal(err)
	}
	for _, s := range all {
		t.Logf("metrics: id=%s class=%s provider=%s verification=%s", s.ID, s.Class, s.Provider, s.Verification)
	}
	// The provider=prometheus identity is registered as class=application-provider.
	// Is that identity reachable by a LOG listing at all? Register an explicit one.
	if err := observability.UpdateSignal(observability.SignalSource{
		ID: "prometheus:bh-demo-dev", Kind: observability.SignalLogs, Provider: capability.ProviderPrometheus,
		Class: observability.SourceApplication, Scope: capability.ScopeApplication, OwnerApplication: "demo",
		Target: observability.RuntimeTarget("bh-demo-dev", "workload"), Protocol: "stdout-stderr",
	}); err != nil {
		t.Fatalf("register app-class prometheus log signal: %v", err)
	}
	sigs, err := observability.ListLogs(placement, []string{"demo"}, true, true)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("ListLogs after registering an app-class prometheus log source: %d", len(sigs))
	for _, s := range sigs {
		t.Logf("  log: id=%s class=%s provider=%s", s.ID, s.Class, s.Provider)
	}
	// Simulate #1680's reclaim.
	if err := observability.PruneProviderSignals("prometheus:bh-demo-dev", capability.ProviderPrometheus, observability.SignalLogs); err != nil {
		t.Fatal(err)
	}
	sigs2, err := observability.List(observability.SignalLogs, placement, []string{"demo"}, true, true, true)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("after #1680 reclaim, raw List(logs, include app-class) returns %d", len(sigs2))
	for _, s := range sigs2 {
		t.Logf("  log: id=%s class=%s provider=%s", s.ID, s.Class, s.Provider)
	}
}
