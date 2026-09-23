"""Regression tests for ADSAT-17 — Validate CSV parsing capabilities.

All assertions are derived exclusively from the ADSAT-17 acceptance criteria:
  AC-1: parse_users returns all records; blank age → age=None
  AC-2: Valid integer ages parse to int
  AC-3: No unhandled ValueError or KeyError on malformed rows
"""
import csv
import os
import tempfile

import pytest

from csv_parser import parse_users


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_csv(rows: list[dict], fieldnames: list[str] = None) -> str:
    """Write *rows* to a temporary CSV file and return its path.

    The caller is responsible for deleting the file after use.
    """
    if fieldnames is None:
        fieldnames = ["name", "email", "age"]
    fd, path = tempfile.mkstemp(suffix=".csv", prefix="adsat17_")
    try:
        with os.fdopen(fd, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except Exception:
        os.unlink(path)
        raise
    return path


@pytest.fixture()
def three_row_csv_with_blank_age(tmp_path):
    """CSV matching the sample.csv described in ADSAT-17:
    Row 1 – Alice, age 30 (valid int)
    Row 2 – Bob,   age '' (blank)
    Row 3 – Carol, age 25 (valid int)
    """
    path = tmp_path / "sample.csv"
    path.write_text(
        "name,email,age\n"
        "Alice,alice@example.com,30\n"
        "Bob,bob@example.com,\n"
        "Carol,carol@example.com,25\n"
    )
    return str(path)


@pytest.fixture()
def all_valid_ages_csv(tmp_path):
    """CSV where every row has a well-formed integer age."""
    path = tmp_path / "valid_ages.csv"
    path.write_text(
        "name,email,age\n"
        "Alice,alice@example.com,30\n"
        "Carol,carol@example.com,25\n"
    )
    return str(path)


@pytest.fixture()
def non_numeric_age_csv(tmp_path):
    """CSV where one row has a non-numeric age string (e.g. 'N/A')."""
    path = tmp_path / "non_numeric.csv"
    path.write_text(
        "name,email,age\n"
        "Alice,alice@example.com,30\n"
        "Bob,bob@example.com,N/A\n"
        "Carol,carol@example.com,25\n"
    )
    return str(path)


@pytest.fixture()
def mixed_ages_csv(tmp_path):
    """CSV with a mix of valid integer ages and blank ages."""
    path = tmp_path / "mixed.csv"
    path.write_text(
        "name,email,age\n"
        "Alice,alice@example.com,30\n"
        "Bob,bob@example.com,\n"
        "Carol,carol@example.com,25\n"
        "Dave,dave@example.com,\n"
        "Eve,eve@example.com,40\n"
    )
    return str(path)


@pytest.fixture()
def alpha_age_middle_csv(tmp_path):
    """CSV where the middle row has age='abc' (non-numeric string)."""
    path = tmp_path / "alpha_middle.csv"
    path.write_text(
        "name,email,age\n"
        "Alice,alice@example.com,30\n"
        "Bob,bob@example.com,abc\n"
        "Carol,carol@example.com,25\n"
    )
    return str(path)


# ---------------------------------------------------------------------------
# Scenario 1 — Blank age field yields None and all records are returned (AC-1)
# ---------------------------------------------------------------------------

class TestBlankAgeYieldsNone:
    """AC-1: parse_users returns all 3 records; Bob's record has age=None."""

    def test_returns_all_three_records(self, three_row_csv_with_blank_age):
        """All rows must be present in the result — none silently dropped."""
        result = parse_users(three_row_csv_with_blank_age)
        assert len(result) == 3, (
            f"Expected 3 records but got {len(result)}. "
            "ADSAT-17 AC-1: all rows must be returned."
        )

    def test_blank_age_row_has_age_none(self, three_row_csv_with_blank_age):
        """Bob's row (blank age) must have age=None, not raise an exception."""
        result = parse_users(three_row_csv_with_blank_age)
        bob = next((r for r in result if r["name"] == "Bob"), None)
        assert bob is not None, "Bob's record was not found in the result."
        assert bob["age"] is None, (
            f"Expected bob['age'] to be None but got {bob['age']!r}. "
            "ADSAT-17 AC-1: blank age must become None."
        )

    def test_no_exception_raised_on_blank_age(self, three_row_csv_with_blank_age):
        """parse_users must not raise any exception when a blank age is present."""
        try:
            parse_users(three_row_csv_with_blank_age)
        except (ValueError, KeyError) as exc:
            pytest.fail(
                f"parse_users raised {type(exc).__name__} on blank age: {exc}. "
                "ADSAT-17 AC-3: no unhandled ValueError or KeyError."
            )


# ---------------------------------------------------------------------------
# Scenario 2 — Valid integer age parses to Python int (AC-2)
# ---------------------------------------------------------------------------

class TestValidAgesParsedAsInt:
    """AC-2: Valid integer ages still parse to int."""

    def test_valid_ages_are_int_instances(self, all_valid_ages_csv):
        """Every age in an all-valid CSV must be a Python int."""
        result = parse_users(all_valid_ages_csv)
        for record in result:
            assert isinstance(record["age"], int), (
                f"Expected age to be int for record {record['name']!r}, "
                f"got {type(record['age']).__name__!r}. "
                "ADSAT-17 AC-2: valid integer ages must parse to int."
            )

    def test_valid_ages_have_correct_values(self, all_valid_ages_csv):
        """Parsed integer values must match the CSV source values exactly."""
        result = parse_users(all_valid_ages_csv)
        by_name = {r["name"]: r for r in result}
        assert by_name["Alice"]["age"] == 30, (
            "ADSAT-17 AC-2: Alice's age must be 30."
        )
        assert by_name["Carol"]["age"] == 25, (
            "ADSAT-17 AC-2: Carol's age must be 25."
        )


# ---------------------------------------------------------------------------
# Scenario 3 — Non-numeric age string yields None without raising (AC-3)
# ---------------------------------------------------------------------------

class TestNonNumericAgeYieldsNone:
    """AC-3: No unhandled ValueError or KeyError on malformed rows."""

    def test_no_value_error_on_non_numeric_age(self, non_numeric_age_csv):
        """parse_users must not raise ValueError when age is a non-numeric string."""
        try:
            parse_users(non_numeric_age_csv)
        except ValueError as exc:
            pytest.fail(
                f"parse_users raised ValueError on non-numeric age: {exc}. "
                "ADSAT-17 AC-3: no unhandled ValueError."
            )

    def test_non_numeric_age_row_has_age_none(self, non_numeric_age_csv):
        """The row with a non-numeric age must have age=None in the result."""
        result = parse_users(non_numeric_age_csv)
        bob = next((r for r in result if r["name"] == "Bob"), None)
        assert bob is not None, "Bob's record was not found in the result."
        assert bob["age"] is None, (
            f"Expected bob['age'] to be None for non-numeric age, got {bob['age']!r}. "
            "ADSAT-17 AC-3."
        )

    def test_other_records_present_when_one_non_numeric(self, non_numeric_age_csv):
        """All records must still be returned even when one age is non-numeric."""
        result = parse_users(non_numeric_age_csv)
        assert len(result) == 3, (
            f"Expected 3 records but got {len(result)}. "
            "ADSAT-17 AC-3: malformed row must not suppress other rows."
        )


# ---------------------------------------------------------------------------
# Scenario 4 — Mixed valid and blank ages in the same file (AC-1 + AC-2)
# ---------------------------------------------------------------------------

class TestMixedAgeFields:
    """AC-1 + AC-2: All records returned; blank → None, valid → int."""

    def test_all_records_returned_in_mixed_file(self, mixed_ages_csv):
        """Total record count must equal the number of data rows in the CSV."""
        result = parse_users(mixed_ages_csv)
        assert len(result) == 5, (
            f"Expected 5 records but got {len(result)}. "
            "ADSAT-17 AC-1: all rows must be returned."
        )

    def test_valid_ages_are_int_in_mixed_file(self, mixed_ages_csv):
        """Records with a valid age must have an int age in a mixed file."""
        result = parse_users(mixed_ages_csv)
        by_name = {r["name"]: r for r in result}
        assert isinstance(by_name["Alice"]["age"], int), (
            "ADSAT-17 AC-2: Alice's age must be int in mixed file."
        )
        assert by_name["Alice"]["age"] == 30
        assert isinstance(by_name["Carol"]["age"], int), (
            "ADSAT-17 AC-2: Carol's age must be int in mixed file."
        )
        assert by_name["Carol"]["age"] == 25
        assert isinstance(by_name["Eve"]["age"], int), (
            "ADSAT-17 AC-2: Eve's age must be int in mixed file."
        )
        assert by_name["Eve"]["age"] == 40

    def test_blank_ages_are_none_in_mixed_file(self, mixed_ages_csv):
        """Records with a blank age must have age=None in a mixed file."""
        result = parse_users(mixed_ages_csv)
        by_name = {r["name"]: r for r in result}
        assert by_name["Bob"]["age"] is None, (
            "ADSAT-17 AC-1: Bob's age must be None in mixed file."
        )
        assert by_name["Dave"]["age"] is None, (
            "ADSAT-17 AC-1: Dave's age must be None in mixed file."
        )


# ---------------------------------------------------------------------------
# Scenario 5 — name and email fields are preserved correctly (AC-1)
# ---------------------------------------------------------------------------

class TestFieldPreservation:
    """AC-1: All 3 records are returned with correct field values."""

    def test_name_and_email_preserved_for_all_rows(self, three_row_csv_with_blank_age):
        """name and email must match the CSV source (stripped) for every record."""
        result = parse_users(three_row_csv_with_blank_age)
        expected = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob",   "email": "bob@example.com"},
            {"name": "Carol", "email": "carol@example.com"},
        ]
        for exp in expected:
            match = next(
                (r for r in result if r["name"] == exp["name"]), None
            )
            assert match is not None, (
                f"Record for {exp['name']!r} not found. "
                "ADSAT-17 AC-1: all records must be present."
            )
            assert match["email"] == exp["email"], (
                f"Email mismatch for {exp['name']!r}: "
                f"expected {exp['email']!r}, got {match['email']!r}. "
                "ADSAT-17 AC-1."
            )


