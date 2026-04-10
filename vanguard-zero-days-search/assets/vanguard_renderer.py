#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


RENDERED_FINDINGS_DIRNAME = "rendered-findings"
FINDINGS_FILENAME = "findings.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Perform the vanguard-zero-days-search Triager workflow for an mpitt batch "
            "by rendering each Vanguard analysis result into "
            "rendered-findings/<project>/<detector>/findings.txt."
        )
    )
    parser.add_argument("batch_path", help="Path to the mpitt batch directory.")
    parser.add_argument(
        "--output-dir",
        help=(
            "Optional directory for rendered findings. "
            "Defaults to <batch_path>/rendered-findings."
        ),
    )
    return parser.parse_args()


def validate_batch(batch_path: Path) -> None:
    if not batch_path.exists():
        raise FileNotFoundError(f"Batch path does not exist: {batch_path}")
    if not batch_path.is_dir():
        raise NotADirectoryError(f"Batch path is not a directory: {batch_path}")


def ensure_rmm_cli() -> str:
    rmm_cli = shutil.which("rmm-cli")
    if rmm_cli is None:
        raise FileNotFoundError("rmm-cli was not found in PATH")
    return rmm_cli


def project_dirs(batch_path: Path) -> list[Path]:
    return sorted(
        child for child in batch_path.iterdir() if child.is_dir() and (child / "workarea").is_dir()
    )


def detector_name_from_result(result_json: Path, vanguard_root: Path) -> str:
    relative = result_json.relative_to(vanguard_root)
    parts = relative.parts
    results_index = parts.index("results")
    detector_parts = parts[:results_index]
    if detector_parts and detector_parts[0] == "hiyul":
        return detector_parts[-1]
    return detector_parts[0]


def find_results_for_project(project_dir: Path) -> list[tuple[str, Path]]:
    vanguard_root = project_dir / "workarea" / "veridise_artifacts" / "vanguard"
    if not vanguard_root.is_dir():
        return []

    results: list[tuple[str, Path]] = []
    for result_json in sorted(vanguard_root.rglob("*.json")):
        if "results" not in result_json.parts:
            continue
        detector = detector_name_from_result(result_json, vanguard_root)
        results.append((detector, result_json))
    return results


def render_finding(rmm_cli: str, result_json: Path) -> str:
    completed = subprocess.run(
        [rmm_cli, "render", "text", str(result_json)],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        error_output = completed.stderr.strip() or completed.stdout.strip() or "Unknown error"
        raise RuntimeError(f"rmm-cli failed for {result_json}: {error_output}")
    return completed.stdout


def render_batch(batch_path: Path, output_dir: Path, rmm_cli: str) -> list[Path]:
    written_files: list[Path] = []
    output_dir.mkdir(parents=True, exist_ok=True)

    projects = project_dirs(batch_path)
    if not projects:
        raise RuntimeError(f"No project directories with a workarea were found in batch: {batch_path}")

    for project_dir in projects:
        project_output_dir = output_dir / project_dir.name
        project_has_findings = False

        for detector, result_json in find_results_for_project(project_dir):
            findings_text = render_finding(rmm_cli, result_json)
            if not findings_text.strip():
                continue

            if not project_has_findings:
                project_output_dir.mkdir(parents=True, exist_ok=True)
                project_has_findings = True

            detector_output_dir = project_output_dir / detector
            detector_output_dir.mkdir(parents=True, exist_ok=True)
            findings_path = detector_output_dir / FINDINGS_FILENAME
            findings_path.write_text(findings_text, encoding="utf-8")
            written_files.append(findings_path)

    return written_files


def main() -> int:
    args = parse_args()
    batch_path = Path(args.batch_path).expanduser().resolve()
    validate_batch(batch_path)
    rmm_cli = ensure_rmm_cli()

    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else batch_path / RENDERED_FINDINGS_DIRNAME
    )

    written_files = render_batch(batch_path, output_dir, rmm_cli)
    for path in written_files:
        print(path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
