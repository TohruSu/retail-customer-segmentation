# Engineering review and validation record

**Reviewed:** 2026-10-13  
**Repository:** [retail-customer-segmentation](https://github.com/TohruSu/retail-customer-segmentation)  
**Status:** Public · MIT License · `main` · no GitHub Release planned

This document records the checks performed during the initial implementation and publication review. It is a record of that review, not a claim that the software has been validated against real customers or deployed in a store.

## Review findings and resolutions

| Finding | Resolution |
| --- | --- |
| Historical project specification included unnecessary background | Replaced in the current tree with [PROJECT_CHARTER.md](PROJECT_CHARTER.md). The owner reviewed and accepted the original file's presence in public Git history. |
| Original survey and source-data boundary | Intended source files, notebook metadata, figures, generated output and the publication tree were reviewed; the project uses independently generated synthetic data. |
| Monthly and weekly visits plotted together | Each distribution now uses its own axis and explicitly labeled time unit. Underlying values were not changed. |
| Whitespace checks ignored committed changes | CI now compares the committed base/head range, with an initial-push fallback. |
| Generated SVG formatting | Normalized nonsemantic trailing whitespace and added regression tests; chart coordinates and reported values were preserved. |
| Dependency compatibility | CI covers Python 3.11, 3.12 and 3.13 with documented conditional transitive pins. |
| README and provenance | Added clear navigation, reproducible commands, original visuals and distinct methodology/strategy explanations. |
| License and publication | The owner selected MIT for the independently authored project and approved the historical disclosures. PR #1 was merged; the repository is public. |

## Reproducibility evidence

The reference development environment used Python **3.12.14**, NumPy **2.3.5**, pandas **2.2.3**, scikit-learn **1.8.0** and matplotlib **3.10.8**.

| Check | Recorded result |
| --- | --- |
| Test suite | **72 tests passed** in a single local run (53.58 s) |
| Notebooks | **8/8** executed from clean, output-free sources |
| Style | Ruff lint and format checks passed |
| Package | Editable install, built wheel and isolated install passed |
| Offline workflow | Two 720-row runs at seed 2026 produced **11 byte-identical files** in the reference environment |
| Visuals | Preview assets regenerated and verified; visit-unit regression checks passed |
| GitHub Actions | **Success** on `main` for Python 3.11–3.13, including tests and notebook execution |

**Hosted CI:** [latest README commit `6af50c5`](https://github.com/TohruSu/retail-customer-segmentation/actions/runs/38390736397) · [merged implementation `b6f84a7`](https://github.com/TohruSu/retail-customer-segmentation/actions/runs/38389466177).

These results demonstrate that the implementation runs reproducibly in the documented environments. Clustering metrics are based on synthetic observations; their meaning and limitations are discussed in [ANALYTICAL_LIMITATIONS.md](ANALYTICAL_LIMITATIONS.md).

## Data, assets and history

The published implementation uses the repository's deterministic generator, new Python code, eight clean notebooks and original illustrations. It does **not** contain original questionnaires, respondent data, original survey statistics, executed historical notebooks, or proprietary business images. See [PROVENANCE_AND_SCOPE.md](PROVENANCE_AND_SCOPE.md) for the detailed scope.

The earlier `ADK_Public_Safe_Project_Specification.md` was deleted from the current tree but remains accessible in historical commit `a8d5488`. The owner explicitly reviewed and accepted that historical disclosure before making the repository public. No Git history was rewritten.

The project is licensed under [MIT](../LICENSE). Its case-study conclusions and simulation metrics are illustrative and should not be interpreted as evidence of measured retail impact.

## Maintenance

To reproduce or update results, use the commands in the [README](../README.md). If the generator, dependencies, figures or analytical interpretation change, re-run the complete tests, eight notebooks and preview generation, and update the methodology documentation as needed.
