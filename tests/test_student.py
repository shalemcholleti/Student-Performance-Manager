import json
import tempfile
import unittest
from pathlib import Path

from src.file_handler import export_json, load_students, save_students
from src.student import Student
from src.utils import filter_students, parse_mark, search_students, sort_students


class StudentTests(unittest.TestCase):
    def setUp(self):
        self.rahul = Student(101, "Rahul", 21, 85, 78, 72)
        self.ananya = Student(102, "Ananya", 20, 92, 88, 95)
        self.failed = Student(103, "Kiran", 22, 30, 40, 45)
        self.students = [self.rahul, self.ananya, self.failed]

    def test_student_creation(self):
        self.assertEqual(self.rahul.to_dict()["name"], "Rahul")
        self.assertEqual(self.rahul.age, 21)

    def test_average_calculation(self):
        self.assertEqual(self.rahul.average(), 78.33)

    def test_grade_calculation(self):
        self.assertEqual(self.rahul.grade(), "B")
        self.assertEqual(self.ananya.grade(), "A+")
        self.assertEqual(self.failed.grade(), "F")

    def test_status_and_subject_extremes(self):
        self.assertEqual(self.rahul.status(), "Good")
        self.assertEqual(self.rahul.strongest_subject(), "Python")
        self.assertEqual(self.rahul.weakest_subject(), "Math")

    def test_invalid_marks_are_rejected(self):
        with self.assertRaises(ValueError):
            Student(1, "Bad", 20, -1, 50, 50)
        with self.assertRaises(ValueError):
            Student(1, "Bad", 20, 101, 50, 50)
        with self.assertRaises(ValueError):
            parse_mark("abc", "Python")

    def test_invalid_student_fields_are_rejected(self):
        with self.assertRaises(ValueError):
            Student(0, "Bad", 20, 50, 50, 50)
        with self.assertRaises(ValueError):
            Student(1, "", 20, 50, 50, 50)
        with self.assertRaises(ValueError):
            Student(1, "Bad", -4, 50, 50, 50)

    def test_case_insensitive_search_by_name_and_id(self):
        self.assertEqual(search_students(self.students, "rahul"), [self.rahul])
        self.assertEqual(search_students(self.students, "101"), [self.rahul])
        self.assertEqual(search_students(self.students, ""), [])

    def test_filters(self):
        self.assertEqual(filter_students(self.students, "1"), [self.ananya])
        self.assertEqual(filter_students(self.students, "3"), [self.failed])
        self.assertEqual(filter_students(self.students, "4"), [self.rahul, self.ananya])

    def test_sorting(self):
        self.assertEqual([s.name for s in sort_students(self.students, "1")], ["Ananya", "Kiran", "Rahul"])
        self.assertEqual([s.name for s in sort_students(self.students, "2")], ["Ananya", "Rahul", "Kiran"])
        self.assertEqual([s.name for s in sort_students(self.students, "3")], ["Ananya", "Rahul", "Kiran"])

    def test_report_contains_calculated_fields(self):
        report = self.rahul.report()
        self.assertIn("Average  : 78.33", report)
        self.assertIn("Grade    : B", report)
        self.assertIn("Strongest Subject : Python", report)

    def test_csv_and_json_persistence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            csv_path = root / "students.csv"
            json_path = root / "students.json"
            save_students(self.students, csv_path)
            loaded = load_students(csv_path)
            self.assertEqual([s.to_dict() for s in loaded], [s.to_dict() for s in self.students])
            export_json(loaded, json_path)
            self.assertEqual(json.loads(json_path.read_text()), [s.to_dict() for s in self.students])


if __name__ == "__main__":
    unittest.main()
