package logs

import (
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
	"github.com/mcpdev80/baseharbor/internal/observability"
)

// zz_hunt918_l_test.go — BUG-HUNT 918 cell (2l): the destroy path drops the
// Loki provider identity with observability.Remove(ID), which has no class or
// kind filter. Probe what Remove() does to a multi-class identity.
func TestHunt918RemoveIsIDScopedAcrossClasses(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())
	const id = "loki:shared"
	_ = id
	// One identity, three classes (the shape RegisterProviderSignals produces
	// when the same collector instance serves several owners).
	for _, tc := range []struct {
		kind  observability.SignalKind
		class observability.SourceClass
		proto string
	}{
		{observability.SignalLogs, observability.SourceApplication, "stdout-stderr"},
		{observability.SignalLogs, observability.SourceApplicationProvider, "syslog-rfc5424"},
		{observability.SignalTraces, observability.SourcePlatformProvider, "otlp"},
	} {
		c, kind := tc.class, tc.kind
		src := observability.SignalSource{
			ID: id, Kind: kind, Provider: capability.ProviderLoki,
			Class: c, Scope: capability.ScopeShared, SharingBoundary: "shared",
			Target: observability.RuntimeTarget("bh-shared", "loki"), Protocol: tc.proto,
		}
		if kind == observability.SignalTraces {
			src.Path = "/services/loki:shared"
		}
		// All three are application-scoped so a single placement enumerates them.
		src.Scope = capability.ScopeApplication
		src.OwnerApplication = "demo"
		src.SharingBoundary = ""
		if err := observability.UpdateSignal(src); err != nil {
			t.Fatalf("register %s: %v", c, err)
		}
	}
	before, err := observability.ListLogs(capability.ProviderPlacement{Scope: capability.ScopeApplication}, []string{"demo"}, true, true)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("ListLogs before Remove (application placement, provider classes only): %d", len(before))

	allBefore, err := observability.List(observability.SignalLogs,
		capability.ProviderPlacement{Scope: capability.ScopeApplication}, []string{"demo"}, true, true, true)
	otherBefore, _ := observability.List(observability.SignalTraces,
		capability.ProviderPlacement{Scope: capability.ScopeApplication}, []string{"demo"}, true, true, true)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("raw List(logs+traces) before Remove: %d", len(allBefore))

	if err := observability.Remove(id); err != nil {
		t.Fatal(err)
	}
	allAfter, err := observability.List(observability.SignalLogs,
		capability.ProviderPlacement{Scope: capability.ScopeApplication}, []string{"demo"}, true, true, true)
	if err != nil {
		t.Fatal(err)
	}
	tracesAfter, err2 := observability.List(observability.SignalTraces,
		capability.ProviderPlacement{Scope: capability.ScopeApplication}, []string{"demo"}, true, true, true)
	if err2 != nil {
		t.Fatal(err2)
	}
	t.Logf("after one Remove(%s): logs=%d traces=%d", id, len(allAfter), len(tracesAfter))
	if len(allAfter) != 0 || len(tracesAfter) != 0 {
		t.Fatalf("Remove left residue: %d", len(allAfter))
	}
	t.Logf("raw List(traces) before Remove: %d", len(otherBefore))
	// Two log signals share one ID, but UpdateSignal keys on ID+Kind, so the
	// second log class overwrote the first. That is the real finding.
	if len(allBefore) != 1 || len(otherBefore) != 1 {
		t.Fatalf("fixture: expected 1 log + 1 trace under one ID, got logs=%d traces=%d", len(allBefore), len(otherBefore))
	}
	// Show which of the two log classes survived.
	for _, x := range allBefore {
		t.Logf("surviving log signal under %s: class=%s", id, x.Class)
	}
	t.Log("observability.Remove is ID-scoped, not class/kind-scoped: one destroy call drops every class registered under that identity, including other owners'")
}
