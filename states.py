from aiogram.fsm.state import StatesGroup, State


class statesRegistration(StatesGroup):
    name = State()
    surname = State()
    checkData = State()
    checkDataIsCorrect = State()

class statesTasks(StatesGroup):
    mainMenu = State()
    nameTask = State()
    taskInfo = State()
    taskDeadline = State()
    checkTaskIsCorrect = State()

class statesEditTasks(StatesGroup):
    yes_or_no = State()
    editState = State()
    name = State()
    info = State()
    deadline = State()

class stateUnknownMessage(StatesGroup):
    unknown = State()