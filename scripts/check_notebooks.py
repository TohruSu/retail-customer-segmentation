#!/usr/bin/env python3
"""Execute the eight public notebooks while preserving their clean source files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

NOTEBOOK_NAMES = (
    "01_data_understanding.ipynb",
    "02_retail_diagnosis.ipynb",
    "03_opportunity.ipynb",
    "04_segmentation.ipynb",
    "05_targeting.ipynb",
    "06_competitor_3c.ipynb",
    "07_positioning.ipynb",
    "08_strategy_pilot.ipynb",
)
PLOT_NOTEBOOKS = {
    "02_retail_diagnosis.ipynb",
    "04_segmentation.ipynb",
    "08_strategy_pilot.ipynb",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Executed copies; default: build/executed_notebooks in the repository.",
    )
    parser.add_argument("--timeout", type=int, default=180, help="Seconds per code cell.")
    parser.add_argument(
        "--notebook",
        action="append",
        choices=NOTEBOOK_NAMES,
        help="Execute only this stage; repeat to select several. Default: all eight.",
    )
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")

    repository = Path(__file__).resolve().parents[1]
    notebook_dir = repository / "notebooks"
    output_dir = (args.output_dir or repository / "build" / "executed_notebooks").resolve()
    if output_dir == notebook_dir.resolve() or notebook_dir.resolve() in output_dir.parents:
        parser.error("--output-dir must be outside the source notebooks directory")

    notebooks = []
    source_hashes = {}
    selected_names = tuple(dict.fromkeys(args.notebook or NOTEBOOK_NAMES))
    for name in selected_names:
        path = notebook_dir / name
        if not path.is_file():
            parser.error(f"missing source notebook: {name}")
        source_hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        for cell in notebook.cells:
            if cell.cell_type == "code" and (cell.outputs or cell.execution_count is not None):
                parser.error(f"source notebook contains stored execution state: {name}")
        notebooks.append((name, notebook))

    output_dir.mkdir(parents=True, exist_ok=True)
    # A temporary python3 kernelspec points at this interpreter. This avoids a
    # system Jupyter kernel silently escaping the activated development venv.
    with tempfile.TemporaryDirectory(prefix="retail-case-kernel-") as temporary:
        kernel_root = Path(temporary)
        kernel_dir = kernel_root / "python3"
        kernel_dir.mkdir()
        (kernel_dir / "kernel.json").write_text(
            json.dumps(
                {
                    "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                    "display_name": "Python (current retail-case environment)",
                    "language": "python",
                    "env": {"MPLBACKEND": "module://matplotlib_inline.backend_inline"},
                }
            ),
            encoding="utf-8",
        )
        kernel_specs = KernelSpecManager(kernel_dirs=[str(kernel_root)])
        for name, notebook in notebooks:
            manager = KernelManager(
                kernel_name="python3",
                kernel_spec_manager=kernel_specs,
                transport="ipc" if os.name == "posix" else "tcp",
            )
            client = NotebookClient(
                notebook,
                km=manager,
                kernel_name="python3",
                timeout=args.timeout,
                allow_errors=False,
                resources={"metadata": {"path": str(repository)}},
            )
            try:
                client.execute()
            except CellExecutionError as error:
                print(f"FAIL {name}: {error}", file=sys.stderr)
                return 1
            finally:
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
                    manager.cleanup_resources()
            outputs = [
                output
                for cell in notebook.cells
                if cell.cell_type == "code"
                for output in cell.outputs
            ]
            if any(output.output_type == "error" for output in outputs):
                print(f"FAIL {name}: execution produced an error output", file=sys.stderr)
                return 1
            mime_types = {mime for output in outputs for mime in output.get("data", {})}
            if name in PLOT_NOTEBOOKS and "image/png" not in mime_types:
                print(f"FAIL {name}: expected plot did not render an image", file=sys.stderr)
                return 1
            if name[:2] <= "05":
                streams = "".join(output.get("text", "") for output in outputs)
                if "SYNTHETIC" not in streams or "text/html" not in mime_types:
                    print(f"FAIL {name}: missing labeled computational table", file=sys.stderr)
                    return 1
            nbformat.write(notebook, output_dir / name)
            print(f"PASS {name}", flush=True)

    for path, before in source_hashes.items():
        if hashlib.sha256(path.read_bytes()).hexdigest() != before:
            print(f"FAIL source notebook changed during execution: {path.name}", file=sys.stderr)
            return 1
    print(f"PASS {len(notebooks)}/{len(selected_names)} notebooks; clean sources preserved.")
    print(f"Executed copies: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
