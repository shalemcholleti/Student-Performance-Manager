"""File persistence for student records."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .student import Student

FIELDS = ["id", "name", "age", "python", "sql", "math"]


def load_students(csv_path: Path) -> list[Student]:
    """Load students from CSV; return an empty list when the file is absent."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return []
    students: list[Student] = []
    with csv_path.open("r", newline="", encoding="utf-8") as file:
        for row_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                students.append(Student.from_dict(row))
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"Invalid student record on CSV row {row_number}: {error}") from error
    return students


def save_students(students: list[Student], csv_path: Path) -> None:
    """Write all students to CSV."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(student.to_dict() for student in students)


def export_json(students: list[Student], json_path: Path) -> None:
    """Export all students to a readable JSON array."""
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as file:
        json.dump([student.to_dict() for student in students], file, indent=2)
        file.write("\n")
