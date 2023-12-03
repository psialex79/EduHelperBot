from db_operations.db_connection import get_db
from models import Assignment

def add_student(kid, comment, teacher_id):
    db = get_db()
    db.students.insert_one({"kid": kid, "comment": comment, "teacher_id": teacher_id})

def add_assignment(teacher_id, file_id, right_answer, hint, solution_id, is_photo):
    db = get_db()
    assignment = Assignment(teacher_id, file_id, right_answer, hint, solution_id, is_photo)
    db.assignments.insert_one(assignment.__dict__)

    student_ids = get_students_of_teacher(teacher_id)

    return student_ids

def get_students_of_teacher(teacher_id):
    db = get_db()
    students = db.students.find({"teacher_id": teacher_id})
    return [student['kid'] for student in students]

