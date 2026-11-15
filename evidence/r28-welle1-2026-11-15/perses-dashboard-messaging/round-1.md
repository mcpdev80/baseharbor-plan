# 0428-079 — Perses messaging dashboards — round-1

- Worker: w079
- Session: df058c89 (model verified; no session/switch recorded this shift)
- Branch: lane-0428-079-r28-perses-messaging
- Candidate SHA: c385abe4e451ff50df997c86d7420dcb2c4bb1aa
- PR: #1603 (draft), base lane-0428-080-r28-perses-selection, head lane-0428-079-r28-perses-messaging
- Base HEAD (develop): 0e9ccb582f5bdcdc74049bbe3996263cdce6500c — confirmed ancestor of c385abe4

## PLAN

- Reality check: confirm 079 branch absent; 080 selection PR #1590 still OPEN (not accepted); develop HEAD pinned.
- Signal evidence: verify RabbitMQ has NO native metrics signal (capability/reference.go) and no metrics source flows through observability/registry.go ListMetrics; record concrete witness.
- Perses format evidence: confirm Perses native panel/dashboard JSON schema (percli DAC), pinned release v0.55.1, and no Go SDK module vendored — Go structs -> JSON via encoding/json, golden-file tests.
- Create lane-0428-079-r28-perses-messaging from develop HEAD; write basehead sha in evidence; show ancestor; log lists only my commits.
- Implement messaging dashboard eligibility: RabbitMQ ships no native Perses signal -> UNAVAILABLE (mirror postgres/mongo); own messaging catalog + Go structs -> Perses JSON; minimal shared symbols (PersesDefaultRelease value) in a new file.
- Golden-file test per panel + eligibility tests (absent provider, no exporter, fail-closed, tenant isolation, dashboard provisioning).
- Draft PR #1603 (title includes 0428-079) against lane-0428-080-r28-perses-selection; record candidate SHA.
- Clean up; END witness to Coordinator.

## Acceptance witnesses

- Real provider signals verified, missing coverage explicit:
  - RabbitMQ declares NO observability signal on its integration descriptor. Witness
    (internal/capability/reference.go:173-180):
    ```
    RabbitMQIntegration = IntegrationDescriptor{
      ID: "baseharbor/rabbitmq", Version: "0.1.0",
      Protocol: ProviderProtocolV1, Provider: RabbitMQ,
      Services: []ServiceKind{ServiceMessaging},
      Capabilities: []SpecificationID{MessagingQueueV1.ID, MessagingPubSubV1.ID, MessagingStreamV1.ID},
      SupportedScopes: []ProviderScope{ScopeApplication, ScopeExternal},
      Interfaces: []ProviderInterface{{Name: "amqp", Class: InterfaceApplication, Protocol: "amqp", Intrinsic: true}, {Name: "management-ui", Class: InterfaceAdministration, Protocol: "https", Optional: true}},
    }
    ```
    No `Observability:` field — unlike PostgreSQL/Valkey (requires-adapter metrics),
    Prometheus/Loki/Tempo/OTelCollector (native metrics). No real metric family is
    ever produced.
  - Therefore the messaging dashboard is UNAVAILABLE for every selection / pinned
    release / signal inventory; fail-closed, with a concrete reason. Decision recorded
    in evidence and in `internal/metrics/perses_messaging.go`.
- Access scoped by Target/tenant; secrets out of logs/manifests/audit: no secrets
  referenced; the rendered JSON carries only metadata + a title.
- Prometheus/Loki/Tempo backend ownership preserved: no changes to those backends;
  the messaging catalog is a separate, self-contained file.

## Scope / file ownership

- Own assets: internal/metrics/perses_messaging.go, internal/metrics/perses_messaging_test.go,
  internal/metrics/testdata/perses/rabbitmq-messaging.json.
- Shared symbols used (read-only): capability.ProviderRabbitMQ; a local mirror of the
  seam release value (v0.55.1) to avoid importing the seam file. No registry/catalog
  line shared with another lane.
- No .github/** edits (Owner scope). No merge, no ready_for_review, no subagents.

## Evidence: CI / test run

- Local test (run by worker, own session): `go test ./internal/metrics/ ./internal/capability/` -> ok; `go vet ./...` clean; `go build ./...` clean.
- CI coverage: CI `Release Source Preflight` job (`.github/workflows/ci.yml:122`) runs
  `go test ./contracts/... ./internal/... ./spec/...` on every PR, so the new
  internal/metrics test executes in GitHub-hosted shared runners under the existing
  group. Trigger: `pull_request` to develop/main (ci.yml:13-19).
- CI rulesets are disabled during the current CI repair (per repo AGENTS); CI was NOT
  dispatched (Owner scope: no reruns, no workflow_dispatch). Trigger reported, not run.

## PR / SHA provenance

- Base head fetched (fresh clone of mcpdev80/baseharbor, origin/develop): 0e9ccb582f5bdcdc74049bbe3996263cdce6500c
- `git merge-base --is-ancestor 0e9ccb58 HEAD` -> ancestor confirmed.
- `git log --oneline origin/develop..HEAD` lists ONLY c385abe4 (no foreign commits carried).
- Remote branch head (ls-remote): c385abe4e451ff50df997c86d7420dcb2c4bb1aa == candidate.
- Branch provenance: cut from develop HEAD 0e9ccb58, not from any PR head (#1590/#1597).

## Cleanliness state

- Worktree: /tmp/opencode/w079-wt (baseharbor clone; my branch lane-0428-079-r28-perses-messaging).
- No docker/podman compose project started this shift; nothing to bring down.
- Misplaced product-repo evidence removed from workers/.models/ornith/evidence.
- /tmp/opencode/w079-wt left as-is; /tmp/perses-verify left as-is (read-only verify clone).

## State

- END lane-0428-079-r28-perses-messaging DONE: round-1 deliverable (UNAVAILABLE messaging dashboard contract + golden/eligibility tests) delivered as draft PR #1603 on base lane-0428-080-r28-perses-selection. CI reported not dispatched (rulesets disabled; Owner scope).
