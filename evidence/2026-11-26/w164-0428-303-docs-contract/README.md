# w164-0428-303-docs-contract

Docs contract lane for two hunt34 cards sharing one write-set (`docs/reference/cli.md` family):

- `t-20261125-hunt34-ghost-subcommand-app-show` (0428-303) — ghost `baha app show`
- `t-20261125-hunt34-cli-json-flag-contract` (0428-304) — single `--json`/`--output` contract

Branch: `lane-0428-hunt34-docs-contract`

## PLAN

- Verify planning repo remote is github (not the workers/ bookkeeping checkout)
- Fetch develop + main via ls-remote witnesses from own clone zone
- Build the shipped binary from develop HEAD and drive `baha <cmd> --help` as ground truth
- Check `baha app show` existence + `--json`/`--output`/`--format` contract per subcommand
- Run the authoritative machine-docs drift test
- Record findings; no product change needed when drift is a false positive

## Reality witnesses (own clone zone /tmp/opencode/v34-wt)

- `git -C /tmp/opencode/v34-wt remote -v` -> `origin ssh://git@github.com/mcpdev80/baseharbor.git`
- `git ls-remote origin refs/heads/develop` -> `a87da7d179e08d43e8987885c38ab459ff1d887d`
- `git ls-remote origin refs/heads/main` -> `7bdeae95ccf0ce0d2fe39ae6d4c884402268995d`

Planning repo (evidence home):
- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` -> `https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push). Confirmed NOT the workers/ bookkeeping checkout.

Branch provenance:
- `git ls-remote origin refs/heads/develop` -> `a87da7d179e08d43e8987885c38ab459ff1d887d` (base anchor)
- Branch cut from develop head `a87da7d179e08d43e8987885c38ab459ff1d887d`
- `git merge-base --is-ancestor a87da7d179e08d43e8987885c38ab459ff1d887d HEAD` -> true

## Ground truth (built binary from develop HEAD, NOT guessed)

Built `/tmp/baha-develop-v34` from develop HEAD `a87da7d17` and `/tmp/baha-v34-demo` from the product checkout.

### BF-01 — `baha app show` is NOT a ghost (HUNT FINDING REVERSED)

- The hunt34 akte (BF-01) claimed `baha app show` is "documented but NOT a real CLI subcommand" and that the real overview command is `baha status`, repro `/tmp/baha-v34 app show --help -> Error: 'show' is not a registered subcommand of 'app'`.
- Reality on develop HEAD `a87da7d17`: `cmd/baha/app_show.go` exists (long-standing since v0.4.22); wired into `cmd/baha/commands.go:220` (`case "show"` -> `appShowCommandWithRecoveryMetadata(store)`); the `--json` output path is live.
- Empirical: `/tmp/baha-develop-v34 app show --help` prints `show - Show a coherent application overview` with `Usage: baha app show [NAME]`. `/tmp/baha-develop-v34 app show --json` returns a structured contract.
- Conclusion: the BF-01 ghost was a false positive from a stale develop anchor (the akte anchor was `f7540e59`). The docs reference `baha app show` correctly; there is nothing to remove or point-out.

### BF-02 — single `--json`/`--output` contract already holds (no drift)

- Product ground truth per read subcommand (both flags accepted, return structured contract):
  - `app show`, `app plan`, `app list`, `app status`, `app new`, `app inspect`, `app env`, `app restore`, `app secret list` -> both `--json` and `--output json` accepted.
  - `app env` additionally uses `--format dotenv|shell|json|yaml` (documented in `docs/reference/cli-machine-coverage.md:25`).
  - `app exec` has no JSON output (execute-only, correctly undocumented).
- Docs already document the single contract: `docs/reference/cli-machine-coverage.md` (`CLI -o json / typed MCP result`, with `--format json` noted for `app env`); EN `docs/cli/command-index.md` per-row (`[-o json\|--output json]` / `--json`); DE mirror likewise.

### Authoritative drift test (contract, not guess)

- `BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test ./cmd/baha/ -run TestMachineDocumentationTracksRegistryAndCommandTree -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` -> `ok` (exit 0). Docs already track the command tree and JSON contract. No write-set change required.

## repo-rule compliance

- Docs-only verification. No `cmd/` code touched; no flag renamed; no `.github/**` touched.
- No product repo writes outside the write-set; no `.evidence/` directory in the product repo.
- All flag claims verified against a freshly-built develop binary, not guessed.

## cleanliness

- No containers/compose started. `docker ps -a` header-only before and after (session pid, read-only desk).
- cleanliness: read-only docs verification, zero runtime started, no orphaned resources.

## END

- w164-0428-303-docs-contract END_DONE — hunt34 findings reversed (BF-01 ghost = false positive from stale anchor; BF-02 JSON contract already holds). No product change needed. Authoritative drift test `ok`. Two cards documented as one verification lane.
