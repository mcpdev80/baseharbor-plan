# Fifth #1627 failure analysis — consent after preview

## PLAN

1. Pin the analysis to exact #1627 head `b3b0c2c9efc43e9696c5eeda2a7164c88889e188` and failed Docker application job `137020935578` from run `44961334018`; no verdict or merge action.
2. Compare the five candidate heads `8de37f58caa`, `62dd38f9b6d`, `ac05cc4efbc`, `38be89aa4a0`, and `b3b0c2c9efc`, recording each round’s actual change.
3. Trace production consent creation in preview and validation during apply, with exact file:line references.
4. Classify the failure as fixture-side or product-side from the source and failure path; state uncertainty if source evidence is insufficient.
5. Publish this read-only analysis in Planning origin/main and leave #1627 without a verdict.
