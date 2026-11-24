#!/usr/bin/env python3
"""Publish the everyday-things entry for make.fun.

Reads the two-line explanation from ``entry.txt`` beside this file,
validates it against the competition gate (UTF-8 text, 1-400
characters, not only whitespace, exactly two lines, one sentence
per line), and writes the exact bytes to ``/output/entry.txt``.

Line 1 explains one everyday thing to a 10-year-old in a single
vivid sentence built on an analogy. Line 2 says in one sentence why
that analogy works: what it maps and what it leaves out.

Usage:
    python3 main.py [--out PATH] [--check-only]

The default output path is /output/entry.txt, the path the sealed
scorer reads. ``--out`` points the publish step elsewhere (handy for
a local dry run); ``--check-only`` validates without writing anything.
"""

import argparse
import sys
from pathlib import Path

# Gate limits sealed in the competition rules.
MAX_CHARS = 400
MIN_CHARS = 1
EXPECTED_LINES = 2
DEFAULT_OUTPUT = Path("/output/entry.txt")


def load_entry(source: Path) -> bytes:
    """Read the entry bytes verbatim from ``entry.txt``.

    The bytes are never decoded-and-re-encoded here, so what is
    published is byte-identical to the file in this repository.
    """
    if not source.is_file():
        raise FileNotFoundError(f"entry file not found: {source}")
    data = source.read_bytes()
    if not data:
        raise ValueError("entry file is empty")
    return data


def validate_entry(data: bytes, max_chars: int = MAX_CHARS) -> str:
    """Check the entry bytes against the gate and return the text.

    Raises ValueError with a specific reason when any rule fails:
    not valid UTF-8, outside 1-max_chars characters, only whitespace,
    not exactly two lines, or a line that is not a single sentence.
    ``max_chars`` defaults to the sealed gate limit of 400; passing a
    smaller value lets a local run enforce a tighter budget.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"entry is not valid UTF-8: {exc}") from exc
    if not MIN_CHARS <= len(text) <= max_chars:
        raise ValueError(
            f"entry is {len(text)} characters; gate needs "
            f"{MIN_CHARS}-{max_chars}"
        )
    if not text.strip():
        raise ValueError("entry is only whitespace")
    lines = text.splitlines()
    if len(lines) != EXPECTED_LINES:
        raise ValueError(
            f"entry has {len(lines)} lines; "
            f"this competition needs exactly {EXPECTED_LINES}"
        )
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            raise ValueError(f"line {number} is empty")
        if line != line.strip():
            raise ValueError(f"line {number} has leading or trailing space")
        if not line.endswith("."):
            raise ValueError(f"line {number} does not end with a full stop")
        if line.count(".") != 1:
            raise ValueError(
                f"line {number} has {line.count('.')} full stops; "
                "each line must be a single sentence"
            )
    return text


def publish_entry(data: bytes, output: Path) -> Path:
    """Write the entry bytes unchanged to the output path.

    Creates the parent directory when needed and writes the raw bytes
    exactly as loaded, so the published file is byte-identical to
    ``entry.txt`` in this repository.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return output


def check_craft(text: str) -> None:
    """Check the two lines do the jobs the judge weighs, in order.

    Line 1 must explain one everyday thing through a concrete
    analogy (it names a familiar thing and joins it with "is a" or
    "like"), with a single metaphor and no list of comparisons.
    Line 2 must be honest and specific about the mapping: it says
    what the analogy maps and what it leaves out, instead of
    praising the analogy.
    """
    first, second = text.splitlines()
    everyday_things = (
        "toaster", "traffic", "rain", "queue", "kettle", "fridge",
        "umbrella", "elevator", "escalator", "washing machine",
    )
    lowered_first = first.lower()
    if not any(thing in lowered_first for thing in everyday_things):
        raise ValueError(
            "line 1 names no everyday thing "
            "(toaster, traffic jam, rain, queue, ...)"
        )
    if " is a " not in lowered_first and " like " not in lowered_first:
        raise ValueError("line 1 carries no analogy ('is a' / 'like')")
    lowered_second = second.lower()
    if "map" not in lowered_second:
        raise ValueError("line 2 does not say what the analogy maps")
    if "leave" not in lowered_second and "miss" not in lowered_second:
        raise ValueError("line 2 does not say what the analogy leaves out")


def report(text: str, output: Path) -> str:
    """Build the one-line human-readable summary of the publish."""
    lines = text.splitlines()
    return (
        f"published {len(text)}-character two-line explanation "
        f"({len(lines[0])} + {len(lines[1])} chars) "
        f"to {output} ({len(text.encode('utf-8'))} bytes)"
    )


def build_parser() -> argparse.ArgumentParser:
    """Define the command-line interface for the publisher."""
    parser = argparse.ArgumentParser(
        description="Validate and publish the everyday-things entry."
    )
    parser.add_argument(
        "--entry",
        type=Path,
        default=Path(__file__).with_name("entry.txt"),
        help="path to entry.txt (default: entry.txt beside main.py)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="where to write the published entry (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate the entry without writing anything",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=MAX_CHARS,
        help="tighter character limit to enforce locally (default: 400)",
    )
    parser.add_argument(
        "--no-craft-check",
        action="store_true",
        help="skip the analogy / honest-second-line craft check",
    )
    return parser


def main(argv=None) -> int:
    """Load, validate and publish the entry; 0 on success, 1 on failure."""
    args = build_parser().parse_args(argv)
    if args.max_chars < MIN_CHARS:
        print(f"error: --max-chars must be at least {MIN_CHARS}", file=sys.stderr)
        return 1
    try:
        data = load_entry(args.entry)
        text = validate_entry(data, max_chars=args.max_chars)
        if not args.no_craft_check:
            check_craft(text)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.check_only:
        print(f"valid: {len(text)} characters, two lines, UTF-8")
        return 0
    try:
        output = publish_entry(data, args.out)
    except OSError as exc:
        print(f"error: cannot write {args.out}: {exc}", file=sys.stderr)
        return 1
    print(report(text, output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
