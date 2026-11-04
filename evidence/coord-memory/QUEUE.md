# Vorgemerkte Missionen (Warteschlange, durch Tick zu prüfen)

Frei wird ein Platz, sobald eine Lane plattenfest abgeliefert und released ist. Eintrag löschen, sobald die
Lane dispatcht wurde. Der Audit-Punkt "POOL" zeigt beim Tick, ob ein Platz frei ist.

| # | Mission | Warum noch nicht dispatcht | Nächster Auslöser |
| --- | --- | --- | --- |
| 1 | coordinator/missions/w123-codec-r3.txt | Pool 5/5 belegt | Profil-Kodierung Runde 3 (review-1363b REJECT: secret-felder, atomarer commit, vertrauenspflicht, vollständiger rundlauf, gates) |
| 2 | ~~w121-podman-rebuild~~ | ERLEDIGT-DURCH-ANDEREN | Podman-Host läuft jetzt in codex-ops-podman (zweite Codex-Instanz, Owner-Direktive 17:5x). w121 bleibt als Fallback-Mission, wird NICHT doppelt dispatcht (ein Host, ein Bearbeiter). |
| 3 | VM-Folgeauftrag Docker-Host: keycloak-stapel crasht in schleife (datenbankzertifikat wird stapeluebergreifend falsch aufgeloest) — down/up mit berichtigter zertifikatsangabe, definition liegt vor | Pool 5/5 belegt | naechster freier ornith-sitz |
| 4 | ~~w119-journal-r2~~ | ERLEDIGT | wurde von cx01 (Codex-Worker) geliefert: head 11ed442e, Karte auf review, Luna prueft | Pool 4/4 | Ausführungstagebuch-Runde 2 (Codex review-1373a REJECT, fünf Rezepte) |
| 4 | coordinator/missions/w118-connector-fmt.txt | Pool 4/4 | Connectort-Antrag #19 hat nur den roten Source-Format-Job |

## Tor vor der Integrationsphase

Die eigentlichen Docker-/Podman-Integrationstests (Karte t-20261104-r27-vm-integration-runs) starten erst, wenn
beide Rechner ein `baha` aus der geprüften Quellrevision melden. Befund 2026-11-04: auf beiden Hosts lag
BaseHarbor 0.4.23, auf dem Podman-Rechner wurde diese alte Version heute sogar vom Setup-Skript neu
installiert. Läufe gegen 0.4.23 zählen nicht als Test.

## Kanalbesetzung

- `codex-luna-ch` (d9eca6e7): Abnahme-Kanal, gerade leer, weil kein Kandidat eine grüne Pflichtprüfung hat.
- `codex-pod-ops` (a0ce49b3, zweite Instanz, Owner-Direktive 2026-11-04): OPS-Auftrag Podman-Host.
  Rollenhygiene: dieser Kanal führt einen ausdrucklich als OPS gekennzeichneten Auftrag aus — er schreibt kein
  Review-Urteil und merged nichts; die Revisions- und Versionsnachweise legt er als Evidence ab.
