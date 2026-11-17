//go:build perses_infra_cell

// Cell witness (0428-082 round-5, Luna batch18 unproof (b)): it runs the
// PRODUCT verification path — metricsprovider.PersesInfraDashboardAvailability
// and VerifyPersesInfraDashboard, exactly what cmd/baha/app_status_result.go
// calls from `baha status --json` — against a Prometheus the deploy path
// materialized on the cell machine (BASEHARBOR_STATE_DIR points at the
// provider state a `baha app up` wrote). Every panel verdict printed here
// came from the panel's own real /api/v1/query round trip over the
// service-access client; scrape series actually returned rows. The build tag
// keeps it out of the default CI matrix; scripts/cell-witness.sh runs it
// explicitly on the named cell host.
package metrics

import (
	"os"
	"strings"
	"testing"

	"github.com/mcpdev80/baseharbor/internal/application"
)

func TestPersesInfraDashboardCellWitness(t *testing.T) {
	state := strings.TrimSpace(os.Getenv("BASEHARBOR_STATE_DIR"))
	if state == "" {
		t.Fatal("BASEHARBOR_STATE_DIR must point at the deploy-path provider state")
	}
	targetName := strings.TrimSpace(os.Getenv("BASEHARBOR_TARGET"))
	if targetName == "" {
		t.Fatal("BASEHARBOR_TARGET must name the deploy-path Target owning the provider state")
	}
	manifestPath := strings.TrimSpace(os.Getenv("BAHA_CELL_MANIFEST"))
	if manifestPath == "" {
		t.Fatal("BAHA_CELL_MANIFEST must name the applied baseharbor.yaml")
	}
	data, err := os.ReadFile(manifestPath)
	if err != nil {
		t.Fatalf("read manifest: %v", err)
	}
	m, err := application.ParseYAML(string(data))
	if err != nil {
		t.Fatalf("parse manifest: %v", err)
	}
	if !m.Services.ObservabilityManagementUI || !m.Services.Perses {
		t.Fatal("the cell manifest must select the Perses observability surface")
	}

		res, err := VerifyPersesInfraDashboardAt(t.Context(), m, state, targetName)
	for _, s := range res.Signals {
		t.Logf("CELL panel=%s missing=%v query=%s", s.Panel, s.MissingSignal, s.Query)
	}
	if err != nil {
		t.Fatalf("CELL verify over the materialized Prometheus failed: %v", err)
	}
	entries := PersesInfraDashboardAvailabilityAt(t.Context(), m, state, targetName)
	available := 0
	for key, entry := range entries {
		t.Logf("CELL availability[%s]=%s query=%s reason=%s", key, entry.Available, entry.Query, entry.Reason)
		if entry.Available == PersesInfraDashboardAvailable {
			available++
		}
	}
	if available == 0 {
		t.Fatal("CELL no panel answered rows against the materialized Prometheus")
	}
	t.Logf("CELL RESULT available=%d/%d", available, len(entries))
}
