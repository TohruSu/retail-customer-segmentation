# Public project charter

## Purpose and identity

**今日の食えらび編集室 / Meal-Choice Editorial Studio** is an independent Python portfolio case study. It connects exploratory retail analytics on **new synthetic data** to a **hypothetical, unimplemented strategy proposal** and a transparent pilot plan. The project demonstrates engineering and analytical judgment; it claims no real market insight, deployment, or business uplift.

The user-created 「食の比較編集ハブ」 concept is a meal-occasion comparison hub: compare ingredients to cook, prepared food, frozen/easy meals, and combinations for the same occasion; take an optional shopping note to existing food-floor categories; refresh themes as a proposed reason to revisit. Demand and effectiveness remain hypotheses.

This charter records current public requirements. It contains no private-source archive names, historical notebook inventory, named-retailer scenario, or survey findings.

## Eight-stage scope

1. **Data understanding:** validate the independently generated schema, ranges, missingness, and assumptions.
2. **Retail visits:** describe synthetic store and other-channel activity with explicit time units.
3. **Opportunity:** compare hypothetical routes to engagement and identify missing real-world evidence.
4. **Segmentation:** impute and standardize invented attitudes, use a variance-based PCA rule, compare KMeans k=2–5 when feasible, and report separation, balance, and sensitivity.
5. **Targeting:** interpret candidate profiles conditionally against unsegmented/descriptive baselines; never select an objectively superior audience from synthetic scores.
6. **3C:** compare generic channels as assumptions; distinguish any future sourced public facts from the case scenario.
7. **Positioning:** propose points of parity/difference and a meal-comparison value proposition without measured positioning coordinates.
8. **Strategy and pilot:** specify the journey, 4P, operating risks, KPI denominators/data needs, and a preregistered comparison addressing seasonality, promotions, stockouts, footfall, and attribution uncertainty.

Stages 01–05 are computational; stages 06–08 use concise narrative and original concept diagrams. Eight notebooks call reusable package logic rather than duplicate pipelines. English is the primary documentation language; retain and explain the Japanese title.

## Independent data and evidence boundary

- Use only the repository’s deterministic generator and newly invented proxies. Default size is 720 fictional rows, with seed 2026; assumptions and equations are declared in [synthetic data](SYNTHETIC_DATA.md).
- Include fictional SYN-prefixed IDs, a `SYNTHETIC` status marker, two visit counts, and seven invented attitude proxies. Only attitudes enter clustering.
- Use overlapping continuous factors and noise without planted true clusters; never fit, sample, perturb, or statistically match restricted records.
- Label every computed result **SYNTHETIC / ILLUSTRATIVE**. Explicitly state that it is not a finding from any original consumer survey. Label strategy diagrams **HYPOTHETICAL PROPOSAL**.
- Exclude original questionnaires, respondent records, mappings, summaries, survey results, historical executed notebooks, source-derived profiles/plots, private business assets, and credentials from the tree, generated outputs, cloud inputs, logs, and proposed publication history.
- Do not request or inspect restricted source materials. Valid schema and labels alone cannot prove provenance.
- Make no affiliation, endorsement, measured consumer-segment, visitation-uplift, sales, or ROI claim.

## Deliverables and validation

Maintain a compact package and CLI for generation, validation, preprocessing, diagnostics, and reports; eight stage notebooks; original diagnostic and journey graphics; clear provenance, assumptions, limitations, strategy, and publication documents; tests; and CI.

Fresh installation must support deterministic generation and end-to-end analysis without network or private inputs **after dependencies are installed**. Generated datasets and reports belong in ignored output directories. Validate bounds, types, duplicates, missingness, finite values, edge conditions, repeatability, and CLI errors. Execute all notebooks from clean source; verify lint/format, meaningful committed-diff whitespace checks, and hosted CI before merge/public release. Preview graphics must reflect actual computed values and disclose their units.

Detailed limitations belong in [analytical limitations](ANALYTICAL_LIMITATIONS.md); business choices and future evaluation belong in [the strategy case](STRATEGY_CASE.md). An optional roughly 150-tsubo space is only an exercise assumption, not a verified site or architectural plan.

## Review and release boundary

A private feature commit, push, and PR are authorized for review. Publishing, merging, tagging a release, or changing visibility requires separate owner approval. Before public release, the owner must confirm concept/prose/asset rights, review the full current and historical repository, resolve earlier historical references, choose a license for known-owned materials, and verify hosted CI. Removing a file now does not remove historical copies; history remediation remains owner-controlled.

See [provenance and scope](PROVENANCE_AND_SCOPE.md), [the audit report](AUDIT_REPORT.md), and [the publication checklist](PUBLICATION_CHECKLIST.md). No publication permission or license is inferred from successful tests.
