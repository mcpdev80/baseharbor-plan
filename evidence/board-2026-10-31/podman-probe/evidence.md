# podman-probe Evidence

## PLAN Step 0: Branch setup (probe/pod0427 from develop, merge #1244 + #1239)
- Working tree: /home/marcel/dev/baseharbor-ecosystem/workers/worktrees/podman-probe
- Branch: probe/pod0427
- Merging: work/podman-gh (#1244) and work/gh-ci-core (#1239)
- Status: DONE — clean merge of both branches, CI changes integrated

## PLAN Step 1: Push to runtime-validation/ha/control-plane/podman/int0427
- Status: DONE — pushed probe/pod0427 to refs/heads/runtime-validation/ha/control-plane/podman/int0427

## PLAN Step 2: Observe CI run
- Branch: runtime-validation/ha/control-plane/podman/int0427
- Target Job: 'Targeted HA · podman' (ubuntu-26.04)
- Expected: GRUEN
- Result: ✓ GRUEN — ALL STEPS SUCCESSFUL
- Run-ID: 41267346809 (run level), Job-ID: 124732810007
- Commit SHA: 1e22d6753a0cf13fde5869b9c995f2975b853ab3
- Runtime: podman on ubuntu-26.04 GitHub-hosted runner
- Error line: N/A — no failure
- Component: rootful Podman HA setup on GitHub-hosted ubuntu-26.04
- Status: DONE — GRUEN ✓

## PLAN Step 3: Clean up temp ref
- Delete: refs/heads/runtime-validation/ha/control-plane/podman/int0427
- Status: DONE — ref deleted

## END
- Status: DONE — podman-probe complete. Targeted HA · podman GRUEN on ubuntu-26.04 GitHub-hosted.
