"""Модуль для операций с базой данных, связанных с администраторами."""

from db_operations.db_connection import get_db

def add_teacher(teacher_id):
    """Добавляет учителя в базу данных."""
    db = get_db()
    db.teachers.insert_one({"teacher": teacher_id})
