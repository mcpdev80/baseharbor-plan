# 0428-079 — Perses messaging dashboards — round-1

- Worker: w079 (mission-messaging lane)
- Session: own session (model verified; no session-switch this shift)
- Branch: lane-0428-079-r28-perses-messaging (the branch named in the mission)
- Candidate SHA: 62c35c9a4505fd195a2b500530dc338150698c9a
- PR: #1603 (draft), base lane-0428-080-r28-perses-selection, head lane-0428-079-r28-perses-messaging
- Planning main (evidence base): 9713c68fe06df9594b0e3cb9fc518b6a4e9d6546
- Selection base head: 8ce0df9148e4f388ba18386e3b731f1fc2cbd500 (confirmed ancestor of candidate)

## PLAN

- Reality check: confirm task is `waiting`, depends on t-20261114-r28-perses-dashboard-selection which is `NOT accepted` (content-stacking on the selection base is allowed, not a blocker); base is lane-0428-080-r28-perses-selection.
- Signal evidence: RabbitMQ declares NO observability signal on its integration descriptor. Witness (internal/capability/reference.go:173-180) — RabbitMQIntegration has `Services: []ServiceKind{ServiceMessaging}` and no `Observability:` field, unlike PostgreSQL/Valkey (requires-adapter metrics) and Prometheus/Loki/Tempo/OTelCollector (native metrics). No real metric family is produced.
- Perses format evidence: Perses native panel/dashboard JSON schema (perses.dev/v1alpha1), pinned release v0.55.1, no Go SDK module vendored in go.mod — Go structs -> JSON via encoding/json, golden-file tests.
- Confirm the branch named in the mission (lane-0428-079-r28-perses-messaging) already carries the deliverable content (PR #1603, draft, base selection). Branch is the established 079 fan; its 079 feature commit is c385abe4.
- Implement / verify own messaging catalog: internal/metrics/perses_messaging.go (fail-closed UNAVAILABLE verdict, Perses v1alpha1 JSON structs, RenderPersesMessagingDashboard, VerifyMessagingDashboardCatalogBuilds), golden JSON internal/metrics/testdata/perses/rabbitmq-messaging.json, test internal/metrics/perses_messaging_test.go.
- Local checks on candidate HEAD 62c35c9a: go build ./..., go vet ./..., go test ./internal/metrics/ ./internal/capability/, gofmt -l on the two go files.
- Record CI coverage (Release Source Preflight, ci.yml:122 go test ./internal/... under the pull_request group ci.yml:13-19, plus gofmt at ci.yml:107). Trigger reported, not dispatched (CI rulesets disabled this shift; reruns are Owner scope).
- Evidence to baseharbor-plan origin/main; END witness to Coordinator.

## Acceptance witnesses

- Real provider signals verified, missing coverage explicit:
  - RabbitMQ declares NO observability signal on its integration descriptor. Witness (internal/capability/reference.go:173-180):
    ```
    RabbitMQIntegration = IntegrationDescriptor{
      ID: "baseharbor/rabbitmq", Version: "0.1.0",
      Protocol: ProviderProtocolV1, Provider: RabbitMQ,
      Services:        []ServiceKind{ServiceMessaging},
      Capabilities:    []SpecificationID{MessagingQueueV1.ID, MessagingPubSubV1.ID, MessagingStreamV1.ID},
      SupportedScopes: []ProviderScope{ScopeApplication, ScopeExternal},
      Interfaces:      []ProviderInterface{{Name: "amqp", Class: InterfaceApplication, Protocol: "amqp", Intrinsic: true}, {Name: "management-ui", Class: InterfaceAdministration, Protocol: "https", Optional: true}},
    }
    ```
    No `Observability:` field — unlike PostgreSQL/Valkey (requires-adapter metrics) and Prometheus/Loki/Tempo/OTelCollector (native metrics). No real metric family is ever produced.
  - Therefore the messaging dashboard is UNAVAILABLE for every selection / pinned release / signal inventory; fail-closed, with a concrete reason. Decision recorded in internal/metrics/perses_messaging.go.
- Access scoped by Target/tenant; secrets out of logs/manifests/audit: the rendered JSON carries only apiVersion, kind, metadata.name, duration and a title; no secret, token, password, credential or endpoint (verified by TestMessagingDashboardRenderCarriesNoSecrets).
- Prometheus/Loki/Tempo backend ownership preserved: no changes to those backends; the messaging catalog is a separate, self-contained file. No shared file written by another lane.
- No new application capability or mandatory service forced; Perses stays a management surface, never an application capability.

## Scope / file ownership

- Own assets: internal/metrics/perses_messaging.go, internal/metrics/perses_messaging_test.go, internal/metrics/testdata/perses/rabbitmq-messaging.json.
- Shared symbols used (read-only): capability.ProviderRabbitMQ; a local mirror of the seam release value (v0.55.1) to avoid importing the seam file. No line shared with the selection catalog (internal/capability/perses_selection.go) or another lane.
- No .github/** edits (Owner scope). No merge, no ready_for_review, no force-push, no subagent.

## Evidence: CI / test run

- Local test (run in own session): on candidate HEAD 62c35c9a —
  - `go build ./...` -> exit 0
  - `go vet ./internal/metrics/ ./internal/capability/` -> clean
  - `go test ./internal/metrics/ ./internal/capability/` -> ok (metrics 0.163s, capability 0.004s)
  - `gofmt -l internal/metrics/perses_messaging.go internal/metrics/perses_messaging_test.go` -> clean
  - Verbose run of the messaging tests: TestRenderPersesMessagingDeterministic, TestVerifyMessagingDashboardCatalogBuilds, TestMessagingDashboardCatalogAlwaysUnavailable (4 subcases), TestMessagingDashboardFailClosedOnUnpinnedRelease, TestMessagingDashboardRenderIsEmptyPanels, TestMessagingDashboardRenderCarriesNoSecrets, TestMessagingDashboardEligibleForUnknownKeyStillUnavailable — all PASS.
- CI coverage: CI `Release Source Preflight` job (.github/workflows/ci.yml:122) runs `go test ./contracts/... ./internal/... ./spec/...` on every PR, so internal/metrics/perses_messaging_test.go executes in GitHub-hosted shared runners under the existing group. Trigger: pull_request to develop/main (ci.yml:13-19). gofmt compliance is also enforced at ci.yml:107-108.
- CI rulesets are disabled during the current CI repair (per repo AGENTS); CI was NOT dispatched (Owner scope: no reruns, no workflow_dispatch). Trigger reported, not run.

## PR / SHA provenance

- Branch head (ls-remote): 62c35c9a4505fd195a2b500530dc338150698c9a == candidate.
- PR #1603 head (ls-remote): 62c35c9a4505fd195a2b500530dc338150698c9a == branch head.
- PR #1603: base lane-0428-080-r28-perses-selection, head lane-0428-079-r28-perses-messaging, isDraft=true, state=OPEN, title "draft(0428-079): Perses-native messaging dashboard eligibility" (card number in title).
- Selection base 8ce0df9148e4f388ba18386e3b731f1fc2cbd500 is an ancestor of the candidate (git merge-base --is-ancestor 8ce0df91 HEAD -> OK).
- 079 feature commit c385abe4 (feat(metrics): Perses-native messaging dashboard eligibility) is the only 079 feature commit; no foreign candidate carried on top.
- Note: this shift's local worktree was a selection-base-stack branch (commit 2b8bda15) whose content is byte-for-byte identical to the existing 079 candidate. My extra branch was never pushed (push rejected: remote already has lane-0428-079-r28-perses-messaging) and carries no remote ref; nothing to delete. The mission names the existing 079 branch as the candidate and it is the one that delivers.

## Cleanliness state

- Local clones: /tmp/w-msg (renamed branch w-msg-extra-2b8bda15, unpushed, no remote ref), /tmp/fresh-079, /tmp/baseharbor-1603-check, /tmp/golden-check (scratch, git init only, no tracked product writes).
- No docker/podman compose project started this shift; nothing to bring down.
- No stray files in /home/marcel/dev/baseharbor-ecosystem; all scratch under /tmp.

## State

- END lane-0428-079-r28-perses-messaging DONE: round-1 deliverable (UNAVAILABLE messaging dashboard contract + golden/eligibility tests) delivered as draft PR #1603 on base lane-0428-080-r28-perses-selection (candidate 62c35c9a). Local build/vet/test/gofmt pass; CI trigger reported, not dispatched (rulesets disabled, Owner scope).
