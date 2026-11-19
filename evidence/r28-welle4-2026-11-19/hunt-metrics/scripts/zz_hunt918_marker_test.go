package application

import (
	"strings"
	"testing"
)

// zz_hunt918_marker_test.go — BUG-HUNT 918 cell (4), read-only probe. NOT
// committed to the product branch.
//
// Question: after #1663 renamed the emitted marker to "Warning", does any Go
// code path still compare the marker against the literal "Achtung"? A surviving
// comparison would silently disable the attention gate for the renamed value.
func TestHunt918NoCodePathMatchesOnTheGermanMarker(t *testing.T) {
	// The catalog plus the wire marker must be the only vocabulary.
	catalog := ProviderImpactConsentCatalog()
	for name, label := range map[string]string{
		"provider-impact-lead":        catalog.ProviderImpactLead,
		"provider-destructive":        catalog.ProviderDestructiveConfirm,
		"provider-two-stage":          catalog.ProviderTwoStageConfirm,
		"provider-data-consent":       catalog.ProviderDestructiveDataConsentPrompt,
		"application-stop-impact":     catalog.ApplicationStopImpact,
		"external-provider-removal":   catalog.ExternalProviderRemovalImpact,
		"control-plane-stop-impact":   catalog.ControlPlaneStopImpact,
		"node-disconnect-impact":      catalog.NodeDisconnectImpact,
		"target-definition-impact":    catalog.TargetDefinitionChangeImpact,
		"runtime-destroy-destructive": catalog.RuntimeDestroyImpactDestructive,
	} {
		if strings.HasPrefix(label, "Achtung") {
			t.Fatalf("%s still emits the German marker: %q", name, label)
		}
		if !strings.HasPrefix(label, "Warning") {
			t.Fatalf("%s does not lead with the English marker: %q", name, label)
		}
	}

	// The gate is `plan.Attention != ""`, so the marker's value is irrelevant to
	// it — as long as no caller hardcodes either spelling.
	scope, err := ComposeProviderImpactScope(
		ProviderScopeOwner{Owner: "installation.destroy", Reference: "/tmp/ref", Subject: "subj", Revision: "rev", Destructive: true},
		nil, false)
	if err != nil {
		t.Fatal(err)
	}
	if scope.Attention == "" {
		t.Fatalf("destructive scope lost the attention marker: %#v", scope)
	}
	t.Logf("marker value=%q confirmations=%d destructive=%v complete=%v",
		scope.Attention, scope.ConfirmationsRequired, scope.Destructive, scope.Complete)
}
