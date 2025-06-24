import asyncio 
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from osm import location_reply_button, router as osm_router, user_action_map
from database_save import get_today_visits
from keyboards import main_menu_keyboard  

load_dotenv() #загружает токен 
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") # передает в переменную TELEGRAM_TOKEN то что os.getenv находит в файле .env

bot = Bot(token=TELEGRAM_TOKEN) # инициализация метода Bot() и передача ему данных по токену(в качестве аргумента) в переменную token
dp = Dispatcher() # инициализация метода из айограм 

with open("instructions.txt", "r", encoding="utf-8") as file:
    instructions_text = file.read() # Читает файл с инструкциями и передает в переменную instructions_text
    
# При нажатии команды старт все данные из instructions.txt которые есть в выше определенной переменной передаются и создается reply_markup в который передается логика появления кнопок 
@dp.message(Command("start"))
async def send_instructions(message: Message):
    await message.answer(instructions_text, reply_markup=main_menu_keyboard())

# Следующая команда    
@dp.message(Command("пришел"))
async def ask_geolocation(message: Message):
    
    # Сохраняется действие пользователя по статусу "пришел" — в словарь user_action_map
    user_action_map[message.from_user.id] = "пришел"  
    
    # Клавиатура которая отправляет данные
    keyboard = await location_reply_button()
    
    # Спрашивает пользователя о местоположении путем вызова метода message.answer(args)
    await message.answer("Пожалуйста, отправьте ваше местоположение", reply_markup=keyboard)

@dp.message(Command("ушел"))
async def ask_geolocation_leave(message: Message):
    # аналогично с пришел
    user_action_map[message.from_user.id] = "ушел"
    keyboard = await location_reply_button()
    await message.answer("Пожалуйста, отправьте ваше местоположение для фиксации ухода", reply_markup=keyboard)
    
# Команда которая через переменную visits инициализирует метод get_today_visits из файла database_save.py и передаеи в качестве аргумента данные из БД через message.from_user.id
@dp.message(Command("статистика"))
async def send_statistics(message: Message):
    visits = get_today_visits(message.from_user.id)
    # Проверяет на ошибки 
    if not visits:
        await message.answer("Сегодня ещё нет зафиксированных посещений.")
        return
    #передает в text отредактированные данные с БД.
    text = "История за сегодня:\n\n"
    for action, time, address in visits:
        text += f"{action.capitalize()} — {time}\n{address}\n\n"

    await message.answer(text.strip())

# Подключаем router из osm.py, где обрабатывается отправка геолокации
dp.include_router(osm_router)

async def main():
    await dp.start_polling(bot)
    
# Запуск асинхронного метода
if __name__ == "__main__":
    asyncio.run(main())
