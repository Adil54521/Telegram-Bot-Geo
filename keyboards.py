from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")],
            [KeyboardButton(text="Отправить местоположение", request_location=True)],
            [KeyboardButton(text="/пришел"), KeyboardButton(text="/ушел")],
            [KeyboardButton(text="/статистика")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )