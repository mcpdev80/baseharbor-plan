# 0428-072 · Programm-stand CLI-redesign + Perses (coord-Artefakt, keine product-Aenderung)

Programm-Grenze: max. 5 gleichzeitige Implementierungs-Lanes (Kartenwort). Aktuell: 2 lanes aktiv
(0428-094, 0428-082), weitere sitze idle-protected/gehalten — grenze eingehalten.

CLI2-schiene: umsetzungskarten haengen an der CLI-vertragskette (fan-out); keine CLI2-karte ist
derzeit dep-frei ausser dieser programm-karte (audit/contract-vorlagen noch in arbeit/review).

Perses-schiene: welle2 abgenommen/approved (PRs draft unter frost), welle3 laeuft:
- approved content: #1663 (093), demo #164 (099), 074-design-akte, selection #1590, registry #1591,
  alerts #1613, env-policy #1594, uid-app/env/target, seam #1575, boundary #1577, loki #1616,
  hosts #1602, source-model #1595, org-env #1596, valkey #1604, app-status #1614, 097 #1660
- letzte stufe: #1666 (094 double-append-E2E), #1665 (082 produkt-caller + query-witness)
- acceptance-hold im fenster: #1650 (078 dedup nach 097-merge)

Fenster-plan (nach 0.4.27-tag), ketten-reihenfolge: uid-app -> uid-env -> uid-target |
seam #1575 -> #1645 | 097 -> 078-dedup -> 078-final | 082 (base w083) nach datasources/selection |
demo #164 (099) parallel; jedes fenster-werk auf eigener frischer lane laut rules.
