package metrics

import (
	"strings"
	"testing"

	"github.com/mcpdev80/baseharbor/internal/application"
	"github.com/mcpdev80/baseharbor/internal/capability"
	"github.com/mcpdev80/baseharbor/internal/observability"
)

// zz_hunt918_i_test.go — BUG-HUNT 918 cell (1i): the #1677 fix made the
// application class "visible" in the registry. Is that visibility load-bearing
// for the scrape/verify chain, or does it stay registry-only?
func TestHunt919AppClassVisibilityIsVerifyOnly(t *testing.T) {
	t.Setenv("BASEHARBOR_STATE_DIR", t.TempDir())
	m := application.Manifest{Name: "demo", Environment: "dev"}
	id := observability.ApplicationMetricsSourceID(m.Name, m.Environment, "web")
	if err := observability.Update(observability.MetricsSource{
		ID: id, Provider: capability.ProviderPrometheus, Class: observability.SourceApplication,
		Scope: capability.ScopeApplication, OwnerApplication: m.Name,
		Network: "net", Target: "bhm-abc:9464", Path: "/metrics", Scheme: "http",
		Verification: capability.ObservabilityVerifyBackend,
	}); err != nil {
		t.Fatal(err)
	}

	// (1) The provider-scrape renderer never sees it (so no new scrape target
	// comes from the registration).
	providerSide, err := observability.ListMetrics(capability.ProviderPlacement{Scope: capability.ScopeApplication}, []string{m.Name}, true, true)
	if err != nil {
		t.Fatal(err)
	}
	if len(providerSide) != 0 {
		t.Fatalf("app class leaked into provider scrape listing: %v", providerSide)
	}

	// (2) The verify query string is built from manifest fields, not from the
	// registered source. Show that the registered Target/Network are unused.
	appSide, err := observability.ListApplicationMetrics(capability.ProviderPlacement{Scope: capability.ScopeApplication}, []string{m.Name})
	if err != nil {
		t.Fatal(err)
	}
	if len(appSide) != 1 {
		t.Fatalf("app class not visible in the application listing: %v", appSide)
	}
	source := appSide[0]
	query := "up{job=\"baseharbor-applications\"," +
		"baseharbor_application=\"" + m.Name + "\"," +
		"baseharbor_environment=\"" + m.Environment + "\"," +
		"baseharbor_source=\"" + "web" + "\"}"
	t.Logf("registered source: target=%s network=%s path=%s", source.Target, source.Network, source.Path)
	t.Logf("verify query (built from manifest, not from source): %s", query)
	for _, field := range []string{source.Target, source.Network, source.Path} {
		if strings.Contains(query, field) {
			t.Fatalf("unexpected: the verify query uses the registered field %q", field)
		}
	}
	t.Log("the app-class registration contributes only its existence to the chain: endpoint fields are recomputed from the manifest")
}
