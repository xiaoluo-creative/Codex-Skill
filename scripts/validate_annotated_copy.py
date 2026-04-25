#!/usr/bin/env python3
"""Validate a CodeExplanation annotated copy.

The validator checks that each non-empty source line is preserved in the
annotated copy with two explanation lines immediately above it.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


DEFAULT_EXTENSIONS = [".c"]


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def parse_extensions(raw: str) -> set[str]:
    result: set[str] = set()
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        result.add(item if item.startswith(".") else f".{item}")
    return result or set(DEFAULT_EXTENSIONS)


def validate_file(
    src_path: Path,
    dst_path: Path,
    comment_marker: str,
    normal_prefix: str,
    translation_prefix: str,
    logic_prefix: str,
) -> list[str]:
    errors: list[str] = []
    src_lines = read_lines(src_path)
    dst_lines = read_lines(dst_path)
    j = 0

    first_prefixes = (
        f"{comment_marker} {normal_prefix}",
        f"{comment_marker}{normal_prefix}",
        f"{comment_marker} {translation_prefix}",
        f"{comment_marker}{translation_prefix}",
    )
    second_prefixes = (
        f"{comment_marker} {logic_prefix}",
        f"{comment_marker}{logic_prefix}",
    )

    for i, src_line in enumerate(src_lines, start=1):
        if not src_line.strip():
            if j >= len(dst_lines) or dst_lines[j] != src_line:
                errors.append(f"{src_path.name}:{i}: blank line not preserved")
            else:
                j += 1
            continue

        if j + 2 >= len(dst_lines):
            errors.append(f"{src_path.name}:{i}: missing annotation block")
            break

        if not dst_lines[j].startswith(first_prefixes):
            errors.append(
                f"{src_path.name}:{i}: first annotation must start with "
                f"{normal_prefix} or {translation_prefix}"
            )
        if not dst_lines[j + 1].startswith(second_prefixes):
            errors.append(
                f"{src_path.name}:{i}: second annotation must start with {logic_prefix}"
            )
        if dst_lines[j + 2] != src_line:
            errors.append(f"{src_path.name}:{i}: original line text changed")
        j += 3

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Original source folder")
    parser.add_argument("annotated", type=Path, help="Annotated copy folder")
    parser.add_argument(
        "--extensions",
        default=",".join(DEFAULT_EXTENSIONS),
        help="Comma-separated file extensions to validate, default: .c",
    )
    parser.add_argument("--comment-marker", default="//")
    parser.add_argument("--normal-prefix", default="注释：")
    parser.add_argument("--translation-prefix", default="原注释翻译：")
    parser.add_argument("--logic-prefix", default="逻辑：")
    args = parser.parse_args()

    source = args.source.resolve()
    annotated = args.annotated.resolve()
    extensions = parse_extensions(args.extensions)

    if not source.is_dir():
        print(f"Source folder not found: {source}", file=sys.stderr)
        return 2
    if not annotated.is_dir():
        print(f"Annotated folder not found: {annotated}", file=sys.stderr)
        return 2

    errors: list[str] = []
    checked = 0
    for src_path in sorted(source.rglob("*")):
        if not src_path.is_file() or src_path.suffix not in extensions:
            continue
        rel = src_path.relative_to(source)
        dst_path = annotated / rel
        if not dst_path.is_file():
            errors.append(f"{rel}: missing annotated file")
            continue
        checked += 1
        errors.extend(
            f"{rel}: {message}"
            for message in validate_file(
                src_path,
                dst_path,
                args.comment_marker,
                args.normal_prefix,
                args.translation_prefix,
                args.logic_prefix,
            )
        )

    if errors:
        print("Validation failed:")
        for error in errors[:100]:
            print(f"- {error}")
        if len(errors) > 100:
            print(f"- ... {len(errors) - 100} more errors")
        return 1

    print(f"OK: validated {checked} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
