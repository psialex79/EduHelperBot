from db_operations.db_connection import get_db

def get_latest_assignment_for_student(student_id):
    db = get_db()
    student_info = db.students.find_one({"kid": student_id})
    if student_info:
        teacher_id = student_info['teacher_id']
        latest_assignment = db.assignments.find_one(
            {"teacher_id": teacher_id},
            sort=[('_id', -1)]
        )
        return latest_assignment
    return None

def get_right_answer_for_student(student_id):
    db = get_db()
    student_info = db.students.find_one({"kid": student_id})
    if student_info:
        teacher_id = student_info['teacher_id']
        latest_assignment = db.assignments.find_one(
            {"teacher_id": teacher_id},
            sort=[('_id', -1)]
        )
        if latest_assignment:
            return latest_assignment.get('right_answer')
    return None

def get_solution_for_student(student_id):
    db = get_db()
    student_info = db.students.find_one({"kid": student_id})
    if student_info:
        teacher_id = student_info['teacher_id']
        latest_assignment = db.assignments.find_one(
            {"teacher_id": teacher_id},
            sort=[('_id', -1)]
        )
        if latest_assignment:
            return latest_assignment.get('solution_id')
    return None
