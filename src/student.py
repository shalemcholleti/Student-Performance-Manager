"""Student domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Student:
    """Represent one student's identity, age, and subject marks."""

    id: int
    name: str
    age: int
    python: int
    sql: int
    math: int

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or isinstance(self.id, bool) or self.id <= 0:
            raise ValueError("Student ID must be a positive integer")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name cannot be blank")
        self.name = self.name.strip()
        if not isinstance(self.age, int) or isinstance(self.age, bool) or self.age <= 0:
            raise ValueError("Age must be a positive integer")
        for subject in ("python", "sql", "math"):
            mark = getattr(self, subject)
            if not isinstance(mark, int) or isinstance(mark, bool) or not 0 <= mark <= 100:
                raise ValueError(f"{subject.title()} mark must be an integer from 0 to 100")

    def average(self) -> float:
        """Return the mean of the three subject marks."""
        return round((self.python + self.sql + self.math) / 3, 2)

    def grade(self) -> str:
        """Return the letter grade for the student's average."""
        average = self.average()
        if average >= 90:
            return "A+"
        if average >= 80:
            return "A"
        if average >= 70:
            return "B"
        if average >= 60:
            return "C"
        if average >= 50:
            return "D"
        return "F"

    def status(self) -> str:
        """Return a friendly performance status."""
        average = self.average()
        if average >= 80:
            return "Excellent"
        if average >= 70:
            return "Good"
        if average >= 50:
            return "Needs Improvement"
        return "Failed"

    def strongest_subject(self) -> str:
        """Return the subject with the highest mark."""
        marks = {"Python": self.python, "SQL": self.sql, "Math": self.math}
        return max(marks, key=marks.get)

    def weakest_subject(self) -> str:
        """Return the subject with the lowest mark."""
        marks = {"Python": self.python, "SQL": self.sql, "Math": self.math}
        return min(marks, key=marks.get)

    def report(self) -> str:
        """Return a formatted full report for the student."""
        return (
            "===== STUDENT REPORT =====\n\n"
            f"ID       : {self.id}\n"
            f"Name     : {self.name}\n"
            f"Age      : {self.age}\n\n"
            f"Python   : {self.python}\n"
            f"SQL      : {self.sql}\n"
            f"Math     : {self.math}\n\n"
            f"Average  : {self.average():.2f}\n"
            f"Grade    : {self.grade()}\n"
            f"Status   : {self.status()}\n\n"
            f"Strongest Subject : {self.strongest_subject()}\n"
            f"Weakest Subject   : {self.weakest_subject()}"
        )

    def to_dict(self) -> dict[str, Any]:
        """Return the storage representation of this student."""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "python": self.python,
            "sql": self.sql,
            "math": self.math,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Student":
        """Build a Student from CSV/JSON-style values."""
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            age=int(data["age"]),
            python=int(data["python"]),
            sql=int(data["sql"]),
            math=int(data["math"]),
        )
