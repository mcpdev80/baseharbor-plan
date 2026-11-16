# Design — opt-in notification routing on the existing Perses/alerts contract

Card: `t-20261114-r28-perses-contact-routing` / mission-074 (design-only, read-only)
Evidence base: alerts PR #1613 @ `470735c1d` (lane `w073-perses-alerts`) + secure-access PR #1599 @ `85b01f0ff` (lane `lane-welle2-089-perses-secure-access`). Both READ-ONLY: fetch + inspect, no merge, no product change this round.

## PLAN (nummerliste, no checkboxes)

- Read mission + coordinator scope decision (design-only, no product code)
- Verify planning origin HEAD (`0f07a89a`) and both base heads via `git ls-remote`; both base heads confirmed as ancestors of their PR heads
- Inventory alerts #1613 recipient/routing surface (file:line)
- Inventory secure-access #1599 recipient/routing surface (file:line)
- Alertmanager compatibility check: compatible integration, opt-in routing cost, decision options A/B/C with cuts + risk
- Interface sketch (types + file paths, file-accurate) + recommendation
- Open-point list for owner-pin incl. explicit address of the alerts positive-path contract (queue 124)
- Write this design-akte
- Commit to planning origin/main, push, witness origin/main in evidence
- END post

## SCOPE

Design artifact only. No product code, no PR to baseharbor, no `.github/**` edit, no merge, no subagent. The two base PRs are read-only references. The owner decides the queue-124 positive-path contract; this design only shows which place depends on it.

## WITNESSES

Planning repo (authoritative, before first evidence commit):
```
$ git ls-remote origin HEAD
0f07a89a9b965d2983649f6759a422e6ccf61d28	HEAD
```

Base heads (read-only refs, both ancestors of their PR heads):
```
$ git ls-remote origin refs/heads/w073-perses-alerts
470735c1d187d8a680ae3b0539d75f592c945110	refs/heads/w073-perses-alerts
$ git ls-remote origin refs/heads/lane-welle2-089-perses-secure-access
85b01f0ff6df9f45179a7754f6cf4a5daa224d1a	refs/heads/lane-welle2-089-perses-secure-access
```

## 1. Inventory — what the two PRs already deliver on the routing/recipient surface

### 1.1 alerts PR #1613 (`470735c1d`)

File: `internal/metrics/perses_prometheus_alerts.go` (224 lines). It delivers ONLY the fail-closed alerting **data model + contract**, never a running evaluator or a notification sender:

- `PersesAlertEvaluator` struct — `json:"kind"`, `json:"name"`, `json:"evaluator,omitempty"`, `json:"owner,omitempty"`, `json:"recipient_validated"` — `internal/metrics/perses_prometheus_alerts.go:74-92`.
- `PersesAlertEvaluationResult` — `Evaluator` + `Reachability` — `:96-106`.
- Reachability vocabulary is the three-state fail-closed contract: `not_enabled` (`PersesAlertReachabilityNotEnabled`, `:54`) and `configured_unverified` (`:61`). The "real evaluator" is `PersesAlertEvaluatorKind = "PrometheusRuleEvaluator"`, `:68`.
- Entry points: `BuildPersesAlertEvaluator(m)` (`:131`) and `VerifyPersesAlertEvaluatorHealth(ctx, m)` (`:194`).
- The fail-closed guard is `persesAlertRealEvaluatorContractPresent() -> false` (`:181`); every selected+pinned surface returns `not_enabled` with `RecipientValidated=false`.
- **Not wired into the CLI/status surface.** `git grep` at the PR head shows the two public entry points are referenced only in `internal/metrics/perses_prometheus_alerts_test.go`. Nothing in `cmd/baha` or `app_status_result.go` calls them yet (`git grep` result: zero non-test references outside the contract file). The existing Perses three-state status (`not_configured | configured_unverified | verified`) in `capability.PersesStatusNow` (`internal/capability/perses.go`) is a SEPARATE surface from the alert evaluator contract.
- Test contract confirms fail-closed: `recipient_validated` never true without the (currently-absent) evaluator contract; no secrets ever materialized (`PersesAlertEvaluatorNoSecretInContract` test).

Recipient surface delivered by #1613: **a typed evaluator/owner/recipient_validated contract plus two reachability states (`not_enabled`, `configured_unverified`), gated behind a contract gate that is currently hard-false.** No route, no sender, no Alertmanager-facing field.

### 1.2 secure-access PR #1599 (`85b01f0ff`)

Delivers the operator-access **decision** contract for the Perses surface behind the service-access gateway — this is the closest existing "recipient" contract, but it is an operator-ACCESS contract, not a notification-recipient contract:

