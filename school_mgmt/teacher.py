"""Teacher module: registration and detail lookup for teachers."""
from school_mgmt.persons import persons
from school_mgmt.storage import data, save


class Teacher(persons):

    def get_roles(self):
        return "Teacher"
    
    def register(self):
        name = input("Enter Student Name: ")
        age = int(input("Enter Student Age: "))
        email = input("Enter Student Email: ")
        subject = input("Enter Subject: ")
        emp_id = input("Enter Employee ID: ")

        if not persons.validate_email(email):
            print("Email is invalid.")
            return
        
        for i in data['Teachers']:
            if i['emp_id'] == emp_id:
                print("Employee ID already exists.")
                return
        
        data['Teachers'].append({
            "name": name,
            "age": age,
            "email": email,
            "subject": subject,
            "emp_id": emp_id
        })
        save()
        print("Teacher registered successfully.")

    def show_details(self):
        emp_id = input("Enter Employee ID: ")
        for i in data['Teachers']:
            if i['emp_id'] == emp_id:
                print(f"Name: {i['name']}")
                print(f"Age: {i['age']}")
                print(f"Email: {i['email']}")
                print(f"Subject: {i['subject']}")
                print(f"Employee ID: {i['emp_id']}")
                return
