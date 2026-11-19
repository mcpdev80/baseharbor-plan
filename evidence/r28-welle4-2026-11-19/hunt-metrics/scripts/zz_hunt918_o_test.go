package metrics

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/mcpdev80/baseharbor/internal/runtimeoperation"
)

// zz_hunt918_o_test.go — BUG-HUNT 918 cell (1o): the runtime-metrics target
// file key. runtimeTargetFileName hashes app+caller+resource (no environment)
// and the writer then stores an environment-labeled group; readTarget rejects a
// mismatch. Probe: can two environments of one application coexist in the shared
// runtime-metrics directory, and what does the environment field feed?
func TestHunt918RuntimeTargetFileKeyHasNoEnvironment(t *testing.T) {
	dir := t.TempDir()
	req := runtimeoperation.Request{Application: "demo", CallerService: "api", ResourceName: "runtime"}
	t.Logf("file key for app+caller+resource: %s (no environment in the hash inputs)", runtimeTargetFileName(req))

	// The same tuple under two environments lands at the SAME path.
	for _, env := range []string{"dev", "prod"} {
		e, err := NewRuntimeSourceExecutor(env, dir)
		if err != nil {
			t.Fatal(err)
		}
		if err := e.writeTarget(req, runtimeSource{Port: 9464, Path: "/metrics"}); err != nil {
			t.Fatalf("writeTarget %s: %v", env, err)
		}
		entries, _ := os.ReadDir(dir)
		names := []string{}
		for _, en := range entries {
			names = append(names, en.Name())
		}
		if len(names) != 1 {
			t.Fatalf("expected exactly one shared file, got %v", names)
		}
		got, err := e.readTarget(req)
		if err != nil {
			t.Fatalf("readTarget %s: %v", env, err)
		}
		t.Logf("environment=%s file=%s -> readTarget port=%d path=%s", env, names[0], got.Port, got.Path)
		// Both environments read successfully from the same file because the
		// ownership check compares only application/service/source; the stored
		// environment label is the LAST writer's.
		data, _ := os.ReadFile(filepath.Join(dir, names[0]))
		if len(data) == 0 {
			t.Fatal("empty target file")
		}
	}
	// The final on-disk environment label is whichever deployment wrote last.
	last, err := NewRuntimeSourceExecutor("dev", dir)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := last.readTarget(req); err == nil {
		t.Log("a dev executor still reads the tuple after a prod write overwrote the file label (label is not a read key)")
	} else {
		t.Logf("dev executor after prod write: %v (environment IS part of the read-time ownership check)", err)
	}
}
