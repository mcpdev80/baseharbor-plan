# CODEX-REVIEW — PR #1590

**ROLLE: REVIEW**  
**Task:** `t-20261114-r28-perses-dashboard-selection`  
**Candidate:** `e6f5e650d048c28004cdc59608e9205c648bb509`  
**Exact-head CI:** run `43794354018`, COMPLETED SUCCESS, exact SHA; `./internal/capability` passed.  
**Scope:** against seam branch at `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`; authored catalog change is two files. `git diff --check` clean.

## Verdict: REQUEST CHANGES

`internal/capability/perses_selection.go` derives eligibility from caller-supplied booleans (`persesSelected`, backend map). A caller can set these true without evidence that the manifest selects the provider, that the required signal exists for this Target, or that the provider is authorized. The contract requires eligibility based on actual signal/label/permission state, including missing metrics, unauthorized providers, other Targets, and stale registry cases; those proof conditions are absent from this API and its tests.

## Recipe

- **File/change:** `internal/capability/perses_selection.go`; take a resolved manifest/provider/signal/Target authorization witness (or an equivalent non-forgeable result from the authoritative resolver) and derive eligibility from it. Do not use freely supplied booleans as proof.
- **Tests:** cover unselected provider, absent/stale signal, unauthorized provider, other Target, and valid selected signal. Wire the caller to the authoritative resolution path and ensure the selected CI group runs the tests.
- **Stop:** stop if the repository has no authoritative signal/permission witness yet; keep the dashboard unavailable and record the missing prerequisite rather than treating a boolean as proof.

Read-only review; no merge performed.
