class Student:
    def __init__(self, kid, comment, teacher_id):
        self.kid = kid
        self.comment = comment
        self.teacher_id = teacher_id

class Teacher:
    def __init__(self, teacher):
        self.teacher = teacher

class Assignment:
    def __init__(self, teacher_id, file_id, right_answer, hint, is_photo):
        self.teacher_id = teacher_id
        self.file_id = file_id
        self.right_answer = right_answer
        self.hint = hint  
        self.is_photo = is_photo

class WaitingList:
    def __init__(self, user_id):
        self.user_id = user_id
