# Provenance and scope

## What this project is

**今日の食えらび編集室 / Meal-Choice Editorial Studio** is an independent portfolio implementation of an exploratory analytics-to-strategy workflow. Its computational evidence comes only from a newly designed deterministic simulation. Its meal-choice concept is a hypothetical proposal supplied as the user’s self-authored idea.

The initial implementation was informed by a user-provided public-safe conceptual brief and build request. Current repository requirements are recorded in [the public project charter](PROJECT_CHARTER.md). The charter describes the independent project; it does not retroactively replace the initial brief as an implementation input. Neither supplies survey evidence. No original private archive, questionnaire, respondent data, question mapping, survey summary, executed original notebook, or private business asset is needed or used.

Historical internship work and the user’s original self-authored concept are background. The newly written portfolio code demonstrates general methods using independent synthetic data; it does not reproduce historical survey segments, metrics, or achievements.

## Provenance by artifact

| Artifact | Basis | Permitted interpretation |
| --- | --- | --- |
| `src/retail_case/`, tests, CI | Newly written implementation of general methods | Engineering and reproducibility demonstration |
| Generated rows and reports | Deterministic RNG and declared invented equations | **SYNTHETIC / ILLUSTRATIVE** outcomes only |
| Analytical notebooks | New code using the package and independent simulation | Exploratory demonstration; no real market inference |
| Diagnostic graphic | Newly generated synthetic analysis | Description of the simulated dataset and model sensitivity |
| Journey graphic | Original schematic of the proposed concept | **HYPOTHETICAL PROPOSAL**, not an actual store plan |
| Strategy narrative | Permitted conceptual brief and explicitly marked assumptions | Conditional design recommendations requiring a pilot |
| Public project charter | Sanitized requirements for this independent implementation | Current scope and publication boundary, not a source of survey findings |

The simulation is not fitted to, sampled from, perturbed from, or statistically matched to restricted records. Invented field names are generic modelling choices, not renamed questionnaire items. Synthetic participant IDs cannot identify people. There are no known true consumer clusters in the generator.

## Publication boundary

Keep the following outside this repository, its history, cloud inputs, CI logs, notebook outputs, screenshots, and examples:

- Original survey data, respondent examples, questionnaires, question/code lists, and mapping files.
- Source-derived counts, percentages, means, cross-tabs, PCA/KMeans results, profiles, or plots.
- Original executed notebooks, private archives, commercial images, internal documents, and materials without publication rights.
- Credentials, personal identifiers, or any dataset of unknown provenance.

Removing identifiers or raw data does not make a source-derived survey result publishable. Rewording an item or changing a file name does not establish independent provenance. A filename scan alone cannot prove absence of protected content.

## Claims and affiliation

All numbers computed here must retain the statement **“Illustrative results on independently generated synthetic data; not findings from the ADK consumer survey.”** Charts use `SYNTHETIC` labels; concept diagrams use `HYPOTHETICAL PROPOSAL` labels. The names of organizations in provenance notices do not imply endorsement, commissioning, adoption, or evaluation.

This case uses generic retail channels. It makes no factual claims about a named company’s capabilities, site availability, current real estate, sales, or customers. No external photographs, logos, borrowed diagrams, or architectural plans are required. Any future factual company claim needs a public source, access date, and a clear distinction from scenario assumptions.

The optional space scenario of roughly 150 tsubo is only a case-design assumption. It is not a verified location, allocated retail space, implementation budget, or authenticated floor plan.

## Ownership and review

The user reports permission for self-authored analysis materials, while questionnaires and survey results remain restricted. That statement is the working boundary; it does not establish rights in every sentence or asset. The owner reports selecting the MIT License for independently owned code, documentation, and original artwork (`../LICENSE`). The owner must still confirm rights in each final narrative and graphic; third-party dependencies retain their own license terms.

Automated repository checks and a written audit support review but cannot certify legal permissions or the full history. A feature-branch commit, push, and PR in the private repository are authorized for review. Public release still requires [the publication checklist](PUBLICATION_CHECKLIST.md), including manual review of every historical revision, rights confirmation, license choice, and hosted CI verification. Merge, tag, and visibility changes require separate owner approval.

Removing an earlier requirements document from the current tree does not remove it from existing commits. Historical background references in earlier revisions remain an owner review/remediation decision; this refinement does not rewrite history. See [the audit report](AUDIT_REPORT.md) for the recorded history scope and remaining decisions.
