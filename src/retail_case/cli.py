"""Small offline CLI for independently synthetic generation and analysis."""

from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
from io import BytesIO
from pathlib import Path

import pandas as pd

from .clustering import analyze_data
from .figures import publish_staged_file, write_visual_assets
from .reporting import write_report
from .schema import SYNTHETIC_NOTICE
from .synthetic import generate_data
from .validation import validate_data


def _cohort_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--n", type=int, default=720, help="number of fictional records (default: 720)"
    )
    parser.add_argument(
        "--seed", type=int, default=2026, help="deterministic RNG seed (default: 2026)"
    )
    parser.add_argument(
        "--missing-rate",
        type=float,
        default=0.03,
        help="fraction of missing cells in each attitude column (default: 0.03)",
    )


def _overwrite_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--overwrite", action="store_true", help="explicitly replace generated output files"
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="retail-case",
        description="Independent SYNTHETIC retail analytics; no private survey data is required.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    generate = commands.add_parser("generate", help="generate an independent synthetic cohort")
    generate.add_argument("--output", type=Path, required=True, help="synthetic CSV destination")
    _cohort_options(generate)
    _overwrite_option(generate)

    analyze = commands.add_parser(
        "analyze", help="analyze synthetic CSV and write aggregate report"
    )
    analyze.add_argument(
        "--input", type=Path, required=True, help="independently synthetic input CSV"
    )
    analyze.add_argument(
        "--output-dir", type=Path, required=True, help="aggregate report directory"
    )
    analyze.add_argument(
        "--seed",
        type=int,
        default=2026,
        help="analysis RNG seed; the input's generation seed cannot be inferred",
    )
    analyze.add_argument("--variance-target", type=float, default=0.9)
    _overwrite_option(analyze)

    visuals = commands.add_parser("visuals", help="regenerate original visuals from synthetic data")
    visuals.add_argument(
        "--output-dir", type=Path, required=True, help="PNG/SVG destination directory"
    )
    visuals.add_argument("--variance-target", type=float, default=0.9)
    _cohort_options(visuals)
    _overwrite_option(visuals)
    return parser


def _generate(args: argparse.Namespace) -> None:
    output: Path = args.output
    if output.is_dir():
        raise ValueError(f"output path is a directory: {output}")
    if (output.exists() or output.is_symlink()) and not args.overwrite:
        raise FileExistsError(f"output already exists: {output}; use --overwrite to replace it")
    frame = generate_data(n=args.n, seed=args.seed, missing_rate=args.missing_rate)
    validate_data(frame)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".retail-generate-", dir=output.parent) as staging:
        staged = Path(staging) / "synthetic.csv"
        frame.to_csv(staged, index=False, lineterminator="\n")
        publish_staged_file(staged, output, overwrite=args.overwrite)
    print(f"SYNTHETIC: generated {len(frame)} fictional records in {output}")


def main(argv: list[str] | None = None) -> int:
    """Return a nonzero status with a concise error for invalid input or output."""
    args = _parser().parse_args(argv)
    try:
        if args.command == "generate":
            _generate(args)
        elif args.command == "analyze":
            input_bytes = args.input.read_bytes()
            frame = pd.read_csv(BytesIO(input_bytes))
            validate_data(frame)
            result = analyze_data(frame, seed=args.seed, variance_target=args.variance_target)
            result["input_sha256"] = hashlib.sha256(input_bytes).hexdigest()
            write_report(result, frame, args.output_dir, seed=args.seed, overwrite=args.overwrite)
            print(
                "SYNTHETIC: aggregate diagnostics and original visuals written to "
                f"{args.output_dir}"
            )
        else:
            frame = generate_data(n=args.n, seed=args.seed, missing_rate=args.missing_rate)
            result = analyze_data(frame, seed=args.seed, variance_target=args.variance_target)
            write_visual_assets(
                result, frame, args.output_dir, seed=args.seed, overwrite=args.overwrite
            )
            print(f"SYNTHETIC diagnostics and ILLUSTRATIVE journey written to {args.output_dir}")
        print(SYNTHETIC_NOTICE)
        return 0
    except (ValueError, OSError, pd.errors.ParserError) as exc:
        # Validation messages name rules and columns without dumping input rows.
        message = " ".join(str(exc).splitlines())
        print(f"retail-case: error: {message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
