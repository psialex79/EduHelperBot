from db_handlers.db_connection import get_db

def add_teacher(teacher_id):
    db = get_db()
    db.teachers.insert_one({"teacher": teacher_id})