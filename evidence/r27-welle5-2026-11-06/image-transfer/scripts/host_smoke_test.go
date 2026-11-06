package main

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"testing"
	"time"

	bhruntime "github.com/mcpdev80/baseharbor/internal/runtime/contract"
)

type hostSmokeRuntime struct {
	bhruntime.RuntimeProvider
	kind   bhruntime.ProviderKind
	runner ExecFunc
}

func (r hostSmokeRuntime) Kind() bhruntime.ProviderKind { return r.kind }

func (r hostSmokeRuntime) PullImage(ctx context.Context, ref string) error {
	_, err := r.runner(ctx, string(r.kind), "image", "pull", ref)
	return err
}

func hostSmokeQuote(value string) string {
	return "'" + strings.ReplaceAll(value, "'", "'\"'\"'") + "'"
}

func TestRuntimeImageTransferRemoteHostSmoke(t *testing.T) {
	host := os.Getenv("BH_IMAGE_TRANSFER_SMOKE_HOST")
	kind := bhruntime.ProviderKind(os.Getenv("BH_IMAGE_TRANSFER_SMOKE_RUNTIME"))
	if host == "" || kind == "" {
		t.Skip("set BH_IMAGE_TRANSFER_SMOKE_HOST and BH_IMAGE_TRANSFER_SMOKE_RUNTIME for locked host smoke")
	}
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Minute)
	defer cancel()
	runner := func(ctx context.Context, tool string, args ...string) (string, error) {
		parts := []string{hostSmokeQuote(tool)}
		for _, arg := range args {
			parts = append(parts, hostSmokeQuote(arg))
		}
		command := exec.CommandContext(ctx, "ssh", "-F", "/home/marcel/.ssh/config", "-o", "BatchMode=yes", host, strings.Join(parts, " "))
		out, err := command.Output()
		if err != nil {
			return "", fmt.Errorf("remote %s failed (exit=%v)", tool, err)
		}
		return strings.TrimSpace(string(out)), nil
	}
	location := "quay.io/libpod/alpine:latest"
	beforeContainers, err := runner(ctx, string(kind), "ps", "-aq")
	if err != nil {
		t.Fatal(err)
	}
	identity, err := (RuntimeImageTransferSource{
		Runtime: kind, Location: location, Exec: runner,
	}).Resolve(ctx)
	if err != nil {
		t.Fatalf("source adapter resolve failed: %v", err)
	}
	runtime := hostSmokeRuntime{kind: kind, runner: runner}
	target := RuntimeImageTransferTarget{Compose: runtime, Exec: runner}
	if err := target.Copy(ctx, identity.ImmutableIdentity()); err != nil {
		t.Fatalf("target adapter copy failed: %v", err)
	}
	verified, err := target.Verify(ctx, identity.ImmutableIdentity())
	if err != nil {
		t.Fatalf("target adapter verify failed: %v", err)
	}
	if err := identity.Verify(verified.Digest, verified.ManifestDigest, verified.Architecture, verified.OS); err != nil {
		t.Fatalf("source/target identity mismatch: %v", err)
	}
	afterContainers, err := runner(ctx, string(kind), "ps", "-aq")
	if err != nil {
		t.Fatal(err)
	}
	if beforeContainers != afterContainers {
		t.Fatalf("host container list changed: before=%q after=%q", beforeContainers, afterContainers)
	}
	t.Logf("host=%s runtime=%s source=%s target=%s digest=%s platform=%s/%s containers-before=%q containers-after=%q",
		host, kind, location, identity.ImmutableIdentity(), identity.Digest, identity.Architecture, identity.OS, beforeContainers, afterContainers)
}
