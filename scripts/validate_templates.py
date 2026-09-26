#!/usr/bin/env python3
"""
Gitignore Template Validator

Validates .gitignore template files for syntax correctness, duplicate patterns,
conflicting rules, and provides coverage analysis with detailed reporting.
"""

import argparse
import fnmatch
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    SUGGESTION = "SUGGESTION"


@dataclass
class Issue:
    severity: Severity
    line_number: int
    line_content: str
    message: str
    template_file: str = ""


@dataclass
class ValidationReport:
    template_file: str
    total_lines: int = 0
    pattern_count: int = 0
    comment_count: int = 0
    blank_count: int = 0
    issues: List[Issue] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)

    @property
    def suggestion_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.SUGGESTION)

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0


def is_valid_glob_pattern(pattern: str) -> bool:
    """Check if a pattern is a valid glob/gitignore pattern."""
    clean = pattern.lstrip("!")
    if clean.startswith("/"):
        clean = clean[1:]
    if clean.endswith("/"):
        clean = clean[:-1]
    if not clean:
        return False
    try:
        # Check for unmatched brackets
        bracket_depth = 0
        i = 0
        while i < len(clean):
            ch = clean[i]
            if ch == "\\" and i + 1 < len(clean):
                i += 2
                continue
            if ch == "[":
                bracket_depth += 1
            elif ch == "]":
                if bracket_depth > 0:
                    bracket_depth -= 1
                else:
                    return False
            i += 1
        if bracket_depth != 0:
            return False
        # Test compile the pattern via fnmatch
        fnmatch.translate(clean)
        return True
    except Exception:
        return False


def check_trailing_whitespace(line: str, line_number: int) -> Optional[Issue]:
    """Detect trailing whitespace on a line."""
    if line != line.rstrip() and line.strip():
        return Issue(
            severity=Severity.WARNING,
            line_number=line_number,
            line_content=line,
            message="Line has trailing whitespace",
        )
    return None


def find_duplicates(patterns: List[tuple]) -> List[Issue]:
    """Find duplicate patterns in the list."""
    issues = []
    seen = {}
    for line_num, pattern in patterns:
        normalized = pattern.strip().rstrip("/")
        if normalized in seen:
            issues.append(
                Issue(
                    severity=Severity.WARNING,
                    line_number=line_num,
                    line_content=pattern,
                    message=f"Duplicate pattern (first seen at line {seen[normalized]})",
                )
            )
        else:
            seen[normalized] = line_num
    return issues


def find_conflicts(patterns: List[tuple]) -> List[Issue]:
    """Find conflicting include/exclude rules for the same pattern."""
    issues = []
    include_patterns = {}
    exclude_patterns = {}

    for line_num, pattern in patterns:
        stripped = pattern.strip()
        if stripped.startswith("!"):
            base = stripped[1:].strip().rstrip("/")
            exclude_patterns[base] = line_num
            if base in include_patterns:
                issues.append(
                    Issue(
                        severity=Severity.WARNING,
                        line_number=line_num,
                        line_content=stripped,
                        message=(
                            f"Negation pattern conflicts with include at line "
                            f"{include_patterns[base]}. Order matters in gitignore."
                        ),
                    )
                )
        else:
            base = stripped.rstrip("/")
            include_patterns[base] = line_num

    return issues


def analyze_coverage(patterns: List[tuple]) -> List[Issue]:
    """Analyze pattern coverage and suggest improvements."""
    issues = []
    wildcard_count = 0
    extension_patterns = []
    directory_patterns = []

    for line_num, pattern in patterns:
        stripped = pattern.strip().lstrip("!")
        if stripped.startswith("*"):
            wildcard_count += 1
        if re.match(r"^\*\.[a-zA-Z0-9]+$", stripped):
            extension_patterns.append((line_num, stripped))
        if stripped.endswith("/"):
            directory_patterns.append((line_num, stripped))

    if wildcard_count > 10:
        issues.append(
            Issue(
                severity=Severity.SUGGESTION,
                line_number=0,
                line_content="",
                message=(
                    f"Template has {wildcard_count} wildcard patterns. "
                    "Consider grouping related patterns with comments."
                ),
            )
        )

    ext_groups = {}
    for line_num, pat in extension_patterns:
        ext = pat.split(".")[-1].lower()
        ext_groups.setdefault(ext, []).append(line_num)

    for ext, lines in ext_groups.items():
        if len(lines) > 1:
            issues.append(
                Issue(
                    severity=Severity.SUGGESTION,
                    line_number=lines[1],
                    line_content="",
                    message=(
                        f"Multiple patterns target .{ext} files "
                        f"(lines {', '.join(map(str, lines))}). Consider consolidating."
                    ),
                )
            )

    if not directory_patterns and len(patterns) > 5:
        issues.append(
            Issue(
                severity=Severity.SUGGESTION,
                line_number=0,
                line_content="",
                message=(
                    "No directory-specific patterns found. "
                    "Consider adding directory ignores (e.g., build/)."
                ),
            )
        )

    return issues


