# Owner publication checklist

**Public release is pending owner review and explicit approval.** The current refinement authorizes a feature-branch commit, push, and PR in the private repository. That authorization does not include merging, tagging a release, publishing, or changing repository visibility.

## Provenance and permissions

- [ ] Confirm the independently authored concept and every business-case detail are permitted to publish.
- [ ] Confirm all data are produced only by the declared independent generator, with no fitting, sampling, perturbation, or statistical matching to protected records.
- [ ] Confirm no original questionnaire, respondent example, mapping, survey result, original segment/profile, or executed original notebook is included or required.
- [ ] Inspect every image, table, caption, and notebook output; confirm rights and source. Omit uncertain external material.
- [ ] Check all public factual claims for an authoritative source and access date. Generic channel assumptions remain explicitly hypothetical.
- [ ] Confirm Japanese concept attribution and English explanations are accurate without implying organizational endorsement.
- [ ] Review [the public project charter](PROJECT_CHARTER.md) as the current scope; confirm that historical experience is separated from the new synthetic method demonstration.
- [x] Select MIT License for independently owned code, documentation, and original assets (`LICENSE`). Owner confirms that all included material is owned or authorized; third-party dependencies retain their separate licenses.

## Full repository and history inspection

- [ ] Manually inspect the complete file tree, hidden dotfiles, symlinks, Git configuration relevant to publication, and all untracked/generated artifacts proposed for release.
- [ ] Manually inspect **all commits, branches, tags, historical blobs, and renamed/deleted files**, not only `git diff` or the current tree. Confirm history proposed for public release contains no restricted material and resolve unnecessary private-background references in earlier requirements documents.
- [ ] Decide how to handle historical copies of removed requirements material before publication. Current-tree removal is not history remediation; do not rewrite existing history without a separate owner decision.
- [ ] Review existing remote history before public release. An automated scan of selected commits cannot certify all remote branches or earlier uploads.
- [ ] Treat suspicious names such as `raw_data.csv`, `questionnaire.xlsx`, `question_mapping.csv`, `simple_summary.xlsx`, and private archive extensions as investigation signals within the public repository. Filename absence alone proves nothing.
- [ ] Inspect notebook source, metadata, attachments, outputs, execution counts, embedded images, and local paths. Keep committed notebooks free of executed data blobs and private paths.
- [ ] Check generated diagnostic/report text for `SYNTHETIC` / `ILLUSTRATIVE` context and strategy figures for `HYPOTHETICAL PROPOSAL` context.
- [ ] Check for credentials, `.env` files, tokens, keys, personal identifiers, CI logs, and unknown-provenance datasets. Never publish actual secret values.
- [ ] Confirm ignore rules cover private archives, local environments, caches, generated datasets/reports, and credential files. Ignore rules do not remove already tracked or historical files.
- [ ] Review [the written audit](AUDIT_REPORT.md) and resolve remaining owner decisions. An automated audit is supporting evidence, not permission or a full privacy/legal certification.

If restricted content is discovered, stop publication and handle removal through an appropriate owner-controlled process. Do not upload it to another service for review. Merely deleting the current file does not remove history or earlier remote copies.

## Reproducibility and presentation

- [ ] In a clean supported Python environment, install the package and generate/analyze fresh synthetic data using the README commands.
- [ ] Run `pytest`, `ruff check .`, `ruff format --check .`, `python scripts/check_notebooks.py`, and `git diff --check`.
- [ ] Regenerate the two original visuals; compare their labels, legends, units, and captions with actual report values.
- [ ] Ensure the eight notebooks execute without internet or private files after dependency installation.
- [ ] Verify README/doc/notebook links and the cited external URLs, if any.
- [ ] Confirm no metrics imply real market validity, proven targeting, deployment, uplift, or ROI.
- [ ] Confirm the pilot plan defines observation units, denominators, consent/linkage limits, comparison design, calendar effects, promotions, footfall, and stockouts.
- [ ] Review supported dependencies, their licenses, packaging metadata, and CI results. Record differences between local validation and hosted CI execution.
- [x] Hosted GitHub Actions passed on the private feature commit for Python 3.11, 3.12, and 3.13, including a full test suite per job: https://github.com/TohruSu/retail-customer-segmentation/actions/runs/38374579296 . Recheck the latest commit before merging.

## Release decisions

- [ ] Owner confirms final contents, concept and narrative rights, asset rights, and complete intended-publication Git history. The MIT license has been selected for independently owned material.
- [ ] Keep the authorized feature commit/push/PR within the private repository; describe the independent synthetic case and actual validation without claiming a store result.
- [ ] Obtain separate explicit owner approval before merge, release tag, publication, or Public visibility change.
- [ ] After final review and explicit approval, consider a versioned release and portfolio link. No publication is automatic.
