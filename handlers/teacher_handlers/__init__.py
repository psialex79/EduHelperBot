from .assignment_creation import router as assignment_creation_router
from .student_addition import router as student_addition_router

def get_teacher_routers():
    return [assignment_creation_router, student_addition_router]