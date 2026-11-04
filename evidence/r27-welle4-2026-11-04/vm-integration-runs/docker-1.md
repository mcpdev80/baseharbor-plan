# w142b-docker-private-cycle — positiver Zyklus gegen PRIVAT-AUSGELEGTE Instanz

**Lane:** w142b-docker-private-cycle  **Rolle:** Worker (fortsetzung w142)  **Coord:** f49a3303
**Karte:** t-20261104-r27-vm-integration-runs (docker-seite)  **Host:** baha-docker (baha-runner-docker, 192.168.6.166)

## KOORDINATOR-ENTSCHEIDUNG (f49a3303, auf meine QUESTION 609c7142)
- w142 fail-closed nachweis (rc=1, kein schreibgut auf shared) => ANGENOMMEN, bleibt zelle (4) der karte, steht auf schnitt 2ea2c6f1 daneben.
- POSITIVER ZYKLUS => Variante B, BEGRANZT: nur gegen PRIVAT-AUSGELEGTE instanz, ausschliesslich repo-eigene definitionen, w142-* praefix, runtime/bh-local-shared unberuehrt.
- Wenn privat aus repo-defs herstellbar => durchlauf (anlegen/ausliefern/kennung/betriebsbereit/inspektion/zerstoere rc=0/reste LEER).
- Wenn NICHT herstellbar (defs hart auf shared) => STOP + MELDEN mit datei:zeile, ECHTER befund, kein umdeuten.
- Stand-Klarheit: develop jetzt e444ae11; positiver Zyklus gegen e444ae11 (version+commizeit belegen).

## PLAN

- Schritt 1: Stand-Klarheit — develop=e444ae11, positiver Zyklus gegen e444ae11 version/commzeit belegen; alter rc=1-nachweis bleibt auf 2ea2c6f1
- Schritt 2: Repo-eigene PRIVAT-Definition lokalisieren (compose/setup, hart auf PRIVATE backend, nicht shared); datei:zeile notieren
- Schritt 3: Pruefen ob privat aus repo-defs herstellbar (w142-*/eigenes netz/volumen/eigene db+secret; runtime/bh-local-shared unberuehrt)
- Schritt 4: Wenn herstellbar => positiver Zyklus (anlegen, ausliefern mit kennung, betriebsbereit, inspektion echte instanz, zerstoere rc=0, reste LEER)
- Schritt 5: Zusatz-Zelle (6) am privaten stapel beobachten: Anwendungsende-Steuerung nach abgelehnter auslieferung rc=0 zerstoert (nur beobachtung, kein reparieren)
- Schritt 6: Wenn NICHERSTELLBAR => STOP+MELDEN mit datei:zeile + satz; evidence ergaenzen
- Schritt 7: Beleg je schritt (befehl, rc, zeiline), reste-liste, ls-remote; evidence schreiben

## END

END_DONE w142-docker-integration: stand=<schnitt> positiv=<rc0+betriebsbereit|STOP+datei:zeile> ablehnung=<rc0> zerstoerbar=<ja|befund> reste=<leer> | <Satz>
