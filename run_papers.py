"""
Interactive launcher for the Zero Parameter Structure paper scripts.

Examples:
    python run_papers.py
    python run_papers.py 1
    python run_papers.py 1 3 7
    python run_papers.py 1-4
    python run_papers.py --all
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Paper:
    number: int
    title: str
    module: str


PAPERS: tuple[Paper, ...] = (
    Paper(1, "Cosmology", "code.paper1_cosmology"),
    Paper(2, "Electron", "code.paper2_electron"),
    Paper(3, "Gravity", "code.paper3_gravity"),
    Paper(4, "Quark Masses", "code.paper4_quark_mass"),
    Paper(5, "Neutrino", "code.paper5_neutrino"),
    Paper(
        6,
        "Higgs, Electroweak, and Strong Coupling",
        "code.paper6_higgs_electroweak",
    ),
    Paper(
        7,
        "Cosmological and Local Kinematic Scales",
        "code.paper7_cosmological_kinematics",
    ),
)

PAPER_BY_NUMBER = {paper.number: paper for paper in PAPERS}


def show_menu() -> None:
    print("Zero Parameter Structure - Paper Runner")
    print("=" * 44)
    for paper in PAPERS:
        print(f"{paper.number}. {paper.title}")
    print("a. Run all papers")
    print("q. Quit")
    print()
    print("Examples: 1, 1 3 7, 1-4, a")


def parse_selection(tokens: list[str]) -> list[int]:
    """Parse paper numbers, comma-separated values, and ranges."""
    normalized: list[str] = []
    for token in tokens:
        normalized.extend(part.strip() for part in token.split(","))

    selected: set[int] = set()

    for token in normalized:
        if not token:
            continue

        lower = token.lower()
        if lower in {"a", "all", "--all"}:
            return [paper.number for paper in PAPERS]

        if "-" in token:
            parts = token.split("-", maxsplit=1)
            if len(parts) != 2 or not all(part.strip().isdigit() for part in parts):
                raise ValueError(f"Invalid range: {token}")

            start, end = (int(part.strip()) for part in parts)
            if start > end:
                start, end = end, start

            for number in range(start, end + 1):
                if number not in PAPER_BY_NUMBER:
                    raise ValueError(f"Paper number out of range: {number}")
                selected.add(number)
            continue

        if not token.isdigit():
            raise ValueError(f"Invalid selection: {token}")

        number = int(token)
        if number not in PAPER_BY_NUMBER:
            raise ValueError(f"Paper number out of range: {number}")
        selected.add(number)

    if not selected:
        raise ValueError("No paper was selected.")

    return sorted(selected)


def run_paper(paper: Paper) -> bool:
    print()
    print("=" * 72)
    print(f"Paper {paper.number}: {paper.title}")
    print(f"Command: {sys.executable} -m {paper.module}")
    print("=" * 72)

    completed = subprocess.run(
        [sys.executable, "-m", paper.module],
        check=False,
    )

    if completed.returncode == 0:
        print(f"\nPaper {paper.number} completed successfully.")
        return True

    print(
        f"\nPaper {paper.number} failed "
        f"with exit code {completed.returncode}.",
        file=sys.stderr,
    )
    return False


def run_selected(numbers: list[int]) -> int:
    failures: list[int] = []

    for number in numbers:
        if not run_paper(PAPER_BY_NUMBER[number]):
            failures.append(number)

    print()
    print("=" * 72)
    if failures:
        failed_text = ", ".join(str(number) for number in failures)
        print(f"Completed with failures: Paper {failed_text}")
        return 1

    print("All selected papers completed successfully.")
    return 0


def interactive_selection() -> list[int] | None:
    while True:
        show_menu()
        response = input("Select paper(s): ").strip()

        if response.lower() in {"q", "quit", "exit"}:
            return None

        try:
            return parse_selection(response.split())
        except ValueError as error:
            print(f"\nError: {error}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run selected Zero Parameter Structure paper scripts."
    )
    parser.add_argument(
        "papers",
        nargs="*",
        help="Paper numbers or ranges, for example: 1 3 5-7",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Run all paper scripts.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.all:
        selected = [paper.number for paper in PAPERS]
    elif args.papers:
        try:
            selected = parse_selection(args.papers)
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 2
    else:
        selected = interactive_selection()
        if selected is None:
            print("Cancelled.")
            return 0

    print("Selected:", ", ".join(f"Paper {number}" for number in selected))
    return run_selected(selected)


if __name__ == "__main__":
    raise SystemExit(main())
