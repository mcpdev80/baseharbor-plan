package observability

import (
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
)

// zz_hunt918_m_test.go — BUG-HUNT 918 cell (2m): the destroy/reclaim boundary.
// RegisterProviderSignals and ReconcileProviderSignals both key replacement on
// ID+provider, and both stamp one Class for the whole identity. PruneProviderSignals
// and Remove key on ID (+provider). Probe: what survives a two-owner shared
// collector identity?
func TestHunt918SharedIdentityHasNoPerOwnerBoundary(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())
	const id = "loki:bh-shared"
	ownerA := "owner-a"
	ownerB := "owner-b"

	// Owner A reconciles the shared collector identity as platform-provider.
	if err := ReconcileProviderSignals(id,
		map[capability.ProviderKind]struct{}{capability.ProviderLoki: {}},
		[]SignalSource{{
			ID: id, Kind: SignalLogs, Provider: capability.ProviderLoki,
			Class: SourcePlatformProvider, Scope: capability.ScopeShared, SharingBoundary: "shared",
			Target: "runtime://bh-shared/loki", Protocol: "syslog-rfc5424",
			Mode: capability.ObservabilityNative, Verification: capability.ObservabilityVerifyBackend,
		}}); err != nil {
		t.Fatal(err)
	}
	// Owner B, whose policy selects an application-scoped view of the same
	// collector instance, reconciles the SAME identity.
	if err := ReconcileProviderSignals(id,
		map[capability.ProviderKind]struct{}{capability.ProviderLoki: {}},
		[]SignalSource{{
			ID: id, Kind: SignalLogs, Provider: capability.ProviderLoki,
			Class: SourceApplicationProvider, Scope: capability.ScopeApplication, OwnerApplication: ownerB,
			Target: "runtime://bh-shared/loki", Protocol: "syslog-rfc5424",
			Mode: capability.ObservabilityNative, Verification: capability.ObservabilityVerifyBackend,
		}}); err != nil {
		t.Fatal(err)
	}

	all, err := List(SignalLogs, capability.ProviderPlacement{Scope: capability.ScopeApplication},
		[]string{ownerA, ownerB}, true, true, true)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("signals under %s after two owners reconciled it: %d", id, len(all))
	for _, s := range all {
		t.Logf("  class=%s scope=%s owner=%q", s.Class, s.Scope, s.OwnerApplication)
	}
	if len(all) != 1 {
		t.Fatalf("expected the second reconciliation to overwrite the first, got %d", len(all))
	}
	if all[0].OwnerApplication != ownerB {
		t.Fatalf("owner attribution is not last-writer-wins: %q", all[0].OwnerApplication)
	}
	// Owner A's destroy reclaims "its" identity by ID+provider: it deletes B's
	// registration, because the identity carries no owner dimension.
	if err := PruneProviderSignals(id, capability.ProviderLoki, SignalLogs); err != nil {
		t.Fatal(err)
	}
	left, err := RegistryHasSignal(id, capability.ProviderLoki, SignalLogs)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("after owner A prunes the shared identity, B's registration present=%v", left)
	if left {
		t.Fatalf("expected the cross-owner deletion to have happened (it is the finding)")
	}
	t.Log("reclaim keys are ID+provider with a single stamped Class/Scope/Owner: two owners of one collector identity overwrite and delete each other")
}