def validate_template(filepath: str) -> ValidationReport:
    """Validate a single gitignore template file."""
    report = ValidationReport(template_file=filepath)

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError as e:
        report.issues.append(
            Issue(
                severity=Severity.ERROR,
                line_number=0,
                line_content="",
                message=f"Cannot read file: {e}",
                template_file=filepath,
            )
        )
        return report

    report.total_lines = len(lines)
    patterns = []

    for i, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\n\r")

        # Check trailing whitespace
        ws_issue = check_trailing_whitespace(line, i)
        if ws_issue:
            ws_issue.template_file = filepath
            report.issues.append(ws_issue)

        stripped = line.strip()

        # Blank line
        if not stripped:
            report.blank_count += 1
            continue

        # Comment
        if stripped.startswith("#"):
            report.comment_count += 1
            continue

        # Pattern line
        report.pattern_count += 1
        patterns.append((i, stripped))

        # Validate glob syntax
        if not is_valid_glob_pattern(stripped):
            report.issues.append(
                Issue(
                    severity=Severity.ERROR,
                    line_number=i,
                    line_content=stripped,
                    message="Invalid glob pattern syntax",
                    template_file=filepath,
                )
            )

        # Check for spaces in patterns (usually a mistake)
        if " " in stripped and not stripped.startswith("\\"):
            report.issues.append(
                Issue(
                    severity=Severity.WARNING,
                    line_number=i,
                    line_content=stripped,
                    message="Pattern contains spaces — this may be unintentional",
                    template_file=filepath,
                )
            )

    # Run duplicate detection
    dup_issues = find_duplicates(patterns)
    for issue in dup_issues:
        issue.template_file = filepath
    report.issues.extend(dup_issues)

    # Run conflict detection
    conflict_issues = find_conflicts(patterns)
    for issue in conflict_issues:
        issue.template_file = filepath
    report.issues.extend(conflict_issues)

    # Run coverage analysis
    coverage_issues = analyze_coverage(patterns)
    for issue in coverage_issues:
        issue.template_file = filepath
    report.issues.extend(coverage_issues)

    return report


def format_report(report: ValidationReport, verbose: bool = False) -> str:
    """Format a validation report as human-readable text."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"File: {report.template_file}")
    lines.append(f"{'='*60}")
    lines.append(
        f"  Lines: {report.total_lines}  |  Patterns: {report.pattern_count}  "
        f"|  Comments: {report.comment_count}  |  Blank: {report.blank_count}"
    )
    lines.append(
        f"  Errors: {report.error_count}  |  Warnings: {report.warning_count}  "
        f"|  Suggestions: {report.suggestion_count}"
    )

    if report.issues:
        lines.append("")
        for issue in sorted(report.issues, key=lambda x: (x.severity.value, x.line_number)):
            prefix = f"  [{issue.severity.value}]"
            loc = f" Line {issue.line_number}:" if issue.line_number > 0 else ""
            lines.append(f"{prefix}{loc} {issue.message}")
            if verbose and issue.line_content:
                lines.append(f"         > {issue.line_content}")
    else:
        lines.append("  No issues found. ✓")

    return "\n".join(lines)


def discover_templates(repo_root: str) -> List[str]:
    """Discover all .gitignore template files in the repository."""
    templates = []
    for entry in os.listdir(repo_root):
        full_path = os.path.join(repo_root, entry)
        if os.path.isfile(full_path) and entry.endswith(".gitignore"):
            templates.append(full_path)
    # Also check Global/ and community/ subdirectories
    for subdir in ["Global", "community"]:
        subdir_path = os.path.join(repo_root, subdir)
        if os.path.isdir(subdir_path):
            for entry in os.listdir(subdir_path):
                full_path = os.path.join(subdir_path, entry)
                if os.path.isfile(full_path) and entry.endswith(".gitignore"):
                    templates.append(full_path)
    return sorted(templates)


def main():
    parser = argparse.ArgumentParser(
        description="Validate .gitignore template files for common issues."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Template files to validate. If none given, validates all in repo.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Root directory of the gitignore repo (default: current directory).",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show pattern content alongside issues.",
    )
    parser.add_argument(
        "--errors-only",
        action="store_true",
        help="Only report errors, not warnings or suggestions.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print only a summary, not per-file details.",
    )

    args = parser.parse_args()

    if args.files:
        templates = args.files
    else:
        templates = discover_templates(args.repo_root)

    if not templates:
        print("No .gitignore templates found.")
        sys.exit(0)

    reports = []
    for tpl in templates:
        report = validate_template(tpl)
        reports.append(report)

    total_errors = 0
    total_warnings = 0
    total_suggestions = 0

    for report in reports:
        if args.errors_only:
            report.issues = [i for i in report.issues if i.severity == Severity.ERROR]
        if not args.summary:
            print(format_report(report, verbose=args.verbose))
        total_errors += report.error_count
        total_warnings += report.warning_count
        total_suggestions += report.suggestion_count

    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(reports)} templates validated")
    print(f"  Total errors:      {total_errors}")
    print(f"  Total warnings:    {total_warnings}")
    print(f"  Total suggestions: {total_suggestions}")
    print(f"{'='*60}")

    if total_errors > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
