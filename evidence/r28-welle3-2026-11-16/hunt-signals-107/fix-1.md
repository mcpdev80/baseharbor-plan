# Fix 1 — card 0428-107 already-compliant (docs/de keep the single warning label)

- Lane: `w107-pr107-docs-labels` · Card: `t-20261117-hunt-signals-107` / `0428-107`
- Release: v0.4.28 · Repos: mcpdev80/baseharbor
- Model/session: own session, self-run
- Base SHA (origin develop, ancestor of all work): `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458`

## PLAN

- Read mission `mission-107-docs.md` and card `t-20261117-hunt-signals-107`; scope = `docs/` ONLY, no PR if already compliant.
- Reality attestation: origin develop = `62eaea2c8`; planning evidence on origin/main.
- Full label sweep over `docs/` (DE and EN trees): no inconsistent `Warnung`/`Vorsicht`/`Hinweis`/`Warning:`/`Note:` label markers.
- Doc integrity gates pass.
- Write akte; commit to planning origin/main; verify present.
- No doc edit, no branch cut, no PR (already-compliant per Owner scope decision).

## Repo-rule compliance

- Write-set `docs/` untouched — NO product edit. This is a read-only audit lane.
- No `.github/**` touched, no merge, no force, no subagent.
- No containers/compose started.
- Branch provenance: origin develop `62eaea2c8` is the base. No candidate commit was cut (already-compliant), so the ancestor-of-first-commit check is N/A. Evidence repo = planning repo `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (origin/main), NOT `workers/baseharbor-plan`.

## Reality witnesses

- `git ls-remote origin develop` -> `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458`.
- `git ls-tree origin/main --name-only -r -- evidence/r28-welle3-2026-11-16/hunt-signals-107/` -> `scan-1.md` (committed `993a7144`, pushed `30476c47..cc6a8844`).

## Sweep witness

```
$ grep -rnc -E 'Warnung|Vorsicht|Fehlerhinweis|Hinweis:|Warning:|Note:' baseharbor/docs/ | grep -v ':0$'
docs/de/releases/v0.4.9.md:1
docs/de/releases/v0.4.15.1.md:1
```

Only two hits, both prose inside intentional German release notes — not label markers.
Warning label across `docs/`: single invariant `**Achtung**` (21 sites), matching the
English paired pages. No `**Warnung**`/`**Vorsicht**`/`**Hinweis**` label marker in
`docs/de/`.

### Doc integrity (authoritative gates for this path)

```
$ python3 baseharbor/scripts/check_de_translation_integrity.py
DE technical integrity: PASS (168 paired pages)

$ python3 baseharbor/scripts/check_docs_locale_parity.py
EN/DE page coverage OK: 168 matched Markdown pages
```

`mkdocs build` exited on a host disk-quota error (`[Errno 122] Disk quota exceeded`
on output write) — a local environment limit, not a docs fault.

## Befund vs. Kartenvertrag

The card text (and hunt source `befund-1.md`) describe **Go CLI `Achtung:` strings**
on destructive/consent-gated paths — a consumer-visible CLI-surface finding handled by
the **separate card 106**. The docs-de label contract was checked against `develop`
and is already consistent: no action required. No stale claim carried over from the
CLI view; the CLI portion is out of scope for this lane.

## EVIDENCE ON origin/main (before END)

`git ls-tree origin/main --name-only -r -- evidence/r28-welle3-2026-11-16/hunt-signals-107/` after `git fetch origin main`:

```
evidence/r28-welle3-2026-11-16/hunt-signals-107/scan-1.md
```

Committed locally in `993a7144`; present on `origin/main` (`30476c47..cc6a8844`). Path confirmed.

## END STATUS

END_DONE. already-compliant. No product edit, no branch cut, no PR.
No containers/compose started (cleanliness: none; ambient-core `bh-local-shared-*`
stacks are foreign and left untouched).
