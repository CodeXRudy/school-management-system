"""Student module: registration, grade entry and detail lookup for students."""
from school_mgmt.persons import persons
from school_mgmt.storage import data, save


class Student(persons):

    def get_roles(self):
        return "Student"
    
    def register(self):
        name = input("Enter Student Name: ")
        age = int(input("Enter Student Age: "))
        email = input("Enter Student Email: ")
        roll_number = input("Enter Student Roll Number: ")

        if not persons.validate_email(email):
            print("Email is invalid.")
            return
        
        for i in data['Students']:
            if i['roll_number'] == roll_number:
                print("Roll number already exists.")
                return

        data['Students'].append({
            "name": name,
            "age": age,
            "email": email,
            "roll_number": roll_number,
            "grades": []
        })
        save()
        print("Student registered successfully.")

    def show_details(self):
        roll_number = input("Enter Student Roll Number: ")
        for i in data['Students']:
            if i['roll_number'] == roll_number:
                print(f"Name: {i['name']}")
                print(f"Age: {i['age']}")
                print(f"Email: {i['email']}")
                print(f"Roll Number: {i['roll_number']}")
                print("Grades:")
                for grade in i['grades']:
                    print(f"{grade['subject']}: {grade['grade']}")
                return

    def add_grades(self):
        roll_number = input("Enter Student Roll Number: ")
        for i in data['Students']:
            if i['roll_number'] == roll_number:
                subject = input("Enter Subject: ")
                grade = input("Enter Grade: ")
                i['grades'].append({"subject": subject, "grade": grade})
                save()
                print("Grade added successfully.")
                return
        print("Student not found.")       
