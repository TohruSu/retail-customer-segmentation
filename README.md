# 今日の食えらび編集室 / Meal-Choice Editorial Studio

An independent Python portfolio case study connecting **SYNTHETIC retail analytics** to a **hypothetical, unimplemented meal-choice experience**. It demonstrates data validation, reproducible simulation, PCA/KMeans diagnostics, critical interpretation, plotting, and strategy-to-measurement design.

The proposed 「食の比較編集ハブ」—a meal-occasion comparison hub—helps a shopper compare cooking from ingredients, prepared food, frozen/easy meals, and combinations for the same occasion. A lightweight shopping note links the choice to an existing food floor. Recurring themes are proposed reasons to return; their effect remains untested.

Historical ADK internship work and the original self-authored concept are background. This newly written code independently demonstrates methods using synthetic data; it does not reproduce the original survey, its segments, or its quantitative results.

## Eight stages, one evidence chain

| Stage | Notebook | What it establishes |
| --- | --- | --- |
| 01 · Understand | [Data understanding](notebooks/01_data_understanding.ipynb) | Synthetic schema, bounds, missingness, and generative assumptions |
| 02 · Diagnose | [Retail visits](notebooks/02_retail_diagnosis.ipynb) | Descriptive synthetic store and other-channel activity |
| 03 · Explore | [Opportunity](notebooks/03_opportunity.ipynb) | Hypothetical routes to engagement and the evidence each would need |
| 04 · Segment | [Segmentation](notebooks/04_segmentation.ipynb) | Standardization, PCA, candidate k, balance, and sensitivity |
| 05 · Interpret | [Targeting](notebooks/05_targeting.ipynb) | Conditional editorial choices against an unsegmented baseline |
| 06 · Compare | [Competitor / 3C](notebooks/06_competitor_3c.ipynb) | Generic channel assumptions; no asserted brand capabilities |
| 07 · Position | [Positioning](notebooks/07_positioning.ipynb) | Provisional points of parity/difference and a value proposition |
| 08 · Test | [Strategy / pilot](notebooks/08_strategy_pilot.ipynb) | Journey, operating risks, KPI definitions, and a comparison plan |

Stages 01–05 use reusable package code. Stages 06–08 turn that exploratory work into an explicit proposal, with **observation, assumption, interpretation, recommendation, and unknown** kept separate.

## Reproduce

Requires Python **3.11–3.13**; the reference environment uses **Python 3.12**. From the repository root:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]' -c requirements-dev.lock

retail-case generate --output build/synthetic.csv --n 720 --seed 2026
retail-case analyze --input build/synthetic.csv --output-dir build/report --seed 2026
retail-case visuals --output-dir build/visuals

pytest
ruff check .
ruff format --check .
python scripts/check_notebooks.py
```

After dependencies are installed, generation, analysis, tests, and notebook execution need no network or private files. Analysis writes `report.json`, `report.md`, `diagnostics.csv`, `profiles.csv`, `sensitivity.csv`, `baseline.csv`, and diagnostic/journey figures under `build/report/`. Generated CSVs and reports belong in ignored `build/`.

`requirements-dev.lock` records the reference environment's pinned dependency snapshot, with conditional transitive pins for Python 3.11 compatibility. CI covers Python 3.11–3.13; local reference results use 3.12. The two committed preview figures are regenerated from the independent simulation and original concept. Existing outputs are protected: to intentionally regenerate them, use `retail-case visuals --output-dir assets --overwrite`. Each visual is available as PNG and SVG. See [synthetic data](docs/SYNTHETIC_DATA.md) for the schema and assumptions.

## Method and interpretation

![Synthetic silhouette, cluster balance, initialization sensitivity, and separate monthly/weekly visit distributions; independently simulated observations, not real consumer findings.](assets/synthetic_diagnostics.png)

The generator uses continuous, overlapping latent factors and noise, **without predefined true clusters**. Only seven invented attitude proxies enter clustering; visits, IDs, and the synthetic-status label are excluded. Missing attitudes are imputed, standardized, and projected using a documented explained-variance rule. Candidate KMeans partitions are compared using silhouette, size balance, repeated-initialization adjusted Rand index, and PCA/feature sensitivity. An unsegmented view remains a valid alternative.

All computed values are **illustrative results on independently generated synthetic data; not findings from the ADK consumer survey**. A stable partition can describe the simulation without establishing a real consumer segment. No cluster score determines a business target or proves an impact. Read [analytical limitations](docs/ANALYTICAL_LIMITATIONS.md) before interpreting a report.

### SYNTHETIC reference run

For **720 fictional rows, seed 2026**, with the default missingness setting, the 90% PCA variance rule retains **6 components and 91.75% of standardized variance**. Candidate silhouettes are **0.178, 0.154, 0.147, and 0.137** for k=2–5. These values indicate weak separation in this simulation.

The k=2 partition is a technical reference selected by silhouette, not a target recommendation. Across five single-initialization fits, its mean pairwise ARI is **0.541**, with minimum **0.0003**; omitting the time-pressure proxy yields ARI **0.553** against the reference. Initialization and feature choices matter. The unsegmented meal-occasion concept and a real pilot remain more defensible than declaring a discovered market segment.

## From a proposal to a pilot

![Hypothetical meal-choice journey from occasion discovery through comparison and a shopping note to an existing food floor, with proposed evaluation before scaling.](assets/meal_choice_journey.png)

The concept’s conditional audience is a shopper making a meal decision under time pressure while remaining interested in comparing options. This is a design hypothesis, not a recovered consumer profile. [The strategy case](docs/STRATEGY_CASE.md) specifies 3C/POP/POD assumptions, 4P choices, risks, KPI denominators, and a preregistered comparison plan addressing seasonality, promotions, stockouts, footfall, and attribution uncertainty.

## Provenance and release status

This is an independent implementation informed by a user-provided conceptual brief; [the public project charter](docs/PROJECT_CHARTER.md) now records its requirements. Its code, data, and graphics are newly produced. It includes no original questionnaires, respondent records, survey results, original notebook outputs, or source-derived segment profiles. No affiliation or endorsement by ADK, retailers, or their clients is claimed, and no real store deployment, market validity, visitation uplift, or sales gain is claimed.

[Provenance and scope](docs/PROVENANCE_AND_SCOPE.md) records the boundary. This project includes an [MIT License](LICENSE) for independently owned code, documentation, and original assets. [The publication checklist](docs/PUBLICATION_CHECKLIST.md) still requires owner review of the full Git history and final publication rights. Hosted GitHub Actions passed on Python 3.11–3.13; merge, release tagging, and Public visibility remain separate owner decisions.