- `internal/application/perses_management_ui.go`: `EvaluatePersesOperatorAccess(ctx, PersesAccessRequest) (PersesAccessDecision, error)` (`:85`).
- `PersesAccessDecision` struct (`:47-71`): `Allowed`, `ReasonCode`, `Reason`, `ActorMode`, `Tenant`, `ManagementRole`, `Class`, `RoleMappings`, `ProxyRoutes`, `ProxyDenyReason`.
- `perses_security.go`: `PersesSecurityPolicy` (`:50`), `DefaultPersesSecurityPolicy`/`AnonymousPersesSecurityPolicy` (`:97`,`:113`), `ValidatePersesSecurityPolicy` (`:120`), version floor `persesMinSecureVersion = "v0.55.0"` (`:39`), `PersesProxyDestinationAllowed(policy, endpoint)` (`:307`) — most-specific-prefix precedence.
- `internal/serviceaccess/perses_gateway.go`: `BuildPersesGateway` (`:106`), `PersesComposeServices` (`:240`), `EnsurePersesGatewayMaterial` (`:298`) — binds Perses to loopback, gateway is the only published address, refuses `/proxy/`.

Recipient surface delivered by #1599: **an operator-access allow/deny decision (with tenant + role + proxy-deny) evaluated against a validating security policy.** It proves *who may reach Perses*, not *who is the recipient of a notification*. No notification/recipient field exists here (`git grep` for recipient/evaluator/notify/registry in `perses_management_ui.go`: none).

## 2. Alertmanager compatibility check

### 2.1 What "compatible Alertmanager integration" would mean here

BaseHarbor does **not** ship an Alertmanager client or a Prometheus-rule-evaluation runtime in this Core. The existing contract (1613) deliberately ships *only* the evaluator/owner/recipient data model + a fail-closed gate, and names `prometheus` as the owner reference. A compatible Alertmanager integration therefore must:

- carry the Alertmanager notification-relevant fields on the same owner/scoped contract (receiver + routes),
- stay fail-closed: an opt-in alert with no validated recipient must never advertise "alerting enabled" / "route configured",
- not invent a notification-channel secret or a Prometheus/Perses runtime probe.

### 2.2 Decision options for opt-in routing on the existing integration

**Option A — Extend the existing contract with a typed notification-route field, fail-closed.**
- Cut: add exactly one field to `PersesAlertEvaluator` in `internal/metrics/perses_prometheus_alerts.go:74` — e.g. a `*PersesAlertNotificationRoute` (receiver name + optional route matcher / escalation) — gated behind the same `persesAlertRealEvaluatorContractPresent()` gate so it cannot pass without a real evaluator. Wire `VerifyPersesAlertEvaluatorHealth` (`:194`) to also require the route before returning the positive reachability.
- Risk: LOW. Uses the already-established fail-closed guard; the field is inert (fail-closed) until the evaluator contract is present. No new package, no new surface. The only real decision — *what the receiver name / route shape is* — is the queue-124 owner contract and stays with the owner.

**Option B — Gate opt-in routing behind a NEW, owner-approved real evaluator + recipient contract.**
- Cut: introduce a new `internal/metrics/perses_alert_routing.go` + a new capability contract for the real Alertmanager/Prometheus notification receiver, plus a golden test. Keep `persesAlertRealEvaluatorContractPresent()` false.
- Risk: MEDIUM-HIGH. Expands scope to a new contract surface and a new positive-path; the positive path is exactly the queue-124 contract this mission must not decide. Best as a follow-on, not this design.

**Option C — Do not extend the contract this round; document the routing seam as STATE.**
- Cut: leave `perses_prometheus_alerts.go` untouched; record the required notification-route field + the wiring point in `app_status_result.go`/`app_dev_routing.go` as an open finding.
- Risk: LOWEST for scope, but delivers a weaker artifact. Good as a fallback, but Option A is strictly better for a "contact-routing design" because it pins the exact field + wiring and keeps the fail-closed invariant.

### 2.3 Compatibility verdict

The existing integration is **compatible for Option A** because the fail-closed gate already exists and already rejects exactly the wrong thing (an alert with no validated recipient). The cost of opt-in routing on it is: one typed route field, one caller check in the health verifier, one golden test. The cost of Option B (a real Alertmanager notification runtime) is a whole new subsystem and is out of scope for a design round. **Recommendation: Option A**, with the receiver/route shape left to the owner's queue-124 contract.

## 3. Interface sketch (types + file paths, file-accurate)

### 3.1 Where opt-in routing plugs in

- The routing/recipient surface the opt-in route must feed is the **devgateway route graph**, not a parallel surface:
  - `internal/devgateway/gateway.go:39` — `Route` struct (`Owner, Key, Host, PathPrefix, LandingPath, Upstream, Network, TrustFile, ServerName, ManagementKey, DirectIPPort`).
  - `internal/devgateway/gateway.go:53` — `OwnerRoutes{Owner, Routes}`.
  - `cmd/baha/app_dev_routing.go:35-62` — filters routes by `route.Owner` (`app/...`, `shared/prometheus`, etc.) and dedupes by `route.Host`.
  - `cmd/baha/app_dev_routing.go:179` — `plan.groups = append(plan.groups, devgateway.OwnerRoutes{Owner: plan.appOwner, Routes: plan.appRoutes})`.
- The alerting contract the route hangs on is:
  - `internal/metrics/perses_prometheus_alerts.go:74` — `PersesAlertEvaluator`.
  - `internal/metrics/perses_prometheus_alerts.go:131` — `BuildPersesAlertEvaluator(m)`.
  - `internal/metrics/perses_prometheus_alerts.go:194` — `VerifyPersesAlertEvaluatorHealth(ctx, m)`.

