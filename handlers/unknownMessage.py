from aiogram.fsm.context import FSMContext

from states import stateUnknownMessage
from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

import states

router = Router()

@router.message()
async def handler_unknown_message(message: Message, state: FSMContext):
    # Обработка неизвестных сообщений
    kb = [[KeyboardButton(text="Назад")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await state.set_state(stateUnknownMessage.unknown)
    await message.answer("Я такое не знаю", reply_markup=keyboard)