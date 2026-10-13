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

## Ownership and publication

The owner confirmed the right to publish their original strategy concept and independently authored project materials, while questionnaires and original survey results remain outside this repository. Code, documentation and original artwork are published under the [MIT License](../LICENSE); third-party Python dependencies retain their respective licenses.

The initial review inspected the intended source tree, notebook metadata, generated assets and Git history. The owner accepted the earlier specification's presence in historical commit `a8d5488`; that document is absent from the current tree. See the [engineering review](AUDIT_REPORT.md) and [publication record](PUBLICATION_CHECKLIST.md) for the completed checks.

Synthetic-data analysis demonstrates a workflow, not observed retail performance. Any future real-world data, external visual, or company-specific claim requires appropriate permission and evidence before publication.
