# Publication and reproducibility record

**Published:** 2026-10-13  
**Status:** Public · `main` · MIT License  
**Initial implementation:** [PR #1](https://github.com/TohruSu/retail-customer-segmentation/pull/1) (merged)

This page records the initial publication review and provides a compact checklist for future updates. It replaces the pre-publication approval checklist.

## Completed at publication

- [x] Reviewed the intended source tree, notebooks, reports and original artwork for restricted inputs, credentials and survey-derived results.
- [x] Confirmed that reproducible examples use the project's independent synthetic-data generator.
- [x] Distinguished simulated analytical outputs from business strategy and pilot proposals.
- [x] Confirmed the owner's publication approval and acceptance of the historical specification in commit `a8d5488`.
- [x] Added the [MIT License](../LICENSE) for independently owned project materials.
- [x] Ran **72 automated tests**, **8 notebooks**, lint, formatting and package installation checks.
- [x] Checked deterministic output generation, figure labels, README links and provenance.
- [x] Confirmed passing [GitHub Actions on `main`](https://github.com/TohruSu/retail-customer-segmentation/actions/runs/38390736397) for Python 3.11–3.13.

The complete findings and test environment are documented in [AUDIT_REPORT.md](AUDIT_REPORT.md).

## Before future changes

- [ ] Keep original questionnaires, restricted datasets, survey results, private assets and credentials out of the repository and commit history.
- [ ] For newly added data or visuals, document their source and rights; use approved public inputs or independent synthetic generation.
- [ ] Run `pytest`, `ruff check .`, `ruff format --check .`, and `python scripts/check_notebooks.py` in a clean environment.
- [ ] Regenerate preview images if analysis or figures change; confirm units, captions and reproducibility.
- [ ] Review GitHub Actions, documentation links and the assumptions in the strategy/pilot proposal.
- [ ] Keep simulated analysis distinct from any future measured customer or business outcomes.

The initial version is published directly from `main`; **no GitHub Release is planned**. See [PROVENANCE_AND_SCOPE.md](PROVENANCE_AND_SCOPE.md) for source boundaries and [ANALYTICAL_LIMITATIONS.md](ANALYTICAL_LIMITATIONS.md) for interpretation.
