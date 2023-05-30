from datetime import datetime
from aiogram import Router
from aiogram.fsm.context import FSMContext
from connection import all_tasks_for_executer, one_task, update_status_executer, all_tasks, update_name, \
    update_info, update_status, update_deadline
from states import statesEditTasks, statesTasks
from aiogram.filters import Text
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

router = Router()

#для исполнителя

@router.message(Text("Изменить статус задачи"), statesEditTasks.editState)
async def get_task_executer(message: Message, state: FSMContext):
    buttons = []
    userId = message.from_user.id
    allTasks = await all_tasks_for_executer(userId)
    task_list = " "
    for user in allTasks:
        idTask = f"idTaskExecuter:{user.get('idTask')}"
        nameTask = user.get("nameTask")
        statusTask = user.get("status")
        text = f"{nameTask}: {statusTask}"
        task_list += text
        buttons.append([InlineKeyboardButton(text=text, callback_data=idTask)])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберите задачу", reply_markup=ReplyKeyboardRemove())
    await message.answer("Ваши задачи:", reply_markup=kb)


@router.callback_query(lambda call: call.data.startswith("idTaskExecuter"))
async def choise_task(call: CallbackQuery, state: FSMContext):
    taskId = call.data.split(":")[1]
    await state.update_data(taskId=taskId)
    oneTask = await one_task(taskId)
    oneTaskStatus = oneTask.get("status")
    if oneTaskStatus == "Выполнена":
        kb = [[KeyboardButton(text="Задачи, назначенные мне")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await call.message.answer("Эта задача уже выполнена", reply_markup=keyboard)
        await state.set_state(statesTasks.mainMenu)
    else:
        kb = [[KeyboardButton(text="Да")], [KeyboardButton(text="Нет")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await call.message.answer(f"Хотите изменить статус задачи на 'Выполнена'?", reply_markup=keyboard)
        await state.set_state(statesEditTasks.yes_or_no)


@router.message(Text("Да"), statesEditTasks.yes_or_no)
async def update_status_executer_def(message: Message, state: FSMContext):
    taskId = await state.get_data()
    taskIdStr = taskId['taskId']
    await update_status_executer(str(taskIdStr))
    kb = [[KeyboardButton(text="Задачи, назначенные мне")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Статус задачи обновлен", reply_markup=keyboard)
    await state.set_state(statesTasks.mainMenu)

#для того кто назначает задачи

@router.message(Text("Изменить задачу"), statesEditTasks.editState)
async def get_task_customer(message: Message, state: FSMContext):
    buttons = []
    userId = message.from_user.id
    allTasks = await all_tasks(userId)
    task_list = " "
    for user in allTasks:
        idTask = f"idTask:{user.get('idTask')}"
        nameTask = user.get("nameTask")
        statusTask = user.get("status")
        text = f"{nameTask}: {statusTask}"
        task_list += text
        buttons.append([InlineKeyboardButton(text=text, callback_data=idTask)])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберите задачу", reply_markup=ReplyKeyboardRemove())
    await message.answer("Задачи, назначенные мной:", reply_markup=kb)


@router.callback_query(lambda call: call.data.startswith("idTask"))
async def choise_task_customer(call: CallbackQuery, state: FSMContext):
    taskId = call.data.split(":")[1]
    await state.update_data(taskId=taskId)
    oneTask = await one_task(taskId)

    nameTask = oneTask.get('nameTask')
    textName = f"Название задачи: {nameTask}"
    name_task_button = InlineKeyboardButton(text=textName, callback_data=f"nameTask:{nameTask}")

    taskInfo = oneTask.get('taskInfo')
    textInfo = f"Описание задачи: {taskInfo}"
    info_task_button = InlineKeyboardButton(text=textInfo, callback_data=f"taskInfo:{taskInfo}")

    taskDeadline = oneTask.get('taskDeadline')
    textDeadline = f"Дедлайн: {taskDeadline}"
    deadline_task_button = InlineKeyboardButton(text=textDeadline, callback_data=f"taskDeadline:{taskDeadline}")

    status = oneTask.get('status')
    textStatus = f"Статус задачи: {status}"
    status_task_button = InlineKeyboardButton(text=textStatus, callback_data=f"status:{status}")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [name_task_button],
        [info_task_button],
        [deadline_task_button],
        [status_task_button]
    ])
    await call.message.answer("Выберите, что хотите изменить", reply_markup=keyboard)


@router.callback_query(lambda call: call.data.startswith("nameTask"))
async def get_name_task(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите новое название задачи")
    await state.set_state(statesEditTasks.name)

@router.message(statesEditTasks.name)
async def update_name_task(message: Message, state: FSMContext):
    taskId = await state.get_data()
    taskIdStr = taskId['taskId']
    nameTask = message.text
    await update_name(str(taskIdStr), nameTask)
    kb = [[KeyboardButton(text="Задачи, назначенные мной")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Название задачи обновлено", reply_markup=keyboard)
    await state.set_state(statesTasks.mainMenu)


@router.callback_query(lambda call: call.data.startswith("taskInfo"))
async def get_info_task(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите новое описание задачи")
    await state.set_state(statesEditTasks.info)


@router.message(statesEditTasks.info)
async def update_info_task(message: Message, state: FSMContext):
    taskId = await state.get_data()
    taskIdStr = taskId['taskId']
    taskInfo = message.text
    await update_info(str(taskIdStr), taskInfo)
    kb = [[KeyboardButton(text="Задачи, назначенные мной")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Описание задачи обновлено", reply_markup=keyboard)
    await state.set_state(statesTasks.mainMenu)


@router.callback_query(lambda call: call.data.startswith("status"))
async def update_status_task(call: CallbackQuery, state: FSMContext):
    status = call.data.split(":")[1]
    taskId = await state.get_data()
    taskIdStr = taskId['taskId']
    await update_status(str(taskIdStr), status)
    kb = [[KeyboardButton(text="Задачи, назначенные мной")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await call.message.answer("Статус задачи обновлен", reply_markup=keyboard)
    await state.set_state(statesTasks.mainMenu)


@router.callback_query(lambda call: call.data.startswith("taskDeadline"))
async def get_deadline_task(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите новый дедлайн задачи в формате 'YYYY-MM-DD HH:MM")
    await state.set_state(statesEditTasks.deadline)


@router.message(statesEditTasks.deadline)
async def update_deadline_task(message: Message, state: FSMContext):
    kb = [[KeyboardButton(text="Задачи, назначенные мной")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    deadline_str = message.text
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        taskId = await state.get_data()
        taskIdStr = taskId['taskId']
        await update_deadline(str(taskIdStr), deadline)
        await message.answer("Дедлайн задачи обновлен", reply_markup=keyboard)
        await state.set_state(statesTasks.mainMenu)
    except ValueError:
        await message.answer("Неправильный формат даты и времени. Введите дату и время в формате YYYY-MM-DD HH:MM", reply_markup=keyboard)
        await state.set_state(statesTasks.mainMenu)







