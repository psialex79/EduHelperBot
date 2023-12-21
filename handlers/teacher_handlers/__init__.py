from .adding_assignment import router as assignment_creation_router
from .adding_topic import router as topic_creation_router
from .student_addition import router as student_addition_router
from .view_sections import router as view_sections_router

def get_teacher_routers():
    return [assignment_creation_router, student_addition_router, topic_creation_router, view_sections_router]