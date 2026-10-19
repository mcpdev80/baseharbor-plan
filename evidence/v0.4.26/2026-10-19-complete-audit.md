# v0.4.26 complete defect audit — 2026-10-19

## Scope and authority

Marcel assigned inspection and repair of the complete v0.4.26 scope. This report applies the existing canonical release audit; infrastructure resumption, closed task cards and ordinary PR CI are not release qualification. Product main remains `54acc4b66715681213788fdba395a569ddc95a1b`; no tag, promotion, publication, Pages deployment or complete pre-release was performed.

## Immutable audit inputs

| Source | Inspected revision | Meaning |
| --- | --- | --- |
| BaseHarbor develop at audit start | `7827e6491a7715e0ffffb1e7938764f6788cc30b` | Existing integrated implementation; not a frozen final release candidate |
| SQL standards correction #1004 | `887eece62ffdfe2ba694ceb1f332dc5a74ce7872` | Independently reviewed formatting/layout source |
| #1004 current trusted-target integration | `48f4c5fa443b219d160f37058a60126ddf26a68e` | Same reviewed three source blobs plus accepted #1005 policy |
| #1005 policy | `cf70fb5446ae20239836ad4f30c2dd850e3cad07` | Exact three-file/status qualification, no generic exception |
| #995 recovery correction | `be972ff39006037a9f06b904c156fe73f7f24ba8` | Real fresh-consent/current-consumer fixture correction; native result absent |
| #998 registration | `756b22dc8967d0daa7393065cd5bc15f262c7050` | Rejected by fresh source audit; original owner/branch preserved |
| #990 guided fixture | `bc6bb47a238e4fcd3d18c9ee4a51d7052f98616f` | Not independently accepted as full recovery; depends on replacement proof |
| Demo main snapshot | `a92347900ed4d1015d9bcde3d265cf9326664a40` | Its existing Core pin is `f325b93c589d8b807f44dd0086636aabe83fcd65`; no current joint qualification inferred |
| Console main snapshot | `4724d9962486de5c9f4d226a8a27edcaf8da2fcc` | Snapshot only, not tested current-Core compatibility |
| Node Connector main snapshot | `813f08a307f2357f2e16ae9307ea247186ea7dda` | Snapshot only, not tested current-Core compatibility |

These are inspected snapshots, not a replacement immutable ecosystem release matrix. Read live refs before further writes and freeze final inputs only after remaining implementation and documentation.

## Confirmed defects and actual repairs

| Finding | Exact corrective work | Actual result |
| --- | --- | --- |
| Recovery test has no fresh operations-bound consent | #995 reaches each actual fail-closed authority, accepts only its typed current plan, retries once; restore explicitly acknowledges its own destructive scope and separate owned-data decision | [CI39223771804](https://github.com/mcpdev80/baseharbor/actions/runs/39223771804) Guided/build/vet/source checks PASS; independent five-file source review [5568897605](https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5568897605) positive; native result and formal coverage still absent |
| SQL recovery seed/readback guesses runtime project/bootstrap identity despite shared default | #995 resolves the existing protected consumer binding, validates TLS/identity fields and uses the existing pgx dependency for real seed/readback; no parallel provider resolver | Same focused CI/source review; actual native consumer data recovery remains to execute |
| Complete source preflight stops at gofmt | #1004 applies exact formatter output for native SQL files | [Baseline39223971364](https://github.com/mcpdev80/baseharbor/actions/runs/39223971364) failed as diagnosed; corrected source passes formatting |
| Complete source preflight then stops at 989-line file above800/953ratchet | #1004 moves17 unchanged functions into same-package runtime_environment.go;517/481lines, no larger limits, no behavior or API changes | Complete source [39225066336](https://github.com/mcpdev80/baseharbor/actions/runs/39225066336) SUCCESS; independent full-diff review [5568994921](https://github.com/mcpdev80/baseharbor/pull/1004#pullrequestreview-5568994921) positive |
| Existing planner cannot qualify that reviewed layout | #1005 exact SHA, complete three statuses and unchanged existing Git ancestry/integration proof; existing Source Contracts/Guided/Vet/Build requirements | [CI39225531904](https://github.com/mcpdev80/baseharbor/actions/runs/39225531904) SUCCESS,60planner tests plus8consent/7GC/5reset utilities; independent policy review [5569033250](https://github.com/mcpdev80/baseharbor/pull/1005#pullrequestreview-5569033250) positive; merged `b4a5334da5bfebd9748304a68d221724ff327889` |
| #998 inferred MCP schema is PascalCase and requires proposal/consent for propose | Existing Flash/core-921 owner must correct public/nested JSON schema and actual SDK tests on its original branch | Fresh [review5569055023](https://github.com/mcpdev80/baseharbor/pull/998#pullrequestreview-5569055023): Changes required; no competing source patch or qualification of rejected old source |
| #998 expected input/consent/domain errors collapse to internal_error at real MCP boundary | Existing owner must reuse typed error owners and assert public Code/CauseCode/remediation and handler-level denial without writes | Same source review; source must be fixed and independently re-reviewed before final o1 binding |

