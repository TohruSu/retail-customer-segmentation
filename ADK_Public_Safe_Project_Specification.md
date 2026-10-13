# Public-Safe Project Specification

**Project:** 今日の食えらび編集室 — A Data-Driven Retail Strategy Case Study  
**Proposed repository:** `retail-customer-segmentation`  
**Status:** Design specification; implementation not yet started  
**Intended audience:** Software/data engineering recruiters, data scientists, and other developers  
**Language:** English for technical documentation; retain the original Japanese project title and explain it in English

## 0. Background and basis

This specification was prepared after reviewing the eight Jupyter Notebooks in the privately supplied `ADK Project.7z`. The Notebook sequence is:

1. `01_data_understanding.ipynb`
2. `02_gms_diagnosis.ipynb`
3. `03_growth_opportunity.ipynb`
4. `04_need_segmentation.ipynb`
5. `05_targeting.ipynb`
6. `06_competitor_3c.ipynb`
7. `07_positioning.ipynb`
8. `08_strategy_evidence.ipynb`

The existing private work develops an end-to-end reasoning path from retail behavior analysis to exploratory segmentation, targeting, 3C/positioning, and a retail-space concept with measurement and pilot validation. In Notebook 08, the user's proposed concept is **「今日の食えらび編集室」**, described as a **「食の比較編集ハブ」**: a place to compare different ways to complete a meal by *meal occasion* and connect choices to an existing food floor. The notebook treats increased visits and food-related sales as hypotheses to be validated, not achieved outcomes.

**Permission supplied by the user:** ADK restricts public disclosure of questionnaires and survey results; the user's own analysis materials may be public. This statement is the operating premise, not a substitute for checking individual images, borrowed materials, third-party claims, and data-derived outputs.

## 1. Public project identity

**Pitch:** An independent, reproducible retail analytics and strategy case study: from exploratory customer behavior and segmentation to an original meal-choice experience concept and an evaluation plan.

**One-sentence summary:** An end-to-end Python portfolio project that demonstrates how exploratory customer segmentation can inform a *hypothetical* retail experience concept, with explicit limits on what synthetic evidence can prove.

**Positioning:** This is **not** an ADK code release, not a re-publication of the ADK survey, not a validated consumer-insight product, and not an officially implemented Ito-Yokado/retailer program.

Preserve the Japanese concept name 「今日の食えらび編集室」 and the independently authored strategy idea. A retail food-floor scenario, optionally involving an approximately 150-tsubo design brief, may be retained as a **case assumption** because it belongs to the user's permitted analysis narrative—not as evidence of an actual currently vacant commercial site. If publicly naming a retailer, distinguish publicly sourced corporate facts from fictional/hypothetical case assumptions and include a non-affiliation note. Prefer generic retail branding and original graphics.

## 2. Non-negotiable publication boundary

### Not allowed in public repository, Git history, Codex Cloud inputs, generated assets, tests, or logs

- Original survey datasets or respondent-level records.
- Original questionnaire text, question screens, exact survey option/code lists, and proprietary question-mapping files.
- Survey summaries, cross-tabulations, descriptive counts, percentages, means, original PCA/KMeans outputs, source-derived cluster labels or profiles, original plots, or any equivalent derived **survey results**.
- Original notebook execution outputs that show survey data, even when raw data have been removed.
- Source code, commercial assets, or internal documents that the user does not have permission to publish or supply to a cloud tool.
- Real respondent examples, even if IDs have been removed. Do not create a synthetic dataset by perturbing, sampling, fitting to, or statistically matching restricted source records.

**Important:** Do not give the original `.7z`, original notebooks, original source data, protected results, or screenshots to Codex Cloud. The Codex build must use only *this independent public-safe specification* and its own newly written code.

### Permitted as the user-described scope allows

- Independently authored, generalizable methodological ideas: data validation, feature scaling, PCA, KMeans, silhouette and stability checks, qualitative 3C/POP/POD reasoning, KPI design, and pilot evaluation design.
- The user's **independently conceived** strategy concept and non-sensitive strategy narrative; remove or rewrite any sentence whose stated factual basis is a restricted survey result.
- Public corporate facts with a citation and access date, where necessary. Do not present unsourced brand-capability claims as verified.
- Entirely new synthetic data, charts, code, tests, diagrams, and README screenshots made for this project.

Create `docs/PROVENANCE_AND_SCOPE.md` specifying the boundaries, independently produced work, synthetic-data status, and absence of business endorsement. A manual privacy/security review remains required **before changing repository visibility to Public**.

## 3. Desired analytical storyline — eight phases

The public version should preserve the **logic** of the original eight notebooks but must not replay original questionnaire codes, original sample-derived segments, or source survey findings.

