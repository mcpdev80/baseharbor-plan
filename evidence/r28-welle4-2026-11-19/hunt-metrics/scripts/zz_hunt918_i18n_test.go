package application

import (
	"encoding/json"
	"regexp"
	"strings"
	"testing"
)

// zz_hunt918_i18n_test.go — BUG-HUNT 918 cell (4), read-only probe. NOT
// committed to the product branch.
//
// Question: after #1663 ("localize Achtung to Warning"), is the German marker
// still produced by any Go code path, and do the two marker spellings actually
// dual-match on every machine surface?

var hunt918Marker = regexp.MustCompile(`Achtung|Warning`)

func TestHunt918MarkerVocabularyIsSingleValue(t *testing.T) {
	// The wire model value is the marker a consumer must match. Collect every
	// literal marker the shipped catalogs can emit.
	catalog := ProviderImpactConsentCatalog()
	stringsFound := []string{
		catalog.ProviderImpactLead,
		catalog.ProviderDestructiveConfirm,
		catalog.ProviderTwoStageConfirm,
		catalog.ProviderDestructiveDataConsentPrompt,
	}
	for _, s := range stringsFound {
		if strings.HasPrefix(s, "Achtung") {
			t.Fatalf("consent catalog still emits the German marker: %q", s)
		}
		t.Logf("catalog label: %s", s)
	}

	// The machine-readable marker field: build a scope that requires attention.
	scope, err := ComposeProviderImpactScope(
		ProviderScopeOwner{Owner: "installation.destroy", Reference: "/tmp/ref", Subject: "subj", Revision: "rev", Destructive: true},
		nil,
		false,
	)
	if err != nil {
		t.Fatalf("compose scope: %v", err)
	}
	raw, err := json.Marshal(scope)
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("scope attention marker on the wire: %q", scope.Attention)
	if strings.Contains(string(raw), "Achtung") {
		t.Fatalf("the JSON surface still emits the German marker: %s", raw)
	}
	if !strings.Contains(string(raw), `"attention":"Warning"`) {
		t.Fatalf("expected the English marker on the wire, got: %s", raw)
	}
}

func TestHunt918DemoMatcherVocabularyCoversBothMarkers(t *testing.T) {
	// The two marker spellings a consumer must tolerate during the rename
	// window, and the two prompt shapes the CLI actually prints.
	warnPrompt := "Warning: confirm the displayed outcome without a working alternative (2/2, plan " + strings.Repeat("a", 64) + ")? [y/N]: "
	achtPrompt := "Achtung: confirm the displayed outcome without a working alternative (2/2, plan " + strings.Repeat("a", 64) + ")? [y/N]: "
	// The non-destructive stage-1/2 label the CLI prints when
	// ConfirmationsRequired == 1 (hardcoded in cmd/baha, not the catalog):
	lowStagePrompt := "Confirm the displayed provider changes (1/1, plan " + strings.Repeat("a", 64) + ")? [y/N]: "

	for _, tc := range []struct{ name, line string }{
		{"Warning two-stage", warnPrompt},
		{"Achtung two-stage", achtPrompt},
		{"single-stage no-marker", lowStagePrompt},
	} {
		matched := hunt918Marker.MatchString(tc.line)
		t.Logf("%-24s matched-by-marker-regex=%v", tc.name, matched)
	}
	// The single-stage prompt carries no marker at all: a consumer that gates
	// on the marker string never sees this acknowledgement stage.
	if hunt918Marker.MatchString(lowStagePrompt) {
		t.Fatalf("unexpected: single-stage prompt carries a marker")
	}
}
