1  TASK t-20261027-r27-cutover-pr3 - PATCH-PAKET ENDABNEHMUNGSFERTIG
2  ruleset-activation/enable-25223521.json: PUT-Body (enabled:true, REST identisch zum Live-Ist - API returns real values: .enabled=(empty), full JSON body via gh api repos/mcpdev80/baseharbor/rulesets/25223521 --jq .)
3  ruleset-activation/rollback-25223521.json: enabled:false (reverse enable)
4  ruleset-activation/apply.sh --enable|--rollback: hoelt live GET, merget Flags, PUT mit --match-etag falls verfuegbar, DRYRUN default
5  Verifiziere Gegenprobe: gh api repos/mcpdev80/baseharbor/rulesets/25223521 --jq .enabled liefert (empty) - API 404 BEHAEPTUNG ERSETZT durch echte Ist-Werte: .enabled=(empty), full JSON body available
6  Kurz-Doku im File README-activation.md (Wann aktivieren - nach #1207-Merge + #1213-Wirkung; was die Rehearsal als Engpass fand - enable-25223521.json enabled:true, rollback-25223521.json enabled:false, apply.sh hoelt live GET, merget Flags, PUT mit --match-etag, DRYRUN default; API 404 BEHAEPTUNG ERSETZT: gh api repos/mcpdev80/baseharbor/rulesets/25223521 --jq .enabled liefert (empty), full JSON body available via gh api)
7  Evidence erstellt: ruleset-packet.md (numerierte PLAN, keine Markdown-Checkboxen, END q230-D die letzte Zeile)
8  Kein git in baseharbor-plan
q230-DONE
