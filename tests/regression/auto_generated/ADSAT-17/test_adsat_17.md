# Regression Scenarios — ADSAT-17
## Validate CSV Parsing Capabilities (`parse_users`)

**Ticket:** ADSAT-17  
**Component:** `csv_parser.py` → `parse_users(path)`  
**Source of truth:** ADSAT-17 acceptance criteria

---

## Scenario 1 — Blank `age` field yields `None` and all records are returned (AC-1)

**Requirement:** `parse_users('sample.csv')` returns all 3 records; Bob's record has `age=None`.

**Preconditions:**
- A temporary CSV file is created with 3 rows:
  - Row 1: Alice, alice@example.com, 30
  - Row 2: Bob, bob@example.com, *(blank age)*
  - Row 3: Carol, carol@example.com, 25

**Steps:**
1. Call `parse_users(<path to temp CSV>)`.
2. Inspect the returned list.

**Expected result:**
- The returned list contains exactly **3** records.
- The record for Bob has `age` equal to `None`.
- The function does **not** raise any exception.

---

## Scenario 2 — Valid integer `age` parses to Python `int` (AC-2)

**Requirement:** Valid integer ages still parse to `int`.

**Preconditions:**
- A temporary CSV file is created with rows that all have well-formed numeric ages (e.g., 30, 25).

**Steps:**
1. Call `parse_users(<path to temp CSV>)`.
2. Inspect the `age` field of each returned record.

**Expected result:**
- Every `age` value in the returned list is an instance of Python `int`.
- The numeric values match the values in the CSV exactly.

---

## Scenario 3 — Non-numeric `age` string yields `None` without raising (AC-3)

**Requirement:** No unhandled `ValueError` or `KeyError` on malformed rows.

**Preconditions:**
- A temporary CSV file is created with a row whose `age` column contains a non-numeric string (e.g., `"N/A"`).

**Steps:**
1. Call `parse_users(<path to temp CSV>)`.
2. Inspect the returned list.

**Expected result:**
- The function does **not** raise `ValueError`.
- The record with the non-numeric age has `age` equal to `None`.
- All other records are still present in the result.

---

## Scenario 4 — Mixed valid and blank `age` fields in the same file (AC-1 + AC-2)

**Requirement:** All records are returned; blank ages become `None`; valid ages become `int`.

**Preconditions:**
- A temporary CSV file is created with multiple rows, some with valid integer ages and some with blank ages.

**Steps:**
1. Call `parse_users(<path to temp CSV>)`.
2. Inspect the `age` field of each returned record.

**Expected result:**
- The total number of returned records equals the total number of rows in the CSV.
- Records with a valid integer age have `age` as a Python `int` with the correct value.
- Records with a blank age have `age` equal to `None`.

---

## Scenario 5 — `name` and `email` fields are preserved correctly for all rows (AC-1)

**Requirement:** `parse_users` returns all 3 records with correct field values.

**Preconditions:**
- A temporary CSV file is created with 3 rows including one with a blank age.

**Steps:**
1. Call `parse_users(<path to temp CSV>)`.
2. Inspect the `name` and `email` fields of each returned record.

**Expected result:**
- Each record's `name` and `email` match the corresponding CSV row values (stripped of surrounding whitespace).

---

## Scenario 6 — Row with non-numeric `age` does not suppress other rows (AC-3)

**Requirement:** No unhandled `ValueError` or `KeyError` on malformed rows; all records are returned.

**Preconditions:**
- A temporary CSV file is created with 3 rows where the middle row has `age = "abc"`.

**Steps:**
1. Call `parse_users(<path to temp CSV>)`.
2. Inspect the length and contents of the returned list.

**Expected result:**
- The returned list has exactly 3 records.
- The first and third records have their correct integer `age` values.
- The second record has `age=None`.
