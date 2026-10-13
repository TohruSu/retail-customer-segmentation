"""Aggregate-only reports with explicit independently synthetic provenance."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

import pandas as pd

from .figures import VISUAL_FILENAMES, check_output_paths, publish_staged_file, render_visuals
from .schema import SYNTHETIC_NOTICE

REPORT_FILENAMES = (
    "report.json",
    "diagnostics.csv",
    "profiles.csv",
    "sensitivity.csv",
    "baseline.csv",
    "report.md",
    *VISUAL_FILENAMES,
)


def _table(rows: list[dict[str, Any]]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    frame.insert(0, "data_status", "SYNTHETIC")
    return frame


def _number(value: Any) -> str:
    if value is None:
        return "not estimable"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.4f}"


def _markdown_table(rows: list[dict[str, Any]], columns: tuple[str, ...]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        cells = []
        for column in columns:
            value = row.get(column)
            cells.append(str(value) if isinstance(value, str) else _number(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def report_markdown(result: dict[str, Any]) -> str:
    """Create a readable quantitative report without selecting a managerial target."""
    preprocessing = result["preprocessing"]
    settings = result.get("analysis_settings", {})
    baseline = result["baseline"]
    diagnostics = _markdown_table(
        result["candidates"],
        (
            "k",
            "silhouette",
            "min_cluster_share",
            "max_cluster_share",
            "initialization_ari_mean",
            "initialization_ari_min",
        ),
    )
    sensitivity = _markdown_table(
        result["sensitivity"], ("variant", "k", "ari_vs_reference", "silhouette")
    )
    profiles = _markdown_table(result["profiles"], ("cluster", "count", "share"))
    feature_names = ", ".join(f"`{name}`" for name in preprocessing["features"])
    warning_lines = "\n".join(f"- {warning}" for warning in result["warnings"])
    input_provenance = (
        f"Input CSV SHA-256: `{result['input_sha256']}`.\n" if "input_sha256" in result else ""
    )
    return f"""# Independent retail analytics — SYNTHETIC report

{SYNTHETIC_NOTICE}

All numbers in this report, its tables and diagnostic figures describe fictional
records. The meal-choice diagram is an ILLUSTRATIVE strategy proposal. There is
no observed store deployment, business uplift, or validated customer segment.

## Data and preprocessing

SYNTHETIC cohort: **{result["n_rows"]} fictional records**.
Analysis seed: **{settings.get("seed", "recorded by the caller")}**.
{input_provenance}The analysis seed governs model randomness; an arbitrary input CSV's
generation seed is unknown unless separately documented. Exact settings and
runtime dependency versions are recorded in `report.json`.
Features used for clustering: {feature_names}.
Visit counts and identifiers are excluded from fitting to avoid outcome leakage.
Missing attitude values are imputed with feature medians, then standardized.
PCA retains **{preprocessing["component_count"]} components** and
**{preprocessing["retained_variance"]:.4f}** of standardized SYNTHETIC variance.
Profile means in `profiles.csv` use observed cells rather than imputed values.

## SYNTHETIC candidate diagnostics

{diagnostics}

Shares range from 0 to 1. Silhouette ranges from -1 to 1. ARI measures agreement
between initialization runs; stability does not establish external validity.
Reference k = **{result["exploratory_k"]}**, selected by maximum silhouette with
smaller k breaking ties, is used only to compare technical partitions. It does
not establish a meaningful market-segment count or recommend a customer target.

## SYNTHETIC reference partition sizes

{profiles}

Cluster numbers are arbitrary labels within this run. Full observed SYNTHETIC
attitude and visit means appear in `profiles.csv`. No individual records or
participant-level assignments are exported in this report.

## SYNTHETIC feature/PCA sensitivity

{sensitivity}

Representations change both geometry and assignments. Their silhouette values
are descriptive within each representation, not a leaderboard for business value.

## SYNTHETIC descriptive baseline

An unsegmented summary and a declared convenience-proxy threshold appear in
`baseline.csv`. {baseline["stratification_rule"]}
Compare cluster descriptions against this simpler interpretation before treating
extra model complexity as useful. The synthetic cohort cannot resolve that
managerial choice or the existence of a real unmet need.

## Limits and evaluation

{warning_lines}

Targeting remains a conditional editorial judgment. The proposed meal-occasion
comparison hub requires real, consented evidence and a pilot comparison before
claiming changes in interaction, food-floor transition, purchase or revisit.
See `docs/STRATEGY_CASE.md` and `docs/ANALYTICAL_LIMITATIONS.md` in the repository
for the pilot plan and the distinction between observation and hypothesis.

## Output provenance

`report.json` contains aggregate diagnostics and settings, excluding row labels.
CSV tables include `data_status=SYNTHETIC`. Original PNG/SVG visuals are generated
by `src/retail_case/figures.py`. No private data or external graphic is required.
"""


def write_report(
    result: dict[str, Any],
    df: pd.DataFrame,
    output_dir: str | Path,
    *,
    seed: int = 2026,
    overwrite: bool = False,
) -> list[Path]:
    """Write deterministic aggregate JSON, labeled CSV tables, prose and visuals."""
    destination = check_output_paths(output_dir, REPORT_FILENAMES, overwrite)
    destination.mkdir(parents=True, exist_ok=True)
    summary = {key: value for key, value in result.items() if key != "labels"}
    summary["data_status"] = "SYNTHETIC"
    summary["notice"] = SYNTHETIC_NOTICE
    baseline = result["baseline"]
    baseline_rows = [
        {"interpretation": "unsegmented", "stratum": "all", **baseline["unsegmented"]},
        *[
            {"interpretation": "descriptive_threshold", **row}
            for row in baseline["descriptive_strata"]
        ],
    ]
    with tempfile.TemporaryDirectory(prefix=".retail-report-", dir=destination) as staging:
        staged = Path(staging)
        (staged / "report.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        for filename, rows in (
            ("diagnostics.csv", result["candidates"]),
            ("profiles.csv", result["profiles"]),
            ("sensitivity.csv", result["sensitivity"]),
            ("baseline.csv", baseline_rows),
        ):
            _table(rows).to_csv(staged / filename, index=False, lineterminator="\n")
        (staged / "report.md").write_text(report_markdown(result), encoding="utf-8")
        render_visuals(result, df, staged, seed=seed)
        for filename in REPORT_FILENAMES:
            publish_staged_file(staged / filename, destination / filename, overwrite=overwrite)
    return [destination / name for name in REPORT_FILENAMES]
