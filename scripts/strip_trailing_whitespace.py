#!/usr/bin/env python3
"""
Strip trailing whitespace from .gitignore template files.

This script fixes trailing whitespace issues in gitignore templates,
which can cause unexpected behavior in pattern matching.
"""

import argparse
import os
import sys


def strip_file(filepath: str, dry_run: bool = False) -> int:
    """Strip trailing whitespace from a file. Returns number of lines fixed."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    fixed_count = 0
    new_lines = []
    for line in lines:
        stripped = line.rstrip() + "\n"
        if stripped != line:
            fixed_count += 1
        new_lines.append(stripped)

    # Ensure file ends with a single newline
    if new_lines and new_lines[-1] == "\n":
        pass  # already ends properly
    elif not new_lines:
        new_lines = ["\n"]

    if fixed_count > 0 and not dry_run:
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.writelines(new_lines)

    return fixed_count


def main():
    parser = argparse.ArgumentParser(
        description="Strip trailing whitespace from .gitignore templates."
    )
    parser.add_argument("files", nargs="*", help="Files to process.")
    parser.add_argument("--repo-root", default=".", help="Repo root directory.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Report but do not modify files."
    )
    args = parser.parse_args()

    if args.files:
        targets = args.files
    else:
        targets = []
        for entry in os.listdir(args.repo_root):
            full = os.path.join(args.repo_root, entry)
            if os.path.isfile(full) and entry.endswith(".gitignore"):
                targets.append(full)

    total_fixed = 0
    for filepath in targets:
        count = strip_file(filepath, dry_run=args.dry_run)
        if count > 0:
            action = "would fix" if args.dry_run else "fixed"
            print(f"  {action} {count} line(s) in {filepath}")
            total_fixed += count

    if total_fixed == 0:
        print("No trailing whitespace found.")
    else:
        action = "Would fix" if args.dry_run else "Fixed"
        print(f"\n{action} {total_fixed} line(s) total.")

    sys.exit(0)


if __name__ == "__main__":
    main()
