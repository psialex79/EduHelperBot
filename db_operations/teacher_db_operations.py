"""Модуль для операций с базой данных, связанных с учителями."""

from models import Assignment
from bson import ObjectId
from db_operations.db_connection import get_db

def add_student(kid, comment, teacher_id):
    """Добавляет студента в базу данных."""
    db = get_db()
    db.students.insert_one({"kid": kid, "comment": comment, "teacher_id": teacher_id})

def add_assignment(assignment_details):
    """Добавляет задание для учителя."""
    db = get_db()
    assignment = Assignment(**assignment_details)
    db.assignments.insert_one(assignment.__dict__)
    student_ids = get_students_of_teacher(assignment_details['teacher_id'])
    return student_ids

def get_students_of_teacher(teacher_id):
    """Получает список студентов учителя."""
    db = get_db()
    students = db.students.find({"teacher_id": teacher_id})
    return [student['kid'] for student in students]

def save_topic_to_db(new_topic):
    """Сохраняет тему в базу данных."""
    db = get_db()
    topic_dict = {
        "title": new_topic.title,
        "section_id": ObjectId(new_topic.section_id),
        "teacher_id": new_topic.teacher_id,
        "videos": new_topic.videos
    }
    result = db.topics.insert_one(topic_dict)
    return result.inserted_id

def save_section_to_db(new_section):
    """Сохраняет раздел в базу данных."""
    db = get_db()
    section_dict = {
        "title": new_section.title,
        "teacher_id": new_section.teacher_id
    }
    result = db.sections.insert_one(section_dict)
    return result.inserted_id

def save_assignment_to_db(new_assignment):
    """Сохраняет задание в базу данных."""
    db = get_db()
    assignment_dict = {
        "topic_id": new_assignment.topic_id,
        "task_file": new_assignment.task_file,
        "hint": new_assignment.hint,
        "answer_text": new_assignment.answer_text,
        "solution_file": new_assignment.solution_file
    }
    db.assignments.insert_one(assignment_dict)

def save_homework_to_db(homework):
    """Сохраняет домашнее задание в базу данных."""
    db = get_db()
    homework_dict = {
        "topic_id": homework.topic_id,
        "homework_file": homework.homework_file
    }
    db.homeworks.insert_one(homework_dict)

def is_teacher(user_id):
    db = get_db()
    teacher = db.teachers.find_one({"teacher": user_id})
    return teacher is not None