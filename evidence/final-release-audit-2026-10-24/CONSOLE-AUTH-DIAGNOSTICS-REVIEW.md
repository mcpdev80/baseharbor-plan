# Console callback race and safe native diagnostics review

Independent source verdict: APPROVE for exact staged tree `79d861526dd21606db182df6216d6eec594ad896`, parent actual U `7aed4d58f7ac89d019b1d31fa2d5bc6e557aa2b5`. Exactly seven files change; Core/manifest/receipt policy/runner/workflow bytes remain unchanged. Publication/merge identity and genuine native qualification are pending.

## Concrete source correction

The callback previously queued postMessage and immediately closed its popup. Opener independently observes popup.closed every250ms, so a due close observation can reject the legitimate queued callback before its message event executes. The existing opener already closes only after validating exact origin/source and typed callback; it retains state/issuer/PKCE/token/discovery checks. The correction extracts the unchanged validation/query scrubbing/HTTPS exact-origin handoff and removes only redundant self-close. Actual Docker timeout causality remains unproven; this is a demonstrated source race, not a retroactively fabricated runtime root cause.

A real queued MessageChannel regression fails with original self-close and passes when only opener closes after receipt. Duplicate credential-bearing callback parameters still become invalid_response; queries are scrubbed before handoff; insecure origins never post.

## Safe diagnostics and unchanged failure semantics

Editor diagnostics allow only bounded fixed phase names, popup-closed boolean and up to24 allowlisted path/method/status records. They contain no query strings, authorization codes/state, bodies, headers, credentials or tokens. They are retained in the failed receipt, not only ephemeral logs. Editor lifetime still requires exp-minus-iat1800; expires_in may reflect elapsed time but must remain a positive integer no more than1800.

Only a real failed control-plane.up triggers the fixed readonly `baha --target browser-runtime openbao status --json` command before teardown. It runs once in the selected isolated fixture with exact XDG paths and35second bound, projecting only initialized/unsealed/manager_ready booleans. Malformed or failed status remains invalid/unavailable and never creates success or a mutation retry. Raw CLI stdout/config/recovery/headers are not retained. Public machine error projection copies only validated code/cause and bounded redacted message/next, removing credential-like values, endpoints and paths. Original application/Setup failure is rethrown unchanged; normal owned cleanup remains mandatory.

## Verification

Independently ran all66 contract tests: PASS, zero skips/failures. Focused diagnostics/callback/OIDC8 tests, JS syntax and diff checks PASS. Owner reports exact-final TypeScript, ESLint, architecture and production build33routes PASS. The batch does not claim to repair underlying Core Secrets bootstrap failure; new actual U/K and authenticated native diagnostic/acceptance results remain required.

## Published source identity

Independently authenticated Console PR #11 head `4238e2e2525b5c5a4af0b7573010e4e4dc49ba35`, sole parent actual prior U7aed4d58, complete remote tree exactly `79d861526dd21606db182df6216d6eec594ad896`. Unchanged manifest blob `28fc527c6d3207097be657230e16b535e8a0c645` binds R3e27497b/D09595781. Hosted source CI, actual merge and new native evidence remain pending.

## Hosted source qualification and actual Console merge

Independently authenticated source CI `40135195710`, pull_request attempt1, exact4238e2e: completed/success. Browser opt-in was intentionally skipped and is not native acceptance. Actual Console U is `51181967abfd3170b81857d51e9a4572c84b318b`, complete tree exact reviewed79d86152, parents priorU7aed4d58 plus reviewed4238e2e.

Next Connector pin-only staged tree `740a82389c59c3fed8597590515f07be40ee14d4` independently approved atop actual priorKa956: sole Console manifest pin7aed→actual5118; R3e/D095 fixed, producer `11897d27e332d319f233ca2f6042c2ae9b5be4fc`, sentinel `ba86891cd387201ce0e9aa38763e795b8b81781b` and prior trigger ancestry unchanged. Publication/actual K and fresh actual-R bootstrap diagnostic/native acceptance remain pending.

## Actual diagnostic graph and native origin

Connector PR #12 source `19615e4f71dbebe8781a9c1f33138dff2ca61e94` remotely authenticates the approved740a tree, sole parent actual priorKa956. SourceCI `40135417539`, pull_request attempt1, exact19615: independently authenticated completed/success. Actual merged K is `c4363a28f5fd3d929a430bc6da630ee036bba104`, exact740a tree, parents priorKa956+source19615 and actual message marker `[ecosystem-runtime]`.

Actual K/U5118 manifests and unchanged authenticated D095 Core pin pass R's canonical four-role resolver. Independently generated diagnostic-graph pins SHA256 `dfd87ceb0191702e7b37a287b45ee8f792d00b926cc189a5ec9927f20d5570df`. Existing trigger branch was moved to actual K and new actual-K native run `40135623881` is pending. Underlying Secrets failure cause remains unproven; no new consumer native acceptance, selected63 run or complete65 approval is claimed.
