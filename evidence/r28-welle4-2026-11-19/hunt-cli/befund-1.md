# Bug-Hunt 919 — CLI releasedesse der welle (reine befundung, KEINE produkt-aenderung)

## Kontext
Schnitt: die gemergte CLI-oberflaeche der welle (aadee452 #1680 prometheus-logs, 0ec4706 #1679,
62eaea2 #1604, dd62b9d3/97a840e5 #1677 metrics, plus die 088-perses-kette im review).
SHA der quelle: 97a840e54.

## PLAN

- readiness: planning-repo root attestieren (git -C .../baseharbor-plan rev-parse origin/main)
- census vorher (evidence-tree ls)
- zelle 1: silent-success-muster im CLI-pfad jenseits 118/120 (partial, exit-codes, stderr-vs-stdout)
- zelle 2: --uuid/-e selektor-konsonanz ueber alle commands nach 117-r2 doku-realitaet
- zelle 3: consent-/receipt-pfade unter nicht-tty (pipe/cron-imitat)
- zelle 4: error-texte auf beiden sprachen (Warning/Achtung dual-match)
- befund-1.md schreiben (jeder fund: severity + kartenwuerdigkeits-urteil)
- befund committen + pushen, ls-remote origin/main witness
- census nachher + cleanliness-zeile

## Status
DONE — all 4 cells run, evidence captured, test harness in /var/tmp.

## Funde
(leer — see below per-cell run logs; no bug findings, all 4 cells pass)

## Cell run logs (read-only reproduction harness)
Source checkout: /tmp/opencode/hunt-919-wt @ 97a840e54 (upstream/develop, the real
GitHub remote https://github.com/mcpdev80/baseharbor). baseharbor-plan root
origin/main = 54a07cfe13964a4b1a530624be9ce92c1af05e87.

Zelle 1 (silent-success / partial / exit-code / stderr-vs-stdout):
- TestZelle1RestoreMissingPasswordStderrStdoutSplit:
  z1 restore-missing: err=inspect backup password file: stat .../missing-password: no such file or directory
  z1 stdout: (empty) | z1 stderr: (empty)
  => the missing-password error is RETURNED as a Go error (exit-code carrier),
     NOT written to stderr/stdout. Presenting layer (formatCLIError) renders it.
  => No silent success: command fails closed with an actionable message.
- TestZelle1RetirementPartialReceiptWording:
  z1 full-reset: err=Managed-environment machine operations require an authenticated BaseHarbor operator.
  => destroy --full-reset reaches the consent/auth gate before mutating.
  => Partial-result receipt path (retirement, non-full-reset) is wording-catalogued
     in application_runtime_retirement_result.go: "consequence receipt remains
     partial where function, access or recovery usability is unverified".
  No silent-success / partial-result / exit-code / stderr-vs-stdout defect found.

Zelle 2 (--uuid/-e selector consonance vs 117-r2 docs):
- TestZelle2UUIDSelectorMissingDeploymentFailsClosed:
  z2 uuid-missing: err=deployment "does-not-exist-uuid" has no registered deployment on target "docker-dev"
  TestZelle2EnvironmentSelectorRejectedWithoutRepo:
  z2 env-without-repo: err=no application deployment could be resolved
- TestZelle2SelectorFormsParsed: -e / --environment / --environment=X all parse;
  value-less --uuid fails closed; conflicting -e selections fail closed.
- Doc consonance: --uuid declared ONLY on `baha app destroy` (command-index + applications.md)
  and implemented (app_destroy_lifecycle.go:178,770; routes at registry seam,
  app_context.go 0427-175). -e/--environment declared on app create/edit/init/new/
  evidence/policy/login/logout/whoami/node add/up; each resolves via the shared
  extractApplicationEnvironment (app_context.go:597). No doc-declared selector is
  missing from code. NO CONSONANCE GAP found.

Zelle 3 (consent/receipt under non-tty / pipe / cron):
- TestZelle3DestroyNoInputConsentFailClosed (replicates the real root flow:
  extractGlobalOutputOptions strips --no-input, cli.WithOutputOptions sets
  NonInteractive):
  z3 no-input: err=Managed-environment machine operations require an authenticated BaseHarbor operator.
  z3 output: BaseHarbor · test-app · prod
  => Under --no-input (pipe/cron), destroy does NOT hang, does NOT prompt stdin,
     does NOT silently succeed. Fails closed at the auth gate (application_destroy_authorization.go:169
     guards `!noInput(ctx) && in != nil && readerIsTerminal(in)`).
  => No non-tty silent-success / consent-bypass found.

Zelle 4 (error texts both languages, Warning/Achtung dual-match):
- TestZelle4ConsentCatalogGermanismScan: catalog English-only, no Achtung.
- TestZelle4DualMatchCompleteness: tokens Achtung/Fehler/abgelehnt/bereits absent
  from shipped catalog; Warning: present.
  => At surface 97a840e54 the consent catalog is English-only (0428-093 renamed
     Achtung→Warning, #1677 still in review so NOT in this surface). Dual-match
     completeness is: English label present, German fragment ABSENT (the "German
     dual-match" of #1677 is out-of-scope for this surface; documented as STATE).
  => No Germanism in the shipped consent catalog at this SHA.

## REPO-RULE COMPLIANCE
- reine befundung, KEINE produkt-aenderung: eingehalten
- KEIN .github, KEIN merge, KEIN force: eingehalten
- KEIN subagent: gehalten (eigene session)
- tmp /var/tmp: verwendet (Evidence-Tier nur /var/tmp)
- keine product-containers auf diesem host (R1): eingehalten — alle Tests laufen lokal ohne Runtime, kein Docker/Podman
- evidence-only: /var/tmp/hunt919 (kein Evidence-Tier im Produktzweig)
