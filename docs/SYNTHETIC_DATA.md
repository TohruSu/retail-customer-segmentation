# Independent synthetic data

**SYNTHETIC / ILLUSTRATIVE only.** The generator reads no external data. Every record and coefficient is newly invented; nothing is sampled, fitted, perturbed, or matched to protected records. The cohort does not reproduce the source survey's sample size or instrument. Proxy names are modelling labels, not questionnaire items.

## Contract and defaults

`generate_data(n=720, seed=2026, missing_rate=0.03)` uses `numpy.random.default_rng`. A positive integer cohort size, a nonnegative integer seed, and a finite missingness setting from 0 to 0.20 are required. The generator allows small cohorts for validation; the default k=2–5 analysis requires at least six rows and enough distinct prepared rows. Its default 720 rows are fictional participants, not an observed sample.

| Column | Type / bounds | Role and unit |
| --- | --- | --- |
| `participant_id` | Unique string `SYN000001`, … | Fictional sequential identifier; excluded from features |
| `data_status` | Constant string `SYNTHETIC` | Explicit row-level marker; excluded from features |
| `monthly_store_visits` | Integer 0–30; no missing values | Invented visits per month; descriptive outcome only |
| `weekly_other_channel_visits` | Integer 0–21; no missing values | Invented other-channel visits per week; descriptive outcome only |
| `price_attention` | Integer-valued 1–5 or missing | Invented attitude proxy |
| `meal_planning_interest` | Integer-valued 1–5 or missing | Invented attitude proxy |
| `convenience_preference` | Integer-valued 1–5 or missing | Invented attitude proxy |
| `discovery_interest` | Integer-valued 1–5 or missing | Invented attitude proxy |
| `cooking_interest` | Integer-valued 1–5 or missing | Invented attitude proxy |
| `shopping_time_pressure` | Integer-valued 1–5 or missing | Invented attitude proxy |
| `cross_category_interest` | Integer-valued 1–5 or missing | Invented attitude proxy |

Attitudes are stored as floating-point columns to accommodate `NaN`; every observed score is integer-valued. Weekly and monthly counts have different time units and should not be treated as comparable rates without an explicit conversion assumption. No real product category, respondent, survey code, retailer, or question wording is represented.

## Declared generative equations

Each row receives three independent standard-normal continuous factors:

- `B`: budget attention;
- `T`: time pressure;
- `E`: exploration.

These names describe invented mathematical factors, not empirically validated constructs. There are **no discrete latent groups or ground-truth cluster labels**. Factors are not included in the exported schema.

Each attitude uses `clip(round(3 + w_B·B + w_T·T + w_E·E + ε), 1, 5)`, with independent `ε ~ Normal(0, 0.9²)` for each row/attitude. Rounding uses NumPy's nearest-integer rule. The intercept, coefficients, and noise intentionally produce overlap rather than separated textbook clusters.

| Proxy | `w_B` | `w_T` | `w_E` |
| --- | ---: | ---: | ---: |
| `price_attention` | 0.70 | 0.05 | −0.10 |
| `meal_planning_interest` | 0.10 | −0.55 | 0.25 |
| `convenience_preference` | −0.10 | 0.75 | 0.15 |
| `discovery_interest` | −0.15 | 0.10 | 0.75 |
| `cooking_interest` | 0.15 | −0.65 | 0.20 |
| `shopping_time_pressure` | 0.05 | 0.85 | −0.05 |
| `cross_category_interest` | 0.05 | 0.10 | 0.60 |

The count simulation is:

```text
monthly rate = clip(5 − 0.6·T + 0.4·E, 0.8, 12)
monthly_store_visits = clip(Poisson(monthly rate), 0, 30)

weekly other-channel rate = clip(2.5 + 0.7·T − 0.3·B, 0.3, 7)
weekly_other_channel_visits = clip(Poisson(weekly other-channel rate), 0, 21)
```

This deliberately creates mild within-simulation associations without interpreting them as retail facts or causal effects. Poisson counts, linear rate links, and caps are simplifying choices; the tails and relationships do not estimate a population.

For each attitude independently, the generator selects `floor(n × missing_rate)` row positions uniformly **without replacement** and writes missing values. Each column therefore has the same missing count, while overlap across columns is random. This is a fixed-count missingness design, not a Bernoulli draw per cell. At the defaults, each attitude has **21 missing values among 720 fictional rows (2.92%, SYNTHETIC)**; floor rounding explains the difference from the 0.03 input. Behaviors and IDs remain complete. This does not model systematic nonresponse.

## Validation and preprocessing

Validation requires exactly the declared columns, unique SYN-prefixed IDs, the constant status marker, real numeric types excluding booleans, finite observed values, integer-valued proxies/counts, bounds, complete behaviors, and at most 20% missingness in each attitude. It rejects duplicate columns and duplicate IDs. Error messages describe the failing field or rule without echoing records.

A `SYNTHETIC` marker and valid schema **cannot prove provenance**: arbitrary records can carry a false label. Use only data produced by this repository's independent generator, not unknown external data.

The clustering pipeline uses the seven attitudes only. It fits per-feature median imputation and `StandardScaler` on the exploratory synthetic cohort, then full-solver PCA retaining the minimum component count exceeding the default **90%** explained-variance target. The component count is computed from the data rather than preset. Cluster profile and baseline means use **observed cells**, excluding missing values; they do not silently present imputed cells as observed responses.

KMeans candidates k=2–5 use `n_init=10`. The highest silhouette selects one technical reference partition for profiles and sensitivity, with smaller k breaking ties; it does not recommend a real segment count or audience. Five `n_init=1` fits with deterministically drawn seeds expose initialization sensitivity using all pairwise ARIs. Fixed-reference-k alternatives remove PCA or omit `shopping_time_pressure`.

The baseline reports the whole cohort and a predeclared descriptive convenience split: observed values at least 4 versus below 4, with missing values separate. The threshold is an illustrative choice, not a validated target rule. [Analytical limitations](ANALYTICAL_LIMITATIONS.md) explain what these comparisons can establish.

## Storage and reproducibility

Regenerate CSVs under ignored `build/`; no respondent-level example CSV needs to be committed. The default analysis produces aggregate reports and newly drawn labeled figures. Reusing the same n, seed, missingness, settings, and dependency runtime reproduces the same simulation and analysis. A changed cohort size can change RNG consumption and results; IDs do not represent persistent entities across simulations. Package/library changes and floating-point differences can change borderline diagnostics.

All output descriptions must include **“Illustrative results on independently generated synthetic data; not findings from the ADK consumer survey.”** Preserve labels when exporting figures or summarizing values.
