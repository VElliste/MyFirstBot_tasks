import asyncio
import uuid

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters.command import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from connection import all_tasks, check_user_registration, all_tasks_for_executer, get_all_users, insert_task
from handlers.reminder import schedule_reminder
from states import statesTasks, statesEditTasks
from aiogram.filters import Text
from aiogram.types import Message
from datetime import datetime

router = Router()

@router.message(Text("Задачи, назначенные мне"), statesTasks.mainMenu)
@router.message(Text("Нет"), statesEditTasks.yes_or_no)
async def my_tasks(message: Message, state: FSMContext):
    userId = message.from_user.id
    tasksAll = await all_tasks_for_executer(userId)
    task_list = " "
    for task in tasksAll:
        taskName = task.get('nameTask')
        deadline_str = task.get('taskDeadline')
        taskInfo = task.get('taskInfo')
        taskStatus = task.get('status')
        fromUser = await check_user_registration(int(task.get('idFrom')))
        taskAppend = f"Название задачи: {taskName}\nОписание задачи: {taskInfo}\nДедлайн: {str(deadline_str)}\nСтатус: {taskStatus}\n"
        task_list += taskAppend
        if fromUser:
            fiofrom = f"От кого: {str(fromUser.get('name'))} {str(fromUser.get('surname'))}\n\n"
            task_list += fiofrom
    if task_list == " ":
        kb = [[KeyboardButton(text="Задачи, назначенные мне")], [KeyboardButton(text="Задачи, назначенные мной")],
              [KeyboardButton(text="Добавить новую задачу")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("У вас нет задач.", reply_markup=keyboard)
        await state.set_state(statesTasks.mainMenu)
    else:
        kb = [[KeyboardButton(text="Изменить статус задачи")], [KeyboardButton(text="Назад")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f"Ваши задачи:\n\n{str(task_list)}", reply_markup=keyboard)
        await state.set_state(statesEditTasks.editState)



@router.message(Text("Задачи, назначенные мной"), statesTasks.mainMenu)
async def my_tasks(message: Message, state: FSMContext):
    userId = message.from_user.id
    tasksAll = await all_tasks(userId)
    task_list = " "
    for task in tasksAll:
        taskName = task.get('nameTask')
        deadline_str = task.get('taskDeadline')
        taskInfo = task.get('taskInfo')
        taskStatus = task.get('status')
        forUser = await check_user_registration(int(task.get('idExecuter')))
        taskAppend = f"Название задачи: {taskName}\nОписание задачи: {taskInfo}\nДедлайн: {str(deadline_str)}\nСтатус: {taskStatus}\n"
        task_list += taskAppend
        if forUser:
            fiofor = f"Кому: {str(forUser.get('name'))} {str(forUser.get('surname'))}\n\n"
            task_list += fiofor
    if task_list == " ":
        kb = [[KeyboardButton(text="Задачи, назначенные мне")], [KeyboardButton(text="Задачи, назначенные мной")],
              [KeyboardButton(text="Добавить новую задачу")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("У вас нет задач.", reply_markup=keyboard)
        await state.set_state(statesTasks.mainMenu)
    else:
        kb = [[KeyboardButton(text="Изменить задачу")], [KeyboardButton(text="Назад")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f"Назначенные Вами задачи:\n\n{str(task_list)}", reply_markup=keyboard)
        await state.set_state(statesEditTasks.editState)


@router.message(Text("Добавить новую задачу"), statesTasks.mainMenu)
@router.message(Text("Нет"), statesTasks.checkTaskIsCorrect)
async def append_task(message: Message, state: FSMContext):
    buttons = []
    allUsers = await get_all_users()
    for user in allUsers:
        userName = user.get("name")
        userSurname = user.get("surname")
        text = f"{userName} {userSurname}"
        tgId = f"tgId:{user.get('id')}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=tgId)])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer('Выберите исполнителя', reply_markup=kb)


@router.callback_query(lambda call: call.data.startswith("tgId"), statesTasks.mainMenu)
async def save_executer_id(call: CallbackQuery, state: FSMContext):
    id = call.data.split(":")[1]
    await state.update_data(idExecuter=int(id))
    await call.message.answer("Введите название задачи")
    await state.set_state(statesTasks.nameTask)


@router.message(statesTasks.nameTask)
async def get_name_task(message: Message, state: FSMContext):
    await state.update_data(nameTask=message.text)
    await message.answer("Введите описание задачи")
    await state.set_state(statesTasks.taskInfo)


@router.message(statesTasks.taskInfo)
async def get_info_task(message: Message, state: FSMContext):
    await state.update_data(taskInfo=message.text)
    await message.answer("Введите дедлайн задачи в формате 'YYYY-MM-DD HH:MM'")
    await state.set_state(statesTasks.taskDeadline)


@router.message(statesTasks.taskDeadline)
async def get_name_task(message: Message, state: FSMContext):
    deadline_str = message.text
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")  # Пример формата: "YYYY-MM-DD HH:MM"
        await state.update_data(taskDeadline=deadline)
        taskData = await state.get_data()
        await message.answer(f"Проверьте введенные данные: '{taskData['nameTask']}': {taskData['taskInfo']} {taskData['taskDeadline']}.")
        kb = [[KeyboardButton(text="Да")], [KeyboardButton(text="Нет")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f"Все верно?", reply_markup=keyboard)
        await state.set_state(statesTasks.checkTaskIsCorrect)
    except ValueError:
        await message.answer("Неправильный формат даты и времени. Введите дату и время в формате YYYY-MM-DD HH:MM")


@router.message(Text("Да"), statesTasks.checkTaskIsCorrect)
async def task_is_correct(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(idFrom=message.from_user.id)
    taskId = str(uuid.uuid4())
    await state.update_data(status="Не выполнена", idTask=taskId)
    taskData = await state.get_data()
    await insert_task(taskData)
    await bot.send_message(int(taskData.get('idExecuter')), text="У вас новая задача")
    await message.answer("Задача добавлена.", reply_markup=ReplyKeyboardRemove())
    kb = [[KeyboardButton(text="Задачи, назначенные мне")],[KeyboardButton(text="Задачи, назначенные мной")], [KeyboardButton(text="Добавить новую задачу")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите пункт меню", reply_markup=keyboard)
    await state.set_state(statesTasks.mainMenu)

    # Запланировать напоминание за час до дедлайна
    asyncio.create_task(schedule_reminder(taskData.get('idExecuter'), taskData.get('nameTask'), taskData.get('taskDeadline')))  # Используем create_task для запуска асинхронной функции
