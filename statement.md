# Project Statement

## Problem Statement

Small schools and coaching centres often keep student, teacher and grade records on paper or in loosely organised files. This makes it slow to find a record, easy to create duplicate or inconsistent entries (the same roll number used twice, mistyped emails), and risky because nothing is stored in a single reliable place.

There is a need for a simple, lightweight system that records people and their grades in a structured way, rejects obviously bad or duplicate data at the point of entry, and keeps everything saved permanently so it is available the next time the system is used.

## Scope of the Project

**In scope**

- Registering students (name, age, email, roll number) and teachers (name, age, email, subject, employee ID)
- Validating email format and rejecting duplicate roll numbers / employee IDs
- Adding subject-wise grades to an existing student
- Viewing the complete details of a student (including grades) or a teacher
- Permanent storage of all data in a local JSON file
- A console (text menu) interface, built with object-oriented Python
- Automated unit tests for the main behaviours

**Out of scope (for this version)**

- Graphical or web interface
- Editing or deleting records
- User login / role-based access control
- Attendance, fee management, timetables
- Multi-user or network access, and database servers

## Target Users

- **School administrators / office staff** who register new students and teachers and look up records
- **Teachers** who enter and review grades
- **Students of programming** who want a small, readable example of OOP with file persistence

## High-Level Features

1. **Student management** – register students with validated email and unique roll number
2. **Teacher management** – register teachers with validated email and unique employee ID
3. **Grades and records** – add grades per subject; view full student or teacher profiles
4. **Persistent storage** – all changes saved to `School_data.json` and reloaded automatically
5. **Clean modular design** – abstract base class `persons` with `Student` and `Teacher` subclasses, separate storage and menu modules
6. **Automated testing** – 25 unit tests run with `python -m unittest discover -s tests -v`
