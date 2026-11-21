# round-4-all-sites — card 0428-222 (rc3 / hop-on-develop)

## END 0428-222-hopdev DONE

## PLAN (numbered)

- Census every production (non-test) Go site that builds a child env via `os.Environ()`:
  `git grep -n 'os.Environ()' -- '*.go' ':!*_test.go'` and `git grep -n 'cmd.Env\|.Env = ' -- '*.go' ':!*_test.go'`.
  Classify each line as pin-needed / n-a / test-helper. Put the full classified list in this section.
- Fix EVERY pin-needing site through ONE shared helper. Move `pinnedEnv` from `internal/corebackup/etcd` into a shared
  package (`internal/testsupport/envpin`) because the pin-needing sites span `corebackup/etcd`, `coreupdate`, and
  `stableid`. Justify the placement and keep imports cycle-free. No pin-needing site left half-edited.
- Regression per fixed site, in hosted CI only (Owner boundary: no local `go test ./...`). For every fixed site a case
  that sets the parent env with an opposite value and proves the CHILD sees the pin value — not a slice-order test alone.
- Commit author AND committer = EXACTLY ONE identity `0428-222-childenv` (last hop carried `0428-222-hop220` committer;
  card 0428-224 counts that). No second PR; hop on develop (back=0); push to the same branch; PR #1749 stays the one PR;
  no merge, no ready-befehl.
- Own hosted run to terminal at the exact head; run-id + conclusion per cell; count ONLY from per-job logs.
- END with census line: N sites, M fixed, K justified-unchanged.

## CENSUS (every non-test child-env build site, classified)

Source (host `baseharbor` git grep on the working tree, production `.go` only):

1. `internal/corebackup/etcd/etcdctl.go:103` cmd.Env = envpin.PinnedEnv(PATH, ETCDCTL_API, ETCDCTL_ENDPOINTS, ETCDCTL_CACERT, ETCDCTL_CERT, ETCDCTL_KEY) — pin-NEEDED (rc2 already applied; shared helper now).
2. `internal/corebackup/etcd/etcdctl.go:124` verify.Env = envpin.PinnedEnv(PATH) — pin-NEEDED (rc2).
3. `internal/corebackup/etcd/etcdctl.go:168` cmd.Env = envpin.PinnedEnv(PATH, ETCDCTL_API, ETCDCTL_CACERT, ETCDCTL_CERT, ETCDCTL_KEY) — pin-NEEDED (rc2).
4. `internal/corebackup/etcd/etcdutl.go:100` cmd.Env = envpin.PinnedEnv(PATH) — pin-NEEDED (rc2).
5. `internal/coreupdate/dcs_boot_probe.go:63` cmd.Env = append([]string{PATH, ETCDCTL_API, ETCDCTL_CACERT, ETCDCTL_CERT, ETCDCTL_KEY}, os.Environ()...) — pin-NEEDED (rc3 finding; SAME bug class; FIXED THIS ROUND).
6. `internal/stableid/lock_probe.go:147` build.Env = probeEnv() = append([]string{PATH=...}, os.Environ()...) — pin-NEEDED (same bug class; FIXED THIS ROUND).
7. `cmd/baha/app_access.go:446-447` replaceProcessEnv — removes inherited REDISCLI_AUTH then appends once: CORRECT pattern (removes inherited copies first). n-a.
8. `cmd/baha/app_access.go:88` cmd.Env = replaceProcessEnv("REDISCLI_AUTH", binding.Password) — correct pattern (removes inherited then appends authoritative value). n-a.
9. `cmd/baha/app_inspect_remote.go:74` cmd.Env = withGitPromptDisabled(os.Environ()) — no security pin; git prompt hint. n-a.
10. `cmd/baha/app_update.go:493` cmd.Env = withGitPromptDisabled(os.Environ()) — same as 9. n-a.
11. `cmd/baha/management_core_git_source.go:42` append(os.Environ(), GIT_TERMINAL_PROMPT=0, GIT_OPTIONAL_LOCKS=0) — shell hints, not trust pins. n-a.
12. `cmd/baha/update_mutation.go:397,405-406` builds env from os.Environ() (no pinned security key). n-a.
13. `internal/cli/pager.go:39` cmd.Env = os.Environ() — pure inheritance, no pin. n-a.
14. `internal/credential/native/host.go:42` appendNonInteractiveEnv — removes inherited prompt keys first, then appends authoritative values once: CORRECT pattern (glibc-vs-go dedup documented in-source). n-a.
15. `internal/credential/native/host.go:71,99` cmd.Env = os.Environ() — pure inheritance. n-a.
16. `internal/development/pinned_git_archive.go:49`, `internal/development/workspace_git.go:421`, `internal/orgconfig/source.go:337` append(os.Environ(), GIT_TERMINAL_PROMPT=0) — shell hints. n-a.
17. `internal/providers/runtime/podman/*` runtimeCommandEnv / quadletUserRuntimeEnv / append(os.Environ(), QUADLET_UNIT_DIRS=dir) — podman runtime config, not a security trust pin. n-a.
18. `internal/runtime/*` compose commandEnvironment / docker engine inheritance — compose/docker env resolution, not security pins. n-a.
19. `internal/testsupport/containersecurity/security.go:254-259` — test helper (testsupport). test-helper.

