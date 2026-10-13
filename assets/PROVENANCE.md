# Original visual assets

These figures are generated locally by `src/retail_case/figures.py`. They use no
external images, real customer records, private questionnaires or survey outputs.
PNG and SVG are alternate renderings of each original figure.

- `synthetic_diagnostics.png` / `.svg`: computed **SYNTHETIC** silhouette,
  cluster-size range, initialization agreement and visit ECDFs. The store ECDF
  uses **visits/month** and the other-channel ECDF uses **visits/week**, on separate
  x-axes. Raw counts are not normalized or directly compared across time bases.
  Source: the new
  independent generator, with 720 fictional records, seed 2026 and requested
  missing rate 0.03. Taking `floor(720 * 0.03)` yields 21 missing cells per attitude
  column (**2.92% SYNTHETIC** missingness), with PCA variance target 0.90 and
  candidate k values 2–5. These are workflow diagnostics, not validated consumer
  segments or evidence of real market demand.
- `meal_choice_journey.png` / `.svg`: original **ILLUSTRATIVE / HYPOTHETICAL
  PROPOSAL** diagram of the user's meal-occasion comparison concept. Routes to
  ingredients, prepared food, frozen/easy options and combinations converge on
  an optional shopping note and the existing food floor. Evaluation remains a
  future requirement; no business effect is depicted as observed.

Regenerate both figures after installing project dependencies:

```bash
retail-case visuals --output-dir assets --n 720 --seed 2026 --missing-rate .03 --variance-target .90 --overwrite
```

The overwrite flag explicitly replaces these four generated files. Without it,
the command preserves existing output files. It leaves this provenance document
and unrelated files intact. Rendering writes neither timestamps nor machine
paths into figures; SVG identifiers are seeded for deterministic output in the
same dependency/runtime environment. Fonts may render differently elsewhere.

Exact diagnostic notice:

> SYNTHETIC: illustrative results on independently generated data; not findings from the ADK consumer survey.

Only the independently created code and newly rendered figures are included.
The project makes no endorsement, affiliation, deployment or uplift claim.
