package logs

import (
	"strings"
	"testing"
)

// zz_hunt918_f_test.go — BUG-HUNT 918 cell (2f), read-only probe. NOT committed
// to the product branch.
//
// Question: #1680 dropped the Prometheus-attributed workload log source. Are any
// other provider-attributed log sources with an application class still emitted
// into the collector config (i.e. scrapable) even though the registry listing
// hardwires them away?
func TestHunt918AlloyConfigHasNoApplicationClassDrain(t *testing.T) {
	cfg := alloyConfigForModeSources([]Registration{{Application: "demo", Environment: "dev", SyslogPort: 15140, ProviderSyslogPort: 15141}}, nil, "syslog", 15200)
	for _, line := range strings.Split(cfg, "\n") {
		if strings.Contains(line, "baseharbor_source_class") {
			t.Logf("labels line: %s", strings.TrimSpace(line))
		}
	}
	if strings.Count(cfg, `baseharbor_source_class = "application"`) != 1 {
		t.Fatalf("expected exactly one application-class listener block, got %d",
			strings.Count(cfg, `baseharbor_source_class = "application"`))
	}
}