| Stage | Public-facing purpose | Data/evidence policy |
| --- | --- | --- |
| 01. Data understanding | Validate a **new** synthetic dataset; document schema, ranges, missingness, and assumptions | Newly designed generic variables only |
| 02. Retail visit diagnosis | Describe synthetic store-visit patterns and cross-channel activity | All quantitative findings labeled `SYNTHETIC` |
| 03. Opportunity exploration | Compare hypothetical growth approaches and evidence gaps | No inferred real market size or causal conclusion |
| 04. Segmentation | Standardize selected attitudinal features, PCA, compare KMeans k candidates, silhouette, initialization stability / sensitivity | Do not predetermine k or claim natural market segments |
| 05. Targeting | Interpret candidate profiles, distinguish descriptive evidence from managerial judgment and unknowns | No original segment IDs/profiles; target is a *case-study hypothesis* |
| 06. Competitor / 3C | Compare hypothetical customer needs, generic retail channels, and publicly documented capabilities | Qualitative assumptions explicitly marked; citations for factual company claims |
| 07. Positioning | Formulate provisional POP/POD and value proposition; avoid arbitrary quantitative positioning maps | Conceptual illustration, not measured survey coordinates |
| 08. Strategy / pilot | Present 「今日の食えらび編集室」 meal-choice concept, customer journey, food-floor connection, 4P, risks, KPI tree, pilot design | No claimed uplift, ROI, or causal impact without actual pilot evidence |

Stages 01–05 should be genuinely computational. Stages 06–08 may emphasize carefully sourced Markdown/Notebook narrative with small, generated diagrams and tables. An eight-stage navigation and evidence chain should be clearly visible; do not create eight notebooks with redundant boilerplate merely to hit a count.

## 4. Synthetic data specification

Create a **new, simple, transparent** synthetic dataset using only a deterministic pseudo-random generator. It must not recreate questionnaire item text, identifiers, response distributions, original feature lists, original segment labels, or original data structure.

Suggested new schema (subject to careful design):

- `participant_id`: synthetic sequential or pseudonymous ID; no original respondent identifiers.
- `monthly_store_visits`: integer synthetic behavioral variable.
- `weekly_other_channel_visits`: integer synthetic channel-usage variable.
- `price_attention`: invented 1–5 attitude proxy.
- `meal_planning_interest`: invented 1–5 attitude proxy.
- `convenience_preference`: invented 1–5 attitude proxy.
- `discovery_interest`: invented 1–5 attitude proxy.
- `cooking_interest`: invented 1–5 attitude proxy.
- `shopping_time_pressure`: invented 1–5 attitude proxy.
- `cross_category_interest`: invented 1–5 attitude proxy.

The project should justify its generative assumptions in `docs/SYNTHETIC_DATA.md`. Recommended starting size: a modest synthetic cohort (e.g., 600–900 fictional records), not a replica of the original survey sample size. Use realistic overlap/noise and optionally controlled missingness. No ground-truth clusters need to exist; if latent groups are intentionally generated, disclose them and avoid implying KMeans discovery proves validity.

All statistical outputs must include context such as **"Illustrative results on independently generated synthetic data; not findings from the ADK consumer survey."** Never hard-code favorable silhouette values, target sizes, uplift, sales increases, or other outcome metrics.

## 5. Analytics and methodological safeguards

- Strict input checks: expected columns, types, bounds, duplicate IDs, missingness, finite values, reproducible RNG seeds.
- Train a preprocessing pipeline on the selected data and document any imputation. Prevent target or outcome leakage into clustering features.
- Standardize chosen attitude features; PCA may be used with an explained-variance rationale rather than automatically reproducing the original number of components.
- Compare sensible cluster counts (e.g., k=2–5) using silhouette **and** cluster-size balance, stability/sensitivity, interpretability, and explicit no-cluster alternatives.
- Assess initialization sensitivity with several random seeds and adjusted Rand index, noting that ARI stability does not prove real-world segment validity.
- Show PCA sensitivity and at least one baseline (e.g., descriptive stratification, no segmentation) when meaningful.
- Distinguish **observation / assumption / interpretation / recommendation / unknown** in strategy tables.
- Any targeting choice must be editorial and conditional; never automatically declare a segment objectively superior from a synthetic metric.
- Strategy KPIs should form an explicit path from exposure → interaction → food-floor transition → subsequent purchase / revisit, while indicating which real-world data sources would be necessary.
- Pilot design must address comparison group or staggered rollout where feasible, seasonality, store footfall, promotions, stockouts, POS data, and attribution limits.

## 6. Preserve the original *strategy idea* safely

Explain the user-created concept as a hypothetical **meal-occasion comparison hub**:

1. Discover a changing theme such as "What should I eat tonight?"
2. Compare several ways to complete the same meal occasion: cook from ingredients, prepared food, frozen/easy meal, and a combination.
3. Create a lightweight shopping note / route to an existing food-floor category.
4. Change themes periodically to form a proposed reason to revisit.
5. Test rather than assume whether visits, food-floor transitions, and purchases increase.

Optional scenario: a compact space roughly equivalent to 150 tsubo adjacent to a food retail floor, clearly framed as **exercise assumptions**, not an authenticated retail deployment. Represent a conceptual visitor journey and/or non-architectural zone diagram; no fabricated floor plan.

Strategy deliverables: value proposition, customer journey, 3C and POP/POD caveat table, 4P outline, operating-risk table, KPI tree, and pilot evaluation design. **Do not carry forward any original segment profile, statistics, survey-based competitor claims, or percentages.**

