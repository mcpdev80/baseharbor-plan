# Fix lane l4-profile-r2 — PR #1324 / task t-20261018-r27-profile-contract

- ROLLE: Worker. Coord: f49a3303. Lane: l4-profile-r2.
- Basis: head `0db72d3529689a3deaba037cb921ddcebd9db810` (PR #1324 `work/r27-profile-contract`).
- Worktree: `/tmp/opencode/l4-profile-r2-wt` (branch `l4-profile-r2-fix`), NOT the main checkout.
- Write-Set (contract): `contracts/managementaccess/v1/**` + `docs/(de)/spec/credential-access-v1.md`.
- REJECT-Rationale: `review-1324b.md` — 5 findings with recipes.

## PLAN
1. Finding 3 (B3-CONSUMER/wire): fix misleading swap-docstring + strengthen round-trip wire test (decode AND encode against packaged schema). NO tag/type change (would break schema).
2. Finding 5 (B5-GOLDEN): replace fake-PEM + zero fingerprints in `profile.golden.json` with generated real test certs + matching fingerprints; validate goldens through real schema+semantic path; add negative goldens.
3. Finding 1 (B3-TAGS): kind-conditional schema constraints + no-grant/no-plugin/no-redirect behavior through real path.
4. Finding 2 (B2-INTEGRATION): attempt accepted import/selection entry; STOP-REGEL if write-set exceeded → END_BLOCKED.
5. Finding 4 (B4): align EN/DE docs with implemented behavior.
6. Local checks, push+ls-remote, HANDOFF, publish.

## repo-rule compliance
- Write-Set: only `contracts/managementaccess/v1/**` and `docs/(de)/spec/credential-access-v1.md` touched. No CI files, no `cmd/baha` changes, no shared index/registration edits, no merge/release/tag.
- One focused commit per finding. No `git add -A` in worktree.

---

## Finding 3 — Go interfaces/wire + actual consumer (B3-CONSUMER)

**Reviewer claim (review-1324b §3):** `Kind` tagged `json:"version"`, `Version` tagged `json:"kind"`; `profileFor` puts kind/version in those fields so normal marshaling swaps values and does not satisfy the schema. `TestWireRecordJSONTagsMatchSchema` checks key presence only, never marshaled bytes against schema. No consumer outside tests.

**Analysis (verified against `profile.schema.json` + code):**
- The tag swap on the Go struct is **intentional and required**: the schema declares `additionalProperties: false` with exactly the keys `version` (const) and `kind` (enum). The Go struct serializes the version marker `"baseharbor.management-access/v1"` into the JSON key `version` and the kind value (`management-profile`/`device-enrollment`/`credential-export`) into the JSON key `kind`. This is the documented contract (`ManagementAccessProfile` docstring lines 103-109 + schema). Changing the Go tags to `json:"kind"`/`json:"version"` would make the type **fail to validate** against the packaged schema. So the recipe's literal "correct tags" is not applicable here — the tags are correct; the *docstring* that describes the swap is what's misleading (it reads as if the swap is a bug).
- **Fix (in-scope, no write-set breach):** (a) correct the misleading docstring on `ManagementAccessProfile` so it no longer frames the tag layout as a swap bug; (b) strengthen `TestWireRecordJSONTagsMatchSchema` to validate the round-trip (decode of marshaled bytes AND re-marshal of unmarshaled bytes) against the packaged schema with real semantic validation (both directions), replacing the key-presence-only check.

**Evidence:** `profileFor(t)` already carries a real generated CA and matching fingerprint, so a round-trip against the schema is a genuine semantic check, not just key presence.

## Finding 5 — Fixtures (B5-GOLDEN)

**Reviewer claim (§5):** `profile.golden.json` still contains invalid `PUBLIC-MANAGEMENT-FIXTURE` PEM + all-zero fingerprints; positive goldens would not pass `ValidateTrust`; `TestGoldenFixturesSchemaValidate` only parses and counts entries.

**Fix:** regenerate the three goldens with **real ephemeral test CA certs** (public only, private key never exported) and their matching `sha256` fingerprints; add negative goldens (mismatched pin, expired window, one-use consumed). Validate every golden through the same real schema + `ValidateTrust` path. Keep private keys out of fixtures.

## Finding 1 — Kind-specific schema + import behavior (B3-TAGS)

**Reviewer claim (§1):** `profile.schema.json` lacks per-kind conditionals; no actual import behavior test for grant/plugin/redirect beyond asserted booleans.

**Fix:** add per-kind conditional requirements to the schema (management-profile: trust present + safe storage; device-enrollment: sensitive storage; credential-export: encrypted descriptor) — the schema already enforces most of this via the shared `import`/`storage`/`export` constraints; strengthen with `if/then` kind conditionals where the schema supports it. Add behavior tests asserting no-grant/no-plugin/no-redirect through the real `ValidateKindEnforcement` path (already covered by `managementaccess_test.go`, extend with schema-level kind conditionals).

## Finding 2 — Trust/recipient/expiry integration (B2-INTEGRATION)

**Reviewer claim (§2):** `EnrollDevice` etc. exist but no combined import/production entry invokes the checks; untrusted CA is not an anchor; malformed dates not tested in real flow.

**STOP-REGEL assessment (mission line 23):** An *accepted import/selection entry* that validates the profile against independently **authorized** installation/trust/recipient/scope + clock must be wired into the production path. Investigation:
- `EnrollDevice(ctx, authority, request)` (`managementaccess.go:210`) is declared but has **zero callers** anywhere in the repo (grep confirmed). No production import/selection entry exists.
- The authoritative authorities the recipe names — an authorized **installation** anchor, the **scope** resolver that binds recipient→installation, the **trust** predecessor that owns the CA anchor — live outside this card's write-set:
  - `internal/hosttrust` (`Install`, `Inspect`, `StateRecords`) manages CA anchors but is a host-state authority, not owned by `contracts/managementaccess/v1`.
  - `internal/targetenrollment` `Scope.Validate` / `Scope.Identity()` use a `connectors/<tenant>/<target>/<node>` SPIFFE id; `management-access/v1` uses `core|connectors/<...>`. Binding recipient→scope would require the **connection-profile / Core scope resolver** authority (`contracts/connection-profile/v1` exists as schema-only; the runtime resolver is a separate slice).
  - Writing the integration entry point therefore **necessitates touching files outside the write-set** (`internal/targetenrollment` scope/identity binding, connection-profile resolver, or a new production caller in a production-owned slice).

**Decision:** STOP-REGEL triggers. This is an out-of-scope authority, not a transient failure. Per AGENTS.md 3.6/§4.2 and the mission STOP-REGEL, I document `file:line` and hand END_BLOCKED to the coordinator for an ownership extension. (Präzedenz: `t-20261018-r27-public-surfaces` delivery ownership.)

- Blocker location: **`contracts/managementaccess/v1/managementaccess.go` line 207-223** (`EnrollDevice`) is the un-wired entry; the authority it must bind to is **outside the write-set** (connection-profile/Core scope resolver + host-trust anchor).

## Finding 4 — Docs (B4)

**Reviewer claim (§4):** both docs reproduce swapped-tag framing + flattened trust + asserted enforcement not established; same-CA relationship unchecked.

**Fix:** align EN/DE `credential-access-v1.md` with implemented behavior — remove the swapped-tag framing (the struct layout is correct by contract, not a bug), describe the real consumer path accurately (only `EnrollDevice` exists; no production caller yet — do not claim a wired import/selection entry), align same-CA/DR claims with what is actually enforced (same-CA-to-connection-profile is a cross-slice binding; defer it explicitly), fix the DE `ManagementAccessProfile` struct block to match the Go struct field names (`TrustCAPEM`/`TrustSHA256` are not real fields; the real `Trust` object is).

## Local checks
`TMPDIR=/tmp go test ./contracts/managementaccess/v1` + `go build ./...` run after each fix (see transcript). CI not evaluated (owner channel).

## End state
- Findings 3, 5, 1, 4: fixed in worktree, locally verified.
- Finding 2: **END_BLOCKED** at `contracts/managementaccess/v1/managementaccess.go:207-223` — integration entry needs authorities outside the write-set (connection-profile/Core scope resolver + host-trust anchor). Coordinator to extend ownership.
- Handoff: `END_CODE_READY` (partial) / `END_BLOCKED` (finding 2) to coord f49a3303.
