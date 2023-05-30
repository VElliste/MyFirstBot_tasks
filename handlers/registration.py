from aiogram import Router
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.types import Message
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from states import statesRegistration, statesTasks
from connection import insert_users
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

router = Router()


@router.message(Text("Регистрация"), statesRegistration.name)
@router.message(Text("Нет"), statesRegistration.checkDataIsCorrect)
async def getName(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя",  reply_markup=ReplyKeyboardRemove())
    await state.update_data(id=message.from_user.id)
    await state.set_state(statesRegistration.surname)


@router.message(statesRegistration.surname)
async def getSurname(message: Message, state: FSMContext):
    await message.answer("Введите вашу фамилию")
    await state.update_data(name=message.text)
    await state.set_state(statesRegistration.checkData)


@router.message(statesRegistration.checkData)
async def checkData(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    userData = await state.get_data()
    await message.answer(f"Проверьте введенные данные: {userData['name']} {userData['surname']}.")
    kb = [[KeyboardButton(text="Да")], [KeyboardButton(text="Нет")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Все верно?", reply_markup=keyboard)
    await state.set_state(statesRegistration.checkDataIsCorrect)


@router.message(Text("Да"), statesRegistration.checkDataIsCorrect)
async def checkDataIsCorrect(message: Message, state: FSMContext):
    userData = await state.get_data()
    await message.answer("Отлично! Вы зарегистрированы.", reply_markup=ReplyKeyboardRemove())
    kb = [[KeyboardButton(text="Задачи, назначенные мне")],[KeyboardButton(text="Задачи, назначенные мной")], [KeyboardButton(text="Добавить новую задачу")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите пункт меню", reply_markup=keyboard)
    await insert_users(userData)
    await state.set_state(statesTasks.mainMenu)