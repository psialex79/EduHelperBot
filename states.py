from aiogram.filters.state import State, StatesGroup

#админ
class AddTeacherState(StatesGroup):
    waiting_for_teacher_id = State()
#ученик
class StudentActions(StatesGroup):
    waiting_for_answer = State()
#учитель
class TeacherActions(StatesGroup):
    choosing_action = State()
#учитель
class AddStudentState(StatesGroup):
    waiting_for_student_id = State()
#учитель
class AddStudentInfoState(StatesGroup):
    waiting_for_real_name = State()
#учитель
class AddAssignmentState(StatesGroup):
    waiting_for_file = State()
    waiting_for_right_answer = State()
    waiting_for_hint = State() 

