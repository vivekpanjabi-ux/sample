"""Utilities for parsing CSV exports into records."""
import csv


def parse_users(path):
    """Parse a CSV with name,email,age columns into a list of dicts."""
    records = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            records.append(
                {
                    "name": row["name"].strip(),
                    "email": row["email"].strip(),
                    "age": int(row["age"]),
                }
            )
    return records
