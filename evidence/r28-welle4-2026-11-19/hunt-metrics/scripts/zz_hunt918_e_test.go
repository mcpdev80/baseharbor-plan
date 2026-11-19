package observability

import (
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
)

// zz_hunt918_e_test.go — BUG-HUNT 918 cell (2), read-only probe. NOT committed
// to the product branch.
//
// Question: #1677 gave List() an includeApplicationSources switch, but the only
// caller-facing knob is the constant `false` inside ListLogs/ListTraces. Does the
// exclusion actually reach the log/trace listing — and what happens on destroy?
func TestHunt918LogApplicationSourceNeverLeaksWithoutCleanupKnob(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())

	// The application-class log identity a Loki-bound workload would own.
	logID := "loki:app-project"
	if err := UpdateSignal(SignalSource{
		ID: logID, Kind: SignalLogs, Provider: capability.ProviderLoki,
		Class: SourceApplication, Scope: capability.ScopeApplication, OwnerApplication: "demo",
		Target: RuntimeTarget("app-project", "workload"), Protocol: "stdout-stderr",
	}); err != nil {
		t.Fatal(err)
	}
	// A provider-class log source, the shape every existing caller does register.
	if err := UpdateSignal(SignalSource{
		ID: "loki:shared", Kind: SignalLogs, Provider: capability.ProviderLoki,
		Class: SourceApplicationProvider, Scope: capability.ScopeApplication, OwnerApplication: "demo",
		Target: RuntimeTarget("bh-demo-dev-prometheus", "workload"), Protocol: "syslog-rfc5424",
	}); err != nil {
		t.Fatal(err)
	}

	placement := capability.ProviderPlacement{Scope: capability.ScopeApplication}

	// The public log listing: no caller can ask for the application class.
	listed, err := ListLogs(placement, []string{"demo"}, true, true)
	if err != nil {
		t.Fatal(err)
	}
	classes := map[SourceClass]int{}
	for _, s := range listed {
		classes[s.Class]++
	}
	t.Logf("ListLogs classes: %#v", classes)
	if classes[SourceApplication] != 0 {
		t.Fatalf("application-class log source leaked into ListLogs")
	}

	// The registry itself still holds it: the listing hides it, Remove/cleanup
	// paths do not see the class distinction, and no log-side prune exists.
	all, err := List(SignalLogs, placement, []string{"demo"}, true, true, true)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("List(., includeApplicationSources=true) classes: %d total", len(all))
	found := false
	for _, s := range all {
		if s.Class == SourceApplication {
			found = true
		}
	}
	if !found {
		t.Fatalf("fixture did not persist the application-class log source")
	}
	t.Log("application-class log source persists in the registry while every ListLogs caller is hardwired to exclude it")
}
