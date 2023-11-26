from db_handlers.db_connection import get_db

def is_registered_student(user_id):
    db = get_db()
    return db.students.find_one({"kid": user_id}) is not None

def is_registered_teacher(user_id):
    db = get_db()
    return db.teachers.find_one({"teacher": user_id}) is not None

def add_to_waiting_list(user_id):
    db = get_db()
    db.waiting_list.insert_one({"user_id": user_id})

def remove_from_waiting_list(user_id):
    db = get_db()
    db.waiting_list.delete_one({"user_id": user_id})

def is_in_waiting_list(user_id):
    db = get_db()
    return db.waiting_list.find_one({"user_id": user_id}) is not None