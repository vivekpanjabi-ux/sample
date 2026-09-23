# Regression Test Scenarios — csv_parser.py / parse_users

Source requirements: ENG-RUL-001 (rules.md), ENG-STD-001 (standards.docx)
Function under test: parse_users(path: str) -> list[dict]
Docstring contract: "Parse a CSV with name,email,age columns into a list of dicts."

---

## Scenario 1 — Happy path: well-formed CSV returns correct records

Requirement: ENG-STD-001 §4 — new features MUST ship with unit tests; ENG-RUL-001 §5 — changed lines MUST have >= 80% coverage.
Preconditions: A temporary CSV file exists with a header row name,email,age and two valid data rows.
Steps:
  1. Write a CSV file containing header name,email,age and rows Alice/alice@example.com/30 and Bob/bob@example.com/25.
  2. Call parse_users(path) with the file path.
Expected result: Returns [{"name": "Alice", "email": "alice@example.com", "age": 30}, {"name": "Bob", "email": "bob@example.com", "age": 25}]. The age field is an int, not a string.

---

## Scenario 2 — Whitespace stripping: leading/trailing spaces on name and email are removed

Requirement: ENG-RUL-001 §1 — docstring promises .strip() behaviour on name and email.
Preconditions: A temporary CSV file with padded values in name and email columns.
Steps:
  1. Write a CSV file with row "  Carol  ,  carol@example.com  ,22".
  2. Call parse_users(path).
Expected result: Returns [{"name": "Carol", "email": "carol@example.com", "age": 22}] — no leading or trailing whitespace on name or email.

---

## Scenario 3 — Empty file (header only): returns an empty list

Requirement: ENG-RUL-001 §3 — operations MUST handle missing data gracefully.
Preconditions: A temporary CSV file containing only the header row name,email,age and no data rows.
Steps:
  1. Write a CSV file containing only the header.
  2. Call parse_users(path).
Expected result: Returns [] (an empty list). No exception is raised.

---

## Scenario 4 — Single record: exactly one row is parsed correctly

Requirement: ENG-STD-001 §4 — boundary case for single-element collections.
Preconditions: A temporary CSV file with exactly one data row.
Steps:
  1. Write a CSV file with one row Dave/dave@example.com/40.
  2. Call parse_users(path).
Expected result: Returns a list of length 1 containing {"name": "Dave", "email": "dave@example.com", "age": 40}.

---

## Scenario 5 — Age is returned as integer, not string

Requirement: ENG-RUL-001 §1 — docstring contract; the function casts age via int().
Preconditions: A valid CSV file with a numeric age value.
Steps:
  1. Write a CSV file with one row where age is "28".
  2. Call parse_users(path) and inspect the type of result[0]["age"].
Expected result: type(result[0]["age"]) is int evaluates to True.

---

## Scenario 6 — Non-existent file raises an exception (not silently swallowed)

Requirement: ENG-RUL-001 §3 — "Exceptions MUST NOT be swallowed silently (except: pass is prohibited)".
Preconditions: The path passed to parse_users does not exist on the filesystem.
Steps:
  1. Call parse_users("/nonexistent/path/users.csv").
Expected result: A FileNotFoundError propagates to the caller. No silent swallowing occurs.

---

## Scenario 7 — Missing age column raises an exception (not silently swallowed)

Requirement: ENG-RUL-001 §3 — "Exceptions MUST NOT be swallowed silently".
Preconditions: A CSV file that is missing the age column entirely.
Steps:
  1. Write a CSV file with only name,email columns and one data row.
  2. Call parse_users(path).
Expected result: A KeyError propagates to the caller. The exception is not swallowed.

---

## Scenario 8 — Non-integer age value raises an exception (not silently swallowed)

Requirement: ENG-RUL-001 §3 — exceptions MUST NOT be swallowed; int() raises ValueError on non-numeric input.
Preconditions: A CSV file where the age field contains a non-numeric string.
Steps:
  1. Write a CSV file with one row where age is "not-a-number".
  2. Call parse_users(path).
Expected result: A ValueError propagates to the caller. The exception is not swallowed.

---

## Scenario 9 — Return value is a list of dicts (correct container type)

Requirement: ENG-STD-001 §2.3 — docstrings MUST describe return values accurately; docstring promises "a list of dicts".
Preconditions: A valid CSV file with at least one row.
Steps:
  1. Write a valid CSV file and call parse_users(path).
Expected result: The return value is an instance of list, and each element is an instance of dict.

---

## Scenario 10 — Each returned dict contains exactly the keys name, email, age

Requirement: ENG-STD-001 §2.3 — docstring column contract specifies the three columns.
Preconditions: A valid CSV file with one data row.
Steps:
  1. Write a valid CSV file and call parse_users(path).
  2. Inspect the keys of result[0].
Expected result: set(result[0].keys()) == {"name", "email", "age"}.

---

## Scenario 11 — Tests are independent: each test uses its own isolated temporary file

Requirement: ENG-RUL-001 §5 — "Tests MUST NOT depend on execution order or shared mutable state."
Preconditions: Each test creates its own tmp_path-scoped file via pytest fixtures.
Steps: Structural — verified by fixture design, not by a runtime assertion.
Expected result: No test shares a file handle or file path with another test.
