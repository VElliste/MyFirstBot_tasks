import types

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from connection import check_user_registration
from states import statesTasks, statesEditTasks, stateUnknownMessage
from aiogram.filters import Text
from states import statesRegistration

router = Router()

@router.message(Command("start"))
@router.message(Text("Назад"), statesEditTasks.editState)
@router.message(Text("Назад"), stateUnknownMessage.unknown)
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    is_registered = await check_user_registration(user_id)

    if is_registered != False:
        kb = [
            [KeyboardButton(text="Задачи, назначенные мне")],
            [KeyboardButton(text="Задачи, назначенные мной")],
            [KeyboardButton(text="Добавить новую задачу")]
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Выберите пункт меню", reply_markup=keyboard)
        await state.set_state(statesTasks.mainMenu)
    else:
        kb = [[KeyboardButton(text="Регистрация")]]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=keyboard)
        await state.set_state(statesRegistration.name)

