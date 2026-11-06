# w244 image-adapter smoke — round 4

- Role: CODEX-WORKER; coordinator: `841e7734`.
- Mission: `coordinator/missions/w244-img-adapter-smoke.txt`.
- Candidate: PR #1402, exact source SHA `c8272e9f3d04654fb711fbc5a716eb538bdba6dd`.
- Result: **END_BLOCKED — product defect confirmed from exact candidate source and the round-3 runtime transcript.** No product source was changed.

## PLAN

1. Read mission, task card, prior review act 1402d, and round-3 host evidence.
2. Inspect the exact PR source and its executable dispatch path; search for production CLI call sites.
3. Check and claim VM locks one host at a time; perform no host operation while another lane owns the lock.
4. Record the exact product finding and lock outcome in this evidence file; publish it to plan `origin/main` before END.

## Exact candidate finding

At `c8272e9f3d04654fb711fbc5a716eb538bdba6dd`:

- `cmd/baha/application_image_transfer.go:251-252` makes `RuntimeImageTransferSource.Resolve` run `podman image inspect --format '{{.RepoDigests[0]}}'`.
- `cmd/baha/application_image_transfer.go:260` and `:362-364` make platform inspection run `podman image inspect --format '{{.Config.Architecture}}|{{.Config.OS}}'`. Target inspection repeats the Podman repo-digest command at `:324-325`.
- When `Exec` is nil, `runTransfer` calls `execArtifact`; `cmd/baha/application_registry_source.go:184-193` runs the supplied executable name directly with `exec.CommandContext`. The default path therefore invokes `podman`, independent of the Docker runtime.
- A candidate-branch search finds the adapter definition and tests only; no production CLI call site invokes `ImageTransfer` or constructs `RuntimeImageTransferSource`. The requested `baha` command path is not present in this candidate.

The prior real-host record `round-3.md` identifies the tested Podman as 5.7.0 and explicitly records that `{{.RepoDigests[0]}}` fails with `bad character '['`, and that `.Config.Architecture` is not parseable there. Its successful Podman transcript instead uses `{{(index .RepoDigests 0)}}` and `{{.Architecture}}|{{.Os}}`. The Docker host transcript manually uses `docker` commands, which do not exercise this candidate's hard-coded `podman` execution path. These are direct command/content mismatches, not an ambiguous host-identity issue.

## VM lock and smoke status

At `2026-11-06T13:11:08Z`, `coordinator/scripts/vm-lock.sh status` reported:

```text
baha-docker: w237 @ 2026-11-06T13:06:05Z
baha-podman: w243 @ 2026-11-06T13:04:44Z
```

`codeman agent list --json` showed both `w237-devenv-smoke` and `w243-remote-control-r2` busy. Sequential `vm-lock.sh claim` attempts for this lane returned `BUSY` / exit 3 on both hosts: Docker was held by w237 (contrary to this mission's “docker frei” note), and Podman was held by w243. No claim was acquired. No SSH command or other VM operation was run; neither foreign lock was released or modified.

Because the exact candidate already has a reproducible runtime-template defect documented by the prior Podman 5.7 host output, the alternative “round-3 note was misleading” path is not supported. This lane did not repeat the host smokes because both VM locks were held and the candidate's default adapter command is known to fail on Podman 5.7 and is fixed to the wrong executable for Docker.

## Handoff

The required adapter-level Docker/Podman smoke cannot pass on this candidate. The correction must select the native executable and supported inspect format for the chosen runtime, add a real callable CLI/production path, and exercise that exact candidate path on both hosts after the VM locks are released. No such correction was made in this worker lane.

No subagents, product edits, branch updates, PR actions, tests, or VM mutations were performed.

## origin/main publication witness

Pending publication; record the exact `ls-tree` output after pushing this evidence.

Initial origin/main witness: `100644 blob 6c795f102da6cbdb2ab690ee60b010651f84bc19 evidence/r27-welle5-2026-11-06/image-transfer/round-4.md`.
