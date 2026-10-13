"""Original, reproducible visuals from aggregate synthetic diagnostics."""

from __future__ import annotations

import os
import tempfile
import textwrap
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from .schema import SYNTHETIC_NOTICE

VISUAL_FILENAMES = (
    "synthetic_diagnostics.png",
    "synthetic_diagnostics.svg",
    "meal_choice_journey.png",
    "meal_choice_journey.svg",
)

_INK = "#18334a"
_TEAL = "#087e8b"
_ORANGE = "#c66b38"
_BLUE = "#426bba"
_STYLE = {
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.labelcolor": _INK,
    "text.color": _INK,
    "axes.edgecolor": "#9caab6",
    "svg.hashsalt": "meal-choice-editorial-studio-v1",
    "svg.fonttype": "none",
}


def check_output_paths(output_dir: str | Path, filenames: tuple[str, ...], overwrite: bool) -> Path:
    """Check the whole output set before writing; preserve unrelated user files."""
    destination = Path(output_dir)
    if destination.exists() and not destination.is_dir():
        raise ValueError(f"output directory is not a directory: {destination}")
    for name in filenames:
        path = destination / name
        if path.exists() or path.is_symlink():
            if path.is_dir():
                raise ValueError(f"output path is a directory: {path}")
            if not overwrite:
                raise FileExistsError(
                    f"output already exists: {path}; use --overwrite to replace it"
                )
    return destination


def publish_staged_file(source: Path, destination: Path, *, overwrite: bool) -> None:
    """Publish a completed file atomically without accidental overwrites."""
    if overwrite:
        os.replace(source, destination)
    else:
        # Unlike a check followed by rename, link also protects against a race.
        os.link(source, destination)
        source.unlink()


def make_diagnostics_figure(
    result: dict[str, Any], df: pd.DataFrame, *, seed: int = 2026
) -> Figure:
    """Show computed diagnostics and visit ECDFs, never marketing targets."""
    with plt.rc_context(_STYLE):
        figure, axes = plt.subplots(2, 2, figsize=(13.5, 9.2))
        figure.subplots_adjust(
            left=0.075, right=0.96, top=0.82, bottom=0.18, hspace=0.60, wspace=0.30
        )
        figure.suptitle(
            "SYNTHETIC cohort: diagnostics and retail visits",
            fontsize=21,
            fontweight="bold",
            y=0.97,
        )
        figure.text(
            0.075,
            0.905,
            f"{result['n_rows']:,} fictional records  |  analysis seed {seed}  |  "
            f"exploratory k = {result['exploratory_k']}",
            fontsize=12,
        )
        figure.text(
            0.075,
            0.866,
            "Candidate partitions illustrate a workflow; "
            "they do not identify validated consumer segments.",
            fontsize=11,
        )

        candidates = result["candidates"]
        ks = [row["k"] for row in candidates]
        silhouette = [row["silhouette"] for row in candidates]
        axes[0, 0].plot(ks, silhouette, "o-", color=_TEAL, linewidth=2.1)
        axes[0, 0].set(
            title="SYNTHETIC silhouette by candidate k",
            xlabel="Number of KMeans clusters",
            ylabel="Silhouette score (−1 to 1)",
        )
        axes[0, 0].set_xticks(ks)
        low = max(-1.0, min(0.0, min(silhouette) - 0.035))
        high = min(1.0, max(0.3, max(silhouette) + 0.06))
        axes[0, 0].set_ylim(low, high)

        smallest = np.array([row["min_cluster_share"] for row in candidates]) * 100
        largest = np.array([row["max_cluster_share"] for row in candidates]) * 100
        axes[0, 1].plot(ks, smallest, "o-", color=_TEAL, label="Smallest cluster")
        axes[0, 1].plot(ks, largest, "s--", color=_ORANGE, label="Largest cluster")
        axes[0, 1].fill_between(ks, smallest, largest, color=_TEAL, alpha=0.08)
        axes[0, 1].set(
            title="SYNTHETIC cluster-size range",
            xlabel="Number of KMeans clusters",
            ylabel="Share of fictional cohort (%)",
            ylim=(0, 100),
        )
        axes[0, 1].set_xticks(ks)
        axes[0, 1].legend(frameon=False, fontsize=10)

        mean_ari = [row["initialization_ari_mean"] for row in candidates]
        min_ari = [row["initialization_ari_min"] for row in candidates]
        axes[1, 0].plot(ks, mean_ari, "o-", color=_BLUE, label="Mean pairwise ARI")
        axes[1, 0].plot(ks, min_ari, "s--", color=_ORANGE, label="Minimum pairwise ARI")
        axes[1, 0].set(
            title="SYNTHETIC initialization sensitivity",
            xlabel="Number of KMeans clusters",
            ylabel="Adjusted Rand index",
            ylim=(min(-0.05, min(min_ari) - 0.05), 1.05),
        )
        axes[1, 0].set_xticks(ks)
        axes[1, 0].legend(frameon=False, fontsize=10, loc="upper right")

        # Raw counts have different time bases; give each ECDF its own x-axis.
        visit_grid = axes[1, 1].get_subplotspec().subgridspec(1, 2, wspace=0.35)
        axes[1, 1].remove()
        visit_axes = [figure.add_subplot(visit_grid[0, index]) for index in range(2)]
        for axis, column, label, title, color in (
            (
                visit_axes[0],
                "monthly_store_visits",
                "Store visits / month",
                "SYNTHETIC\nStore visits",
                _TEAL,
            ),
            (
                visit_axes[1],
                "weekly_other_channel_visits",
                "Other-channel visits / week",
                "SYNTHETIC\nOther-channel visits",
                _ORANGE,
            ),
        ):
            values = np.sort(df[column].dropna().to_numpy(dtype=float))
            cumulative = np.arange(1, len(values) + 1) / len(values)
            axis.step(values, cumulative, where="post", color=color, linewidth=2)
            axis.set(title=title, xlabel=label, ylim=(0, 1.04))
        visit_axes[0].set_ylabel("Cumulative cohort share")

        for axis in figure.axes:
            axis.grid(axis="y", color="#dce3e8", linewidth=0.7)
            axis.set_axisbelow(True)
            axis.title.set_fontsize(12)
            axis.title.set_fontweight("bold")
        figure.text(
            0.075,
            0.102,
            "Source: independently generated data; src/retail_case/synthetic.py. "
            "All plotted values are SYNTHETIC.",
            fontsize=10,
        )
        figure.text(
            0.075, 0.054, textwrap.fill(SYNTHETIC_NOTICE, width=130), fontsize=9.4, va="center"
        )
        return figure


