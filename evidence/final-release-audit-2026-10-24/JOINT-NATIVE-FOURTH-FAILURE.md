# Fourth joint native attempt — authenticated failure

Verdict: FAILURE, no current native acceptance. Run `40137607614`, push attempt1, `.github/workflows/release-integration.yml` on fixed `work/v0.4.26-integrations-docs`, exact Connector K `acc6fba541a47e73781d8ebb7b7f910e2e2e5d42`, tree `510b79340fdc5d23d5bc7d6a82dd3a1bf70d56fb`. Inputs remain Core R `3e27497b4ef7b567858ba646bc3071bee37d19bd`, Demo D `09595781b68e1f41caaba9aec1402eb8009d700f`, Console U `52993ac5623cdfa2a3b91001ed078dfd27f31b5e`. Canonical pins SHA256 `33cd462d0f159821a6f16c1d2c1e85d311fd92724b3bf61f63806d42f52011bb`.

Independent API, completed job logs and downloaded ZIP authentication:

| Runtime | Qualification job | Diagnostic artifact | Authenticated ZIP SHA256 |
| --- | --- | --- | --- |
| Docker | 121002381187 | 12577858253 | 253ae872f413021bce1bf89f628f64309cf5fd6683bdf7a07a0b235d3cde48cd |
| Podman | 121002381169 | 12577292908 | 46be09746a9913f43e22851f5a6986d8795d112ac3c2dea5e7244ff97c13d9c6 |

Both qualification jobs completed FAILURE at actual Chromium; resolver121002346682 succeeded. Prior native enrollment and exact runtime fixture cleanup succeeded. Each unexpired artifact is a distinct backend-permitted same-name `actual-browser-core-read-receipt`; its API workflow origin binds exact run/K. Actual Docker and Podman log upload IDs authenticate the mapping above. Downloaded bytes independently match API digests. Each ZIP contains only browser-receipt.json, with exact repository/K/R/D/run/attempt, result=failure, cleanup=success, release_eligible=false and error_type=TimeoutError. These are diagnostics, not qualified private integration manifests; none exists for this attempt.

Both receipts record real Core Setup phases through READY with SQL, Secrets and Identity all true. Both editor authentication diagnostics show verified lifetime and metadata/callback/token/discovery HTTP200. The protected-parent correction therefore crossed the previously failing persistence boundary in this actual execution.

Both completed job logs show consented apply succeeded, followed by plan/status/doctor/repair, successful openbao.rotate, and post-rotation status/doctor. The next ordinary destroy correctly returned approval_required / impact-confirmation-required. The browser then timed out waiting for the Provider consequences group at application-journey.mjs:295. Full application journey completion is not claimed, and the remote operator browser journey was not reached.

Independent source diagnosis corroborates the bounded Console defect: exact R local !fullReset destroy routes to runtime retirement and acknowledges a leaf provider-impact plan. Current U529's sender requires details.scope for every destroy, hiding this legitimate leaf although the generic fixture parser accepts it. Core still revalidates the PlanID before retirement; this is a consumer rendering/decoding mismatch, not evidence for weakening Core authorization. Reviewed six-file correction is documented separately in CONSOLE-RETIREMENT-REVIEW.md and requires fresh normal integration plus real native qualification.

The authoritative published0fd6c922 freeze was terminally updated and preserved as freeze-sources.failed-acc6fba5.json, with exact corresponding failed pin snapshot. All earlier failed snapshots remain. Current selected63, W1, full65 approval, promotion/Pages and tag readiness remain open. No retry, source successor or future native success is inferred here.