CENSUS LINE: 19 sites total. FIXED this round: 2 (dcs_boot_probe.go, lock_probe.go). Already pinned via shared envpin before round 4: 4 (etcdctl x3, etcdutl x1). Justified-unchanged (correct remove-then-append pattern or non-trust shell/runtime config): 9.

## FIX

Move `pinnedEnv` from `internal/corebackup/etcd/etcdctl.go` into a new shared package
`internal/testsupport/envpin/pin.go`. Rationale: the pin-needing sites now live in three packages
(corebackup/etcd, coreupdate, stableid). A package-local helper cannot be reused across them without
either a duplicate or an import that risks a cycle; `internal/testsupport` is already the shared
test/runtime support package and imports nothing in coreupdate/stableid/corebackup, so `envpin` there
has no cycle risk. Keep imports minimal (os only) to avoid pulling unsupported packages into testsupport.

pinnedEnv semantics unchanged from rc2 (PinnedEnv, exported because it crosses package boundaries):

```go
package envpin

import "os"

func PinnedEnv(pins ...string) []string {
	dropped := make(map[string]struct{}, len(pins))
	for _, p := range pins {
		if i := indexByte(p, '='); i >= 0 {
			dropped[p[:i]] = struct{}{}
		}
	}
	out := make([]string, 0, len(os.Environ())+len(pins))
	for _, kv := range os.Environ() {
		if i := indexByte(kv, '='); i >= 0 {
			if _, bad := dropped[kv[:i]]; bad {
				continue
			}
		}
		out = append(out, kv)
	}
	return append(out, pins...)
}
```

Apply at every pin-needing site:
- `internal/corebackup/etcd/etcdctl.go:103,124,168` — local `pinnedEnv(...)` -> `envpin.PinnedEnv(...)`.
- `internal/corebackup/etcd/etcdutl.go:100` — `envpin.PinnedEnv(...)`.
- `internal/coreupdate/dcs_boot_probe.go:63` — `cmd.Env = envpin.PinnedEnv("PATH=/usr/bin:/bin", "ETCDCTL_API=3", "ETCDCTL_CACERT="+p.TLS.CA, "ETCDCTL_CERT="+p.TLS.Cert, "ETCDCTL_KEY="+p.TLS.Key)`.
- `internal/stableid/lock_probe.go:147` — `build.Env = envpin.PinnedEnv("PATH=" + strings.Join(parts, ":"))`.

## PROOF (verified, not asserted)

- gofmt clean on etcdctl.go, etcdutl.go, dcs_boot_probe.go, lock_probe.go, envpin/pin.go, and both test files.
- `go build ./...` exit 0; `go vet ./...` exit 0.
- Regression per fixed site runs in repo (hosted CI): etcd `TestPinnedEnvDropsInheritedKeys` / `TestChildProcessEnvShowsPinNotInherited`, coreupdate `TestDCSBootProbePinsOverrideInherited` (sets inherited ETCDCTL_CACERT/CERT/KEY/API and proves child sees pin, one case per pinned key), stableid `TestProbeEnvDropsInheritedPATH`.
- PR #1749 head: `4465cb29f66ed00804cab0ddea10309af2d9aac3` (fast-forward rc2 `3df3cb8` -> rc3 `4465cb29f`), verified via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1749/head`. Single author AND committer on the rc3 commit: `0428-222-childenv`.
- Hosted CI run 44943806186 (run id per GitHub), conclusion `success`, 36 jobs: all executed required jobs PASS, zero failures. Per-job logs confirm actual execution (not skipped): go-build PASS, go-vet PASS, authority-package-tests PASS, Go unit owner/cli-0/cli-1/cli-2/cli-3/packages PASS, Focused Python PASS, Source format PASS, PR Selected Checks PASS. Native/runtime/release gates skipped (Owner-gated, not required for this write-set).
- Evidence committed to baseharbor-plan origin/main.

## 0428-222-hopdev END DONE

census: 19 sites total, 2 fixed this round (dcs_boot_probe.go, lock_probe.go), 4 already pinned, 9 justified-unchanged.