def make_journey_figure() -> Figure:
    """Draw the author's strategy proposal without fabricated measured effects."""
    with plt.rc_context(_STYLE):
        figure, axis = plt.subplots(figsize=(14, 8.2))
        figure.subplots_adjust(left=0.035, right=0.98, bottom=0.15, top=0.83)
        axis.set(xlim=(0, 14), ylim=(0, 7.35))
        axis.axis("off")
        figure.suptitle("Meal-Choice Editorial Studio", fontsize=23, fontweight="bold", y=0.97)
        figure.text(
            0.055,
            0.902,
            "HYPOTHETICAL PROPOSAL: compare ways to complete the same meal occasion",
            fontsize=13,
        )

        def box(
            x: float,
            y: float,
            width: float,
            height: float,
            title: str,
            detail: str,
            *,
            fill: str = "#edf5f5",
        ) -> None:
            axis.add_patch(
                FancyBboxPatch(
                    (x, y),
                    width,
                    height,
                    boxstyle="round,pad=0.08,rounding_size=0.13",
                    linewidth=1.2,
                    edgecolor=_TEAL,
                    facecolor=fill,
                )
            )
            axis.text(
                x + width / 2,
                y + height * 0.64,
                title,
                ha="center",
                va="center",
                fontsize=12,
                fontweight="bold",
            )
            axis.text(
                x + width / 2, y + height * 0.28, detail, ha="center", va="center", fontsize=10
            )

        def arrow(
            start: tuple[float, float], end: tuple[float, float], *, dashed: bool = False
        ) -> None:
            axis.add_patch(
                FancyArrowPatch(
                    start,
                    end,
                    arrowstyle="-|>",
                    mutation_scale=14,
                    linewidth=1.4,
                    color=_INK,
                    linestyle="--" if dashed else "-",
                )
            )

        box(0.15, 3.0, 2.35, 1.8, "Discover a theme", "What should I eat tonight?")
        box(
            3.05,
            3.0,
            2.5,
            1.8,
            "Compare one occasion",
            "Time, cost and effort\nare comparison prompts",
        )
        arrow((2.58, 3.9), (2.97, 3.9))

        paths = [
            (5.8, "Ingredients", "Cook this meal"),
            (4.1, "Prepared food", "Ready to eat"),
            (2.4, "Frozen / easy", "Simplify preparation"),
            (0.7, "Mix and match", "Combine several routes"),
        ]
        for y, title, detail in paths:
            box(6.25, y, 2.1, 1.2, title, detail, fill="#fff4eb")
            arrow((5.63, 3.9), (6.17, y + 0.6))
            arrow((8.43, y + 0.6), (9.0, 3.9))
        box(9.08, 3.0, 2.15, 1.8, "Shopping note", "Optional category route\nto the food floor")
        arrow((11.31, 3.9), (11.68, 3.9))
        box(11.76, 3.0, 2.05, 1.8, "Existing food floor", "Choose and shop\n(no purchase assumed)")
        box(
            9.08,
            0.45,
            4.73,
            1.3,
            "Evaluate before scaling",
            "Compare interaction, transition and purchase;\n"
            "control for footfall, promotions and seasonality.",
            fill="#f0f1fa",
        )
        arrow((12.78, 2.92), (12.78, 1.83), dashed=True)
        figure.text(
            0.055,
            0.128,
            "Recurring themes and shopping notes are hypotheses; "
            "any effect on purchase or revisit remains unknown.",
            fontsize=10,
        )

        figure.text(
            0.055,
            0.087,
            "Original conceptual diagram generated by src/retail_case/figures.py; "
            "arrows describe a proposed journey, not observed behavior.",
            fontsize=10,
        )
        figure.text(
            0.055,
            0.045,
            "ILLUSTRATIVE strategy concept. No measured uplift, real deployment, "
            "retailer affiliation or endorsement is claimed.",
            fontsize=10,
        )
        return figure


