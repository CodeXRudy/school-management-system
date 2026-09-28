"""Unit tests for the School Management System.

Run from the project root with:
    python -m unittest discover -s tests -v

Every test uses a temporary JSON file, so real data in School_data.json is never touched.
"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from school_mgmt import storage
from school_mgmt.menu import run_menu
from school_mgmt.persons import persons
from school_mgmt.student import Student
from school_mgmt.teacher import Teacher


class BaseTest(unittest.TestCase):
    """Points storage at a temp file and empties the in-memory data before each test."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.patcher = patch.object(storage, "database", self.tmp.name)
        self.patcher.start()
        storage.data["Students"].clear()
        storage.data["Teachers"].clear()

    def tearDown(self):
        self.patcher.stop()
        os.unlink(self.tmp.name)

    @staticmethod
    def run_with_input(func, answers):
        """Run func() feeding `answers` to input(); return everything it printed."""
        buf = io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(buf):
            func()
        return buf.getvalue()

    def saved_file(self):
        with open(self.tmp.name) as f:
            return json.load(f)


class TestEmailValidation(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(persons.validate_email("a@b.com"))

    def test_missing_at_symbol(self):
        self.assertFalse(persons.validate_email("ab.com"))

    def test_missing_dot(self):
        self.assertFalse(persons.validate_email("a@bcom"))

    def test_empty_string(self):
        self.assertFalse(persons.validate_email(""))


class TestAbstractBase(unittest.TestCase):
    def test_persons_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            persons()

    def test_roles(self):
        self.assertEqual(Student().get_roles(), "Student")
        self.assertEqual(Teacher().get_roles(), "Teacher")


class TestStudent(BaseTest):
    def register(self, roll="R1", email="a@x.com"):
        return self.run_with_input(Student().register, ["Asha", "16", email, roll])

    def test_register_success(self):
        out = self.register()
        self.assertIn("Student registered successfully.", out)
        self.assertEqual(len(storage.data["Students"]), 1)
        self.assertEqual(storage.data["Students"][0]["grades"], [])

    def test_register_persists_to_disk(self):
        self.register()
        self.assertEqual(self.saved_file()["Students"][0]["roll_number"], "R1")

    def test_register_invalid_email(self):
        out = self.register(email="bad-email")
        self.assertIn("Email is invalid.", out)
        self.assertEqual(storage.data["Students"], [])

    def test_register_duplicate_roll_number(self):
        self.register()
        out = self.register()
        self.assertIn("Roll number already exists.", out)
        self.assertEqual(len(storage.data["Students"]), 1)

    def test_register_non_numeric_age_raises(self):
        with self.assertRaises(ValueError):
            self.run_with_input(Student().register, ["Asha", "abc", "a@x.com", "R1"])

    def test_add_grade_success(self):
        self.register()
        out = self.run_with_input(Student().add_grades, ["R1", "Maths", "A"])
        self.assertIn("Grade added successfully.", out)
        self.assertEqual(storage.data["Students"][0]["grades"], [{"subject": "Maths", "grade": "A"}])
        self.assertEqual(self.saved_file()["Students"][0]["grades"][0]["grade"], "A")

    def test_add_multiple_grades(self):
        self.register()
        self.run_with_input(Student().add_grades, ["R1", "Maths", "A"])
        self.run_with_input(Student().add_grades, ["R1", "Physics", "B"])
        self.assertEqual(len(storage.data["Students"][0]["grades"]), 2)

    def test_add_grade_unknown_student(self):
        out = self.run_with_input(Student().add_grades, ["NOPE"])
        self.assertIn("Student not found.", out)

    def test_show_details(self):
        self.register()
        self.run_with_input(Student().add_grades, ["R1", "Maths", "A"])
        out = self.run_with_input(Student().show_details, ["R1"])
        for expected in ("Name: Asha", "Age: 16", "Email: a@x.com", "Roll Number: R1", "Maths: A"):
            self.assertIn(expected, out)


class TestTeacher(BaseTest):
    def register(self, emp="T1", email="t@x.com"):
        return self.run_with_input(Teacher().register, ["Ravi", "40", email, "Physics", emp])

    def test_register_success(self):
        out = self.register()
        self.assertIn("Teacher registered successfully.", out)
        self.assertEqual(storage.data["Teachers"][0]["subject"], "Physics")
        self.assertEqual(self.saved_file()["Teachers"][0]["emp_id"], "T1")

    def test_register_invalid_email(self):
        out = self.register(email="nope")
        self.assertIn("Email is invalid.", out)
        self.assertEqual(storage.data["Teachers"], [])

    def test_register_duplicate_emp_id(self):
        self.register()
        out = self.register()
        self.assertIn("Employee ID already exists.", out)
        self.assertEqual(len(storage.data["Teachers"]), 1)

    def test_show_details(self):
        self.register()
        out = self.run_with_input(Teacher().show_details, ["T1"])
        for expected in ("Name: Ravi", "Age: 40", "Email: t@x.com", "Subject: Physics", "Employee ID: T1"):
            self.assertIn(expected, out)


class TestMenu(BaseTest):
    def test_choice_1_registers_student(self):
        self.run_with_input(run_menu, ["1", "Asha", "16", "a@x.com", "R1"])
        self.assertEqual(len(storage.data["Students"]), 1)

    def test_choice_2_registers_teacher(self):
        self.run_with_input(run_menu, ["2", "Ravi", "40", "t@x.com", "Physics", "T1"])
        self.assertEqual(len(storage.data["Teachers"]), 1)

    def test_choice_3_adds_grade(self):
        self.run_with_input(run_menu, ["1", "Asha", "16", "a@x.com", "R1"])
        self.run_with_input(run_menu, ["3", "R1", "Maths", "A"])
        self.assertEqual(len(storage.data["Students"][0]["grades"]), 1)

    def test_choice_4_shows_student(self):
        self.run_with_input(run_menu, ["1", "Asha", "16", "a@x.com", "R1"])
        out = self.run_with_input(run_menu, ["4", "R1"])
        self.assertIn("Name: Asha", out)

    def test_choice_5_shows_teacher(self):
        self.run_with_input(run_menu, ["2", "Ravi", "40", "t@x.com", "Physics", "T1"])
        out = self.run_with_input(run_menu, ["5", "T1"])
        self.assertIn("Name: Ravi", out)

    def test_menu_lists_all_options(self):
        out = self.run_with_input(run_menu, ["9"])
        self.assertEqual(out.count("Press "), 5)


if __name__ == "__main__":
    unittest.main()