## 7. Suggested repository structure

```text
retail-customer-segmentation/
├── README.md
├── LICENSE                         # only for newly owned code, if chosen
├── pyproject.toml                  # pinned/limited supported dependencies
├── .gitignore
├── .github/workflows/ci.yml
├── src/retail_case/
│   ├── __init__.py
│   ├── synthetic.py
│   ├── validation.py
│   ├── preprocess.py
│   ├── clustering.py
│   ├── evaluation.py
│   └── cli.py
├── notebooks/                     # 8 analytical stages; small and reproducible
│   ├── 01_data_understanding.ipynb
│   ├── 02_retail_diagnosis.ipynb
│   ├── 03_opportunity.ipynb
│   ├── 04_segmentation.ipynb
│   ├── 05_targeting.ipynb
│   ├── 06_competitor_3c.ipynb
│   ├── 07_positioning.ipynb
│   └── 08_strategy_pilot.ipynb
├── docs/
│   ├── PROVENANCE_AND_SCOPE.md
│   ├── SYNTHETIC_DATA.md
│   ├── ANALYTICAL_LIMITATIONS.md
│   ├── STRATEGY_CASE.md
│   └── PUBLICATION_CHECKLIST.md
├── tests/
│   ├── test_synthetic.py
│   ├── test_validation.py
│   ├── test_clustering.py
│   └── test_cli.py
├── assets/                          # entirely new public-safe figures
└── examples/                        # generated examples, never restricted data
```

This is a suggested structure, not a mandatory number of classes/modules. Favor straightforward implementation over scaffolding. CLI should support, at minimum, generating a synthetic dataset and running a deterministic analysis pipeline.

## 8. README quality bar

The README should communicate in the first screen:

- **Project title:** 今日の食えらび編集室 / Meal-Choice Editorial Studio.
- **Nature:** independent portfolio case study / simulated analytics / unimplemented strategy proposal.
- **Skills demonstrated:** Python data validation, PCA/KMeans, critical evaluation, plotting, reproducibility, strategy translation.
- **Visuals:** one honest synthetic cluster/ECDF or sensitivity chart, one original meal-choice journey / KPI concept diagram. Do not show real survey results.
- **Reproduction:** installation, one command to generate data, one command to run analysis, one command for tests, expected output filenames.
- **Limitations:** synthetic-data validity, subjective business decisions, need for future real-world pilot.
- **Provenance:** independent reimplementation; no ADK survey/questions/results; no organizational endorsement.

Avoid claiming this strategy was adopted, tested in a store, or caused business uplift.

## 9. Definition of Done (acceptance gates)

**Gate A — Safe inputs:** The new repository never contained protected files, notebooks, survey prompts/results, or data-derived tables in any commit, even temporarily; Codex Cloud never received them.

**Gate B — Reproducibility:** A fresh environment can install supported dependencies, generate deterministic synthetic data, execute an end-to-end analysis, and produce figures/reports without internet or private files. Repeated runs with the same seed are deterministic within the declared runtime.

**Gate C — Scientific honesty:** Tests cover preprocessing behavior, PCA/clustering edges, stable/repeatable run properties, and no fabricated success metrics. Reports label all synthetic values and do not conflate model stability with real segment validity.

**Gate D — Strategy transparency:** Original concept is retained, but customer/competitor/impact assertions are marked as case assumptions or correctly sourced public facts. Effectiveness remains a testable hypothesis.

**Gate E — Publication:** Documentation, citations, images, packaging and CI are ready; manual inspection checks text, notebook metadata/outputs, generated artifacts, hidden dotfiles, commit history, and external links before making repository public.

## 10. Explicitly out of scope for v0.1.0

- An application deployed at a real retail location or integration with POS or customer tracking.
- Claims of real consumer-segmentation performance or statistically significant market insight.
- A full marketing automation system, commercial recommender, or production dashboard.
- Reproducing the ADK survey results or rebuilding its questionnaire under alternate names.
- Unnecessary microservices, complicated web UI, expensive model training, or model cards masquerading as real-world validation.

## 11. Phased implementation

1. **Phase 0 — Review/spec:** Start from this spec only; document publication boundaries; choose exact new synthetic schema, evaluation criteria, and project layout.
2. **Phase 1 — Reproducible analytics MVP:** Implement generator, validation, standardization, PCA, candidate clustering, evaluations, deterministic CLI, and tests.
3. **Phase 2 — Eight-stage narrative:** Complete concise notebooks and explicit strategy/limitations documents; generate trustworthy preview figures.
4. **Phase 3 — Engineering/presentation:** CI, README, new artwork, link checks, clean-run validation, provenance/publication checklist.
5. **Phase 4 — Manual owner review:** User examines code, images, outputs, and entire history. Only after approval consider Public visibility, a version tag, and profile featuring.

**Owner decision required before public release:** Confirm independently authored narrative and business-case details are permitted, final output contains no prohibited survey/questionnaire/results, and all cited external material is properly attributed.
