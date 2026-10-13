# Analytical limitations

**Every computed result is SYNTHETIC / ILLUSTRATIVE.** It describes an independent simulation, not real shoppers, the ADK consumer survey, an actual retail market, or a deployed intervention.

## What the analytical evidence can establish

| Evidence | Useful conclusion | Conclusion it cannot establish |
| --- | --- | --- |
| Schema, bounds, duplicates, missingness checks | Input conforms to the public modelling contract | Real survey quality or representativeness |
| Descriptive visit summaries | What the synthetic generator produced | Market size, frequency of real visits, or growth opportunity |
| PCA explained variance | How a linear projection summarizes standardized synthetic attitudes | Validated psychological constructs or causally important needs |
| Silhouette and cluster sizes | Separation and balance of a chosen synthetic partition | Natural or actionable real-world customer segments |
| Initialization ARI | Agreement between algorithm runs on the same observations | External validity, longitudinal persistence, or commercial value |
| PCA / feature sensitivity | Dependence on analytical choices | A statistically proven optimal representation |
| Strategy tables and journey | A coherent, falsifiable design proposal | Customer demand, adoption, uplift, or return on investment |

## Simulation assumptions

The modest cohort is fictional. Its continuous latent factors, coefficients, noise, clipping, rounding, count caps, and missingness rate are author choices, not estimates of a population. There is no discrete generative segment label for KMeans to recover. Reported proportions are proportions of simulated rows; they are not population prevalence estimates. Simulation-based confidence intervals would not repair that evidence gap.

Missingness is generated independently rather than arising from real response processes. Imputation is therefore a method demonstration, not a solution to nonresponse bias. The 1–5 proxies are invented ordinal variables; treating their spacing as equal for scaling, Euclidean distance, and PCA is a modelling approximation. Count bounds deliberately simplify tails and cannot model all retail behavior.

## Model choices and sensitivity

The clustering features contain only seven attitude proxies. Store visits, other-channel visits, participant IDs, and the synthetic label are excluded. Relating visit outcomes to profiles afterward is descriptive; a within-sample association is not evidence that a need causes a visit or that targeting it changes behavior.

Median imputation, unit-variance scaling, the PCA variance rule, KMeans distance, and candidate k values shape the result. Standardization gives each retained feature a comparable scale, not a validated importance weight. PCA maximizes retained variance, not business usefulness. KMeans favors approximately spherical partitions and will assign clusters even when continuous gradients are the better explanation.

Initialization checks vary seeds on the same data. Agreement can still be high for an arbitrary but easy-to-fit partition. PCA and feature sensitivity compare reasonable representations; agreement across them remains internal evidence. The full cohort is used for exploratory fitting, so these diagnostics are not held-out estimates of prediction quality. With real data, preprocessing would need to be fitted within any training/resampling design to avoid leakage into evaluation.

Do not choose a business target by maximizing silhouette or label one numeric cluster “best.” Numeric labels are arbitrary and may permute across fits. Compare the candidate partition with an unsegmented summary and simple descriptive views; a recommendation can remain at the meal-occasion level without using clusters at all. External stability, reachable audiences, intervention feasibility, and customer benefit would require new permitted evidence.

## Strategy inference and future evidence

The proposed audience, generic competitor strengths, points of parity/difference, and recurring-theme mechanism are case assumptions. A synthetic profile may illustrate a design tension but cannot justify a claim about who shops at a real store or which channel they prefer. The narrative distinguishes **observation, assumption, interpretation, recommendation, and unknown**.

No intervention has been run. The repository contains definitions of pilot metrics, not observed conversion, sales uplift, revisit, ROI, or statistically significant effects. Purchases after an interaction may have happened anyway. POS linkage, an appropriate comparison, consent where needed, and control for footfall, seasonality, promotions, and stockouts are required. Cross-shopping and spillover can contaminate comparisons; anonymous footfall cannot establish unique-customer revisit.

See [the strategy case](STRATEGY_CASE.md) for a preregistration outline. A real pilot would need independent ethics/privacy decisions, rights to operational data, and power calculations using permitted pilot or historical data; the synthetic cohort is unsuitable for sizing its sample or promising impact.

## Reproducibility limits

Seeds make repeated runs reproducible within the supported, declared runtime. Floating-point and library-version differences can alter borderline PCA or KMeans decisions. Record versions with each report and compare numerical results using justified tolerances. Reproducibility verifies execution of a chosen model; it does not validate its realism.
