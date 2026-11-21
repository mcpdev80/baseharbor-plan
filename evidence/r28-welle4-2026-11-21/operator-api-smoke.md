# Operator API runbook smoke — 2026-11-21

## Source and CI

- Product source inspected at current `develop` `97b2ba5543f07b820b5c18a688058fd932c4516f`.
- PR [#1587](https://github.com/mcpdev80/baseharbor/pull/1587) was merged at `5b26be1ccfc52e41d53e88ef91e7f77c92e9e8ef`.
- Exact ready-PR run [44885697655](https://github.com/mcpdev80/baseharbor/actions/runs/44885697655) completed SUCCESS at PR head `c43d816120651c33a7a9c02f6ee805ae78440602`; PR `Selected Checks` and documentation jobs executed. The merged develop tree contains the English and German operator API runbook and the `baha serve --help` documentation reference.

## Read-only real-Core probes

The dedicated test VM `192.168.6.178` already had a running Core installation and `baha serve` process when inspected. No process, container, or Core state was started, stopped, or changed. The installed server binary reports commit `50610004d4bb9af26c495b1fcbe509a50681858f`, which is an ancestor of the inspected develop SHA above.

The Core API CA at `$HOME/.local/share/baseharbor/targets/local/managed-serving/core-api/ca.pem` was used with normal certificate validation; no TLS verification bypass was used. Read-only requests to `https://192.168.6.178:18443` returned:

| Request | HTTP result | Meaning |
| --- | --- | --- |
| `GET /healthz` | 200 | TLS and liveness route respond |
| `GET /readyz` | 200 | readiness route responds |
| `GET /api/v1/machine/discovery` without credentials | 401 | protected API rejects anonymous caller |
| `GET http://192.168.6.178:18443/healthz` | 400 | plaintext request does not reach the HTTPS handler |

## Remaining acceptance gap

This validates the live Core's TLS/liveness/readiness and anonymous-denial behavior. It does not validate the full documented workstation-to-Core path: no `baseharbor-core` remote Target is configured in the workstation CLI, no workstation enrollment was performed, no operator login/token was used, and no authenticated discovery or CLI status request was made. The documentation itself labels that physical workstation-enrollment path unverified. Leave 0427-169 in Wait until that full path can be exercised without guessing or changing another user's active workstation configuration.
