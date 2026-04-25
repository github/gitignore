#!/usr/bin/env python3
"""Tests for the gitignore template validator."""

import os
import tempfile
import pytest

from validate_templates import (
    Issue,
    Severity,
    ValidationReport,
    analyze_coverage,
    check_trailing_whitespace,
    discover_templates,
    find_conflicts,
    find_duplicates,
    format_report,
    is_valid_glob_pattern,
    validate_template,
)


class TestIsValidGlobPattern:
    def test_simple_extension(self):
        assert is_valid_glob_pattern("*.py") is True

    def test_directory_pattern(self):
        assert is_valid_glob_pattern("build/") is True

    def test_negation(self):
        assert is_valid_glob_pattern("!important.txt") is True

    def test_double_star(self):
        assert is_valid_glob_pattern("**/logs") is True

    def test_bracket_pattern(self):
        assert is_valid_glob_pattern("*.[oa]") is True

    def test_unmatched_bracket(self):
        assert is_valid_glob_pattern("*.[o") is False

    def test_empty_after_strip(self):
        assert is_valid_glob_pattern("!") is False

    def test_rooted_pattern(self):
        assert is_valid_glob_pattern("/build") is True


class TestCheckTrailingWhitespace:
    def test_no_trailing(self):
        assert check_trailing_whitespace("*.py", 1) is None

    def test_with_trailing_space(self):
        issue = check_trailing_whitespace("*.py ", 5)
        assert issue is not None
        assert issue.severity == Severity.WARNING
        assert issue.line_number == 5

    def test_blank_line_ignored(self):
        assert check_trailing_whitespace("   ", 1) is None


class TestFindDuplicates:
    def test_no_duplicates(self):
        patterns = [(1, "*.py"), (2, "*.js"), (3, "build/")]
        assert find_duplicates(patterns) == []

    def test_exact_duplicate(self):
        patterns = [(1, "*.py"), (2, "*.js"), (3, "*.py")]
        issues = find_duplicates(patterns)
        assert len(issues) == 1
        assert issues[0].line_number == 3

    def test_trailing_slash_normalization(self):
        patterns = [(1, "build"), (2, "build/")]
        issues = find_duplicates(patterns)
        assert len(issues) == 1


class TestFindConflicts:
    def test_no_conflicts(self):
        patterns = [(1, "*.log"), (2, "*.tmp")]
        assert find_conflicts(patterns) == []

    def test_include_then_negate(self):
        patterns = [(1, "*.log"), (2, "!*.log")]
        issues = find_conflicts(patterns)
        assert len(issues) == 1
        assert issues[0].severity == Severity.WARNING

    def test_negate_without_include(self):
        patterns = [(1, "!important.txt")]
        issues = find_conflicts(patterns)
        assert len(issues) == 0


class TestAnalyzeCoverage:
    def test_many_wildcards(self):
        patterns = [(i, f"*.ext{i}") for i in range(12)]
        issues = analyze_coverage(patterns)
        msgs = [i.message for i in issues]
        assert any("wildcard" in m for m in msgs)

    def test_no_directory_patterns(self):
        patterns = [(i, f"*.ext{i}") for i in range(6)]
        issues = analyze_coverage(patterns)
        msgs = [i.message for i in issues]
        assert any("directory" in m.lower() for m in msgs)

    def test_duplicate_extension_suggestion(self):
        patterns = [(1, "*.py"), (2, "*.py")]
        issues = analyze_coverage(patterns)
        msgs = [i.message for i in issues]
        assert any(".py" in m for m in msgs)


class TestValidateTemplate:
    def test_valid_template(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".gitignore", delete=False
        ) as f:
            f.write("# Build output\nbuild/\n*.o\n*.a\n")
            f.flush()
            report = validate_template(f.name)
        os.unlink(f.name)
        assert report.error_count == 0
        assert report.pattern_count == 3
        assert report.comment_count == 1

    def test_invalid_pattern(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".gitignore", delete=False
        ) as f:
            f.write("*.[invalid\n")
            f.flush()
            report = validate_template(f.name)
        os.unlink(f.name)
        assert report.error_count > 0

    def test_file_not_found(self):
        report = validate_template("/nonexistent/file.gitignore")
        assert report.error_count > 0


class TestFormatReport:
    def test_clean_report(self):
        report = ValidationReport(
            template_file="test.gitignore",
            total_lines=5,
            pattern_count=3,
            comment_count=1,
            blank_count=1,
        )
        output = format_report(report)
        assert "No issues found" in output

    def test_report_with_issues(self):
        report = ValidationReport(
            template_file="test.gitignore",
            total_lines=5,
            pattern_count=3,
        )
        report.issues.append(
            Issue(
                severity=Severity.ERROR,
                line_number=2,
                line_content="*.[bad",
                message="Invalid glob pattern",
            )
        )
        output = format_report(report, verbose=True)
        assert "ERROR" in output
        assert "*.[bad" in output


class TestDiscoverTemplates:
    def test_discover_in_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create fake gitignore files
            for name in ["Python.gitignore", "Java.gitignore", "README.md"]:
                with open(os.path.join(tmpdir, name), "w") as f:
                    f.write("# test\n")
            templates = discover_templates(tmpdir)
            assert len(templates) == 2
            assert all(t.endswith(".gitignore") for t in templates)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
