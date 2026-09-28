"""Command-line interface for the Student Performance Manager."""

from __future__ import annotations

from pathlib import Path

from .file_handler import export_json, load_students, save_students
from .student import Student
from .utils import (
    calculate_averages,
    filter_students,
    format_student_line,
    parse_mark,
    parse_positive_int,
    search_students,
    sort_students,
)

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "students.csv"
JSON_PATH = ROOT / "data" / "students.json"


def print_students(students: list[Student], heading: str = "STUDENTS") -> None:
    print(f"\n===== {heading} =====")
    if not students:
        print("No students found.")
        return
    for student in students:
        print(format_student_line(student))


def input_student(existing_ids: set[int] | None = None, current: Student | None = None) -> Student:
    """Prompt for a new or replacement Student, retrying invalid fields."""
    existing_ids = existing_ids or set()

    def ask(prompt: str, parser, current_value=None):
        while True:
            raw = input(f"{prompt}{f' [{current_value}]' if current_value is not None else ''}: ").strip()
            if not raw and current_value is not None:
                return current_value
            try:
                return parser(raw)
            except ValueError as error:
                print(f"Invalid input: {error}")

    student_id = ask("Student ID", lambda value: parse_positive_int(value, "Student ID"), current.id if current else None)
    if student_id in existing_ids and (current is None or student_id != current.id):
        raise ValueError("A student with that ID already exists")
    name = ask("Name", lambda value: value if value else (_ for _ in ()).throw(ValueError("Name cannot be blank")), current.name if current else None)
    age = ask("Age", lambda value: parse_positive_int(value, "Age"), current.age if current else None)
    python = ask("Python", lambda value: parse_mark(value, "Python"), current.python if current else None)
    sql = ask("SQL", lambda value: parse_mark(value, "SQL"), current.sql if current else None)
    math = ask("Math", lambda value: parse_mark(value, "Math"), current.math if current else None)
    return Student(student_id, name, age, python, sql, math)


def add_student(students: list[Student]) -> None:
    try:
        student = input_student({item.id for item in students})
        students.append(student)
        save_students(students, CSV_PATH)
        print("Student added successfully.")
    except ValueError as error:
        print(f"Could not add student: {error}")


def update_student(students: list[Student]) -> None:
    try:
        student_id = parse_positive_int(input("Enter the student ID to update: "), "Student ID")
    except ValueError as error:
        print(f"Invalid input: {error}")
        return
    student = next((item for item in students if item.id == student_id), None)
    if student is None:
        print("Student not found.")
        return
    try:
        replacement = input_student({item.id for item in students}, student)
        students[students.index(student)] = replacement
        save_students(students, CSV_PATH)
        print("Student updated successfully.")
    except ValueError as error:
        print(f"Could not update student: {error}")


def delete_student(students: list[Student]) -> None:
    try:
        student_id = parse_positive_int(input("Enter the student ID to delete: "), "Student ID")
    except ValueError as error:
        print(f"Invalid input: {error}")
        return
    for index, student in enumerate(students):
        if student.id == student_id:
            del students[index]
            save_students(students, CSV_PATH)
            print("Student deleted successfully.")
            return
    print("Student not found.")


def show_top_students(students: list[Student]) -> None:
    try:
        count = parse_positive_int(input("Show top how many students? (3/5/10): "), "Count")
        if count not in (3, 5, 10):
            raise ValueError("Please choose 3, 5, or 10")
    except ValueError as error:
        print(f"Invalid input: {error}")
        return
    averages = calculate_averages(students)
    ranked = sorted(zip(students, averages), key=lambda pair: pair[1], reverse=True)
    print_students([student for student, _ in ranked[:count]], "TOP STUDENTS")


def run() -> None:
    try:
        students = load_students(CSV_PATH)
    except ValueError as error:
        print(f"Could not load data: {error}")
        students = []

    actions = {
        "1": lambda: add_student(students),
        "2": lambda: print_students(students, "ALL STUDENTS"),
        "3": lambda: do_search(students),
        "4": lambda: do_report(students),
        "5": lambda: show_top_students(students),
        "6": lambda: do_filter(students),
        "7": lambda: update_student(students),
        "8": lambda: delete_student(students),
        "9": lambda: export_and_report(students),
    }
    while True:
        print("\n========================================")
        print("       STUDENT PERFORMANCE MANAGER")
        print("========================================")
        print("1. Add Student\n2. View All Students\n3. Search Student\n4. Calculate Student Performance")
        print("5. Show Top Students\n6. Filter Students\n7. Update Student\n8. Delete Student\n9. Export Report\n10. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "10":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Please choose a number from 1 to 10.")
        else:
            action()


def do_search(students: list[Student]) -> None:
    query = input("Search by student ID or name: ").strip()
    if not query:
        print("Search cannot be blank.")
        return
    print_students(search_students(students, query), "SEARCH RESULTS")


def choose_student(students: list[Student]) -> Student | None:
    try:
        student_id = parse_positive_int(input("Enter student ID: "), "Student ID")
    except ValueError as error:
        print(f"Invalid input: {error}")
        return None
    student = next((item for item in students if item.id == student_id), None)
    if student is None:
        print("Student not found.")
    return student


def do_report(students: list[Student]) -> None:
    student = choose_student(students)
    if student:
        print(f"\n{student.report()}")


def do_filter(students: list[Student]) -> None:
    print("1. Average > 80\n2. Average > 70\n3. Failed students\n4. Passed students")
    try:
        result = filter_students(students, input("Choose a filter: ").strip())
        print_students(result, "FILTER RESULTS")
    except ValueError as error:
        print(f"Invalid input: {error}")


def export_and_report(students: list[Student]) -> None:
    export_json(students, JSON_PATH)
    print(f"Exported {len(students)} student(s) to {JSON_PATH}")


if __name__ == "__main__":
    run()
