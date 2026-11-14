---
id: 2026-11-14-perses-replaces-grafana-v0428
status: accepted
sources: []
---
# v0.4.28 observability: Perses replaces Grafana UI work

On 2026-11-14 the Owner directed that the planned Grafana visualization cards be rewritten or replaced by Perses and that obsolete cards be closed. The 19 unassigned Grafana cards are closed as superseded, with an explicit successor for each; old IDs and history remain. Perses successor cards remain planned and depend on the same release startup, with targeted dependency edges. Card creation is not implementation, acceptance, a release or proof of support.

Perses is an optional provider-owned visualization surface, not an application capability or required Core bundle. Keep Prometheus, Loki and Tempo data owners and explicit selection separate; Grafana Loki and Tempo are distinct backend products and are not removed merely because the Grafana dashboard UI is replaced. Evaluate the pinned Perses release and its actual supported plugins, security fixes, image, data-source models and license before implementation; do not assume direct Grafana dashboard JSON parity. Perses documentation describes [Prometheus](https://perses.dev/docs/plugins/prometheus/), [Loki](https://perses.dev/plugins/docs/loki/) and [Tempo](https://perses.dev/plugins/docs/tempo/) plugins. Verify support and shipped plugin versions in the selected candidate.

Grafana-specific alert rule/contact-point assumptions are not interchangeable with Perses. Re-specify alert rule evaluation, notification routing and optional Alertmanager integration using existing supported Prometheus/Alertmanager contracts or other Owner-approved mechanisms. The [Prometheus Alertmanager documentation](https://github.com/prometheus/alertmanager/blob/main/docs/overview.md) describes Prometheus rule evaluation sending alerts to Alertmanager. Perses's [release notes](https://github.com/perses/perses/blob/main/CHANGELOG.md) mention an Alertmanager plugin, which alone does not prove rule management or routing parity. No silent removal of alerting requirements and no invented integration.

The [public Console/Node Connector freeze](2026-11-14-public-console-connector-scope.md) remains in force: direct work was dropped and historical accepted evidence remains closed. The Core can still contain existing node/connector compatibility code, but v0.4.28 acceptance must not depend on changes or qualification in an archived public repository. This decision does not alter historical release records or publish a new product release.
