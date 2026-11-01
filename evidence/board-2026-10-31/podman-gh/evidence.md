# Evidence: podman-gh Mission

## PLAN

- [x] Step 0: Read mission file, set up evidence and todo
- [ ] Step 1: Create `scripts/ci-podman-gh-runtime.sh` — rootful Podman setup on GH-hosted ubuntu runner
- [ ] Step 2: Update Targeted-HA-podman Job in `.github/workflows/ci.yml` — point Prepare step to new script
- [ ] Step 3: actionlint + YAML validation
- [ ] Step 4: VALIDATION — workflow_dispatch / minimal job proving `podman run alpine` works on GH-hosted
- [ ] Step 5: Push to `work/podman-gh`, open PR against develop, report END_DONE
