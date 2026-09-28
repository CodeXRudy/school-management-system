"""Console menu: shows the options and routes the user's choice to the right module."""
from school_mgmt.student import Student
from school_mgmt.teacher import Teacher


def run_menu():
    student = Student()
    teacher = Teacher()

    print("Press 1 to register a Student")
    print("Press 2 to register a Teacher")
    print("Press 3 to add Grades")
    print("Press 4 to show a Student details")
    print("Press 5 to show a teacher details")

    choice = int(input("Enter your choice: "))

    if choice ==1:
        student.register()

    elif choice == 2:
        teacher.register()

    elif choice == 3:
        student.add_grades()
        
    elif choice == 4:
        student.show_details()

    elif choice == 5:
        teacher.show_details()
