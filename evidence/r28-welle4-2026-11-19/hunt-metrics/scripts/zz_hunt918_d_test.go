package observability

import (
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
)

// zz_hunt918_d_test.go — BUG-HUNT 918 cell (3), read-only probe. NOT committed
// to the product branch.
//
// Question: the alert evaluator (PR #1613, still unmerged) is a signal *consumer*
// of the registry. What does the registry-layer contract actually return for an
// empty signal level, and can a consumer tell "nothing registered" apart from
// "the level does not exist yet"?
func TestHunt918EmptyLevelIsIndistinguishableFromUnreadableLevel(t *testing.T) {
	stateDir := t.TempDir()
	t.Setenv("BASEHARBOR_STATE_DIR", stateDir)

	placement := capability.ProviderPlacement{Scope: capability.ScopeShared, Ownership: capability.OwnershipBaseHarbor}

	// (a) No registry file at all: a fresh installation.
	sources, err := List(SignalMetrics, placement, nil, false, true, true)
	t.Logf("level absent      -> sources=%v err=%v (nil, nil means: indistinguishable from empty)", sources, err)
	if sources != nil || err != nil {
		t.Fatalf("absent-level contract: got (%v, %v)", sources, err)
	}

	// (b) Registry file exists but the alert-relevant level is empty.
	if err := UpdateSignal(SignalSource{
		ID: "postgresql:shared", Kind: SignalLogs, Provider: capability.ProviderPostgreSQL,
		Class: SourcePlatformProvider, Scope: capability.ScopeShared, SharingBoundary: "shared",
		Network: "baseharbor-shared", Target: "runtime://p/svc", Protocol: "syslog-rfc5424",
	}); err != nil {
		t.Fatal(err)
	}
	sources, err = List(SignalMetrics, placement, nil, false, true, true)
	t.Logf("level empty, other level populated -> metrics=%d err=%v", len(sources), err)
	if err != nil || len(sources) != 0 {
		t.Fatalf("empty-level contract: got (%v, %v)", sources, err)
	}

	// (c) RegistryHasSignal is the only probe that reports existence, and it
	// collapses "file missing" into (false, nil) exactly like "no such signal".
	found, err := RegistryHasSignal("anything", capability.ProviderPrometheus, SignalMetrics)
	t.Logf("RegistryHasSignal on absent/empty level -> found=%v err=%v", found, err)
	if found || err != nil {
		t.Fatalf("existence probe must be (false, nil): got (%v, %v)", found, err)
	}

	// Consequence for a persistence-checking consumer: the two states below are
	// byte-identical to it.
	absent, absentErr := List(SignalMetrics, placement, nil, false, true, true)
	empty, emptyErr := List(SignalMetrics, placement, nil, false, true, true)
	if len(absent) != len(empty) || absentErr != nil || emptyErr != nil {
		t.Fatalf("states differ unexpectedly")
	}
	t.Log("a consumer cannot distinguish 'alert level never provisioned' from 'alert level provisioned and empty' at the registry boundary")
}
