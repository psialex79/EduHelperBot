from db_handlers.db_connection import get_db
from models import Assignment

def add_student(kid, comment, teacher_id):
    db = get_db()
    db.students.insert_one({"kid": kid, "comment": comment, "teacher_id": teacher_id})
#teacher
def add_assignment(teacher_id, file_id, right_answer, is_photo):
    db = get_db()
    assignment = Assignment(teacher_id, file_id, right_answer, is_photo)
    db.assignments.insert_one(assignment.__dict__)