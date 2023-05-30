import asyncio
from datetime import datetime, timedelta
from bot import bot

# Функция для отправки напоминания
async def send_reminder(userId, taskName):
    messageText = (f"Напоминание: У вас есть задача '{taskName}' через 1 час!")
    await bot.send_message(chat_id=userId, text=messageText)

# Функция для планирования напоминания за час до дедлайна
async def schedule_reminder(userId, taskName, deadline):
    current_time = datetime.now()
    reminder_time = deadline - timedelta(hours=1)

    if current_time < reminder_time:
        time_difference = (reminder_time - current_time).total_seconds()
        await asyncio.sleep(time_difference)
        await send_reminder(userId, taskName)