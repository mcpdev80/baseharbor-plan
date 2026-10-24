# Corrected-graph joint native failure — independently authenticated

Run `40133582447`, push attempt 1, actual Connector K `a95639b3448fe869fca439d2db071fe75b82d7d2`, Core R `3e27497b4ef7b567858ba646bc3071bee37d19bd`, Demo D `09595781b68e1f41caaba9aec1402eb8009d700f`, Console U `7aed4d58f7ac89d019b1d31fa2d5bc6e557aa2b5` did **not** qualify the three consumer gates. Selected 63 remains held.

## Actual jobs and diagnostic artifacts

| Runtime | Actual job | Actual Chromium failure | Diagnostic artifact | Authenticated ZIP SHA256 |
| --- | --- | --- | --- | --- |
| Docker | 120990316354 | Editor sign-in completion timeout before application journey | 12576541257 | 7964fdea7ef39b21f92d3f5d92618694efd8497e9f93444a82a15a2443dd7ed4 |
| Podman | 120990316278 | Actual Settings control-plane.up terminal failure, internal_error/no cause | 12576257011 | f4726d1d6852f9488ac10af433e07dec0822da91acc641c9ec9f21f808544929 |

Both native managed enrollment and exact runtime-fixture cleanup passed before Chromium. Both final owned test service/private-key cleanup steps completed SUCCESS. Downloaded both ZIPs independently and compared their hashes against current GitHub artifact metadata. Each contains only browser-receipt.json, with exact run/attempt/K/R/D, result failure, cleanup success and release_eligible false. No matrix-specific private qualified manifest exists. Same-name diagnostic uploads both actually succeeded; there is no 409 blocker in this backend.

Podman logs demonstrate the corrected initial unconsented local apply returned approval_required/impact-confirmation-required, then the real explicit Settings Core Setup ran. Installation observation: phase secrets_failed, ready false, SQL true, secrets false, Identity false. The failure is in actual installation bootstrap rather than the consent decoder. Current archived diagnostics do not expose the underlying internal cause, so no exact root cause or Core repair is claimed yet.

Docker diagnostics show twelve prior auth/read-only steps completed, but the network list belongs to the first viewer page; it does not prove the later editor callback/token/discovery cause. A concrete source race exists independently: callback postMessage queues a message then closes itself immediately, while opener polls popup.closed and may reject first. The opener already closes the popup after validated origin/source/typed message. Removing redundant callback self-close preserves existing auth/PKCE/state checks, but must not be represented as experimentally proven cause of this exact timeout. Any bounded safe phase diagnostics must omit authorization codes, state, tokens, credentials and credential-bearing URLs; no automatic sign-in retry.

Both failures remain unresolved at this checkpoint. Source freezes/native acceptance must be updated only after a reviewed concrete correction and genuine new matching-source evidence. Historical source CI, prior native subfamilies and successful cleanup do not create consumer release acceptance.
