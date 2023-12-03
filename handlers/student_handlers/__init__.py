from .answer_processing import router as answer_processing_router
from .assignment_handling import router as assignment_handling_router
from .hint_request import router as hint_request_router

def get_student_routers():
    return [answer_processing_router, assignment_handling_router, hint_request_router]