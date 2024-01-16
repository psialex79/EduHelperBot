"""Модуль для операций с базой данных, связанных с учениками."""

import logging
import bson
from db_operations.db_connection import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_latest_assignment_for_student(assignment_id):
    """Получает последнее задание для ученика по его ID."""

    db = get_db()
    assignment = db.assignments.find_one({"_id": bson.ObjectId(assignment_id)})
    return assignment

def get_right_answer_for_student(assignment_id):
    """Получает правильный ответ для задания ученика по его ID."""
    db = get_db()
    try:
        object_id = bson.ObjectId(assignment_id) 
    except bson.errors.InvalidId:
        return None

    assignment = db.assignments.find_one({"_id": object_id})
    if assignment:
        return assignment.get('answer_text')
    return None

def get_solution_for_student(student_id):
    """Получает решение для последнего задания ученика."""

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

def get_sections_by_teacher(teacher_id):
    """Получает список разделов, связанных с учителем."""

    db = get_db()
    sections_cursor = db.sections.find({"teacher_id": teacher_id})
    sections = []
    for section in sections_cursor:
        # Преобразуем bson.ObjectId в строку
        section['_id'] = str(section['_id'])
        sections.append(section)
    return sections

def get_teacher_id_of_student(student_id):
    """Получает ID учителя ученика."""

    db = get_db()
    student = db.students.find_one({"kid": student_id})
    if student:
        return student.get('teacher_id')
    return None

def get_topic_by_id(topic_id):
    """Получает тему по её ID."""
    db = get_db()
    try:
        object_id = bson.ObjectId(topic_id)
    except bson.errors.InvalidId as e:
        logger.error("Ошибка преобразования topic_id в bson.ObjectId: %s", e)
        return None

    topic = db.topics.find_one({"_id": object_id})
    return topic

def get_section_by_id(section_id):
    """Получает раздел по его ID."""

    db = get_db()
    try:
        object_id = bson.ObjectId(section_id)
    except:
        return None

    section = db.sections.find_one({"_id": object_id})
    return section

def get_assignments_by_topic(topic_id):
    """Получает список заданий по ID темы."""

    db = get_db()
    try:
        object_id = bson.ObjectId(topic_id)
    except:
        return []

    # Получение названия темы
    topic = db.topics.find_one({"_id": object_id})
    if not topic:
        logger.info("Тема с topic_id: %s не найдена", object_id)
        return []
    
    topic_title = topic.get('title', 'Неизвестная тема')
    logger.info("Запрос заданий по теме: %s", topic_title)

    assignments_cursor = db.assignments.find({"topic_id": object_id})
    assignments = list(assignments_cursor)
    return assignments

def get_next_assignment(current_assignment_id):
    """Получает следующее задание по текущему ID задания."""

    db = get_db()
    try:
        current_assignment = db.assignments.find_one({"_id": bson.ObjectId(current_assignment_id)})
        if current_assignment:
            next_assignment = db.assignments.find_one(
                {
                    "topic_id": current_assignment["topic_id"], 
                    "_id": {"$gt": bson.ObjectId(current_assignment_id)}
                },
                sort=[("_id", 1)]
            )
            return next_assignment
    except Exception as e:
        logger.error("Ошибка при получении следующего задания: %s", e)
    return None

def get_topics_by_section_id(section_id):
    """Получает список тем по ID раздела."""

    db = get_db()
    try:
        oid = bson.ObjectId(section_id)
    except:
        return []

    topics_cursor = db.topics.find({"section_id": oid})
    return list(topics_cursor)

def get_topic_id_by_assignment(assignment_id):
    """Получает ID темы по ID задания."""
    db = get_db()
    try:
        object_id = bson.ObjectId(assignment_id)
    except:
        return None

    assignment = db.assignments.find_one({"_id": object_id})
    return assignment['topic_id'] if assignment else None

def get_homework_file_id_by_topic(topic_id):
    """Получает ID файла домашнего задания по ID темы."""
    db = get_db()
    try:
        object_id = bson.ObjectId(topic_id)
    except:
        return None

    homework = db.homeworks.find_one({"topic_id": object_id})
    return str(homework['homework_file']) if homework else None

def is_student(user_id):
    db = get_db()
    student = db.students.find_one({"kid": user_id})
    return student is not None