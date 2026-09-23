# Repository Rules

**Document ID:** ENG-RUL-001
**Version:** 1.0
**Effective Date:** 2026-09-01
**Applies To:** All contributors and automated agents working in this repository.

These rules are mandatory. Violations block merge. Exceptions require a written
waiver approved by the Engineering Lead.

## 1. Code Rules

- Functions MUST do one thing; cyclomatic complexity MUST NOT exceed 15.
- Python code MUST use `snake_case` for functions/variables, `PascalCase` for
  classes, `UPPER_SNAKE_CASE` for constants.
- Mutable default arguments (e.g. `def f(items=[])`) are PROHIBITED. Use
  `None` and initialize inside the function body.
- Division operations MUST guard against a zero denominator.
- NEVER mutate a dict or list while iterating over it.
- NEVER mutate caller-owned arguments unless the function name and docstring
  explicitly say so (e.g. `sort_in_place`).
- Boundary checks MUST use correct boolean logic — validate ranges with `or`,
  not `and`, when rejecting out-of-range values.
- Loops over collections MUST NOT index past `len(collection) - 1`.

## 2. Security Rules

- Secrets, tokens, API keys, and credentials MUST NEVER be committed. Inject
  them via environment variables or a managed secrets store.
- All external input MUST be validated at trust boundaries before use.
- `eval`, `exec`, and `pickle.loads` on untrusted data are PROHIBITED.
- Dependencies MUST pass vulnerability scanning in CI; critical findings fail
  the build.

## 3. Error Handling Rules

- Lookup/delete operations MUST handle missing keys gracefully — return
  `None`/default or raise a documented, domain-specific exception.
- Exceptions MUST NOT be swallowed silently (`except: pass` is prohibited).
- Error messages MUST be actionable and MUST NOT contain secrets or PII.

## 4. Cache and State Rules

- TTL checks MUST return fresh entries and reject expired ones — verify
  comparison direction carefully.
- Time-based logic MUST be unit-testable (inject clock or use a time
  abstraction where feasible).

## 5. Testing Rules

- New features MUST include unit tests; changed lines MUST have >= 80%
  coverage.
- Bug fixes MUST include a regression test that fails without the fix.
- Tests MUST NOT depend on execution order or shared mutable state.

## 6. Version Control Rules

- Direct commits to `main` are PROHIBITED. All changes go through pull
  requests with green CI and at least one approval.
- Commit messages MUST follow conventional commits: `feat:`, `fix:`,
  `chore:`, `docs:`, `refactor:`, `test:`.
- Generated artifacts (`__pycache__`, `*.pyc`, build output) MUST NOT be
  committed.

## 7. Documentation Rules

- Public modules, classes, and functions MUST have docstrings covering
  purpose, parameters, return values, and raised exceptions.
- Comments MUST explain *why*, not *what*.
- A docstring that promises behavior the code does not implement is a defect
  and MUST be fixed before merge.
