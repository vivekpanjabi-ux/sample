"""Regression tests for csv_parser.parse_users.

Requirements covered:
  - ENG-RUL-001 (rules.md): Section 1 Code Rules, Section 3 Error Handling Rules,
    Section 5 Testing Rules
  - ENG-STD-001 (standards.docx): Section 2.3 Documentation, Section 3 Security
    Standards, Section 4 Testing Standards

Each test is fully isolated via pytest's tmp_path fixture (ENG-RUL-001 Section 5:
"Tests MUST NOT depend on execution order or shared mutable state.").
"""

import pytest

from csv_parser import parse_users


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_csv(tmp_path, content, filename="users.csv"):
    """Write content to a fresh file inside tmp_path and return its string path."""
    p = tmp_path / filename
    p.write_text(content, encoding="utf-8")
    return str(p)


# ---------------------------------------------------------------------------
# Scenario 1 - Happy path: well-formed CSV returns correct records
# Requirement: ENG-STD-001 Section 4, ENG-RUL-001 Section 5
# ---------------------------------------------------------------------------

def test_parse_users_happy_path_multiple_rows(tmp_path):
    """Well-formed CSV with two rows returns a list of two correctly typed dicts."""
    csv_content = "name,email,age\nAlice,alice@example.com,30\nBob,bob@example.com,25\n"
    path = _write_csv(tmp_path, csv_content)

    result = parse_users(path)

    assert result == [
        {"name": "Alice", "email": "alice@example.com", "age": 30},
        {"name": "Bob", "email": "bob@example.com", "age": 25},
    ]


# ---------------------------------------------------------------------------
# Scenario 2 - Whitespace stripping on name and email
# Requirement: ENG-RUL-001 Section 1 (docstring contract: .strip() on name and email)
# ---------------------------------------------------------------------------

def test_parse_users_strips_whitespace_from_name_and_email(tmp_path):
    """Leading/trailing whitespace on name and email fields is stripped."""
    csv_content = "name,email,age\n  Carol  ,  carol@example.com  ,22\n"
    path = _write_csv(tmp_path, csv_content)

    result = parse_users(path)

    assert len(result) == 1
    assert result[0]["name"] == "Carol"
    assert result[0]["email"] == "carol@example.com"
    assert result[0]["age"] == 22


# ---------------------------------------------------------------------------
# Scenario 3 - Empty file (header only) returns an empty list
# Requirement: ENG-RUL-001 Section 3 (handle missing data gracefully)
# ---------------------------------------------------------------------------

def test_parse_users_header_only_returns_empty_list(tmp_path):
    """A CSV with only a header row and no data rows returns []."""
    csv_content = "name,email,age\n"
    path = _write_csv(tmp_path, csv_content)

    result = parse_users(path)

    assert result == []


# ---------------------------------------------------------------------------
# Scenario 4 - Single record is parsed correctly
# Requirement: ENG-STD-001 Section 4 (boundary case for single-element collections)
# ---------------------------------------------------------------------------

def test_parse_users_single_row(tmp_path):
    """A CSV with exactly one data row returns a list of length 1."""
    csv_content = "name,email,age\nDave,dave@example.com,40\n"
    path = _write_csv(tmp_path, csv_content)

    result = parse_users(path)

    assert len(result) == 1
    assert result[0] == {"name": "Dave", "email": "dave@example.com", "age": 40}


# ---------------------------------------------------------------------------
# Scenario 5 - Age field is returned as int, not str
# Requirement: ENG-RUL-001 Section 1 (docstring contract: int(row["age"]))
# ---------------------------------------------------------------------------

def test_parse_users_age_is_integer_type(tmp_path):
    """The age value in each returned dict is of type int."""
    csv_content = "name,email,age\nEve,eve@example.com,28\n"
    path = _write_csv(tmp_path, csv_content)

    result = parse_users(path)

    assert isinstance(result[0]["age"], int)


# ---------------------------------------------------------------------------
# Scenario 6 - Non-existent file raises FileNotFoundError (not swallowed)
# Requirement: ENG-RUL-001 Section 3 (exceptions MUST NOT be swallowed silently)
# ---------------------------------------------------------------------------

def test_parse_users_nonexistent_file_raises_file_not_found():
    """Passing a path that does not exist propagates FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parse_users("/nonexistent/path/that/does/not/exist/users.csv")


# ---------------------------------------------------------------------------
# Scenario 7 - Missing 'age' column raises KeyError (not swallowed)
# Requirement: ENG-RUL-001 Section 3 (exceptions MUST NOT be swallowed silently)
# ---------------------------------------------------------------------------

def test_parse_users_missing_age_column_raises_key_error(tmp_path):
    """A CSV missing the 'age' column propagates KeyError to the caller."""
    csv_content = "name,email\nFrank,frank@example.com\n"
    path = _write_csv(tmp_path, csv_content)

    with pytest.raises(KeyError):
        parse_users(path)


# ---------------------------------------------------------------------------
# Scenario 8 - Non-integer age value raises ValueError (not swallowed)
# Requirement: ENG-RUL-001 Section 3 (exceptions MUST NOT be swallowed silently)
# ---------------------------------------------------------------------------

def test_parse_users_non_integer_age_raises_value_error(tmp_path):
    """A non-numeric age field propagates ValueError from int() to the caller."""
    csv_content = "name,email,age\nGrace,grace@example.com,not-a-number\n"
    path = _write_csv(tmp_path, csv_content)

    with pytest.raises(ValueError):
        parse_users(path)


# ---------------------------------------------------------------------------
# Scenario 9 - Return value is a list of dicts
# Requirement: ENG-STD-001 Section 2.3 (docstring return-value accuracy)
# ---------------------------------------------------------------------------

def test_parse_users_returns_list_of_dicts(tmp_path):
    """parse_users always returns a list; every element is a dict."""
    csv_content = "name,email,age\nHank,hank@example.com,35\n"
    path = _write_csv(tmp_path, csv_content)

    result = parse_users(path)

    assert isinstance(result, list)
    for record in result:
        assert isinstance(record, dict)


# ---------------------------------------------------------------------------
# Scenario 10 - Each dict contains exactly the keys name, email, age
# Requirement: ENG-STD-001 Section 2.3 (docstring column contract)
# ---------------------------------------------------------------------------

def test_parse_users_dict_keys_are_name_email_age(tmp_path):
    """Each returned dict has exactly the keys 'name', 'email', and 'age'."""
    csv_content = "name,email,age\nIvy,ivy@example.com,27\n"
    path = _write_csv(tmp_path, csv_content)

    result = parse_users(path)

    assert len(result) == 1
    assert set(result[0].keys()) == {"name", "email", "age"}


# ---------------------------------------------------------------------------
# Scenario 11 - Test isolation: each test uses its own tmp_path (structural)
# Requirement: ENG-RUL-001 Section 5 ("Tests MUST NOT depend on execution order
#              or shared mutable state.")
# Verified by design: every test above receives a unique tmp_path fixture
# instance from pytest, so no file is shared between tests.
# ---------------------------------------------------------------------------
