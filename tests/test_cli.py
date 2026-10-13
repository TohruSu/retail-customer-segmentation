"""Exercise the public commands, labeled deliverables, and overwrite safeguards."""

import json
import os
import subprocess
import sys

import pandas as pd
import pytest


def run_cli(*arguments):
    environment = os.environ.copy()
    environment.update(
        {"OMP_NUM_THREADS": "2", "OPENBLAS_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"}
    )
    return subprocess.run(
        [sys.executable, "-m", "retail_case.cli", *map(str, arguments)],
        capture_output=True,
        text=True,
        env=environment,
        timeout=60,
    )


@pytest.fixture
def input_csv(tmp_path):
    path = tmp_path / "synthetic.csv"
    result = run_cli("generate", "--output", path, "--n", 80, "--seed", 42)
    assert result.returncode == 0, result.stderr
    return path


def test_generate_is_reproducible_and_requires_overwrite(input_csv, tmp_path):
    original = input_csv.read_bytes()
    conflict = run_cli("generate", "--output", input_csv, "--n", 80, "--seed", 99)
    assert conflict.returncode == 2
    assert input_csv.read_bytes() == original
    assert "overwrite" in conflict.stderr.lower()
    repeated = tmp_path / "repeated.csv"
    success = run_cli("generate", "--output", repeated, "--n", 80, "--seed", 42)
    assert success.returncode == 0, success.stderr
    assert repeated.read_bytes() == original
    overwritten = run_cli("generate", "--output", input_csv, "--n", 80, "--seed", 99, "--overwrite")
    assert overwritten.returncode == 0, overwritten.stderr
    assert input_csv.read_bytes() != original


def assert_visual_assets(output_dir):
    for stem in ["synthetic_diagnostics", "meal_choice_journey"]:
        svg = output_dir / f"{stem}.svg"
        png = output_dir / f"{stem}.png"
        assert svg.stat().st_size > 1000
        svg_text = svg.read_text(encoding="utf-8")
        assert "<svg" in svg_text
        assert all(line == line.rstrip(" \t") for line in svg_text.splitlines())
        assert svg_text.endswith("\n") and not svg_text.endswith("\n\n")
        assert png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        assert png.stat().st_size > 1000
    assert "SYNTHETIC" in (output_dir / "synthetic_diagnostics.svg").read_text(encoding="utf-8")
    assert (
        "hypothetical"
        in (output_dir / "meal_choice_journey.svg").read_text(encoding="utf-8").lower()
    )


def test_analyze_produces_labeled_reports_plots_and_safe_repeated_runs(input_csv, tmp_path):
    output_dir = tmp_path / "analysis"
    first = run_cli("analyze", "--input", input_csv, "--output-dir", output_dir, "--seed", 42)
    assert first.returncode == 0, first.stderr
    report_path = output_dir / "report.json"
    report_bytes = report_path.read_bytes()
    report = json.loads(report_bytes)
    assert report["data_status"] == "SYNTHETIC"
    assert "survey" in report["notice"].lower()
    assert "labels" not in report  # The exported report is aggregate-only.
    for name in ["diagnostics.csv", "profiles.csv", "sensitivity.csv", "baseline.csv"]:
        table = pd.read_csv(output_dir / name)
        assert not table.empty
        assert table["data_status"].eq("SYNTHETIC").all()
    markdown = (output_dir / "report.md").read_text(encoding="utf-8")
    assert "SYNTHETIC" in markdown
    assert "survey" in markdown.lower()
    assert_visual_assets(output_dir)
    user_note = output_dir / "owner-note.txt"
    user_note.write_text("Preserve this unrelated file.", encoding="utf-8")
    conflict = run_cli("analyze", "--input", input_csv, "--output-dir", output_dir, "--seed", 43)
    assert conflict.returncode == 2
    assert report_path.read_bytes() == report_bytes
    repeated = run_cli(
        "analyze", "--input", input_csv, "--output-dir", output_dir, "--seed", 42, "--overwrite"
    )
    assert repeated.returncode == 0, repeated.stderr
    assert report_path.read_bytes() == report_bytes
    assert user_note.read_text(encoding="utf-8") == "Preserve this unrelated file."


def test_visuals_command_produces_original_figures_and_protects_existing_files(tmp_path):
    output_dir = tmp_path / "visuals"
    result = run_cli("visuals", "--output-dir", output_dir, "--n", 80, "--seed", 123)
    assert result.returncode == 0, result.stderr
    assert_visual_assets(output_dir)
    original = (output_dir / "synthetic_diagnostics.svg").read_bytes()
    conflict = run_cli("visuals", "--output-dir", output_dir, "--n", 80, "--seed", 125)
    assert conflict.returncode == 2
    assert (output_dir / "synthetic_diagnostics.svg").read_bytes() == original
    replacement = run_cli(
        "visuals", "--output-dir", output_dir, "--n", 80, "--seed", 125, "--overwrite"
    )
    assert replacement.returncode == 0, replacement.stderr
    assert (output_dir / "synthetic_diagnostics.svg").read_bytes() != original


def test_analysis_checks_all_output_collisions_before_writing(input_csv, tmp_path):
    output_dir = tmp_path / "partial-existing-output"
    output_dir.mkdir()
    owned_file = output_dir / "meal_choice_journey.svg"
    owned_file.write_text("An existing user graphic.", encoding="utf-8")
    result = run_cli("analyze", "--input", input_csv, "--output-dir", output_dir)
    assert result.returncode == 2
    assert owned_file.read_text(encoding="utf-8") == "An existing user graphic."
    assert list(output_dir.iterdir()) == [owned_file]


def test_invalid_input_fails_cleanly_without_a_report(input_csv, tmp_path):
    frame = pd.read_csv(input_csv)
    frame.loc[0, "data_status"] = "OBSERVED"
    frame.to_csv(input_csv, index=False)
    output_dir = tmp_path / "invalid_analysis"
    result = run_cli("analyze", "--input", input_csv, "--output-dir", output_dir)
    assert result.returncode == 2
    assert "error:" in result.stderr.lower()
    assert "traceback" not in result.stderr.lower()
    assert not (output_dir / "report.json").exists()


@pytest.mark.parametrize(
    "arguments", [("generate", "--n", "0"), ("analyze", "--input", "missing.csv")]
)
def test_cli_invalid_requests_return_nonzero_with_explanation(tmp_path, arguments):
    if arguments[0] == "generate":
        result = run_cli(*arguments, "--output", tmp_path / "invalid.csv")
    else:
        result = run_cli(*arguments, "--output-dir", tmp_path / "missing")
    assert result.returncode == 2
    assert "error:" in result.stderr.lower()
    assert "traceback" not in result.stderr.lower()
