from aiogram.filters.state import State, StatesGroup

class AddTeacherState(StatesGroup):
    waiting_for_teacher_id = State()

class TeacherActions(StatesGroup):
    choosing_action = State()

class AddStudentState(StatesGroup):
    waiting_for_student_id = State()

class AddStudentInfoState(StatesGroup):
    waiting_for_real_name = State()

class AddAssignmentState(StatesGroup):
    waiting_for_file = State()
    waiting_for_right_answer = State()

class StudentActions(StatesGroup):
    waiting_for_answer = State()

class StudentKeyboardActions(StatesGroup):
    waiting_for_answer_input = State()
    waiting_for_tip_request = State()