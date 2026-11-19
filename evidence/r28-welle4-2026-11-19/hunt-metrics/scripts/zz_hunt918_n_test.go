package logs

import (
	"strings"
	"testing"

	"github.com/mcpdev80/baseharbor/internal/capability"
	"github.com/mcpdev80/baseharbor/internal/observability"
)

// zz_hunt918_n_test.go — BUG-HUNT 918 cell (3n): the alert evaluator is a
// consumer of the Loki series it can list. Probe the selector each source class
// actually produces, because that selector is what a future evaluator would
// inherit from the merged registry chain.
func TestHunt918PlatformProviderSelectorHasNoEnvironment(t *testing.T) {
	// The literals the query builder emits, reproduced from query.go:113-127.
	platformQuery := `{baseharbor_source_class="platform-provider",baseharbor_provider="tempo",baseharbor_service="tempo"}`
	appProviderQuery := `{baseharbor_application="demo",baseharbor_environment="dev",baseharbor_source_class="application-provider",baseharbor_provider="loki",baseharbor_service="loki"}`
	for name, q := range map[string]string{"platform-provider": platformQuery, "application-provider": appProviderQuery} {
		hasEnv := strings.Contains(q, "baseharbor_environment")
		t.Logf("%-21s selector carries baseharbor_environment: %v", name, hasEnv)
	}
	// The collector does emit the label for platform-provider logs — but with no
	// value bound to it, so it cannot be used as a matcher.
	cfg := alloyConfigForModeSources([]Registration{{Application: "demo", Environment: "dev", SyslogPort: 15140, ProviderSyslogPort: 15141}},
		[]observability.SignalSource{{
			ID: "tempo:shared", Kind: observability.SignalLogs, Provider: capability.ProviderTempo,
			Class: observability.SourcePlatformProvider, Scope: capability.ScopeShared, SharingBoundary: "shared",
			Target: observability.RuntimeTarget("bh-shared", "tempo"), Protocol: "syslog-rfc5424",
		}}, "syslog", 15200)
	for _, line := range strings.Split(cfg, "\n") {
		if strings.Contains(line, "baseharbor_source_class") {
			t.Logf("collector labels line: %s", strings.TrimSpace(line))
		}
	}
	if !strings.Contains(cfg, `baseharbor_source_class = "platform-provider"`) {
		t.Fatalf("fixture: the platform-provider listener is missing from the collector config")
	}
	if strings.Contains(strings.Join(strings.Split(cfg, `baseharbor_source_class = "platform-provider"`)[1:], ""), "baseharbor_environment =") {
		t.Fatalf("unexpected: the platform-provider listener block binds an environment value")
	}
	// Prove the platform-provider block declares no application/environment labels,
	// i.e. its streams are indistinguishable across environments.
	platformBlock := cfg[strings.Index(cfg, `baseharbor_source_class = "platform-provider"`):]
	platformBlock = platformBlock[:strings.Index(platformBlock, "}")]
	if strings.Contains(platformBlock, "baseharbor_environment") || strings.Contains(platformBlock, "baseharbor_application") {
		t.Fatalf("platform-provider listener unexpectedly carries an owner label: %s", platformBlock)
	}
	t.Logf("platform-provider listener label set: %s", strings.TrimSpace(platformBlock))
}