## What the broad source run actually proves

At887eece6, [Source Preflight39225066336](https://github.com/mcpdev80/baseharbor/actions/runs/39225066336), job117969224585, completed actual formatting/readability, contract/internal/spec package tests, complete cmd/baha test selection, go vet, specified enrollment/operator/terminal/node-disconnect race checks, evidence/integration regressions, strict EN/DE docs, documentation audit, actionlint, snapshot archives/checksums and exact-commit binary smoke.

It did not enable native acceptance opt-ins and is not a Docker/Podman recovery or joint browser/Connector receipt. The existing workflow also runs historical v0.4.21 hygiene/binary-version smokes; those are not v0.4.26 readiness or release-artifact evidence. The final v0.4.26 release workflow remains separately gated by its proper tag/candidate inputs.

Current #1004 integration CI [39226182313](https://github.com/mcpdev80/baseharbor/actions/runs/39226182313) passes all four newly required hosted checks and PR Selected Checks at48f4c5f. The accompanying exact-integration push Source Preflight39226175528 also completed SUCCESS. Independent integration review5569139915 verified the unchanged source blobs; #1004 was regularly merged as19548bf0f06757bc8d7acc9f3f4001417ddd34ed. Current develop is that merge.

## Complete canonical readiness audit

| Canonical area | Verified observation | Remaining prerequisite and owner |
| --- | --- | --- |
| Scope and implementation | Current release view, task contracts and all open develop PRs were read; source-only validation is now executable after real standards fixes | Flash/core-921 corrects rejected MCP source, then independent review/binding/current CI; no acceptance by issue migration or old local APPROVE |
| Security/ownership/failure paths | #995 fixed typed-consent and actual consumer identity instead of bypassing guards; full source/race checks pass on the audited layout source | Qwen exact-SHA native recovery and automatic cleanup, with foreign/shared preservation |
| Public contracts/standards | Current provider-neutral boundaries preserved; no new provider contract introduced by layout/fixture fixes | #998 SDK/schema/typed-error repair and current CLI/JSON/MCP tests |
| EN/DE product docs/references | Existing strict builds and docs audit pass on audited source | core-922 is not started and waits for accepted registration; current README still describes preparation ofv0.4.25 |
| Changelog/release message | Current Unreleased section is empty; no currentv0.4.26release-note source tree exists at audited develop | core-922 must deliver actualv0.4.26EN/DE release prose/changelog/navigation after stable registration |
| Demo/Console/Connector | Exact current source snapshots and Demo's old Core pin recorded above | core-923 must qualify final integrated New/Edit surface and current real consumer compatibility; no earlier-release PASS substitution |
| Pages | Existing strict EN/DE source builds pass | Final current docs/navigation/Pages candidate with new release content; no public deployment before promotion |
| Final candidate/pins | Audit snapshots explicitly identified | Release preparation owner freezes final Core/Demo/Console/Connector matrix after unfinished tasks; no final candidate frozen yet |
| Required atomic/runtime evidence | Infrastructure retention and exact Git verification repaired; former #985/#989/#993 blockers were genuinely completed earlier | Qwen full #995 native Backup/Destroy/Restore and cleanup, then current-candidate Docker/Podman and consumer atomic evidence under core-923; no automatic full matrix |
| Complete pre-release/promotion/publication | Not performed or implied by these diagnostics | Separate authorized release stages after readiness; no tag, main merge or release-ready claim |

## Operational boundaries

- Protected Flash/o1 original two uncommitted files/worktree and existing claim remain intact. No CORE_921 binding was implemented by this coordinator. The distinct SQL-layout rule must be preserved when that owner normally integrates accepted target changes.
- #995 current integrated head is4ca9881766fc88e850ccdbbc2d837cabb19ebab5 against trusted develop19548bf0. Actual PR CI39226862989 passes Guided/build/vet/Source Contracts/Trusted Plan/Python; final117975666636 blocks only native coverage of five paths, without integration mismatch. Full hosted Source Preflight39227471936 is running, not native evidence.
- #995 earlier Qwen assignment is [6263247019](https://github.com/mcpdev80/baseharbor/pull/995#issuecomment-6263247019), exactbe972ff; superseded for execution by the current integration above. Older36310f/eaf868reports are historical and do not prove this changed source.
- The remote coordinator has no connected local/native executor; HF Jobs is currently unavailable. All new test claims above are actual GitHub CI, not fictional local/HF/native runs.
- An initial automatic review rejected #1005 merge for missing formal codeowner approval. The coordinator did not evade it indirectly: rechecked published solo-Maintainer authority, live PR-only review exception and the separate no-bypass Required Check/app15368, then the same regular merge was accepted. No fake GitHub APPROVE, required-check bypass or private key use.
- Development can continue on disjoint existing assignments; release readiness remains blocked. Missing evidence is never green.
