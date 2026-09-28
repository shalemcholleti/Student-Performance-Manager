"""Reusable helpers for the Student Performance Manager."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Callable

from .student import Student


def parse_int(value: str, field_name: str) -> int:
    """Parse an integer input and raise a useful validation error."""
    try:
        return int(value.strip())
    except (AttributeError, ValueError):
        raise ValueError(f"{field_name} must be a whole number") from None


def parse_positive_int(value: str, field_name: str) -> int:
    number = parse_int(value, field_name)
    if number <= 0:
        raise ValueError(f"{field_name} must be greater than zero")
    return number


def parse_mark(value: str, subject: str) -> int:
    mark = parse_int(value, subject)
    if not 0 <= mark <= 100:
        raise ValueError(f"{subject} mark must be between 0 and 100")
    return mark


def calculate_averages(students: Iterable[Student]) -> list[float]:
    """Transform each student into their average using ``map()``."""
    return list(map(Student.average, students))


def search_students(students: Iterable[Student], query: str) -> list[Student]:
    """Find students by exact ID or case-insensitive name substring."""
    query = query.strip()
    if not query:
        return []
    lowered = query.casefold()
    return [
        student
        for student in students
        if str(student.id) == query or lowered in student.name.casefold()
    ]


def filter_students(students: Iterable[Student], option: str) -> list[Student]:
    """Filter students using the menu's supported criteria."""
    predicates: dict[str, Callable[[Student], bool]] = {
        "1": lambda student: student.average() > 80,
        "2": lambda student: student.average() > 70,
        "3": lambda student: student.grade() == "F",
        "4": lambda student: student.grade() != "F",
    }
    if option not in predicates:
        raise ValueError("Unknown filter option")
    return list(filter(predicates[option], students))


def sort_students(students: Iterable[Student], option: str) -> list[Student]:
    """Sort students by a menu-supported field."""
    keys: dict[str, Callable[[Student], object]] = {
        "1": lambda student: student.name.casefold(),
        "2": lambda student: student.average(),
        "3": lambda student: student.python,
        "4": lambda student: student.sql,
        "5": lambda student: student.math,
    }
    if option not in keys:
        raise ValueError("Unknown sort option")
    return sorted(students, key=keys[option], reverse=option != "1")


def format_student_line(student: Student) -> str:
    return (
        f"{student.id} | {student.name} | {student.age} | "
        f"{student.python} | {student.sql} | {student.math} | "
        f"Avg: {student.average():.2f} | Grade: {student.grade()}"
    )
