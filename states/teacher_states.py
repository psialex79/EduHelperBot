from aiogram.filters.state import State, StatesGroup

class TeacherActions(StatesGroup):
    choosing_action = State()

class AddStudentState(StatesGroup):
    waiting_for_student_id = State()

class AddStudentInfoState(StatesGroup):
    waiting_for_real_name = State()

class AddAssignmentState(StatesGroup):
    waiting_for_file = State()
    waiting_for_right_answer = State()
    waiting_for_hint = State() 
    waiting_for_solution_file = State()