# ---------------------------------------------------------------------------
# Scenario 6 — Non-numeric age does not suppress other rows (AC-3)
# ---------------------------------------------------------------------------

class TestNonNumericAgeDoesNotSuppressOtherRows:
    """AC-3: No unhandled ValueError or KeyError; all records returned."""

    def test_all_three_records_returned_with_alpha_age(self, alpha_age_middle_csv):
        """All 3 records must be present even when the middle row has age='abc'."""
        result = parse_users(alpha_age_middle_csv)
        assert len(result) == 3, (
            f"Expected 3 records but got {len(result)}. "
            "ADSAT-17 AC-3: non-numeric age must not suppress other rows."
        )

    def test_surrounding_rows_have_correct_int_ages(self, alpha_age_middle_csv):
        """Alice and Carol must still have correct int ages when Bob's is 'abc'."""
        result = parse_users(alpha_age_middle_csv)
        by_name = {r["name"]: r for r in result}
        assert by_name["Alice"]["age"] == 30, (
            "ADSAT-17 AC-3: Alice's age must be 30 even when another row is malformed."
        )
        assert isinstance(by_name["Alice"]["age"], int)
        assert by_name["Carol"]["age"] == 25, (
            "ADSAT-17 AC-3: Carol's age must be 25 even when another row is malformed."
        )
        assert isinstance(by_name["Carol"]["age"], int)

    def test_alpha_age_row_has_age_none(self, alpha_age_middle_csv):
        """The row with age='abc' must have age=None in the result."""
        result = parse_users(alpha_age_middle_csv)
        by_name = {r["name"]: r for r in result}
        assert by_name["Bob"]["age"] is None, (
            f"Expected Bob's age to be None for 'abc', got {by_name['Bob']['age']!r}. "
            "ADSAT-17 AC-3."
        )