def render_visuals(
    result: dict[str, Any], df: pd.DataFrame, output_dir: Path, *, seed: int
) -> None:
    """Render figures into a fresh staging directory."""
    figures = {
        "synthetic_diagnostics": make_diagnostics_figure(result, df, seed=seed),
        "meal_choice_journey": make_journey_figure(),
    }
    try:
        with plt.rc_context(_STYLE):
            for name, figure in figures.items():
                figure.savefig(
                    output_dir / f"{name}.png",
                    dpi=160,
                    facecolor="white",
                    metadata={"Software": "retail_case.figures"},
                )
                svg_path = output_dir / f"{name}.svg"
                figure.savefig(
                    svg_path,
                    facecolor="white",
                    metadata={
                        "Date": None,
                        "Creator": "retail_case.figures",
                        "Description": SYNTHETIC_NOTICE
                        if name == "synthetic_diagnostics"
                        else "ILLUSTRATIVE hypothetical strategy; no measured customer behavior.",
                    },
                )
                # Matplotlib leaves trailing spaces in wrapped path coordinates.
                # Trim line endings so generated assets pass Git whitespace checks.
                svg_lines = svg_path.read_text(encoding="utf-8").splitlines()
                svg_path.write_text(
                    "\n".join(line.rstrip(" \t") for line in svg_lines).rstrip("\n") + "\n",
                    encoding="utf-8",
                )
    finally:
        for figure in figures.values():
            plt.close(figure)


def write_visual_assets(
    result: dict[str, Any],
    df: pd.DataFrame,
    output_dir: str | Path,
    *,
    seed: int = 2026,
    overwrite: bool = False,
) -> list[Path]:
    """Generate original PNG/SVG assets without replacing files implicitly."""
    destination = check_output_paths(output_dir, VISUAL_FILENAMES, overwrite)
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".retail-visuals-", dir=destination) as staging:
        staged = Path(staging)
        render_visuals(result, df, staged, seed=seed)
        for filename in VISUAL_FILENAMES:
            publish_staged_file(staged / filename, destination / filename, overwrite=overwrite)
    return [destination / name for name in VISUAL_FILENAMES]