### 3.2 Minimal typed route field (Option A)

Proposed addition to `PersesAlertEvaluator` at `internal/metrics/perses_prometheus_alerts.go:83` (after `Evaluator`, before `Owner`):

```
// NotificationRoute is the opt-in recipient/route this contract requires
// before it may be considered "routing enabled". Nil = no opt-in recipient,
// so the contract stays fail-closed. Shape (receiver name, optional matcher
// and escalation) is the owner's queue-124 contract; this field only carries
// it and never invents a value or a channel secret.
NotificationRoute *AlertNotificationRoute `json:"notification_route,omitempty"`
```

with a local (private, in the same file) supporting type:

```
type alertNotificationRoute struct {
    Receiver       string   `json:"receiver"`
    Matchers       []string `json:"matchers,omitempty"`
    EscalateTo     string   `json:"escalate_to,omitempty"`
}
```

The positive reachability (`configured_unverified`) at `persesAlertEvaluatorFromRelease` (`:158-167`) stays gated by `persesAlertRealEvaluatorContractPresent()` (`:155`); a route without a real evaluator yields `not_enabled`. `VerifyPersesAlertEvaluatorHealth` (`:194`) is the natural place to assert the route is present before returning nil — but the *route shape itself* is the owner's queue-124 contract.

### 3.3 Wiring (design only — no product change this round)

Design point: the opt-in route becomes observable on the status surface at the same place the Perses three-state contract is already exposed (`cmd/baha/app_status_result.go:138`), as a new machine-readable field alongside `Perses`. That wiring is a follow-on task, not part of this design.

## 4. Open points for the owner-pin (explicitly)

### 4.1 [OWNER DECISION] queue-124 — the alerts positive-path contract

The mission names this explicitly. My design **does not** decide it; it only shows where it attaches:

- **What the owner must define:** the real evaluator contract that flips `persesAlertRealEvaluatorContractPresent()` from `false` to `true` (`internal/metrics/perses_prometheus_alerts.go:181`) AND the notification-recipient/route shape (receiver name + matcher + escalation) that the `NotificationRoute` field in §3.2 carries. Until an Owner-approved real evaluator + recipient contract exists, the positive path stays fail-closed (`not_enabled`).
- **Where it blocks the design:** `BuildPersesAlertEvaluator` (`:131`) and `VerifyPersesAlertEvaluatorHealth` (`:194`) both return the fail-closed error when the evaluator contract is absent. Any opt-in routing this round would be gated by that same gate, so the design cannot produce a "routing enabled" result — which is correct and intended.
- **Contract witness (LUNA line):** "Enable a positive path only after a real evaluator and recipient/owner contract is defined and implemented; add tests using that actual contract and exact-head CI" (perses-alerts round-4 evidence). **No evaluator, recipient, receiver, route or secret is invented** by this design (§3.2 carries the field only; it does not name a receiver).

### 4.2 [OWNER DECISION] Alertmanager vs Prometheus rule-evaluation as the real evaluator

This Core ships no Alertmanager client. The owner must decide whether the real evaluator is (a) a Prometheus rule-evaluation path (matching the existing `PrometheusRuleEvaluator` kind at `:68`) or (b) a new Alertmanager notification path. This decision selects the whole downstream implementation; it is not a design choice.

### 4.3 [STATE] opt-in route must not leak into the devgateway route graph as a fabricated capability

The devgateway route graph (`internal/devgateway/gateway.go:39`, `cmd/baha/app_dev_routing.go:35`) reports owned routes. An opt-in notification route must NOT appear as a published gateway route; it is a recipient binding, not a routable address. Design holds the two surfaces separate and reports the coupling point (§3.3).

## 5. Recommendation

Adopt **Option A** in §2.2: extend `PersesAlertEvaluator` (`internal/metrics/perses_prometheus_alerts.go:74`) with exactly one fail-closed `NotificationRoute` field, gated behind the existing `persesAlertRealEvaluatorContractPresent()` (`:181`) and asserted in `VerifyPersesAlertEvaluatorHealth` (`:194`); expose it on the status surface alongside the existing Perses three-state field at `cmd/baha/app_status_result.go:138` as a follow-on. All three open points in §4 remain owner decisions; the design invents no receiver, route, evaluator or secret.

## SCOPE / WITNESS (post)

- planning origin/main HEAD witnessed (above), candidate committed to it, log shows only my own commit.
- no product repo touched, no `.github/**` edited, no merge, no subagent.
- compose/Docker: none started this round.
- Candidate provenance (origin, after push):
  ```
  $ git log --oneline -1 origin/main
  aab30249 design(0428-074): opt-in notification routing on Perses/alerts contract (read-only design-1)
  $ git ls-tree -r origin/main --name-only | grep perses-contact-routing
  evidence/r28-welle3-2026-11-16/perses-contact-routing/design-1.md
  ```

## END

END lane: mission-074-contact-routing-design — DONE (design-1.md committed + pushed to planning origin/main; read-only design, no product change)
