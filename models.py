"""Модуль, содержащий модели данных."""

class Student:
    """Класс, представляющий ученика."""
    def __init__(self, kid, comment, teacher_id):
        self.kid = kid
        self.comment = comment
        self.teacher_id = teacher_id

class Teacher:
    """Класс, представляющий учителя."""
    def __init__(self, teacher):
        self.teacher = teacher

class WaitingList:
    """Класс, представляющий ученика, ожидающего подтверждения от учителя."""
    def __init__(self, user_id):
        self.user_id = user_id

class Section:
    """Класс, представляющий учебный раздел."""
    def __init__(self, title, teacher_id, description=None):
        self.title = title
        self.teacher_id = teacher_id

class Topic:
    def __init__(self, section_id, title, teacher_id, videos=None, description=None, test_link=None):
        self.title = title
        self.section_id = section_id
        self.teacher_id = teacher_id
        self.videos = videos if videos is not None else []
        self.test_link = test_link 

class Assignment:
    """Класс, представляющий задание для ученика."""
    def __init__(self, topic_id, task_file, hint, answer_text, solution_file):
        self.topic_id = topic_id
        self.task_file = task_file
        self.hint = hint
        self.answer_text = answer_text
        self.solution_file = solution_file

class Homework:
    """Класс, представляющий файл с домашним заданием."""
    def __init__(self, topic_id, homework_file):
        self.topic_id = topic_id
        self.homework_file = homework_file
